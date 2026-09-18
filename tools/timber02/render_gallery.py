"""Render named Timber views into ignored review output; never save render state.

Blender --background homes/timber-courtyard-02/model/timber-courtyard-02.blend \
  --python tools/timber02/render_gallery.py -- --draft 05-living-dining 06-kitchen 07-rear-garden
Omit --draft for 2400 x 1600 / 256-sample reviewed candidates. Promote after QA.
"""
import bpy,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from gallery import RENDERS
HOME=ROOT/'homes/timber-courtyard-02';s=bpy.context.scene
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
draft='--draft' in args;names=[x for x in args if not x.startswith('--')] or ['05-living-dining','06-kitchen','07-rear-garden']
assert all(n in RENDERS for n in names),names
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.render.engine='CYCLES';s.cycles.device='GPU';s.cycles.samples=64 if draft else 256;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.01;s.cycles.max_bounces=12;s.cycles.transmission_bounces=12
s.render.resolution_x=2400;s.render.resolution_y=1600;s.render.resolution_percentage=50 if draft else 100;s.render.image_settings.file_format='PNG'
work=HOME/'outputs/work';work.mkdir(parents=True,exist_ok=True)
base_exposure=s.view_settings.exposure
for slug in names:
    cam,role=RENDERS[slug];s.camera=bpy.data.objects[cam]
    s.view_settings.exposure=.3 if slug in ['05-living-dining','06-kitchen'] else (.5 if slug=='07-rear-garden' else base_exposure)
    cut=slug=='04-model-plan'
    bpy.data.collections['09 Roof | hide for cutaway'].hide_render=cut
    bpy.data.collections['08 Structure | cedar'].hide_render=cut
    if cut:
        s.camera.data.type='ORTHO';s.camera.data.ortho_scale=74*.3048;s.render.resolution_x=1600;s.render.resolution_y=1400
    else:
        s.render.resolution_x=2400;s.render.resolution_y=1600
    s.render.filepath=str(work/(slug+'.png'));bpy.ops.render.render(write_still=True)
    (work/(slug+'.json')).write_text(json.dumps({'camera':cam,'role':role,'native_source':'model/timber-courtyard-02.blend','image':slug+'.png','resolution_px':[round(s.render.resolution_x*s.render.resolution_percentage/100),round(s.render.resolution_y*s.render.resolution_percentage/100)],'samples':s.cycles.samples,'exposure':s.view_settings.exposure,'roof_hidden':cut,'stage':'draft' if draft else 'final candidate; promote only after pixel inspection'},indent=2)+'\n')
    print('TIMBER_GALLERY_RENDERED',slug,flush=True)
