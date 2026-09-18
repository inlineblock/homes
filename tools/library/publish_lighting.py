"""Publish missing original lighting assets, or fresh-load/preview existing assets.

Blender --background --python-exit-code 1 --python tools/library/publish_lighting.py
Blender --background --python-exit-code 1 --python tools/library/publish_lighting.py -- --verify
Verification and previews intentionally use CPU Cycles, leaving home render GPU free.
"""
from pathlib import Path
import sys, json
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.lighting_assets import CATALOG, build, place

DETAILS={
 'downlight': ('Recessed 3 inch downlight', [3.6,3.6,3.756],
   'Mounting ceiling plane center Z=0; white trim below plane, housing above; emits -Z',
   'Provide a 3.4 inch ceiling cutout for the 3.336 inch housing (3 inch visible light aperture) and a reserved service space above for the 3.6 inch housing. Do not intersect an opaque slab. Illustrative geometry, not an IC/fire/wet-location rated fixture.'),
 'taskbar': ('Four foot undercabinet task bar', [48,1.104,.66],
   'Top mounting plane center Z=0; long axis X, body below, emits -Z',
   'Mount to cabinet underside near front, with a separate power/cable route. Do not scale length: use repeated bars or a new version for other lengths.'),
 'linear': ('Four foot slim linear pendant', [48,3.6,31.848],
   'Ceiling canopy top Z=0; long axis X; bottom lens 31.848 inches below; emits -Z',
   'Showpiece over an island or dining table. Check finished-floor head clearance at the chosen mounting elevation and keep general lighting separate.'),
}

def publish():
    for key,(slug,*_) in CATALOG.items():
        folder=ROOT/'library/fixtures'/slug/'v001'
        if (folder/f'{slug}.blend').exists():
            print('EXISTING_IMMUTABLE',slug);continue
        folder.mkdir(parents=True,exist_ok=True)
        coll=build(key)
        bpy.data.libraries.write(str(folder/f'{slug}.blend'),{coll},fake_user=True)
        name,dims,origin,host=DETAILS[key]
        metadata={'schema_version':1,'id':f'fixtures/{slug}','version':'v001','name':name,
          'units':'meters','dimensions_m':[round(v*.0254,7) for v in dims],
          'nominal_dimensions_inches':dims,'origin':origin,'front_direction':'Emission -Z; linear long axis +X',
          'allowed_variation':'Rigid Z rotation and placement only. Change light power per host instance. No nonuniform scaling.',
          'host_requirements':host,'dependencies':[],
          'source':{'kind':'original','generator':'tools/library/publish_lighting.py',
                    'geometry':'tools/common/lighting_assets.py','software':'Blender 4.5.14 LTS'},
          'license':'CC-BY-4.0','rights':'Original project asset; CC BY 4.0; attribution: Homes project contributors',
          'files':{'blender':f'{slug}.blend','preview':'preview.png'},
          'illumination':'Low emission diffuser mesh; optional host-owned light via common.lighting_assets.place. Artistic Blender watts, not verified photometry.'}
        (folder/'asset.json').write_text(json.dumps(metadata,indent=2)+'\n')
        (folder.parent/'AGENTS.md').write_text('# Shared lighting fixture\n\n- Read the pinned version manifest for mounting origin and host clearance. Never conceal recessed housings in a solid roof or ceiling.\n- Keep this fixture linked and use `common.lighting_assets.place` for per-instance light power. Do not duplicate local fixture geometry or stretch its dimensions.\n- Published adopted versions are immutable. Create the next version for a changed design.\n- Recessed general lighting and concealed task light are the modern default; reserve pendants for deliberate focal locations. Validate glare and exposure in the actual home render.\n')
        print('PUBLISHED',slug)

def verify():
    rows=[]
    for key,(slug,*_) in CATALOG.items():
        bpy.ops.wm.read_factory_settings(use_empty=True)
        folder=ROOT/'library/fixtures'/slug/'v001'
        with bpy.data.libraries.load(str(folder/f'{slug}.blend'),link=True) as (source,target):
            target.collections=list(source.collections)
        assert len(target.collections)==1
        coll=target.collections[0]
        bpy.context.scene.collection.children.link(coll)
        bpy.context.view_layer.update()
        assert all(o.type=='MESH' for o in coll.all_objects)
        pts=[o.matrix_world@Vector(corner) for o in coll.all_objects for corner in o.bound_box]
        lo=[min(p[i] for p in pts) for i in range(3)]
        hi=[max(p[i] for p in pts) for i in range(3)]
        actual=[hi[i]-lo[i] for i in range(3)]
        manifest=json.loads((folder/'asset.json').read_text())
        assert all(abs(a-b)<.0003 for a,b in zip(actual,manifest['dimensions_m'])),(key,actual,manifest['dimensions_m'])
        # Original objects contain no file textures or links outside the collection file.
        assert not any(image.source=='FILE' for image in bpy.data.images)
        g.collection('Preview studio')
        center=[(lo[i]+hi[i])/2/g.F for i in range(3)]
        span=max(actual)/g.F
        offset=(1.0,-1.9,-.9) if key=='taskbar' else (1.7,-2.25,-1.7)
        camera=g.camera('Asset underside camera',tuple(center[i]+span*offset[i] for i in range(3)),center,55)
        camera.data.clip_start=.001
        bpy.context.scene.camera=camera
        g.area('Studio key',(span*.9,-span,span*.4),center,20*span*span,max(span,.1),(1,.92,.82))
        g.area('Studio face',(span*.2,-span,-span),center,8*span*span,max(span,.1),(.82,.9,1))
        scene=bpy.context.scene
        scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=48
        scene.cycles.use_denoising=True
        scene.world=bpy.data.worlds.new('Neutral studio');scene.world.use_nodes=True
        scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.25,.28,1)
        scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
        scene.render.resolution_x=800;scene.render.resolution_y=800;scene.render.resolution_percentage=100
        scene.render.image_settings.file_format='PNG';scene.render.filepath=str(folder/'preview.png')
        if '--skip-render' not in sys.argv:
            bpy.ops.render.render(write_still=True)
        probe=place('Verification instance',coll,key,(12,7,10),rotation=.8,power=5)
        bpy.context.view_layer.update()
        assert len(probe.children)==1 and probe.children[0].type=='LIGHT'
        source=probe.children[0]
        assert source.data.energy==5
        expected=Vector((12*g.F,7*g.F,(10+CATALOG[key][3])*g.F))
        assert (source.matrix_world.translation-expected).length<.00001
        assert (source.matrix_world.to_quaternion()@Vector((0,0,-1))-Vector((0,0,-1))).length<.00001
        no_light=place('Geometry only verification instance',coll,key,(0,0,0),power=0)
        assert not no_light.children
        rows.append({'id':manifest['id'],'version':'v001','fresh_link':True,'mesh_objects':len(coll.all_objects),
                     'measured_dimensions_m':actual,'dimensions_match':True,'external_images':0,
                     'host_light_placement_dimming_verified':True,'preview':str((folder/'preview.png').relative_to(ROOT))})
    (ROOT/'tools/library/lighting-validation.json').write_text(json.dumps({'software':bpy.app.version_string,'assets':rows},indent=2)+'\n')
    print('LIGHTING_NATIVE_VERIFIED',len(rows))

if '--verify' in sys.argv:verify()
else:publish()
