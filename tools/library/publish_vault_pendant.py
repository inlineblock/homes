"""Publish/reopen the original 4 ft, 90 in drop, 3:12 vault pendant variant.

Blender --background --python tools/library/publish_vault_pendant.py
Blender --background --python tools/library/publish_vault_pendant.py -- --verify
The verifier uses CPU Cycles. It never rewrites the native published asset.
"""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
SLUG='lighting-linear-pendant-4ft-vault-3in12'
FOLDER=ROOT/'library/fixtures'/SLUG/'v001'
SLOPE=-.25
DROP=7.5

def bounds(coll):
    bpy.context.view_layer.update()
    graph=bpy.context.evaluated_depsgraph_get()
    pts=[o.evaluated_get(graph).matrix_world@Vector(v) for o in coll.all_objects for v in o.evaluated_get(graph).bound_box]
    lo=[min(v[i] for v in pts) for i in range(3)];hi=[max(v[i] for v in pts) for i in range(3)]
    return lo,hi

def build():
    coll=g.collection('Four foot linear pendant | 90 inch drop | 3 in 12 vault')
    coll['asset_id']='fixtures/'+SLUG;coll['asset_version']='v001'
    coll['mounting_slope_x']=SLOPE;coll['diffuser_bottom_ft']=-DROP
    metal=g.material('Vault pendant | satin graphite',(.024,.028,.030),.3,.72)
    lens=g.material('Vault pendant | warm opal diffuser',(.87,.84,.76),.35)
    p=lens.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.84,.62,1);p.inputs['Emission Strength'].default_value=.25
    def plate(name,x,width,depth,thickness):
        # Four top corners exactly on the inclined ceiling, followed by bottom.
        xy=[(x-width/2,-depth/2),(x+width/2,-depth/2),(x+width/2,depth/2),(x-width/2,depth/2)]
        verts=[(xx*g.F,yy*g.F,(SLOPE*xx-z)*g.F) for z in [0,thickness] for xx,yy in xy]
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]);mesh.update()
        obj=bpy.data.objects.new(name,mesh);coll.objects.link(obj);mesh.materials.append(metal);obj['ceiling_contact_top_vertices']=4
        return obj
    plate('Vault pendant | sloped canopy',0,1.25,.30,.07)
    for x in [-1.45,1.45]:
        plate('Vault pendant | sloped suspension anchor',x,.09,.10,.04)
        g.rod('Vault pendant | vertical suspension wire',(x,0,SLOPE*x-.04),(x,0,-7.345),.003,metal)
    g.rod('Vault pendant | vertical power lead',(0,0,-.07),(0,0,-7.345),.007,metal)
    g.box('Vault pendant | level aluminum extrusion',(0,0,-7.420),(4,.125,.15),metal,.018)
    g.box('Vault pendant | level opal diffuser',(0,0,-7.498),(3.94,.083,.004),lens,.001)
    return coll

