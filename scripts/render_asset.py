"""render_asset.py (Blender 5.1 headless) — cinematic turntable of a textured glb.
  blender -b -P render_asset.py -- <glb> <out_dir> [tag]
Loads the baked WebGL glb, lights it (key/rim/fill, AgX), renders hero/front/q34/back/face.
"""
import bpy, sys, math, os
from mathutils import Vector
A=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
glb, outdir = A[0], A[1]
tag = A[2] if len(A)>2 else "drm"
os.makedirs(outdir, exist_ok=True)

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete()
bpy.ops.import_scene.gltf(filepath=glb)
ms=[o for o in bpy.context.scene.objects if o.type=="MESH"]
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
body=bpy.context.view_layer.objects.active
bpy.context.view_layer.update()
# normalize height 2, center, base at z=0
co=[body.matrix_world@v.co for v in body.data.vertices]
xs=[v.x for v in co]; ys=[v.y for v in co]; zs=[v.z for v in co]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; h=max(zs)-min(zs); s=2.0/h if h else 1.0
body.location=(-cx*s,-cy*s,-min(zs)*s); body.scale=(s,s,s)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bpy.ops.object.shade_smooth()

sc=bpy.context.scene; sc.render.engine="CYCLES"
try:
    prefs=bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type="METAL"
    for d in prefs.devices: d.use=True
    sc.cycles.device="GPU"
except Exception: pass
sc.cycles.samples=128; sc.cycles.use_denoising=True
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
wn=w.node_tree.nodes["Background"]; wn.inputs[0].default_value=(0.045,0.035,0.025,1); wn.inputs[1].default_value=0.5
def area(nm,loc,e,c,sz):
    d=bpy.data.lights.new(nm,"AREA"); d.energy=e; d.color=c; d.size=sz
    o=bpy.data.objects.new(nm,d); o.location=loc; sc.collection.objects.link(o)
    t=bpy.data.objects.new(nm+"t",None); t.location=(0,0,1.0); sc.collection.objects.link(t)
    cc=o.constraints.new("TRACK_TO"); cc.target=t; cc.track_axis="TRACK_NEGATIVE_Z"; cc.up_axis="UP_Y"
area("key",(3.4,-3.2,4.4),850,(1.0,0.85,0.62),3.0)
area("rim",(-2.6,3.2,3.8),700,(1.0,0.72,0.45),2.0)
area("fill",(-3.8,-2.4,2.2),180,(0.66,0.78,1.0),3.5)
cd=bpy.data.cameras.new("rc"); cd.lens=85; cd.dof.use_dof=True; cd.dof.aperture_fstop=3.2
rc=bpy.data.objects.new("rc",cd); sc.collection.objects.link(rc); sc.camera=rc
sc.render.resolution_x=1000; sc.render.resolution_y=1250; sc.view_settings.view_transform="AgX"
try: sc.view_settings.look="AgX - Medium High Contrast"
except Exception: pass
for t,ang,dist,zz,fz in [("hero",18,4.3,1.15,1.02),("front",0,4.3,1.05,1.02),
                         ("q34",42,4.1,1.1,1.02),("back",178,4.4,1.1,1.02),("face",6,2.4,1.62,1.6)]:
    a=math.radians(ang); rc.location=(math.sin(a)*dist,-math.cos(a)*dist,zz)
    dv=Vector((0,0,fz))-Vector(rc.location); rc.rotation_euler=dv.to_track_quat('-Z','Y').to_euler()
    cd.dof.focus_distance=dv.length
    sc.render.filepath=os.path.join(outdir,f"{tag}-{t}.png"); bpy.ops.render.render(write_still=True); print("WROTE",sc.render.filepath,flush=True)
print("RENDER_DONE",flush=True)
