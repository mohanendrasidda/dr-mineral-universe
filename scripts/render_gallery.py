"""Render each .glb in a folder to a labeled thumbnail (front view).
  blender -b -P render_gallery.py -- <glb_dir> <out_dir>
"""
import bpy, sys, os, math
from mathutils import Vector
A=sys.argv[sys.argv.index("--")+1:]
gdir, outdir = A[0], A[1]
os.makedirs(outdir, exist_ok=True)
glbs=sorted([f for f in os.listdir(gdir) if f.endswith(".glb")])

def setup_scene():
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete()
    sc=bpy.context.scene; sc.render.engine="CYCLES"
    try:
        prefs=bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type="METAL"
        for d in prefs.devices: d.use=True
        sc.cycles.device="GPU"
    except Exception: pass
    sc.cycles.samples=48; sc.cycles.use_denoising=True
    w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
    bn=w.node_tree.nodes["Background"]; bn.inputs[0].default_value=(0.10,0.10,0.11,1); bn.inputs[1].default_value=0.7
    d=bpy.data.lights.new("key","AREA"); d.energy=600; d.size=4
    o=bpy.data.objects.new("key",d); o.location=(3,-3,5); sc.collection.objects.link(o)
    t=bpy.data.objects.new("t",None); t.location=(0,0,0.9); sc.collection.objects.link(t)
    c=o.constraints.new("TRACK_TO"); c.target=t; c.track_axis="TRACK_NEGATIVE_Z"; c.up_axis="UP_Y"
    d2=bpy.data.lights.new("fill","AREA"); d2.energy=200; d2.size=5
    o2=bpy.data.objects.new("fill",d2); o2.location=(-4,-2,3); sc.collection.objects.link(o2)
    c2=o2.constraints.new("TRACK_TO"); c2.target=t; c2.track_axis="TRACK_NEGATIVE_Z"; c2.up_axis="UP_Y"
    cd=bpy.data.cameras.new("rc"); cam=bpy.data.objects.new("rc",cd); sc.collection.objects.link(cam); sc.camera=cam
    sc.render.resolution_x=640; sc.render.resolution_y=800; sc.view_settings.view_transform="AgX"
    return sc,cam

for f in glbs:
    sc,cam=setup_scene()
    bpy.ops.import_scene.gltf(filepath=os.path.join(gdir,f))
    bpy.context.view_layer.update()
    ms=[o for o in bpy.context.scene.objects if o.type=="MESH"]
    if not ms: print("SKIP (no mesh)",f,flush=True); continue
    # world-space bbox of all mesh verts
    co=[o.matrix_world@v.co for o in ms for v in o.data.vertices]
    xs=[v.x for v in co]; ys=[v.y for v in co]; zs=[v.z for v in co]
    cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; cz=(min(zs)+max(zs))/2
    frame=max(max(xs)-min(xs), max(zs)-min(zs))*1.25 or 2.0
    # ortho camera framing the bbox from the front (-Y)
    cam.data.type="ORTHO"; cam.data.ortho_scale=frame
    cam.location=(cx, min(ys)-max(frame,5.0), cz)
    dv=Vector((cx,cy,cz))-Vector(cam.location); cam.rotation_euler=dv.to_track_quat('-Z','Y').to_euler()
    # aim lights at the model center
    for o in bpy.context.scene.objects:
        if o.type=="EMPTY" and o.name=="t": o.location=(cx,cy,cz)
    sc.render.filepath=os.path.join(outdir,f.replace(".glb",".png"))
    bpy.ops.render.render(write_still=True); print("WROTE",sc.render.filepath,flush=True)
print("GALLERY_DONE",flush=True)
