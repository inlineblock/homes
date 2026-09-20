"""Continuous eye-level Timber walkthrough; opens a presentation copy only.

Blender --factory-startup -b --python tools/timber02/walkthrough.py -- --build --keyframes
Blender --factory-startup -b --python tools/timber02/walkthrough.py -- --animate
"""
import argparse, bpy, sys, math, json, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
HOME=ROOT/'homes/timber-courtyard-02'
WORK=HOME/'outputs/work/walkthrough'
MODEL=WORK/'timber-walkthrough.blend'
FPS=24
# Seconds, camera XY feet, target XYZ feet. Camera eye height is constant 5.5 ft.
ROUTE=[(0,(33,-22),(31,17,6.2)),(6,(33,-2),(33,23,5.5)),(9,(33,8.5),(33,31,5.7)),(14,(33,24),(31,40,6.1)),(17,(33,34),(25,43,5.1)),(20,(29,36),(22,44,4.8)),(23,(29,36),(42,41,4.8)),(29,(39,34.5),(48.5,43.5,4.7)),(30,(39,34.5),(48.5,43.5,4.7))]
KEYFRAMES=[1,145,217,337,409,481,553,697]

def interp(t,idx):
    for n in range(len(ROUTE)-1):
        if t<=ROUTE[n+1][0]:break
    a,b=ROUTE[n],ROUTE[n+1];u=max(0,min(1,(t-a[0])/(b[0]-a[0])))
    # Smooth position and gaze changes with zero velocity at intentional viewing pauses.
    u=u*u*(3-2*u)
    return Vector(a[idx]).lerp(Vector(b[idx]),u)

def configure(samples=24,width=1280,height=720):
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=samples;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.04
    s.cycles.max_bounces=8;s.cycles.transmission_bounces=8
    s.cycles.seed=0;s.cycles.use_animated_seed=False
    p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU';s.render.threads_mode='FIXED';s.render.threads=4
    s.render.resolution_x=width;s.render.resolution_y=height;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.fps=FPS;s.frame_start=1;s.frame_end=721
    s.view_settings.exposure=.15
    return s

