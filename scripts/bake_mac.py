"""bake_mac.py  (run inside Blender 5.1, headless)  -- CUDA-free adaptation of the
handoff's per-region baker. The handoff classifies regions from a Hunyuan *paint*
albedo (CUDA-only). On Mac we have shape-only geometry, so instead we OCCLUSION-
AWARE PROJECT the clean front/left/back cutouts onto the mesh to get per-vertex
color -> that drives both region classification AND base color. Procedural
fur/leather/cloth normals are baked per region. No sharp photo texture is wrapped,
so none of the v1-v8 ghosting; the projection only labels regions + tints base.

  blender -b -P bake_mac.py -- --mesh <glb> --views <dir> --maps <dir> --out <glb> \
      [--tris 60000] [--res 4096] [--debug-id]
"""
import bpy, bmesh, os, sys, math, argparse
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view

HANDOFF = "/tmp/drm_handoff/inner/squirrel3d_handoff"
sys.path.insert(0, HANDOFF)
import bake_textures_multimat as B   # reuse pure helpers (not the 4.2-only materials)

def get_args():
    a = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--mesh", required=True)
    p.add_argument("--views", required=True)
    p.add_argument("--maps", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--tris", type=int, default=60000)
    p.add_argument("--res", type=int, default=4096)
    p.add_argument("--fur-scale", type=float, default=22.0)
    p.add_argument("--fur-strength", type=float, default=0.35)
    p.add_argument("--leather-scale", type=float, default=9.0)
    p.add_argument("--leather-strength", type=float, default=0.18)
    p.add_argument("--cloth-scale", type=float, default=40.0)
    p.add_argument("--cloth-strength", type=float, default=0.10)
    p.add_argument("--debug-id", action="store_true")
    return p.parse_args(a)

A = get_args()
M = lambda n: os.path.join(A.maps, n)
heights = {"fur": M("fur_height.png"), "leather": M("leather_height.png"), "cloth": M("cloth_height.png")}
params = dict(fur_scale=A.fur_scale, fur_strength=A.fur_strength,
              leather_scale=A.leather_scale, leather_strength=A.leather_strength,
              cloth_scale=A.cloth_scale, cloth_strength=A.cloth_strength)

# ---- import + normalize (height 2, centered, faces -Y) ----
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete()
bpy.ops.import_scene.gltf(filepath=A.mesh)
ms=[o for o in bpy.context.scene.objects if o.type=="MESH"]
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
obj=bpy.context.view_layer.objects.active
bpy.context.view_layer.update()
co=[obj.matrix_world@v.co for v in obj.data.vertices]
xs=[v.x for v in co]; ys=[v.y for v in co]; zs=[v.z for v in co]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; h=max(zs)-min(zs); s=2.0/h if h else 1.0
obj.location=(-cx*s,-cy*s,-min(zs)*s); obj.scale=(s,s,s)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
# remove floaters: split by loose parts, keep only the largest
bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True); bpy.context.view_layer.objects.active=obj
bpy.ops.mesh.separate(type="LOOSE") if False else None
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.separate(type="LOOSE"); bpy.ops.object.mode_set(mode="OBJECT")
parts=[o for o in bpy.context.selected_objects if o.type=="MESH"]
if len(parts)>1:
    keep=max(parts,key=lambda o:len(o.data.polygons))
    for o in parts:
        if o is not keep: bpy.data.objects.remove(o,do_unlink=True)
    obj=keep; bpy.context.view_layer.objects.active=obj
    print(f"[floaters] kept largest of {len(parts)} parts ({len(obj.data.polygons)} faces)",flush=True)
me=obj.data
B.decimate(obj, A.tris)
bpy.ops.object.shade_smooth()

# UVs for baking — ALWAYS rebuild (imported glb may carry an empty/degenerate UV layer)
for uvl in list(obj.data.uv_layers):
    obj.data.uv_layers.remove(uvl)
bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True); bpy.context.view_layer.objects.active=obj
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.002)
bpy.ops.object.mode_set(mode="OBJECT")
_uv=obj.data.uv_layers.active.data
_us=[d.uv[0] for d in _uv]; _vs=[d.uv[1] for d in _uv]
print(f"[uv] layers={len(obj.data.uv_layers)} u=[{min(_us):.3f},{max(_us):.3f}] v=[{min(_vs):.3f},{max(_vs):.3f}]", flush=True)

