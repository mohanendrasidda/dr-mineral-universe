"""Dr. Mineral 3D v2 — fix the analyzer's defects in Blender (free, headless).
  decimate -> re-unwrap (bigger islands) -> project painting + FUR underlay
  -> bake (big EXTEND margin, no black) -> strip dead channels -> Draco GLB.

Run:
  blender -b -P scripts/blender_drm_v2.py -- <geo.glb> <ref.png> <out_dir> <out.glb> [yaw] [target_tris]
"""
import bpy, sys, math, os, mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
geo, ref, outdir, outglb = argv[0], argv[1], argv[2], argv[3]
yaw = float(argv[4]) if len(argv) > 4 else 35.0
target_tris = int(argv[5]) if len(argv) > 5 else 50000
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

# --- FIX 1: decimate to web budget (collapse), BEFORE unwrap so islands stay big ---
src_tris = len(obj.data.polygons)
ratio = max(0.01, min(1.0, target_tris / max(1, src_tris)))
dec = obj.modifiers.new("dec", "DECIMATE")
dec.decimate_type = "COLLAPSE"; dec.ratio = ratio
bpy.ops.object.modifier_apply(modifier="dec")
bpy.ops.object.shade_smooth()
print(f"decimated {src_tris} -> {len(obj.data.polygons)} tris (ratio {ratio:.3f})")

# normalize: center, height 2, face -Y, apply transforms
bpy.context.view_layer.update()
co = [obj.matrix_world @ v.co for v in obj.data.vertices]
xs=[v.x for v in co]; ys=[v.y for v in co]; zs=[v.z for v in co]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; h=max(zs)-min(zs); s=2.0/h if h else 1.0
obj.location=(-cx*s,-cy*s,-min(zs)*s); obj.scale=(s,s,s); obj.rotation_euler[2]=math.radians(yaw)
bpy.context.view_layer.update()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

img = bpy.data.images.load(os.path.abspath(ref)); iw, ih = img.size

# orthographic projector in front (-Y)
cam_d = bpy.data.cameras.new("proj"); cam_d.type="ORTHO"; cam_d.ortho_scale=2.5
cam = bpy.data.objects.new("proj", cam_d); cam.location=(0,-6,1.0); cam.rotation_euler=(math.radians(90),0,0)
bpy.context.scene.collection.objects.link(cam)

# projection UV via UV Project modifier (headless-safe)
uvp = obj.data.uv_layers.new(name="proj"); obj.data.uv_layers.active = uvp
mod = obj.modifiers.new("proj","UV_PROJECT"); mod.uv_layer="proj"; mod.projector_count=1
mod.projectors[0].object = cam; mod.aspect_x=iw/ih; mod.aspect_y=1.0

# --- FIX 3: material = painting (front) smoothly blended over a FUR underlay (no black) ---
FUR=(0.42,0.115,0.035,1.0)
mat=bpy.data.materials.new("drm"); mat.use_nodes=True; nt=mat.node_tree; nd=nt.nodes
bsdf=next(n for n in nd if n.type=="BSDF_PRINCIPLED")
tex=nd.new("ShaderNodeTexImage"); tex.image=img; tex.extension="EXTEND"
uvn=nd.new("ShaderNodeUVMap"); uvn.uv_map="proj"; nt.links.new(uvn.outputs["UV"],tex.inputs["Vector"])
geo_n=nd.new("ShaderNodeNewGeometry")
dot=nd.new("ShaderNodeVectorMath"); dot.operation="DOT_PRODUCT"; dot.inputs[1].default_value=(0,-1,0)
nt.links.new(geo_n.outputs["Normal"],dot.inputs[0])
rng=nd.new("ShaderNodeMapRange")
rng.inputs["From Min"].default_value=0.05; rng.inputs["From Max"].default_value=0.55; rng.clamp=True
nt.links.new(dot.outputs["Value"],rng.inputs["Value"])
mix=nd.new("ShaderNodeMix"); mix.data_type="RGBA"
mix.inputs[6].default_value=FUR
nt.links.new(tex.outputs["Color"],mix.inputs[7]); nt.links.new(rng.outputs["Result"],mix.inputs[0])
nt.links.new(mix.outputs[2],bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value=0.7
obj.data.materials.clear(); obj.data.materials.append(mat)

# --- FIX 2: re-unwrap the LIGHT mesh -> bigger islands, face gets more texels ---
uvb=obj.data.uv_layers.new(name="bake"); obj.data.uv_layers.active=uvb
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.006)
bpy.ops.object.mode_set(mode="OBJECT")

