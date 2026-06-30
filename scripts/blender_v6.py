"""v6: clean remesh + REAL fur everywhere + clothing projection masked to TORSO only
+ geometry eyes/nose/glasses/whiskers on a fur head + cinematic render.
  blender -b -P scripts/blender_v6.py -- <geo.glb> <refdir> <out_dir> [eyeZ] [eyeX] [noseDY]
"""
import bpy, sys, math, os, mathutils
A=sys.argv[sys.argv.index("--")+1:]
geo, refdir, outdir = A[0], A[1], A[2]
EYEZ=float(A[3]) if len(A)>3 else 1.60
EYEX=float(A[4]) if len(A)>4 else 0.145
R=lambda n: os.path.join(refdir,n)
os.makedirs(outdir, exist_ok=True)
FCX,FCY,FH=0.539,0.503,0.892

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

# muzzle front at eye height (for placing facial geometry)
vs=[v.co for v in body.data.vertices]
band=[v for v in vs if abs(v.z-EYEZ)<0.12]
front_y=min(v.y for v in band) if band else -0.5
print(f"eye anchor z={EYEZ} front_y={front_y:.3f}")

def mat(nm,col,rough,metal=0.0,coat=0.0):
    m=bpy.data.materials.new(nm); m.use_nodes=True
    b=next(n for n in m.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value=(*col,1); b.inputs["Roughness"].default_value=rough; b.inputs["Metallic"].default_value=metal
    for k in ("Coat Weight",):
        if k in b.inputs: b.inputs[k].default_value=coat
    return m,b

# eyes (dark, wet clear-coat)
em,eb=mat("eye",(0.015,0.012,0.01),0.08,coat=1.0)
em2,_=mat("iris",(0.18,0.09,0.04),0.2,coat=1.0)
for sx in (-EYEX,EYEX):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.056,location=(sx,front_y+0.02,EYEZ))
    o=bpy.context.active_object; o.data.materials.append(em2); bpy.ops.object.shade_smooth()
# nose
nm_,nb=mat("nose",(0.18,0.08,0.07),0.28,coat=0.6)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.042,location=(0,front_y-0.03,EYEZ-0.135))
o=bpy.context.active_object; o.scale=(1.3,0.9,0.8); o.data.materials.append(nm_); bpy.ops.object.shade_smooth()
# glasses: gold rings + bridge
gm,gb=mat("frame",(0.62,0.45,0.14),0.22,metal=1.0)
for sx in (-EYEX,EYEX):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.082,minor_radius=0.0085,location=(sx,front_y+0.018,EYEZ))
    o=bpy.context.active_object; o.rotation_euler=(math.radians(90),0,0); o.data.materials.append(gm)
bpy.ops.mesh.primitive_cylinder_add(radius=0.007,depth=0.09,location=(0,front_y+0.012,EYEZ+0.01))
o=bpy.context.active_object; o.rotation_euler=(0,math.radians(90),0); o.data.materials.append(gm)
# whiskers (fine, swept)
wm,wb=mat("whisker",(0.92,0.88,0.8),0.45)
for side in(-1,1):
    for i,a in enumerate((0.28,0.12,-0.04)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0028,depth=0.4,location=(side*0.12,front_y+0.01,EYEZ-0.15-i*0.03))
        o=bpy.context.active_object; o.rotation_euler=(0,math.radians(88)*side,a*side); o.data.materials.append(wm)

# --- body material: fur (triplanar) + TORSO-only clothing projection ---
front=bpy.data.images.load(R("front.png")); iw,ih=front.size
furimg=bpy.data.images.load(R("furbody.png"))
oscale=2.0/FH
pc_d=bpy.data.cameras.new("proj"); pc_d.type="ORTHO"; pc_d.ortho_scale=oscale
pc=bpy.data.objects.new("proj",pc_d); pc.location=((FCX-0.5)*oscale,-6,1.0+(0.5-FCY)*oscale); pc.rotation_euler=(math.radians(90),0,0)
bpy.context.scene.collection.objects.link(pc)
uvp=body.data.uv_layers.new(name="proj"); body.data.uv_layers.active=uvp
mod=body.modifiers.new("proj","UV_PROJECT"); mod.uv_layer="proj"; mod.projector_count=1; mod.projectors[0].object=pc; mod.aspect_x=iw/ih; mod.aspect_y=1.0
bm=bpy.data.materials.new("drm"); bm.use_nodes=True; nt=bm.node_tree; nd=nt.nodes
bsdf=next(n for n in nd if n.type=="BSDF_PRINCIPLED"); bsdf.inputs["Roughness"].default_value=0.72
for k in ("Sheen Weight","Sheen"):
    if k in bsdf.inputs: bsdf.inputs[k].default_value=0.6; break
