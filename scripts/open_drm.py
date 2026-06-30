"""Open the Dr. Mineral GLB in the Blender GUI, framed, with material shading on.
Launch (GUI):  /Applications/Blender.app/Contents/MacOS/Blender --python scripts/open_drm.py -- <glb>
"""
import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
glb = argv[0] if argv else os.path.abspath("assets/3d/drmineral-v2.glb")
glb = os.path.abspath(glb)

# start from a clean scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

bpy.ops.import_scene.gltf(filepath=glb)

# a soft world light so it isn't black in solid areas
w = bpy.data.worlds.new("w"); bpy.context.scene.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.05, 0.05, 0.06, 1); bg.inputs[1].default_value = 1.0
sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 2.0
so = bpy.data.objects.new("sun", sun); so.rotation_euler = (0.9, 0.1, 0.8)
bpy.context.scene.collection.objects.link(so)

# select the mesh + turn on Material Preview shading, then frame it
mesh = next((o for o in bpy.context.scene.objects if o.type == "MESH"), None)
if mesh:
    bpy.ops.object.select_all(action="DESELECT")
    mesh.select_set(True); bpy.context.view_layer.objects.active = mesh

def setup_view():
    for wm in bpy.data.window_managers:
        for win in wm.windows:
            scr = win.screen
            for area in scr.areas:
                if area.type == "VIEW_3D":
                    for sp in area.spaces:
                        if sp.type == "VIEW_3D":
                            sp.shading.type = "MATERIAL"   # show the baked texture
                    # frame the selected object
                    for region in area.regions:
                        if region.type == "WINDOW":
                            with bpy.context.temp_override(window=win, area=area, region=region):
                                try: bpy.ops.view3d.view_selected()
                                except Exception: pass
    return None

# run once UI is ready
bpy.app.timers.register(setup_view, first_interval=0.3)
print("opened", glb)
