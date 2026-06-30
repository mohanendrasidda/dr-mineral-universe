"""Project a front reference painting onto a GLB's geometry as a real texture
(via UV Project modifier — works headless), then render previews + export a GLB.

  blender -b -P scripts/blender_project_texture.py -- <geo.glb> <ref.png> <out_dir> <out.glb> [yaw]
"""
import bpy, sys, math, os, mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
geo, ref, outdir, outglb = argv[0], argv[1], argv[2], argv[3]
yaw = float(argv[4]) if len(argv) > 4 else 35.0
os.makedirs(outdir, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=geo)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
bpy.ops.object.shade_smooth()

# normalize: center on origin, height = 2, sit on floor, yaw to face -Y (toward projector)
bpy.context.view_layer.update()
co = [obj.matrix_world @ v.co for v in obj.data.vertices]
xs=[v.x for v in co]; ys=[v.y for v in co]; zs=[v.z for v in co]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2
h=max(zs)-min(zs); s=2.0/h if h else 1.0
obj.location=(-cx*s,-cy*s,-min(zs)*s); obj.scale=(s,s,s)
obj.rotation_euler[2]=math.radians(yaw)
bpy.context.view_layer.update()
# apply transforms so the projector aligns to world geometry
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# load image, get aspect
img = bpy.data.images.load(os.path.abspath(ref))
iw, ih = img.size[0], img.size[1]

# orthographic projector camera in front (-Y), looking +Y
cam_d = bpy.data.cameras.new("proj"); cam_d.type = "ORTHO"
cam_d.ortho_scale = 2.5
cam = bpy.data.objects.new("proj", cam_d); cam.location = (0, -6, 1.0)
cam.rotation_euler = (math.radians(90), 0, 0)
bpy.context.scene.collection.objects.link(cam)

# UV layer + UV Project modifier (headless-safe camera projection)
uv = obj.data.uv_layers.new(name="proj")
obj.data.uv_layers.active = uv
mod = obj.modifiers.new("proj", "UV_PROJECT")
mod.uv_layer = "proj"
mod.projector_count = 1
mod.projectors[0].object = cam
mod.aspect_x = iw / ih
mod.aspect_y = 1.0
mod.scale_x = 1.0; mod.scale_y = 1.0

# Single material: smoothly blend the projected painting (front) with solid fur (sides/back),
# weighted by how much each surface faces the projector. No jagged seams.
FUR = (0.42, 0.115, 0.035, 1.0)     # warm orange-brown, matched to the painting's tail
mat = bpy.data.materials.new("drm_proj"); mat.use_nodes = True
nt = mat.node_tree; nodes = nt.nodes
bsdf = next(n for n in nodes if n.type == "BSDF_PRINCIPLED")
tex = nodes.new("ShaderNodeTexImage"); tex.image = img; tex.extension = "EXTEND"
uvn = nodes.new("ShaderNodeUVMap"); uvn.uv_map = "proj"
nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
# facing factor: dot(geometry normal, -Y) -> smoothstep
geo = nodes.new("ShaderNodeNewGeometry")
dot = nodes.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
dot.inputs[1].default_value = (0.0, -1.0, 0.0)
nt.links.new(geo.outputs["Normal"], dot.inputs[0])
ramp = nodes.new("ShaderNodeMapRange")     # soft transition band
ramp.inputs["From Min"].default_value = 0.05
ramp.inputs["From Max"].default_value = 0.55
ramp.inputs["To Min"].default_value = 0.0
ramp.inputs["To Max"].default_value = 1.0
ramp.clamp = True
nt.links.new(dot.outputs["Value"], ramp.inputs["Value"])
mix = nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
# socket indices for RGBA mix: 0=Factor(float), 6=A(color), 7=B(color); out 2=Result(color)
mix.inputs[6].default_value = FUR             # facing away -> fur
nt.links.new(tex.outputs["Color"], mix.inputs[7])   # facing front -> painting
nt.links.new(ramp.outputs["Result"], mix.inputs[0])
nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.64
obj.data.materials.clear(); obj.data.materials.append(mat)