# ---- project cutouts -> per-vertex color (occlusion + facing gated) ----
def load_rgba(name):
    img=bpy.data.images.load(os.path.join(A.views,name))
    w,hh=img.size
    px=np.array(img.pixels[:]).reshape(hh,w,4)   # bottom-origin, 0..1, RGBA
    return px
VIEWS=[("front",load_rgba("front.png"),Vector((0,-6,1.0))),
       ("left", load_rgba("left.png"), Vector((-6,0,1.0))),
       ("back", load_rgba("back.png"), Vector((0, 6,1.0)))]
AIM=Vector((0,0,1.0))
scene=bpy.context.scene
cams=[]
for name,px,loc in VIEWS:
    cd=bpy.data.cameras.new(name); cd.type="ORTHO"; cd.ortho_scale=2.2
    cob=bpy.data.objects.new(name,cd); cob.location=loc
    cob.rotation_euler=(AIM-loc).to_track_quat('-Z','Y').to_euler()
    scene.collection.objects.link(cob)
    fwd=(AIM-loc).normalized()
    cams.append((name,px,cob,fwd))
bpy.context.view_layer.update()
bvh=BVHTree.FromObject(obj, bpy.context.evaluated_depsgraph_get())

def sample(px,uv):
    if uv.x<0 or uv.x>1 or uv.y<0 or uv.y>1: return None
    H,W,_=px.shape
    x=min(W-1,max(0,int(uv.x*(W-1)))); y=min(H-1,max(0,int(uv.y*(H-1))))
    p=px[y,x]
    if p[3]<0.5: return None      # transparent bg -> skip
    return p[:3]

me=obj.data; mw=obj.matrix_world
FUR=np.array([0.42,0.115,0.035])
vcol=np.zeros((len(me.vertices),3),dtype=np.float32)
for vi,v in enumerate(me.vertices):
    pw=mw@v.co; n=(mw.to_3x3()@v.normal).normalized()
    acc=np.zeros(3); wsum=0.0
    for name,px,cob,fwd in cams:
        facing=n.dot(-fwd)
        if facing<=0.25: continue
        vd=-fwd
        hit=bvh.ray_cast(pw+vd*8.0,-vd)
        if hit[0] is None or (hit[0]-pw).length>0.02: continue
        uv=world_to_camera_view(scene,cob,pw)
        c=sample(px,uv)
        if c is None: continue
        w=facing**4; acc+=c*w; wsum+=w
    vcol[vi]= acc/wsum if wsum>0 else FUR

print(f"[vcol] min={vcol.min(axis=0)} max={vcol.max(axis=0)} mean={vcol.mean(axis=0)}", flush=True)
# write vertex colors (per-loop)
for ca in list(me.color_attributes): me.color_attributes.remove(ca)
catt=me.color_attributes.new(name="Col",type="FLOAT_COLOR",domain="CORNER")
loopcol=np.ones((len(me.loops),4),dtype=np.float32)
for li,l in enumerate(me.loops): loopcol[li,:3]=vcol[l.vertex_index]
catt.data.foreach_set("color", loopcol.reshape(-1))

# ---- per-face region from mean vertex color ----
facecol=np.zeros((len(me.polygons),3),dtype=np.float32)
for fi,poly in enumerate(me.polygons):
    facecol[fi]=vcol[[me.loops[li].vertex_index for li in poly.loop_indices]].mean(axis=0)
region=B.classify_face_colors(facecol)
bm=bmesh.new(); bm.from_mesh(me); region=B.isolate_apron(bm,region); bm.free()
counts={B.REGIONS[r]:int((region==r).sum()) for r in B.REGIONS}
print("[regions]",counts,flush=True)

# ---- 5.1-safe per-region materials: vertex-color base + procedural normals ----
def region_material(name, rid):
    mat=bpy.data.materials.new(name); mat.use_nodes=True
    nt=mat.node_tree; nt.nodes.clear()
    out=nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf=nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs["BSDF"],out.inputs["Surface"])
    vc=nt.nodes.new("ShaderNodeAttribute"); vc.attribute_type="GEOMETRY"; vc.attribute_name="Col"
    nt.links.new(vc.outputs["Color"],bsdf.inputs["Base Color"])
    if rid==1:
        nrm,_=B.detail_nodes(nt,heights["fur"],params["fur_scale"],params["fur_strength"])
        nt.links.new(nrm,bsdf.inputs["Normal"]); bsdf.inputs["Roughness"].default_value=0.7
        for k in ("Sheen Weight","Sheen"):
            if k in bsdf.inputs: bsdf.inputs[k].default_value=0.4; break
    elif rid==3:
        nrm,_=B.detail_nodes(nt,heights["leather"],params["leather_scale"],params["leather_strength"])
        nt.links.new(nrm,bsdf.inputs["Normal"]); bsdf.inputs["Roughness"].default_value=0.5
    elif rid==2:
        nrm,_=B.detail_nodes(nt,heights["cloth"],params["cloth_scale"],params["cloth_strength"])
        nt.links.new(nrm,bsdf.inputs["Normal"]); bsdf.inputs["Roughness"].default_value=0.85
    else:
        bsdf.inputs["Roughness"].default_value=0.25; bsdf.inputs["Metallic"].default_value=1.0
    return mat

