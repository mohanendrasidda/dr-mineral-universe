"""v8: MULTI-VIEW projection. Per-vertex color sampled from front/back/left/right cameras,
each masked by facing + occlusion (BVH ray_cast) so no view bleeds onto faces it can't see.
Clean remesh carve + geometry eyes/glasses + cinematic render.
  blender -b -P scripts/blender_v8.py -- <geo.glb> <refdir> <out_dir>
"""
import bpy, sys, math, os, mathutils
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
A=sys.argv[sys.argv.index("--")+1:]
geo, refdir, outdir = A[0], A[1], A[2]
R=lambda n: os.path.join(refdir,n)
os.makedirs(outdir, exist_ok=True)
EYEZ,EYEX=1.60,0.145

# views: name, image, cam location, bbox(cx,cy,h), mirror_x
def load(p, mirror=False):
    a=np.load(p)
    if mirror: a=a[:, ::-1, :].copy()
    return a
VIEWS=[
 ("front", load(R("front.npy")),       Vector((0,-6,1.0)), (0.539,0.503,0.892)),
 ("back",  load(R("back.npy")),         Vector((0, 6,1.0)), (0.502,0.515,0.903)),
 ("left",  load(R("left.npy")),         Vector((-6,0,1.0)), (0.521,0.513,0.910)),
 ("right", load(R("left.npy"),True),    Vector((6, 0,1.0)), (0.479,0.513,0.910)),
]
AIM=Vector((0,0,1.0))
BG=np.array([127,127,127]); FUR=(0.42,0.115,0.035)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=geo)
ms=[o for o in bpy.context.scene.objects if o.type=="MESH"]
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
body=bpy.context.view_layer.objects.active
bpy.context.view_layer.update()
co=[body.matrix_world@v.co for v in body.data.vertices]
xs=[v.x for v in co]; ys=[v.y for v in co]; zs=[v.z for v in co]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; h=max(zs)-min(zs); s=2.0/h if h else 1.0
body.location=(-cx*s,-cy*s,-min(zs)*s); body.scale=(s,s,s)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
rm=body.modifiers.new("rm","REMESH"); rm.mode="VOXEL"; rm.voxel_size=0.011; rm.use_smooth_shade=True
bpy.ops.object.modifier_apply(modifier="rm"); bpy.ops.object.shade_smooth()
body.name="DrMineral_body"
me=body.data

# build cameras + BVH
scene=bpy.context.scene
cams=[]
for name,arr,loc,(bcx,bcy,bh) in VIEWS:
    cd=bpy.data.cameras.new(name); cd.type="ORTHO"; cd.ortho_scale=2.0/bh
    cob=bpy.data.objects.new(name,cd); cob.location=loc
    cob.rotation_euler=(AIM-loc).to_track_quat('-Z','Y').to_euler()
    scene.collection.objects.link(cob)
    fwd=(AIM-loc).normalized()
    cams.append((name,arr,cob,fwd,bcx,bcy))
bpy.context.view_layer.update()
bvh=BVHTree.FromObject(body, bpy.context.evaluated_depsgraph_get())

def sample(arr,bcx,bcy,uv):
    iu=uv.x+(bcx-0.5); iv=uv.y+(bcy-0.5)
    if iu<0 or iu>1 or iv<0 or iv>1: return None
    H,W,_=arr.shape
    px=arr[min(H-1,int((1-iv)*(H-1))), min(W-1,int(iu*(W-1)))].astype(float)
    if np.abs(px-BG).max()<22: return None       # background -> skip
    return px/255.0

# per-vertex multi-view color
col=np.zeros((len(me.vertices),4),dtype=np.float32); col[:,3]=1.0
mw=body.matrix_world
for vi,v in enumerate(me.vertices):
    p=mw@v.co; n=(mw.to_3x3()@v.normal).normalized()
    acc=np.zeros(3); wsum=0.0
    for name,arr,cob,fwd,bcx,bcy in cams:
        facing=n.dot(-fwd)
        if facing<=0.25: continue            # cos~75 floor: drop grazing faces (anti-smear)
        # ORTHO occlusion: march a PARALLEL ray from far in front back to the surface;
        # visible iff the first thing it hits is essentially this point.
        vd=-fwd                              # direction from surface toward camera
        hit=bvh.ray_cast(p+vd*8.0, -vd)      # origin far in front, marching toward surface
        if hit[0] is None or (hit[0]-p).length>0.012: continue   # occluded by other geometry
        uv=world_to_camera_view(scene,cob,p)
        c=sample(arr,bcx,bcy,uv)
        if c is None: continue
        w=facing**4                          # high exponent ~ best-view with thin feather
        acc+=c*w; wsum+=w
    if wsum>0: col[vi,:3]=acc/wsum
    else: col[vi,:3]=FUR

# write color attribute
if me.color_attributes:
    for ca in list(me.color_attributes): me.color_attributes.remove(ca)
ca=me.color_attributes.new(name="Col",type="FLOAT_COLOR",domain="POINT")
flat=col.reshape(-1)
ca.data.foreach_set("color", flat)
print("multiview colored", len(me.vertices), "verts")

# ---- material: vertex color base + fur bump + sheen ----
furimg=bpy.data.images.load(R("furbody.png"))
bm=bpy.data.materials.new("drm"); bm.use_nodes=True; nt=bm.node_tree; nd=nt.nodes
bsdf=next(n for n in nd if n.type=="BSDF_PRINCIPLED"); bsdf.inputs["Roughness"].default_value=0.72
for k in ("Sheen Weight","Sheen"):
    if k in bsdf.inputs: bsdf.inputs[k].default_value=0.5; break
