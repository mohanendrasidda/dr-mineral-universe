"""Merge Meshy per-clip glbs into ONE web hero glb with multiple NLA-track animations,
downscaling the 4K texture to 1K. Usage:
  blender -b -P merge_hero.py -- <out.glb> <texpx> <Name=walk.glb> <Name=idle.glb> ...
Each extra arg is 'ClipName=/path/to/withSkin.glb'. The FIRST is the base (keeps its mesh).
"""
import bpy, sys
A=sys.argv[sys.argv.index("--")+1:]
out_glb=A[0]; texpx=int(A[1]); specs=[s.split("=",1) for s in A[2:]]

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete()
for a in list(bpy.data.actions): bpy.data.actions.remove(a)

def names(): return set(o.name for o in bpy.context.scene.objects)

base_arm=None; base_meshes=[]
for i,(clip,path) in enumerate(specs):
    before=names()
    bpy.ops.import_scene.gltf(filepath=path)
    new=[o for o in bpy.context.scene.objects if o.name not in before]
    arm=next((o for o in new if o.type=="ARMATURE"), None)
    meshes=[o for o in new if o.type=="MESH"]
    # grab this import's action, rename to the clip name
    act=None
    if arm and arm.animation_data and arm.animation_data.action:
        act=arm.animation_data.action
    if act is None:
        # fallback: the most recently added action
        act=bpy.data.actions[-1] if bpy.data.actions else None
    if act: act.name=clip; act.use_fake_user=True
    if i==0:
        base_arm=arm; base_meshes=meshes
    else:
        # drop the duplicate geometry+armature, keep only the (renamed) action
        for o in meshes+([arm] if arm else []):
            bpy.data.objects.remove(o, do_unlink=True)
    print("CLIP", clip, "-> action", act.name if act else None, flush=True)

# build one NLA track per action on the base armature
ad=base_arm.animation_data_create(); ad.action=None
for tr in list(ad.nla_tracks): ad.nla_tracks.remove(tr)
for clip,_ in specs:
    act=bpy.data.actions.get(clip)
    if not act: continue
    trk=ad.nla_tracks.new(); trk.name=clip
    trk.strips.new(clip, int(act.frame_range[0]), act)
print("NLA tracks:", [t.name for t in ad.nla_tracks], flush=True)

# downscale big textures
for img in bpy.data.images:
    if img.size[0] > texpx:
        print("SCALE", img.name, tuple(img.size), "->", texpx, flush=True)
        img.scale(texpx, texpx)

# select base armature + meshes and export
bpy.ops.object.select_all(action="DESELECT")
for o in [base_arm]+base_meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active=base_arm
bpy.ops.export_scene.gltf(filepath=out_glb, use_selection=True, export_format='GLB',
                          export_animation_mode='NLA_TRACKS', export_animations=True,
                          export_apply=False)
print("EXPORTED", out_glb, flush=True)
print("MERGE_DONE", flush=True)