# ---- bake the blended base color into a flat texture so the GLB is self-contained ----
# second UV set with no overlaps, for the bake target
uv2 = obj.data.uv_layers.new(name="bake")
obj.data.uv_layers.active = uv2
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.002)
bpy.ops.object.mode_set(mode="OBJECT")
bake_img = bpy.data.images.new("drm_baked", 2048, 2048)
bnode = nodes.new("ShaderNodeTexImage"); bnode.image = bake_img
buv = nodes.new("ShaderNodeUVMap"); buv.uv_map = "bake"
nt.links.new(buv.outputs["UV"], bnode.inputs["Vector"])
nodes.active = bnode    # bake target
sc = bpy.context.scene
sc.render.engine = "CYCLES"
try: sc.cycles.device = "GPU"
except Exception: pass
sc.cycles.samples = 4
sc.render.bake.use_pass_direct = False
sc.render.bake.use_pass_indirect = False
sc.render.bake.margin = 6
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True); bpy.context.view_layer.objects.active = obj
print("baking diffuse color...")
bpy.ops.object.bake(type="DIFFUSE")
baked_path = os.path.join(outdir, "drm_baked.png")
bake_img.filepath_raw = os.path.abspath(baked_path); bake_img.file_format = "PNG"
bake_img.save()
print("baked ->", baked_path)

# rebuild a clean simple material using the baked texture on the 'bake' UV
mat2 = bpy.data.materials.new("drm_final"); mat2.use_nodes = True
n2 = mat2.node_tree
b2 = next(n for n in n2.nodes if n.type == "BSDF_PRINCIPLED")
t2 = n2.nodes.new("ShaderNodeTexImage"); t2.image = bake_img
u2 = n2.nodes.new("ShaderNodeUVMap"); u2.uv_map = "bake"
n2.links.new(u2.outputs["UV"], t2.inputs["Vector"])
n2.links.new(t2.outputs["Color"], b2.inputs["Base Color"])
b2.inputs["Roughness"].default_value = 0.64
obj.data.materials.clear(); obj.data.materials.append(mat2)
# make 'bake' the only/active UV for export cleanliness
obj.data.uv_layers.active = obj.data.uv_layers["bake"]

# ---- preview render setup ----
def lamp(name, loc, energy, color, size=3.0):
    d=bpy.data.lights.new(name,"AREA"); d.energy=energy; d.color=color; d.size=size
    o=bpy.data.objects.new(name,d); o.location=loc
    bpy.context.scene.collection.objects.link(o)
    t=bpy.data.objects.new(name+"_t",None); t.location=(0,0,1)
    bpy.context.scene.collection.objects.link(t)
    c=o.constraints.new("TRACK_TO"); c.target=t; c.track_axis="TRACK_NEGATIVE_Z"; c.up_axis="UP_Y"
    return o
lamp("key",(3,-3,4),900,(1.0,0.86,0.66))
lamp("fill",(-3.5,-2,2.5),250,(0.75,0.82,1.0))
lamp("rim",(0,4,3.5),600,(1.0,0.78,0.5))
world=bpy.data.worlds.new("w"); bpy.context.scene.world=world; world.use_nodes=True
world.node_tree.nodes["Background"].inputs[0].default_value=(0.03,0.022,0.014,1)
world.node_tree.nodes["Background"].inputs[1].default_value=0.35

rcam_d=bpy.data.cameras.new("rcam"); rcam_d.lens=60
rcam=bpy.data.objects.new("rcam",rcam_d); bpy.context.scene.collection.objects.link(rcam)
bpy.context.scene.camera=rcam
sc=bpy.context.scene
try: sc.render.engine="BLENDER_EEVEE_NEXT"
except Exception: sc.render.engine="BLENDER_EEVEE"
sc.render.resolution_x=820; sc.render.resolution_y=1000
sc.view_settings.view_transform="AgX"

# render the SAME geometry from a few camera angles (orbit the render cam, model stays put so projection is fixed)
import math as _m
for tag, ang in [("front",0),("q34",35),("side",90)]:
    r=4.4; a=_m.radians(ang)
    rcam.location=( _m.sin(a)*r, -_m.cos(a)*r, 1.25 )
    # aim at (0,0,1)
    d=mathutils.Vector((0,0,1))-mathutils.Vector(rcam.location)
    rcam.rotation_euler=d.to_track_quat("-Z","Y").to_euler()
    sc.render.filepath=os.path.join(outdir,f"proj-{tag}.png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath)

# export a self-contained GLB (applies the UV Project modifier + embeds texture)
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True); bpy.context.view_layer.objects.active=obj
bpy.ops.export_scene.gltf(filepath=os.path.abspath(outglb), export_format="GLB",
                          use_selection=True, export_apply=True, export_image_format="AUTO")
print("EXPORTED", outglb)
