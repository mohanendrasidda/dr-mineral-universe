"""Voxel-remesh the triangle-soup into a clean, watertight, uniform surface (local, free).
Shows the 'properly carved' form with an even stylized material.
  blender -b -P scripts/blender_remesh.py -- <geo.glb> <out_dir> <out.glb> [voxel]
"""
import bpy, sys, math, os, mathutils
argv = sys.argv[sys.argv.index("--")+1:]
geo, outdir, outglb = argv[0], argv[1], argv[2]
voxel = float(argv[3]) if len(argv) > 3 else 0.015
os.makedirs(outdir, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=geo)
ms=[o for o in bpy.context.scene.objects if o.type=="MESH"]
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
obj=bpy.context.view_layer.objects.active
src=len(obj.data.polygons)

# normalize to height 2 first so voxel size is meaningful
bpy.context.view_layer.update()
co=[obj.matrix_world@v.co for v in obj.data.vertices]
zs=[v.z for v in co]; xs=[v.x for v in co]; ys=[v.y for v in co]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; h=max(zs)-min(zs); s=2.0/h if h else 1.0
obj.location=(-cx*s,-cy*s,-min(zs)*s); obj.scale=(s,s,s)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)

# VOXEL REMESH -> clean watertight uniform surface
rm=obj.modifiers.new("rm","REMESH"); rm.mode="VOXEL"; rm.voxel_size=voxel; rm.use_smooth_shade=True
bpy.ops.object.modifier_apply(modifier="rm")
# light decimate to web budget while keeping the clean topology feel
tris=len(obj.data.polygons)
if tris>60000:
    d=obj.modifiers.new("d","DECIMATE"); d.ratio=60000/tris; bpy.ops.object.modifier_apply(modifier="d")
bpy.ops.object.shade_smooth()
print(f"remesh: {src} -> {len(obj.data.polygons)} tris (voxel {voxel})")

# even stylized material: warm fur base + subtle procedural variation (volumetric read)
mat=bpy.data.materials.new("clay"); mat.use_nodes=True; nt=mat.node_tree; nd=nt.nodes
b=next(n for n in nd if n.type=="BSDF_PRINCIPLED")
b.inputs["Base Color"].default_value=(0.46,0.14,0.05,1); b.inputs["Roughness"].default_value=0.62
noise=nd.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value=18.0
bump=nd.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.12
nt.links.new(noise.outputs["Fac"],bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"],b.inputs["Normal"])
obj.data.materials.clear(); obj.data.materials.append(mat)

# lighting + render
def lamp(nm,loc,e,c,sz=3.0):
    d=bpy.data.lights.new(nm,"AREA"); d.energy=e; d.color=c; d.size=sz
    o=bpy.data.objects.new(nm,d); o.location=loc; bpy.context.scene.collection.objects.link(o)
    t=bpy.data.objects.new(nm+"_t",None); t.location=(0,0,1); bpy.context.scene.collection.objects.link(t)
    cc=o.constraints.new("TRACK_TO"); cc.target=t; cc.track_axis="TRACK_NEGATIVE_Z"; cc.up_axis="UP_Y"
lamp("key",(3,-3,4),900,(1,0.86,0.66)); lamp("fill",(-3.5,-2,2.5),300,(0.75,0.82,1)); lamp("rim",(0,4,3.5),650,(1,0.78,0.5))
w=bpy.data.worlds.new("w"); bpy.context.scene.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[0].default_value=(0.03,0.022,0.014,1); w.node_tree.nodes["Background"].inputs[1].default_value=0.4
rc_d=bpy.data.cameras.new("rc"); rc_d.lens=60; rc=bpy.data.objects.new("rc",rc_d); bpy.context.scene.collection.objects.link(rc); sc=bpy.context.scene; sc.camera=rc
try: sc.render.engine="BLENDER_EEVEE_NEXT"
except Exception: sc.render.engine="BLENDER_EEVEE"
sc.render.resolution_x=820; sc.render.resolution_y=1000; sc.view_settings.view_transform="AgX"
for tag,ang in [("front",0),("q34",35),("side",90),("back",180)]:
    r=4.4; a=math.radians(ang); rc.location=(math.sin(a)*r,-math.cos(a)*r,1.25)
    dv=mathutils.Vector((0,0,1))-mathutils.Vector(rc.location); rc.rotation_euler=dv.to_track_quat("-Z","Y").to_euler()
    sc.render.filepath=os.path.join(outdir,f"remesh-{tag}.png"); bpy.ops.render.render(write_still=True); print("WROTE",sc.render.filepath)

bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True); bpy.context.view_layer.objects.active=obj
bpy.ops.export_scene.gltf(filepath=os.path.abspath(outglb),export_format="GLB",use_selection=True,export_apply=True,
    export_draco_mesh_compression_enable=True)
print("EXPORTED",outglb, round(os.path.getsize(outglb)/1e6,2),"MB")