def build():
    source=HOME/'model/timber-courtyard-02.blend';bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False)
    s=configure();WORK.mkdir(parents=True,exist_ok=True)
    # A rebuilt camera/scene invalidates only this tool's disposable render cache.
    # Resume an interrupted render with --animate, without --build.
    for folder in [WORK/'frames', WORK/'keyframes']:
        if folder.exists():
            for path in folder.glob('frame-*.png'):path.unlink()
    for name in ['09 Roof | hide for cutaway','08 Structure | cedar']:bpy.data.collections[name].hide_render=False
    openings=[]
    for prefix in ['Front glazed entry','Front courtyard threshold','Rear glazed gable']:
        panes=[o for o in s.objects if o.name.startswith(prefix+' glazing') and abs(o.location.x/.3048-33)<.1]
        assert len(panes)==1,(prefix,len(panes))
        o=panes[0];before=list(o.location);o.location.x+=4*.3048
        openings.append({'object':o.name,'state':'Presentation sliding leaf open to adjacent right bay','original_location_m':before,'open_location_m':list(o.location),'clear_opening_x_ft':[31.065,34.935]})
    for o in s.objects:
        if o.name.startswith('Entry door pull') and o.location.x/.3048>31:o.location.x+=4*.3048
    data=bpy.data.cameras.new('Walkthrough fixed 25mm lens');cam=bpy.data.objects.new('Timber continuous walkthrough',data);s.collection.objects.link(cam);s.camera=cam
    cam.data.lens=25;cam.data.clip_start=.05;cam.data.clip_end=300;cam.rotation_mode='QUATERNION';previous=None
    poses=[]
    for f in range(1,722):
        t=(f-1)/FPS;xy=interp(t,1);target=interp(t,2)*.3048;cam.location=Vector((xy.x,xy.y,5.5))*.3048
        q=(target-cam.location).to_track_quat('-Z','Y')
        if previous is not None and q.dot(previous)<0:q.negate()
        previous=q.copy();cam.rotation_quaternion=q
        cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f)
        poses.append({'frame':f,'position_m':list(cam.location),'target_m':list(target)})
    s.frame_set(1);s.render.filepath='//frames/frame-'
    bpy.ops.wm.save_as_mainfile(filepath=str(MODEL),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(MODEL),compress=True)
    record={'source':'model/timber-courtyard-02.blend','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fps':FPS,'frame_count':721,'duration_seconds':721/FPS,'lens_mm':25,'eye_height_m':5.5*.3048,'route':ROUTE,'poses':poses,'opening_overrides':openings,'scope':'Continuous presentation camera and three open sliding leaves; canonical source untouched. Coordinated kitchen and shared living furniture; other legacy interior rooms remain schematic. Not a door hardware or architectural approval.','native_visual_review':'pending'}
    record['presentation_source_sha256']=hashlib.sha256(MODEL.read_bytes()).hexdigest()
    record['authoring_script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    record['linked_asset_sha256']={str(Path(bpy.path.abspath(lib.filepath)).resolve().relative_to(ROOT)):hashlib.sha256(Path(bpy.path.abspath(lib.filepath)).read_bytes()).hexdigest() for lib in bpy.data.libraries}
    (WORK/'route.json').write_text(json.dumps(record,indent=2)+'\n')
    print('WALKTHROUGH_BUILT',flush=True)

def render(keys=False):
    record=json.loads((WORK/'route.json').read_text())
    assert hashlib.sha256((HOME/record['source']).read_bytes()).hexdigest()==record['source_sha256'], 'Source model changed; rebuild walkthrough.'
    assert hashlib.sha256(MODEL.read_bytes()).hexdigest()==record['presentation_source_sha256'], 'Presentation scene changed; rebuild walkthrough.'
    assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==record['authoring_script_sha256'], 'Authoring/render settings changed; rebuild walkthrough.'
    for path, expected in record['linked_asset_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected, f'Linked asset changed: {path}; rebuild walkthrough.'
    s=configure(48 if keys else 24)
    folder=WORK/('keyframes' if keys else 'frames');folder.mkdir(exist_ok=True,parents=True)
    for frame in (KEYFRAMES if keys else range(s.frame_start,s.frame_end+1)):
        out=folder/f'frame-{frame:04}.png'
        if not keys and out.exists():continue
        s.frame_set(frame);s.render.filepath=str(out);bpy.ops.render.render(write_still=True)
        print('WALKTHROUGH_FRAME',frame,flush=True)

def promote(review_note):
    """Save a relocatable presentation scene after the frame sequence is reviewed."""
    assert review_note and review_note.strip(), 'Provide the actual completed visual-review method with --review-note.'
    s=bpy.context.scene
    assert all((WORK/'frames'/f'frame-{f:04}.png').is_file() for f in range(1,722))
    source=HOME/'model/timber-courtyard-02.blend'
    record=json.loads((WORK/'route.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==record['source_sha256']
    s.frame_set(1);s.render.filepath='//../outputs/work/walkthrough/frames/frame-'
    bpy.ops.file.make_paths_absolute()
    bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/timber-walkthrough.blend'),compress=True)
    bpy.ops.file.make_paths_relative()
    bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/timber-walkthrough.blend'),compress=True)
    # The render-work scene and relocatable published resave have distinct bytes.
    # Preserve the historical generating hashes; never relabel them as current.
    record['render_source_scene']='outputs/work/walkthrough/timber-walkthrough.blend'
    record['render_source_scene_sha256']=record['presentation_source_sha256']
    record['generation_authoring_script_sha256']=record['authoring_script_sha256']
    record['published_presentation_scene']='model/timber-walkthrough.blend'
    record['published_presentation_scene_sha256']=hashlib.sha256((HOME/'model/timber-walkthrough.blend').read_bytes()).hexdigest()
    record['promotion_authoring_script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    record['provenance_note']='presentation_source_sha256 and authoring_script_sha256 retain their historical render-generation meanings. Published resave bytes differ after relative-path relocation. The native frame cache requires a rebuild if the current authoring script differs from the generating hash.'
    record['native_visual_review']=review_note
    (HOME/'outputs/videos/camera-route.json').write_text(json.dumps(record,indent=2)+'\n')
    print('WALKTHROUGH_PROMOTED',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--keyframes',action='store_true');p.add_argument('--animate',action='store_true');p.add_argument('--promote',action='store_true');p.add_argument('--review-note',help='Actual review evidence; required when promoting, never infer playback from rendering.')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if a.build:build()
    else:bpy.ops.wm.open_mainfile(filepath=str(MODEL if MODEL.exists() else HOME/'model/timber-walkthrough.blend'),use_scripts=False)
    if a.keyframes:render(True)
    if a.animate:render(False)
    if a.promote:promote(a.review_note)