me.materials.clear(); slot_of={}
for rid in B.REGIONS:
    if (region==rid).any():
        me.materials.append(region_material(f"reg_{B.REGIONS[rid]}",rid))
        slot_of[rid]=len(me.materials)-1
for fi,poly in enumerate(me.polygons):
    poly.material_index=slot_of.get(int(region[fi]),slot_of.get(1,0))

# ---- bake to single map set ----
out_dir=os.path.dirname(os.path.abspath(A.out)); os.makedirs(out_dir,exist_ok=True)
scene.render.engine="CYCLES"; B.enable_gpu(scene); scene.cycles.samples=64; scene.render.bake.margin=16
bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True); bpy.context.view_layer.objects.active=obj
if A.debug_id:
    B.debug_id_bake(obj,region,slot_of,A.res,out_dir)
    me.materials.clear()
    for rid in B.REGIONS:
        if (region==rid).any(): me.materials.append(region_material(f"reg_{B.REGIONS[rid]}",rid))
    for fi,poly in enumerate(me.polygons): poly.material_index=slot_of.get(int(region[fi]),0)

import struct as _struct, zlib as _zlib
def write_png_np(path, t, srgb):
    """Write a baked Blender image to PNG directly from its pixel buffer.
    Bypasses Blender's headless img.save() which writes black. Blender pixels are
    scene-linear, bottom-origin; flip to top-origin and sRGB-encode color maps."""
    W,H = t.size
    a = np.array(t.pixels[:], dtype=np.float32).reshape(H, W, 4)[:, :, :3]
    a = a[::-1]                                  # bottom-origin -> top-origin
    if srgb:
        a = np.where(a<=0.0031308, a*12.92, 1.055*np.power(np.clip(a,0,1),1/2.4)-0.055)
    u8 = (np.clip(a,0,1)*255+0.5).astype(np.uint8)
    raw = bytearray()
    for y in range(H):
        raw.append(0); raw.extend(u8[y].tobytes())
    comp = _zlib.compress(bytes(raw),6)
    def chunk(typ,data): return _struct.pack(">I",len(data))+typ+data+_struct.pack(">I",_zlib.crc32(typ+data)&0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',_struct.pack(">IIBBBBB",W,H,8,2,0,0,0))+chunk(b'IDAT',comp)+chunk(b'IEND',b'')
    open(path,'wb').write(png)

def bake_pass(kind,res,is_data,**kw):
    t=B.make_target(f"bake_{kind}",res,is_data); B.add_target_to_all(obj,t)
    bpy.ops.object.bake(type=kw.pop("type"),**kw)
    _px=np.array(t.pixels[:]).reshape(-1,4)[:,:3]
    print(f"[bake {kind}] pixel mean={_px.mean():.4f} max={_px.max():.4f}", flush=True)
    p=os.path.join(out_dir,f"drmineral_{kind}.png"); write_png_np(p, t, srgb=(not is_data)); return p
alb=bake_pass("albedo",A.res,False,type="DIFFUSE",pass_filter={"COLOR"})
nrm=bake_pass("normal",A.res,True,type="NORMAL")
rgh=bake_pass("rough",A.res,True,type="ROUGHNESS")
ao =bake_pass("ao",A.res,True,type="AO")
mtl=B.bake_metallic_via_emit(obj,region,slot_of,A.res,out_dir)
# rename metal to drmineral_*
mtl2=os.path.join(out_dir,"drmineral_metal.png")
if os.path.exists(mtl) and mtl!=mtl2: os.replace(mtl,mtl2); mtl=mtl2

final=B.build_final(alb,nrm,rgh,mtl)
me.materials.clear(); me.materials.append(final)
bpy.ops.export_scene.gltf(filepath=A.out,export_format="GLB",
    export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_apply=True)
print("DONE ->",A.out,flush=True)
print("AO map (three.js aoMap):",ao,flush=True)
