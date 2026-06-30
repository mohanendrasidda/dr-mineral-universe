"""Canon-texturize a GLB carve by its OWN geometry (front=-y, height z in [0,2], tail=+x):
green coat / brown apron / red-brown fur / cream muzzle+shirt. Exports a vertex-coloured
glb + renders EEVEE previews (Standard transform, dim lights). Glasses are already carved
into the MAX mesh, so none are added.
  blender -b -P texturize_max.py -- <in.glb> <fur_normal.png> <out.glb> <preview_dir> [tag]
"""
import bpy, sys, math, os
import numpy as np
from mathutils import Vector
A=sys.argv[sys.argv.index("--")+1:]
in_glb, furnrm, out_glb, pvdir = A[0], A[1], A[2], A[3]
tag = A[4] if len(A)>4 else "canonmax"
os.makedirs(pvdir, exist_ok=True); os.makedirs(os.path.dirname(out_glb), exist_ok=True)

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete()
bpy.ops.import_scene.gltf(filepath=in_glb)
ms=[o for o in bpy.context.scene.objects if o.type=="MESH"]
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
ob=bpy.context.view_layer.objects.active
bpy.context.view_layer.update()
co=[ob.matrix_world@v.co for v in ob.data.vertices]
xs=[v.x for v in co]; ys=[v.y for v in co]; zs=[v.z for v in co]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; h=max(zs)-min(zs); s=2.0/h if h else 1.0
ob.location=(-cx*s,-cy*s,-min(zs)*s); ob.scale=(s,s,s)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bpy.ops.object.shade_smooth()
me=ob.data; mw=ob.matrix_world

# ---- CANON colour by geometry ----
GREEN=np.array([0.13,0.38,0.16],np.float32)
BROWN=np.array([0.30,0.16,0.07],np.float32)
FUR  =np.array([0.55,0.23,0.08],np.float32)
CREAM=np.array([0.84,0.75,0.58],np.float32)
verts=list(me.vertices)
P=np.array([(mw@v.co)[:] for v in verts],np.float32)
def region(x,y,z):
    # tail owns the entire +x side above the feet (incl. its forward-curling base)
    tail = (x>0.28 and z>0.35)
    if tail: return FUR
    if z>1.58: return FUR
    if 1.26<=z<=1.58:
        return CREAM if (y<-0.16 and abs(x)<0.34) else FUR
    if abs(x)>0.56 and 0.45<z<1.02: return FUR
    if z<0.42: return FUR
    if z<1.18 and y<-0.02 and abs(x)<0.42: return BROWN
    if z>1.02 and y<-0.10 and abs(x)<0.30: return CREAM
    return GREEN
vcol=np.array([region(*P[vi]) for vi in range(len(verts))],np.float32)
for ca in list(me.color_attributes): me.color_attributes.remove(ca)
catt=me.color_attributes.new(name="Col",type="FLOAT_COLOR",domain="POINT")
flat=np.concatenate([vcol,np.ones((len(vcol),1),np.float32)],1).reshape(-1)
catt.data.foreach_set("color", flat)
me.color_attributes.active_color=catt
me.attributes.active_color=catt

# ---- material: vertex colour + fur normal + sheen ----
m=bpy.data.materials.new("canon"); m.use_nodes=True; nt=m.node_tree; nd=nt.nodes
b=next(n for n in nd if n.type=="BSDF_PRINCIPLED"); b.inputs["Roughness"].default_value=0.7
for k in ("Sheen Weight","Sheen"):
    if k in b.inputs: b.inputs[k].default_value=0.4; break
vc=nd.new("ShaderNodeAttribute"); vc.attribute_type="GEOMETRY"; vc.attribute_name="Col"
nt.links.new(vc.outputs["Color"],b.inputs["Base Color"])
if os.path.isfile(furnrm):
    tc=nd.new("ShaderNodeTexCoord"); mp=nd.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(8,8,8)
    nt.links.new(tc.outputs["Object"],mp.inputs["Vector"])
    img=bpy.data.images.load(furnrm); img.colorspace_settings.name="Non-Color"
    tx=nd.new("ShaderNodeTexImage"); tx.image=img; tx.projection="BOX"; tx.projection_blend=0.3
    nt.links.new(mp.outputs["Vector"],tx.inputs["Vector"])
    nmap=nd.new("ShaderNodeNormalMap"); nmap.inputs["Strength"].default_value=0.5
    nt.links.new(tx.outputs["Color"],nmap.inputs["Color"]); nt.links.new(nmap.outputs["Normal"],b.inputs["Normal"])
me.materials.clear(); me.materials.append(m)

# ---- export coloured glb ----
bpy.ops.object.select_all(action="DESELECT"); ob.select_set(True)
bpy.context.view_layer.objects.active=ob
try:
    bpy.ops.export_scene.gltf(filepath=out_glb, use_selection=True, export_format='GLB',
                              export_vertex_color='ACTIVE')
except TypeError:
    bpy.ops.export_scene.gltf(filepath=out_glb, use_selection=True, export_format='GLB')
print("EXPORTED", out_glb, flush=True)

# ---- EEVEE preview render ----
scene=bpy.context.scene
for eng in ("BLENDER_EEVEE_NEXT","BLENDER_EEVEE"):
    try: scene.render.engine=eng; break
    except Exception: continue
try: scene.eevee.taa_render_samples=24
except Exception: pass
w=bpy.data.worlds.new("w"); scene.world=w; w.use_nodes=True
wn=w.node_tree.nodes["Background"]; wn.inputs[0].default_value=(0.10,0.10,0.12,1); wn.inputs[1].default_value=0.5
def area(nm,loc,e,c,sz):
    d=bpy.data.lights.new(nm,"AREA"); d.energy=e; d.color=c; d.size=sz
    o=bpy.data.objects.new(nm,d); o.location=loc; scene.collection.objects.link(o)
    t=bpy.data.objects.new(nm+"t",None); t.location=(0,0,1.0); scene.collection.objects.link(t)
    cc=o.constraints.new("TRACK_TO"); cc.target=t; cc.track_axis="TRACK_NEGATIVE_Z"; cc.up_axis="UP_Y"
area("key",(3,-3,4),300,(1.0,0.94,0.84),3.8); area("rim",(-2.6,3,3.6),260,(0.95,0.82,0.62),2.4); area("fill",(-3.6,-2.2,2.2),95,(0.7,0.8,1.0),4.2)
cd=bpy.data.cameras.new("rc"); cam=bpy.data.objects.new("rc",cd); scene.collection.objects.link(cam); scene.camera=cam
scene.render.resolution_x=820; scene.render.resolution_y=1040
try: scene.view_settings.view_transform="Standard"
except Exception: scene.view_settings.view_transform="AgX"
try: scene.view_settings.look="None"
except Exception: pass
for t,ang in [("front",0),("q34",40)]:
    a=math.radians(ang); cam.location=(math.sin(a)*4.2,-math.cos(a)*4.2,1.15)
    dv=Vector((0,0,1.0))-Vector(cam.location); cam.rotation_euler=dv.to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=os.path.join(pvdir,f"{tag}-{t}.png"); bpy.ops.render.render(write_still=True); print("WROTE",scene.render.filepath,flush=True)
print("CANONMAX_DONE",flush=True)
