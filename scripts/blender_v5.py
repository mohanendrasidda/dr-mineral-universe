"""v5: clean remesh + bbox-aligned front projection + REAL fur (swatch as triplanar
color-fill + bump) + cinematic Cycles render. Free, Blender-only.
  blender -b -P scripts/blender_v5.py -- <geo.glb> <refdir> <out_dir>
"""
import bpy, sys, math, os, mathutils
A=sys.argv[sys.argv.index("--")+1:]
geo, refdir, outdir = A[0], A[1], A[2]
os.makedirs(outdir, exist_ok=True)
R=lambda n: os.path.join(refdir,n)

# front image bbox (measured): center/height -> projector alignment
FCX, FCY, FH = 0.539, 0.503, 0.892

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=geo)
ms=[o for o in bpy.context.scene.objects if o.type=="MESH"]
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
body=bpy.context.view_layer.objects.active

# normalize -> height 2, face -Y, apply
bpy.context.view_layer.update()
co=[body.matrix_world@v.co for v in body.data.vertices]
xs=[v.x for v in co]; ys=[v.y for v in co]; zs=[v.z for v in co]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; h=max(zs)-min(zs); s=2.0/h if h else 1.0
body.location=(-cx*s,-cy*s,-min(zs)*s); body.scale=(s,s,s)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
# clean remesh
rm=body.modifiers.new("rm","REMESH"); rm.mode="VOXEL"; rm.voxel_size=0.011; rm.use_smooth_shade=True
bpy.ops.object.modifier_apply(modifier="rm"); bpy.ops.object.shade_smooth()

# --- front projector, aligned to the painting's character bbox ---
front=bpy.data.images.load(R("front.png")); iw,ih=front.size
oscale=2.0/FH                               # mesh height(2) fills FH of frame
cam_d=bpy.data.cameras.new("proj"); cam_d.type="ORTHO"; cam_d.ortho_scale=oscale
pc=bpy.data.objects.new("proj",cam_d)
pc.location=((FCX-0.5)*oscale, -6, 1.0+(0.5-FCY)*oscale); pc.rotation_euler=(math.radians(90),0,0)
bpy.context.scene.collection.objects.link(pc)
uvp=body.data.uv_layers.new(name="proj"); body.data.uv_layers.active=uvp
mod=body.modifiers.new("proj","UV_PROJECT"); mod.uv_layer="proj"; mod.projector_count=1
mod.projectors[0].object=pc; mod.aspect_x=iw/ih; mod.aspect_y=1.0

# --- material: fur(swatch, triplanar) under, front painting over the front faces ---
furimg=bpy.data.images.load(R("furbody.png"))
bm=bpy.data.materials.new("drm"); bm.use_nodes=True; nt=bm.node_tree; nd=nt.nodes
bsdf=next(n for n in nd if n.type=="BSDF_PRINCIPLED")
bsdf.inputs["Roughness"].default_value=0.72
for k in ("Sheen Weight","Sheen"):
    if k in bsdf.inputs: bsdf.inputs[k].default_value=0.6; break
for k in ("Sheen Tint",):
    if k in bsdf.inputs:
        try: bsdf.inputs[k].default_value=(1.0,0.8,0.55,1.0)
        except Exception: pass