tc=nd.new("ShaderNodeTexCoord"); mp=nd.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(7,7,7)
nt.links.new(tc.outputs["Object"],mp.inputs["Vector"])
fur=nd.new("ShaderNodeTexImage"); fur.image=furimg; fur.projection="BOX"; fur.projection_blend=0.35
nt.links.new(mp.outputs["Vector"],fur.inputs["Vector"])
ftex=nd.new("ShaderNodeTexImage"); ftex.image=front; ftex.extension="EXTEND"
uvn=nd.new("ShaderNodeUVMap"); uvn.uv_map="proj"; nt.links.new(uvn.outputs["UV"],ftex.inputs["Vector"])
# facing weight
gn=nd.new("ShaderNodeNewGeometry"); dp=nd.new("ShaderNodeVectorMath"); dp.operation="DOT_PRODUCT"; dp.inputs[1].default_value=(0,-1,0)
nt.links.new(gn.outputs["Normal"],dp.inputs[0])
fr=nd.new("ShaderNodeMapRange"); fr.inputs["From Min"].default_value=0.45; fr.inputs["From Max"].default_value=0.72; fr.clamp=True
nt.links.new(dp.outputs["Value"],fr.inputs["Value"])
# torso z-band mask (separate position from geometry): low edge ~0.35 high edge ~1.32
sep=nd.new("ShaderNodeSeparateXYZ"); nt.links.new(gn.outputs["Position"],sep.inputs["Vector"])
zlo=nd.new("ShaderNodeMapRange"); zlo.inputs["From Min"].default_value=0.30; zlo.inputs["From Max"].default_value=0.45; zlo.clamp=True
nt.links.new(sep.outputs["Z"],zlo.inputs["Value"])
zhi=nd.new("ShaderNodeMapRange"); zhi.inputs["From Min"].default_value=1.38; zhi.inputs["From Max"].default_value=1.20; zhi.clamp=True
nt.links.new(sep.outputs["Z"],zhi.inputs["Value"])
zmask=nd.new("ShaderNodeMath"); zmask.operation="MULTIPLY"
nt.links.new(zlo.outputs["Result"],zmask.inputs[0]); nt.links.new(zhi.outputs["Result"],zmask.inputs[1])
wgt=nd.new("ShaderNodeMath"); wgt.operation="MULTIPLY"
nt.links.new(fr.outputs["Result"],wgt.inputs[0]); nt.links.new(zmask.outputs["Value"],wgt.inputs[1])
mix=nd.new("ShaderNodeMix"); mix.data_type="RGBA"
nt.links.new(fur.outputs["Color"],mix.inputs[6]); nt.links.new(ftex.outputs["Color"],mix.inputs[7]); nt.links.new(wgt.outputs["Value"],mix.inputs[0])
nt.links.new(mix.outputs[2],bsdf.inputs["Base Color"])
bw=nd.new("ShaderNodeRGBToBW"); nt.links.new(fur.outputs["Color"],bw.inputs["Color"])
bump=nd.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.18; bump.inputs["Distance"].default_value=0.02
nt.links.new(bw.outputs["Val"],bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"],bsdf.inputs["Normal"])
body.data.materials.clear(); body.data.materials.append(bm)

# cinematic render
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
area("key",(3.4,-3.2,4.4),1600,(1.0,0.84,0.6),3.0); area("rim",(-2.6,3.2,3.8),1400,(1.0,0.7,0.42),2.0); area("fill",(-3.8,-2.4,2.2),320,(0.65,0.78,1.0),3.5)
cd=bpy.data.cameras.new("rc"); cd.lens=85; cd.dof.use_dof=True; cd.dof.aperture_fstop=3.2
rc=bpy.data.objects.new("rc",cd); sc.collection.objects.link(rc); sc.camera=rc
sc.render.resolution_x=1000; sc.render.resolution_y=1250; sc.view_settings.view_transform="AgX"
try: sc.view_settings.look="AgX - Medium High Contrast"
except Exception: pass
tgt=mathutils.Vector((0,0,1.02))
for tag,ang,dist,zz,fz in [("hero",18,4.3,1.15,1.02),("face",6,2.4,1.62,1.6),("q34",40,4.1,1.1,1.02),("back",165,4.4,1.1,1.02)]:
    a=math.radians(ang); rc.location=(math.sin(a)*dist,-math.cos(a)*dist,zz)
    dv=mathutils.Vector((0,0,fz))-mathutils.Vector(rc.location); rc.rotation_euler=dv.to_track_quat("-Z","Y").to_euler()
    cd.dof.focus_distance=dv.length
    sc.render.filepath=os.path.join(outdir,f"v6-{tag}.png"); bpy.ops.render.render(write_still=True); print("WROTE",sc.render.filepath)
print("DONE")