vc=nd.new("ShaderNodeVertexColor"); vc.layer_name="Col"
nt.links.new(vc.outputs["Color"],bsdf.inputs["Base Color"])
tc=nd.new("ShaderNodeTexCoord"); mp=nd.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(7,7,7)
nt.links.new(tc.outputs["Object"],mp.inputs["Vector"])
fur=nd.new("ShaderNodeTexImage"); fur.image=furimg; fur.projection="BOX"; fur.projection_blend=0.3
nt.links.new(mp.outputs["Vector"],fur.inputs["Vector"])
bw=nd.new("ShaderNodeRGBToBW"); nt.links.new(fur.outputs["Color"],bw.inputs["Color"])
bump=nd.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.16; bump.inputs["Distance"].default_value=0.02
nt.links.new(bw.outputs["Val"],bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"],bsdf.inputs["Normal"])
me.materials.clear(); me.materials.append(bm)

# ---- facial geometry (same as v7) ----
vs=[v.co for v in me.vertices]; band=[v for v in vs if abs(v.z-EYEZ)<0.12]; fy=min(v.y for v in band) if band else -0.5
def mat(nm,c,r,m=0.0,coat=0.0):
    mm=bpy.data.materials.new(nm); mm.use_nodes=True; b=next(n for n in mm.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value=(*c,1); b.inputs["Roughness"].default_value=r; b.inputs["Metallic"].default_value=m
    if "Coat Weight" in b.inputs: b.inputs["Coat Weight"].default_value=coat
    return mm
im_=mat("iris",(0.18,0.09,0.04),0.2,coat=1.0)
for sx in(-EYEX,EYEX):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.056,location=(sx,fy+0.02,EYEZ)); o=bpy.context.active_object; o.data.materials.append(im_); o.name="eye"; bpy.ops.object.shade_smooth()
nmat=mat("nose",(0.18,0.08,0.07),0.28,coat=0.6)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.042,location=(0,fy-0.03,EYEZ-0.135)); o=bpy.context.active_object; o.scale=(1.3,0.9,0.8); o.data.materials.append(nmat); o.name="nose"; bpy.ops.object.shade_smooth()
gmat=mat("frame",(0.62,0.45,0.14),0.22,m=1.0)
for sx in(-EYEX,EYEX):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.082,minor_radius=0.0085,location=(sx,fy+0.018,EYEZ)); o=bpy.context.active_object; o.rotation_euler=(math.radians(90),0,0); o.data.materials.append(gmat); o.name="glasses"
bpy.ops.mesh.primitive_cylinder_add(radius=0.007,depth=0.09,location=(0,fy+0.012,EYEZ+0.01)); o=bpy.context.active_object; o.rotation_euler=(0,math.radians(90),0); o.data.materials.append(gmat)
wmat=mat("whisker",(0.92,0.88,0.8),0.45)
for side in(-1,1):
    for i,a in enumerate((0.28,0.12,-0.04)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0028,depth=0.4,location=(side*0.12,fy+0.01,EYEZ-0.15-i*0.03)); o=bpy.context.active_object; o.rotation_euler=(0,math.radians(88)*side,a*side); o.data.materials.append(wmat)

# ---- cinematic render ----
for c in cams: c[2].hide_render=True
sc=bpy.context.scene; sc.render.engine="CYCLES"
try: sc.cycles.device="GPU"
except Exception: pass
sc.cycles.samples=128; sc.cycles.use_denoising=True
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
wn=w.node_tree.nodes["Background"]; wn.inputs[0].default_value=(0.045,0.035,0.025,1); wn.inputs[1].default_value=0.45
def area(nm,loc,e,c,sz):
    d=bpy.data.lights.new(nm,"AREA"); d.energy=e; d.color=c; d.size=sz; o=bpy.data.objects.new(nm,d); o.location=loc; sc.collection.objects.link(o)
    t=bpy.data.objects.new(nm+"t",None); t.location=(0,0,1.0); sc.collection.objects.link(t); cc=o.constraints.new("TRACK_TO"); cc.target=t; cc.track_axis="TRACK_NEGATIVE_Z"; cc.up_axis="UP_Y"
area("key",(3.4,-3.2,4.4),1600,(1.0,0.84,0.6),3.0); area("rim",(-2.6,3.2,3.8),1400,(1.0,0.7,0.42),2.0); area("fill",(-3.8,-2.4,2.2),320,(0.65,0.78,1.0),3.5)
cd=bpy.data.cameras.new("rc"); cd.lens=85; cd.dof.use_dof=True; cd.dof.aperture_fstop=3.2
rc=bpy.data.objects.new("rc",cd); sc.collection.objects.link(rc); sc.camera=rc
sc.render.resolution_x=1000; sc.render.resolution_y=1250; sc.view_settings.view_transform="AgX"
try: sc.view_settings.look="AgX - Medium High Contrast"
except Exception: pass
for tag,ang,dist,zz,fz in [("hero",18,4.3,1.15,1.02),("front",0,4.3,1.05,1.02),("q34",42,4.1,1.1,1.02),("back",178,4.4,1.1,1.02),("face",6,2.4,1.62,1.6)]:
    a=math.radians(ang); rc.location=(math.sin(a)*dist,-math.cos(a)*dist,zz)
    dv=Vector((0,0,fz))-Vector(rc.location); rc.rotation_euler=dv.to_track_quat('-Z','Y').to_euler(); cd.dof.focus_distance=dv.length
    sc.render.filepath=os.path.join(outdir,f"v8-{tag}.png"); bpy.ops.render.render(write_still=True); print("WROTE",sc.render.filepath)
print("DONE")
