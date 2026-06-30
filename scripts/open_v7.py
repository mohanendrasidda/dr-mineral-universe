"""Build the v7 Dr. Mineral asset and leave it OPEN in the Blender GUI (Material Preview).
Launch (GUI):  /Applications/Blender.app/Contents/MacOS/Blender --python scripts/open_v7.py -- <geo.glb> <refdir>
"""
import bpy, sys, math, os, mathutils
A=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
geo = A[0] if A else os.path.abspath("assets/3d/drmineral-hy.glb")
refdir = A[1] if len(A)>1 else os.path.abspath("assets/image-to-3d/refs/mv")
R=lambda n: os.path.join(refdir,n)
EYEZ, EYEX = 1.60, 0.145
FCX,FCY,FH=0.539,0.503,0.892

for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath(geo))
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

vs=[v.co for v in body.data.vertices]
band=[v for v in vs if abs(v.z-EYEZ)<0.12]; front_y=min(v.y for v in band) if band else -0.5

def mat(nm,col,rough,metal=0.0,coat=0.0):
    m=bpy.data.materials.new(nm); m.use_nodes=True
    b=next(n for n in m.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value=(*col,1); b.inputs["Roughness"].default_value=rough; b.inputs["Metallic"].default_value=metal
    for k in ("Coat Weight",):
        if k in b.inputs: b.inputs[k].default_value=coat
    return m
em2=mat("iris",(0.18,0.09,0.04),0.2,coat=1.0)
for sx in (-EYEX,EYEX):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.056,location=(sx,front_y+0.02,EYEZ))
    o=bpy.context.active_object; o.data.materials.append(em2); o.name="eye"; bpy.ops.object.shade_smooth()
nm_=mat("nose",(0.18,0.08,0.07),0.28,coat=0.6)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.042,location=(0,front_y-0.03,EYEZ-0.135))
o=bpy.context.active_object; o.scale=(1.3,0.9,0.8); o.data.materials.append(nm_); o.name="nose"; bpy.ops.object.shade_smooth()
gm=mat("frame",(0.62,0.45,0.14),0.22,metal=1.0)
for sx in (-EYEX,EYEX):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.082,minor_radius=0.0085,location=(sx,front_y+0.018,EYEZ))
    o=bpy.context.active_object; o.rotation_euler=(math.radians(90),0,0); o.data.materials.append(gm); o.name="glasses"
bpy.ops.mesh.primitive_cylinder_add(radius=0.007,depth=0.09,location=(0,front_y+0.012,EYEZ+0.01))
o=bpy.context.active_object; o.rotation_euler=(0,math.radians(90),0); o.data.materials.append(gm)
wm=mat("whisker",(0.92,0.88,0.8),0.45)
for side in(-1,1):
    for i,a in enumerate((0.28,0.12,-0.04)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0028,depth=0.4,location=(side*0.12,front_y+0.01,EYEZ-0.15-i*0.03))
        o=bpy.context.active_object; o.rotation_euler=(0,math.radians(88)*side,a*side); o.data.materials.append(wm)

front=bpy.data.images.load(R("front.png")); iw,ih=front.size
furimg=bpy.data.images.load(R("furbody.png"))
oscale=2.0/FH
pc_d=bpy.data.cameras.new("proj"); pc_d.type="ORTHO"; pc_d.ortho_scale=oscale
pc=bpy.data.objects.new("proj",pc_d); pc.location=((FCX-0.5)*oscale,-6,1.0+(0.5-FCY)*oscale); pc.rotation_euler=(math.radians(90),0,0)
bpy.context.scene.collection.objects.link(pc)
uvp=body.data.uv_layers.new(name="proj"); body.data.uv_layers.active=uvp
mod=body.modifiers.new("proj","UV_PROJECT"); mod.uv_layer="proj"; mod.projector_count=1; mod.projectors[0].object=pc; mod.aspect_x=iw/ih; mod.aspect_y=1.0
bm=bpy.data.materials.new("drm_body"); bm.use_nodes=True; nt=bm.node_tree; nd=nt.nodes
bsdf=next(n for n in nd if n.type=="BSDF_PRINCIPLED"); bsdf.inputs["Roughness"].default_value=0.72
for k in ("Sheen Weight","Sheen"):
    if k in bsdf.inputs: bsdf.inputs[k].default_value=0.6; break
tc=nd.new("ShaderNodeTexCoord"); mp=nd.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(7,7,7)
nt.links.new(tc.outputs["Object"],mp.inputs["Vector"])
fur=nd.new("ShaderNodeTexImage"); fur.image=furimg; fur.projection="BOX"; fur.projection_blend=0.35
nt.links.new(mp.outputs["Vector"],fur.inputs["Vector"])
ftex=nd.new("ShaderNodeTexImage"); ftex.image=front; ftex.extension="EXTEND"
uvn=nd.new("ShaderNodeUVMap"); uvn.uv_map="proj"; nt.links.new(uvn.outputs["UV"],ftex.inputs["Vector"])
gn=nd.new("ShaderNodeNewGeometry"); dp=nd.new("ShaderNodeVectorMath"); dp.operation="DOT_PRODUCT"; dp.inputs[1].default_value=(0,-1,0)
nt.links.new(gn.outputs["Normal"],dp.inputs[0])
fr=nd.new("ShaderNodeMapRange"); fr.inputs["From Min"].default_value=0.45; fr.inputs["From Max"].default_value=0.72; fr.clamp=True
nt.links.new(dp.outputs["Value"],fr.inputs["Value"])
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

# soft world + sun so it isn't black
w=bpy.data.worlds.new("w"); bpy.context.scene.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[0].default_value=(0.05,0.05,0.06,1); w.node_tree.nodes["Background"].inputs[1].default_value=1.0
sun=bpy.data.lights.new("sun","SUN"); sun.energy=2.0; so=bpy.data.objects.new("sun",sun); so.rotation_euler=(0.9,0.1,0.8); bpy.context.scene.collection.objects.link(so)

bpy.ops.object.select_all(action="DESELECT"); body.select_set(True); bpy.context.view_layer.objects.active=body
def setup_view():
    for wm_ in bpy.data.window_managers:
        for win in wm_.windows:
            for area in win.screen.areas:
                if area.type=="VIEW_3D":
                    for sp in area.spaces:
                        if sp.type=="VIEW_3D": sp.shading.type="MATERIAL"
                    for region in area.regions:
                        if region.type=="WINDOW":
                            with bpy.context.temp_override(window=win,area=area,region=region):
                                try: bpy.ops.view3d.view_selected()
                                except Exception: pass
    return None
bpy.app.timers.register(setup_view, first_interval=0.4)
print("DrMineral v7 built and open")