# triplanar fur (box projection in object space)
tc=nd.new("ShaderNodeTexCoord")
furscale=nd.new("ShaderNodeMapping"); furscale.inputs["Scale"].default_value=(7,7,7)
nt.links.new(tc.outputs["Object"],furscale.inputs["Vector"])
fur=nd.new("ShaderNodeTexImage"); fur.image=furimg; fur.projection="BOX"; fur.projection_blend=0.35
nt.links.new(furscale.outputs["Vector"],fur.inputs["Vector"])
# front projection
ftex=nd.new("ShaderNodeTexImage"); ftex.image=front; ftex.extension="EXTEND"
uvn=nd.new("ShaderNodeUVMap"); uvn.uv_map="proj"; nt.links.new(uvn.outputs["UV"],ftex.inputs["Vector"])
# facing weight (front faces -> projection)
gn=nd.new("ShaderNodeNewGeometry"); dp=nd.new("ShaderNodeVectorMath"); dp.operation="DOT_PRODUCT"; dp.inputs[1].default_value=(0,-1,0)
nt.links.new(gn.outputs["Normal"],dp.inputs[0])
rg=nd.new("ShaderNodeMapRange"); rg.inputs["From Min"].default_value=0.15; rg.inputs["From Max"].default_value=0.6; rg.clamp=True
nt.links.new(dp.outputs["Value"],rg.inputs["Value"])
mix=nd.new("ShaderNodeMix"); mix.data_type="RGBA"
nt.links.new(fur.outputs["Color"],mix.inputs[6])      # A = fur
nt.links.new(ftex.outputs["Color"],mix.inputs[7])     # B = front painting
nt.links.new(rg.outputs["Result"],mix.inputs[0])
nt.links.new(mix.outputs[2],bsdf.inputs["Base Color"])
# fur micro-relief bump everywhere
bw=nd.new("ShaderNodeRGBToBW"); nt.links.new(fur.outputs["Color"],bw.inputs["Color"])
bump=nd.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.18; bump.inputs["Distance"].default_value=0.02
nt.links.new(bw.outputs["Val"],bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"],bsdf.inputs["Normal"])
body.data.materials.clear(); body.data.materials.append(bm)

# --- cinematic render ---
sc=bpy.context.scene; sc.render.engine="CYCLES"
try: sc.cycles.device="GPU"
except Exception: pass
sc.cycles.samples=128; sc.cycles.use_denoising=True
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
wn=w.node_tree.nodes["Background"]; wn.inputs[0].default_value=(0.045,0.035,0.025,1); wn.inputs[1].default_value=0.45
def area(nm,loc,e,c,sz):
    d=bpy.data.lights.new(nm,"AREA"); d.energy=e; d.color=c; d.size=sz
    o=bpy.data.objects.new(nm,d); o.location=loc; sc.collection.objects.link(o)
    t=bpy.data.objects.new(nm+"t",None); t.location=(0,0,1.0); sc.collection.objects.link(t)
    cc=o.constraints.new("TRACK_TO"); cc.target=t; cc.track_axis="TRACK_NEGATIVE_Z"; cc.up_axis="UP_Y"
area("key",(3.4,-3.2,4.4),1600,(1.0,0.84,0.6),3.0)
area("rim",(-2.6,3.2,3.8),1400,(1.0,0.7,0.42),2.0)
area("fill",(-3.8,-2.4,2.2),320,(0.65,0.78,1.0),3.5)
cd=bpy.data.cameras.new("rc"); cd.lens=85; cd.dof.use_dof=True; cd.dof.aperture_fstop=3.2
rc=bpy.data.objects.new("rc",cd); sc.collection.objects.link(rc); sc.camera=rc
sc.render.resolution_x=1000; sc.render.resolution_y=1250
sc.view_settings.view_transform="AgX"
try: sc.view_settings.look="AgX - Medium High Contrast"
except Exception: pass
tgt=mathutils.Vector((0,0,1.02))
for tag,ang,dist,zz in [("hero",20,4.3,1.15),("front",0,4.3,1.05),("q34",42,4.1,1.1),("back",165,4.4,1.1)]:
    a=math.radians(ang); rc.location=(math.sin(a)*dist,-math.cos(a)*dist,zz)
    dv=tgt-mathutils.Vector(rc.location); rc.rotation_euler=dv.to_track_quat("-Z","Y").to_euler()
    cd.dof.focus_distance=dv.length
    sc.render.filepath=os.path.join(outdir,f"v5-{tag}.png"); bpy.ops.render.render(write_still=True); print("WROTE",sc.render.filepath)
print("DONE")