def publish():
    native=FOLDER/(SLUG+'.blend')
    if native.exists():
        print('EXISTING_IMMUTABLE',native);return
    FOLDER.mkdir(parents=True,exist_ok=True)
    coll=build();lo,hi=bounds(coll)
    bpy.data.libraries.write(str(native),{coll},fake_user=True,path_remap='RELATIVE_ALL')
    meta={'schema_version':1,'id':'fixtures/'+SLUG,'version':'v001','name':'Four-foot linear pendant for a 3:12 vault, 90-inch drop','units':'meters',
      'dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},
      'origin':'Ceiling plane at center of canopy Z=0; X long axis; ceiling slopes downward toward +X at 3:12; level diffuser bottom Z=-2.286 m.',
      'front_direction':'Diffuser emits world/local -Z; level bar long axis X.',
      'placement':{'mounting_ceiling_slope_x':SLOPE,'mounting_ceiling_slope_y':0,'diffuser_drop_m':DROP*g.F,'allowed_variation':'Rigid translation and Z rotation only. Match roof gradient exactly. No tilt or scale; publish a sibling for different pitch or drop.'},
      'installation':{'mounting':'Canopy and two suspension-anchor upper faces touch the sloped ceiling; two vertical cables carry a horizontal bar. Host supplies structural backing and electrical route.',
        'operating_envelope':{'modeled_state':'Fixed suspended light; no motion','host_checked':False,'notes':'Check headroom, table alignment, beam separation, ceiling anchorage and service access in the actual host.'}},
      'derived_from':{'id':'fixtures/lighting-linear-pendant-4ft','version':'v001','basis':'Preserves original four-foot extrusion, opal lens and two-wire concept; replaces 31.848-inch suspension with a 90-inch drop and true 3:12 contact plates.'},
      'dependencies':[],'source':{'kind':'original','generator':'tools/library/publish_vault_pendant.py','parent_geometry':'tools/common/lighting_assets.py'},
      'software':{'blender':bpy.app.version_string},'files':{'blender':native.name,'preview':'preview.png','validation':'validation.json'},
      'license':'CC-BY-4.0','rights':'Original asset; attribution Homes project contributors',
      'illumination':'Low-emission diffuser. Host creates a dimmable downward rectangular light under the bar; artistic watts, not rated photometry.',
      'limitations':'Original concept fixture, not a specified commercial product or structural/electrical approval.'}
    (FOLDER/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
    (FOLDER/'README.md').write_text('# Vault linear pendant\n\n![Native preview](preview.png)\n\nA four-foot level light bar with a 90-inch drop beneath a 3:12 sloped ceiling. The canopy and two suspension plates meet the roof plane while the cables hang vertically. Derived from the original short-drop linear pendant, which remains unchanged.\n\nMount the origin at the center canopy/ceiling contact plane. The roof must fall toward local +X at 3:12. Use rigid placement only; never tilt or stretch the fixture. Review headroom, roof backing, beam clearance, wiring and service access in each host. Original concept, not a commercial product.\n\nNative authoring and CPU verification: `tools/library/publish_vault_pendant.py` and its `--verify` mode. Shared asset: CC BY 4.0; generator: MIT.\n')
    print('VAULT_PENDANT_PUBLISHED',str(native))

def verify():
    with bpy.data.libraries.load(str(FOLDER/(SLUG+'.blend')),link=True) as (a,b):b.collections=list(a.collections)
    assert len(b.collections)==1
    coll=b.collections[0];bpy.context.scene.collection.children.link(coll)
    lo,hi=bounds(coll);meta=json.loads((FOLDER/'asset.json').read_text())
    assert all(abs((hi[i]-lo[i])-meta['dimensions_m'][i])<1e-5 for i in range(3))
    mount_count=0
    for obj in coll.all_objects:
        if obj.get('ceiling_contact_top_vertices'):
            mount_count+=1
            for v in obj.data.vertices[:4]:assert abs(v.co.z-SLOPE*v.co.x)<1e-7
    assert mount_count==3
    lens=next(o for o in coll.all_objects if 'level opal diffuser' in o.name)
    assert abs(lens.location.z/g.F+7.498)<1e-5
    assert abs(lo[2]/g.F+DROP)<1e-5
    g.collection('Vault pendant preview studio')
    camera=g.camera('Native vault pendant preview',(8,-16,-10),(0,0,-3.6),55)
    s=bpy.context.scene;s.camera=camera
    g.area('Warm studio key',(2,-6,2),(0,0,-3.5),500,10,(1,.93,.83))
    g.area('Cool studio fill',(-5,-3,-3),(0,0,-4),250,8,(.83,.91,1))
    s.world=bpy.data.worlds.new('Neutral studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.48,.50,.51,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.5
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=48;s.cycles.use_denoising=True
    s.render.resolution_x=900;s.render.resolution_y=1100;s.render.resolution_percentage=100
    s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG';s.render.filepath=str(FOLDER/'preview.png')
    bpy.ops.render.render(write_still=True)
    result={'software':bpy.app.version_string,'fresh_link':True,'dimensions_match':True,'three_mounting_faces_match_3in12_plane':True,'diffuser_level':True,'drop_inches':90,'mesh_objects':len(coll.all_objects),'preview':'preview.png','host_installation_checked':False}
    (FOLDER/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print('VAULT_PENDANT_VERIFIED',json.dumps(result))

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
if '--verify' in sys.argv:verify()
else:publish()