# bake base color into a clean 2048 atlas with big EXTEND margin (kills speckle)
bake_img=bpy.data.images.new("drm_baked",2048,2048)
bnode=nd.new("ShaderNodeTexImage"); bnode.image=bake_img
buv=nd.new("ShaderNodeUVMap"); buv.uv_map="bake"; nt.links.new(buv.outputs["UV"],bnode.inputs["Vector"])
nd.active=bnode
sc=bpy.context.scene; sc.render.engine="CYCLES"
try: sc.cycles.device="GPU"
except Exception: pass
sc.cycles.samples=4
sc.render.bake.use_pass_direct=False; sc.render.bake.use_pass_indirect=False
sc.render.bake.margin=32
try: sc.render.bake.margin_type="EXTEND"
except Exception: pass
bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True); bpy.context.view_layer.objects.active=obj
print("baking..."); bpy.ops.object.bake(type="DIFFUSE")
bpy.context.view_layer.update()
baked=os.path.join(outdir,"drm_baked.png")
bake_img.filepath_raw=os.path.abspath(baked); bake_img.file_format="PNG"; bake_img.save()

# --- FIX 4: final PBR-ish material: baked color + leather/fur roughness split by facing ---
m2=bpy.data.materials.new("drm_final"); m2.use_nodes=True; n2=m2.node_tree; x2=n2.nodes
b2=next(n for n in x2 if n.type=="BSDF_PRINCIPLED")
t2=x2.new("ShaderNodeTexImage"); t2.image=bake_img
u2=x2.new("ShaderNodeUVMap"); u2.uv_map="bake"; n2.links.new(u2.outputs["UV"],t2.inputs["Vector"])
n2.links.new(t2.outputs["Color"],b2.inputs["Base Color"])
# roughness: front (leather/jacket) a bit glossier, sides/back (fur) matte
g2=x2.new("ShaderNodeNewGeometry"); d2=x2.new("ShaderNodeVectorMath"); d2.operation="DOT_PRODUCT"; d2.inputs[1].default_value=(0,-1,0)
n2.links.new(g2.outputs["Normal"],d2.inputs[0])
mr=x2.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value=0.05; mr.inputs["From Max"].default_value=0.55
mr.inputs["To Min"].default_value=0.85; mr.inputs["To Max"].default_value=0.45; mr.clamp=True
n2.links.new(d2.outputs["Value"],mr.inputs["Value"]); n2.links.new(mr.outputs["Result"],b2.inputs["Roughness"])
obj.data.materials.clear(); obj.data.materials.append(m2)

# --- strip dead data: drop projection UV + any vertex-color attrs -> only 'bake' UV remains ---
uvls=obj.data.uv_layers
if "proj" in uvls: uvls.remove(uvls["proj"])
for ca in list(obj.data.color_attributes):
    obj.data.color_attributes.remove(ca)
obj.data.uv_layers.active = obj.data.uv_layers["bake"]
print("verts:",len(obj.data.vertices)," uv_layers:",[l.name for l in obj.data.uv_layers]," color_attrs:",len(obj.data.color_attributes))

# ---- preview renders (EEVEE) ----
def lamp(nm,loc,e,c,sz=3.0):
    d=bpy.data.lights.new(nm,"AREA"); d.energy=e; d.color=c; d.size=sz
    o=bpy.data.objects.new(nm,d); o.location=loc; bpy.context.scene.collection.objects.link(o)
    t=bpy.data.objects.new(nm+"_t",None); t.location=(0,0,1); bpy.context.scene.collection.objects.link(t)
    cc=o.constraints.new("TRACK_TO"); cc.target=t; cc.track_axis="TRACK_NEGATIVE_Z"; cc.up_axis="UP_Y"
lamp("key",(3,-3,4),900,(1.0,0.86,0.66)); lamp("fill",(-3.5,-2,2.5),250,(0.75,0.82,1.0)); lamp("rim",(0,4,3.5),650,(1.0,0.78,0.5))
w=bpy.data.worlds.new("w"); bpy.context.scene.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[0].default_value=(0.03,0.022,0.014,1); w.node_tree.nodes["Background"].inputs[1].default_value=0.35
rc_d=bpy.data.cameras.new("rc"); rc_d.lens=60; rc=bpy.data.objects.new("rc",rc_d); bpy.context.scene.collection.objects.link(rc); sc.camera=rc
try: sc.render.engine="BLENDER_EEVEE_NEXT"
except Exception: sc.render.engine="BLENDER_EEVEE"
sc.render.resolution_x=820; sc.render.resolution_y=1000; sc.view_settings.view_transform="AgX"
for tag,ang in [("front",0),("q34",35),("side",90),("back",180)]:
    r=4.4; a=math.radians(ang); rc.location=(math.sin(a)*r,-math.cos(a)*r,1.25)
    dv=mathutils.Vector((0,0,1))-mathutils.Vector(rc.location); rc.rotation_euler=dv.to_track_quat("-Z","Y").to_euler()
    sc.render.filepath=os.path.join(outdir,f"v2-{tag}.png"); bpy.ops.render.render(write_still=True); print("WROTE",sc.render.filepath)

# --- export: Draco-compressed GLB, single UV, uint16 indices (auto, verts<65k) ---
bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True); bpy.context.view_layer.objects.active=obj
bpy.ops.export_scene.gltf(filepath=os.path.abspath(outglb), export_format="GLB", use_selection=True,
    export_apply=True, export_image_format="AUTO",
    export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6)
print("EXPORTED",outglb, round(os.path.getsize(outglb)/1e6,2),"MB")
