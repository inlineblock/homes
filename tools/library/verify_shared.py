"""Reopen each shared asset, inspect dependencies and optionally render previews."""
import sys
import json
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from common import geometry as g
from common.shared_assets import CATALOG, _bounds

rows = []
render_keys = None
if '--keys' in sys.argv:
    render_keys = set(sys.argv[sys.argv.index('--keys')+1].split(','))
for key, (category, slug, version) in CATALOG.items():
    folder = ROOT/'library'/category/slug/version
    path = folder/(slug+'.blend')
    bpy.ops.wm.open_mainfile(filepath=str(path))
    matches=[c for c in bpy.data.collections if c.get('asset_id') == category+'/'+slug]
    coll = matches[0] if matches else next(c for c in bpy.data.collections if c.all_objects and not c.library)
    if coll.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(coll)
    bpy.context.view_layer.update()
    assert len(coll.all_objects) > 0
    for library in bpy.data.libraries:
        assert library.filepath.startswith('//'), library.filepath
        resolved = Path(bpy.path.abspath(library.filepath, library=library.parent)).resolve()
        assert resolved.is_relative_to(ROOT/'library') and resolved.exists(), resolved
    lo, hi = _bounds(coll)
    meta = json.loads((folder/'asset.json').read_text())
    assert all(abs((hi[i]-lo[i])-meta['dimensions_m'][i]) < 1e-5 for i in range(3))
    if key == 'paver':
        assert abs(hi[2]) < 1e-5 and abs((hi[0]-lo[0])-4*g.F) < 1e-5
    if key == 'wardrobe':
        assert any('hanging rail' in o.name for o in coll.objects)
        assert sum('hinged oak door' in o.name for o in coll.objects) == 2
        assert abs((hi[0]-lo[0])/g.F-2) < 1e-4
    if key == 'bathtub':
        shell=next(o for o in coll.objects if 'hollow oval bathtub shell' in o.name)
        hit,point,normal,index=shell.ray_cast(Vector((0,0,3*g.F)),Vector((0,0,-1)))
        assert hit and point.z < .4*g.F, 'Bathtub basin must be hollow, not a solid block'
        hit,point,normal,index=shell.ray_cast(Vector((2.93*g.F,0,3*g.F)),Vector((0,0,-1)))
        assert hit and point.z > 1.8*g.F, 'Bathtub requires a raised enclosing rim'
    if key == 'toilet':
        bowl=next(o for o in coll.objects if 'continuous pedestal and hollow bowl' in o.name)
        seat=next(o for o in coll.objects if 'open oval seat' in o.name)
        ray_origin=Vector((0,-.29*g.F,2*g.F))
        hit,point,normal,index=bowl.ray_cast(ray_origin,Vector((0,0,-1)))
        assert hit and point.z < .9*g.F, 'Toilet bowl must be concave'
        assert not seat.ray_cast(ray_origin,Vector((0,0,-1)))[0], 'Seat center must be open'
        assert abs(lo[2]) < 1e-5 and hi[0]-lo[0] <= 16*.0254+1e-5
        assert lo[1] >= -15*.0254-1e-5 and hi[1] <= 15*.0254+1e-5
        from mathutils import Matrix
        import math
        lid=next(o for o in coll.objects if o.name=='Toilet raised lid')
        hinge=Vector((0,lid['hinge_y_ft']*g.F,lid['hinge_z_ft']*g.F))
        for degrees in range(0,91,5):
            transform=Matrix.Translation(hinge)@Matrix.Rotation(math.radians(-degrees),4,'X')@Matrix.Translation(-hinge)
            pts=[transform@Vector(v) for v in lid.bound_box]
            assert min(p.y for p in pts)>=-15*.0254-1e-5 and max(p.y for p in pts)<=15*.0254+1e-5
    rows.append({'id': category+'/'+slug, 'version': version,
                 'objects': len(coll.all_objects), 'relative_dependencies': len(bpy.data.libraries),
                 'native_reopened': True, 'dimensions_verified': True})
    if key=='toilet':
        rows[-1]['geometry_checks']={'floor_contact':True,'hollow_bowl':True,'open_seat':True,
                                    'lid_sweep_degrees':[0,90],'lid_sweep_step_degrees':5,
                                    'swept_plan_within_inches':[16,30],'host_integration_checked':False}
    # Lighting has an underside preview rig in its own publisher. Preserve it.
    if key in {'downlight','taskbar','linear_pendant'}:
        continue
    if '--render' not in sys.argv or (render_keys is not None and key not in render_keys):
        continue
    # These are real Blender renders of the linked source, not substitute images.
    g.collection('Preview rig | excluded from source')
    center = Vector([(lo[i]+hi[i])/2/g.F for i in range(3)])
    extent = max((hi[i]-lo[i])/g.F for i in range(3))
    ground = g.material('Preview warm gray', (.34, .345, .33), .9)
    ground_z = lo[2]/g.F-.03
    g.box('Preview ground', (0, 0, ground_z-.08), (extent*200, extent*200, .16), ground)
    elevation=3.5 if key=='bathtub' else .85
    cam = g.camera('Preview camera', (center.x+extent*1.35, center.y-extent*2.4, center.z+extent*elevation), center, 52)
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = extent*g.F*(1.8 if key == 'paver' else 1.35)
    g.area('Preview key', (-extent*1.4,-extent*1.4,extent*2.2), center, 15*extent**2, extent*2, (.96,.98,1))
    g.area('Preview fill', (extent,extent*.4,extent*1.4), center, 6*extent**2, extent*2, (1,.92,.82))
    scene = bpy.context.scene
    scene.camera = cam
    scene.world = bpy.data.worlds.new('Preview ambient')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value = (.55,.65,.8,1)
    scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value = .35
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x = scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = 'AgX'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(folder/'preview.png')
    bpy.ops.render.render(write_still=True)
    meta['files']['preview'] = 'preview.png'
    (folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
    print('SHARED_ASSET_PREVIEW', key, flush=True)

receipt = {'blender': bpy.app.version_string, 'assets': rows,
           'all_native_reopens_and_dimensions_passed': True}
(ROOT/'tools/library/shared-validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('SHARED_ASSETS_VERIFIED', len(rows), flush=True)
