"""Best free-local polish: clean remesh base + re-add eyes/glasses/whiskers as geometry
+ PBR materials + projected face/clothing + CINEMATIC Cycles render.
  blender -b -P scripts/blender_polish.py -- <geo.glb> <ref.png> <out_dir>
"""
import bpy, sys, math, os, mathutils
A = sys.argv[sys.argv.index("--")+1:]
geo, ref, outdir = A[0], A[1], A[2]
os.makedirs(outdir, exist_ok=True)

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

# clean remesh for a coherent surface
rm=body.modifiers.new("rm","REMESH"); rm.mode="VOXEL"; rm.voxel_size=0.011; rm.use_smooth_shade=True
bpy.ops.object.modifier_apply(modifier="rm")
bpy.ops.object.shade_smooth()

# locate the head-front (top band, frontmost) to anchor eyes/glasses
vs=[v.co for v in body.data.vertices]
top=max(v.z for v in vs)
headband=[v for v in vs if v.z>top-0.42]
hy_front=min(v.y for v in headband)
hz=sum(v.z for v in headband)/len(headband)+0.04
print(f"head anchor: front_y={hy_front:.3f} eye_z={hz:.3f} top={top:.3f}")

def mat(name,color,rough,metal=0.0,sheen=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=next(n for n in m.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value=(*color,1); b.inputs["Roughness"].default_value=rough
    b.inputs["Metallic"].default_value=metal
    for key in ("Sheen Weight","Sheen"):
        if key in b.inputs: b.inputs[key].default_value=sheen; break
    return m

# --- re-add EYES (glossy dark spheres) ---
eye_mat=mat("eye",(0.02,0.015,0.01),0.12)
eyes=[]
for sx in (-0.20,0.20):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.085, location=(sx, hy_front+0.03, hz))
    e=bpy.context.active_object; e.data.materials.append(eye_mat); bpy.ops.object.shade_smooth(); eyes.append(e)

# --- re-add GLASSES (thin metal rings + bridge) ---
glass_mat=mat("glass_frame",(0.08,0.06,0.03),0.25,metal=1.0)
rings=[]
for sx in (-0.20,0.20):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.125, minor_radius=0.012, location=(sx, hy_front+0.02, hz))
    r=bpy.context.active_object; r.rotation_euler=(math.radians(90),0,0); r.data.materials.append(glass_mat); rings.append(r)
bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.16, location=(0, hy_front+0.02, hz))
br=bpy.context.active_object; br.rotation_euler=(0,math.radians(90),0); br.data.materials.append(glass_mat)

# --- WHISKERS (thin tapered cylinders) ---
wh_mat=mat("whisker",(0.9,0.85,0.78),0.4)
muzzle_z=hz-0.12
for side in (-1,1):
    for i,ang in enumerate((0.25,0.0,-0.25)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=0.5,
            location=(side*0.18, hy_front+0.02, muzzle_z - i*0.03))
        w=bpy.context.active_object
        w.rotation_euler=(0, math.radians(90)*side, ang*side)
        w.scale=(1,1,1); w.data.materials.append(wh_mat)

# --- BODY material: project the painting (front) over a warm fur underlay, with fur micro-bump ---
img=bpy.data.images.load(os.path.abspath(ref)); iw,ih=img.size
cam_d=bpy.data.cameras.new("proj"); cam_d.type="ORTHO"; cam_d.ortho_scale=2.5
pc=bpy.data.objects.new("proj",cam_d); pc.location=(0,-6,1.0); pc.rotation_euler=(math.radians(90),0,0)
bpy.context.scene.collection.objects.link(pc)
uvp=body.data.uv_layers.new(name="proj"); body.data.uv_layers.active=uvp
mod=body.modifiers.new("proj","UV_PROJECT"); mod.uv_layer="proj"; mod.projector_count=1
mod.projectors[0].object=pc; mod.aspect_x=iw/ih; mod.aspect_y=1.0
FUR=(0.40,0.11,0.035,1)
bm=bpy.data.materials.new("body"); bm.use_nodes=True; nt=bm.node_tree; nd=nt.nodes
bsdf=next(n for n in nd if n.type=="BSDF_PRINCIPLED"); bsdf.inputs["Roughness"].default_value=0.72
for key in ("Sheen Weight","Sheen"):
    if key in bsdf.inputs: bsdf.inputs[key].default_value=0.5; break
