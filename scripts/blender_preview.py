"""Render a clean studio preview of a GLB. Run headless:
   blender -b -P scripts/blender_preview.py -- <in.glb> <out.png> [yaw_deg]
"""
import bpy, sys, math, os

argv = sys.argv[sys.argv.index("--") + 1:]
src = argv[0]
out = argv[1]
yaw = float(argv[2]) if len(argv) > 2 else 35.0

# clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# import glb
bpy.ops.import_scene.gltf(filepath=src)
objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
if not objs:
    raise SystemExit("no mesh imported")

# join + center + scale to unit height
for o in objs:
    o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
if len(objs) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active

# smooth shading
bpy.ops.object.shade_smooth()

# recompute bounds, center on origin, sit on floor
bpy.context.view_layer.update()
bb = [obj.matrix_world @ v.co for v in obj.data.vertices]
xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
cx = (min(xs)+max(xs))/2; cy = (min(ys)+max(ys))/2
height = max(zs) - min(zs)
s = 2.0 / height if height else 1.0
obj.location = (-cx*s, -cy*s, -min(zs)*s)
obj.scale = (s, s, s)
obj.rotation_euler[2] = math.radians(yaw)
bpy.context.view_layer.update()

# ensure vertex colors show: if material has no base-color texture, wire the color attribute in
for slot in obj.material_slots:
    m = slot.material
    if not m:
        continue
    m.use_nodes = True
    nt = m.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    has_tex = any(n.type == "TEX_IMAGE" for n in nt.nodes)
    if bsdf and not has_tex and obj.data.color_attributes:
        ca = nt.nodes.new("ShaderNodeVertexColor")
        ca.layer_name = obj.data.color_attributes[0].name
        nt.links.new(ca.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.62
# if no material at all, make one from vertex colors
if not obj.material_slots and obj.data.color_attributes:
    m = bpy.data.materials.new("vc"); m.use_nodes = True
    nt = m.node_tree; bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    ca = nt.nodes.new("ShaderNodeVertexColor"); ca.layer_name = obj.data.color_attributes[0].name
    nt.links.new(ca.outputs["Color"], bsdf.inputs["Base Color"])
    obj.data.materials.append(m)

# camera
cam_data = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_data)
bpy.context.scene.collection.objects.link(cam)
cam.location = (0, -4.2, 1.3); cam.rotation_euler = (math.radians(80), 0, 0)
cam_data.lens = 60
bpy.context.scene.camera = cam

# warm 3-point lighting matching the lab mood
def lamp(name, loc, energy, color, size=3.0):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.color = color; d.size = size
    o = bpy.data.objects.new(name, d); o.location = loc
    bpy.context.scene.collection.objects.link(o)
    # aim at origin
    import mathutils
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = (mathutils.Vector(loc)).to_track_quat("Z", "Y").rotation_difference(
        (mathutils.Vector((0,0,1)))) if False else o.rotation_quaternion
    return o
key = lamp("key", (3, -3, 4), 900, (1.0, 0.86, 0.66))
fill = lamp("fill", (-3.5, -2, 2.5), 250, (0.75, 0.82, 1.0))
rim = lamp("rim", (0, 4, 3.5), 600, (1.0, 0.78, 0.5))
# point lamps toward subject
for L in (key, fill, rim):
    c = bpy.data.objects.new(L.name+"_t", None); c.location = (0,0,1)
    bpy.context.scene.collection.objects.link(c)
    tc = L.constraints.new("TRACK_TO"); tc.target = c; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"

# warm dark world bg
world = bpy.data.worlds.new("w"); bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.03, 0.022, 0.014, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.35

# render settings — EEVEE Next, fast, clean
sc = bpy.context.scene
try:
    sc.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x = 900; sc.render.resolution_y = 1100
sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX"
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("WROTE", out)