tex=nd.new("ShaderNodeTexImage"); tex.image=img; tex.extension="EXTEND"
uvn=nd.new("ShaderNodeUVMap"); uvn.uv_map="proj"; nt.links.new(uvn.outputs["UV"],tex.inputs["Vector"])
gn=nd.new("ShaderNodeNewGeometry"); dp=nd.new("ShaderNodeVectorMath"); dp.operation="DOT_PRODUCT"; dp.inputs[1].default_value=(0,-1,0)
nt.links.new(gn.outputs["Normal"],dp.inputs[0])
rg=nd.new("ShaderNodeMapRange"); rg.inputs["From Min"].default_value=0.1; rg.inputs["From Max"].default_value=0.55; rg.clamp=True
nt.links.new(dp.outputs["Value"],rg.inputs["Value"])
mx=nd.new("ShaderNodeMix"); mx.data_type="RGBA"; mx.inputs[6].default_value=FUR
nt.links.new(tex.outputs["Color"],mx.inputs[7]); nt.links.new(rg.outputs["Result"],mx.inputs[0])
nt.links.new(mx.outputs[2],bsdf.inputs["Base Color"])
# fur micro-bump
nz=nd.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value=140
bp=nd.new("ShaderNodeBump"); bp.inputs["Strength"].default_value=0.06
nt.links.new(nz.outputs["Fac"],bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"],bsdf.inputs["Normal"])
body.data.materials.clear(); body.data.materials.append(bm)

# ---------- CINEMATIC render ----------
sc=bpy.context.scene; sc.render.engine="CYCLES"
try: sc.cycles.device="GPU"
except Exception: pass
sc.cycles.samples=96; sc.cycles.use_denoising=True
# warm studio world
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
wn=w.node_tree.nodes["Background"]; wn.inputs[0].default_value=(0.04,0.03,0.02,1); wn.inputs[1].default_value=0.5
def area(nm,loc,e,c,sz):
    d=bpy.data.lights.new(nm,"AREA"); d.energy=e; d.color=c; d.size=sz
    o=bpy.data.objects.new(nm,d); o.location=loc; sc.collection.objects.link(o)
    t=bpy.data.objects.new(nm+"t",None); t.location=(0,0,1.0); sc.collection.objects.link(t)
    cc=o.constraints.new("TRACK_TO"); cc.target=t; cc.track_axis="TRACK_NEGATIVE_Z"; cc.up_axis="UP_Y"
area("key",(3.2,-3.4,4.2),1500,(1.0,0.85,0.62),3.0)
area("rim",(-2.4,3.0,3.6),1200,(1.0,0.72,0.45),2.0)
area("fill",(-3.6,-2.2,2.2),300,(0.7,0.8,1.0),3.5)
cam_d2=bpy.data.cameras.new("rc"); cam_d2.lens=85; cam_d2.dof.use_dof=True; cam_d2.dof.aperture_fstop=2.8
rc=bpy.data.objects.new("rc",cam_d2); sc.collection.objects.link(rc); sc.camera=rc
sc.render.resolution_x=1000; sc.render.resolution_y=1280
sc.view_settings.view_transform="AgX"; sc.view_settings.look="AgX - Medium High Contrast"
tgt=mathutils.Vector((0,0,1.05))
for tag,ang,dist in [("hero",22,4.2),("face",10,2.6),("q34",40,4.0)]:
    a=math.radians(ang); rc.location=(math.sin(a)*dist,-math.cos(a)*dist,1.2 if tag!="face" else 1.55)
    dv=tgt-mathutils.Vector(rc.location); rc.rotation_euler=dv.to_track_quat("-Z","Y").to_euler()
    cam_d2.dof.focus_distance=dv.length
    sc.render.filepath=os.path.join(outdir,f"polish-{tag}.png"); bpy.ops.render.render(write_still=True); print("WROTE",sc.render.filepath)
print("DONE")
