"""Publish/reopen original 4 x 2 ft vertical limestone panel variation.

Blender --background --python tools/library/publish_limestone_wall_panel.py
Blender --background --python tools/library/publish_limestone_wall_panel.py -- --verify --render
Parent paver and material versions remain immutable. Native previews use CPU.
"""
from pathlib import Path
import bpy,json,sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
SLUG='honed-limestone-wall-panel-4x2'
NAME='Honed limestone wall panel 4x2'
FOLDER=ROOT/'library/surfaces'/SLUG/'v001'
PATH=FOLDER/(SLUG+'.blend')
PARENT=ROOT/'library/surfaces/honed-limestone-paver-4ft/v001/honed-limestone-paver-4ft.blend'
MATERIAL=ROOT/'library/materials/coastal-honed-limestone/v001/coastal-honed-limestone.blend'

def save_json(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def bounds(c):
    pts=[o.matrix_world@Vector(v) for o in c.all_objects for v in o.bound_box]
    return [min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]

def publish():
    if PATH.exists():print('IMMUTABLE_EXISTING',PATH);return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Derive actual source mesh vertices in world space, not an invented parent.
    with bpy.data.libraries.load(str(PARENT),link=False) as (source,target):target.collections=[source.collections[0]]
    source_collection=target.collections[0]
    sources=[o for o in source_collection.all_objects if o.type=='MESH']
    assert len(sources)==1,'Expected one original paver mesh'
    original=sources[0];old=[original.matrix_world@v.co for v in original.data.vertices]
    lo=[min(v[i] for v in old) for i in range(3)];hi=[max(v[i] for v in old) for i in range(3)]
    assert abs(hi[0]-lo[0]-4*g.F)<1e-5 and abs(hi[1]-lo[1]-4*g.F)<1e-5
    # Width retained, paver second plan axis becomes half-height; thickness becomes 1.5in.
    verts=[(v.x,(hi[2]-v.z)*1.25,(v.y-lo[1])*.5) for v in old]
    faces=[tuple(poly.vertices) for poly in original.data.polygons]
    with bpy.data.libraries.load(str(MATERIAL),link=True) as (source,target):target.materials=[source.materials[0]]
    mat=target.materials[0]
    c=g.collection(NAME);c['asset_id']='surfaces/'+SLUG;c['asset_version']='v001'
    mesh=bpy.data.meshes.new('Limestone panel derived from four-foot paver');mesh.from_pydata(verts,[],faces);mesh.materials.append(mat);mesh.update()
    obj=bpy.data.objects.new('Honed limestone vertical panel',mesh);c.objects.link(obj)
    bevel=obj.modifiers.new('Fine honed edge .008ft','BEVEL');bevel.width=.008*g.F;bevel.segments=3;obj.modifiers.new('Weighted edge normals','WEIGHTED_NORMAL')
    # Meter UVs are available to perimeter cuts; original shader uses object meters.
    uv=mesh.uv_layers.new(name='Surface meters')
    for poly in mesh.polygons:
        for li in poly.loop_indices:
            co=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(co.x,co.z)
    obj['ifc_class']='IfcCovering';obj['module_size_ft']='4 width x 2 height x .125 depth';obj['front_direction']='+Y'
    bpy.context.view_layer.update();lo,hi=bounds(c);FOLDER.mkdir(parents=True,exist_ok=True)
    bpy.data.libraries.write(str(PATH),{c},fake_user=True,path_remap='RELATIVE_ALL')
    meta={'schema_version':1,'id':'surfaces/'+SLUG,'version':'v001','name':NAME,'units':'meters',
      'dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},
      'blender':{'collection':NAME},'placement':{'origin':'Centered X, back mounting plane Y=0, bottom edge Z=0','front_direction':'+Y','up':'Z','allowed_scaling':'Rigid placement/rotation only. Full modules must use linked collection instances; never stretch panels.'},
      'module':{'width_m':4*g.F,'height_m':2*g.F,'depth_m':.125*g.F,'edge_bevel_m':.008*g.F,'suggested_joint_m':.02*g.F,'pitch_m':[4.02*g.F,2.02*g.F]},
      'installation':{'mounting':'Vertical cladding concept with local back plane Y=0. Host provides continuous designed support and appropriate anchors/cavity beyond the back datum; no anchor or cavity dimension is specified by this appearance asset.','clearances':{'basis':'Concept module geometry, not a manufacturer system','required_host_checks':['Joint widths and boundary cuts','Opening/trim clearances','Anchor and cavity room behind back datum','Drainage, flashing, movement, weight and substrate capacity'],'host_installation_checked':False},'operating_envelope':{'state':'Fixed cladding','moving_parts':False}},
      'variation':{'perimeter_cuts':'Host may create specifically labeled perimeter-cut meshes derived from this panel. Trim mesh vertices to actual boundary dimensions; retain .0381m thickness, .0024384m bevel, linked limestone material and physical-meter coordinates/Surface meters UVs without stretching. Record bespoke cuts in host schedule. Full-size panels remain linked instances.','surface_coordinates':'Local object coordinates in meters; material has no image dependencies. Surface meters UV encodes local X/Z physical meters for future map-compatible variants.'},
      'dependencies':[{'id':'materials/coastal-honed-limestone','version':'v001','path':'../../../materials/coastal-honed-limestone/v001/coastal-honed-limestone.blend'}],
      'derived_from':{'id':'surfaces/honed-limestone-paver-4ft','version':'v001','path':'../../honed-limestone-paver-4ft/v001/','basis':'Actual source paver mesh; retained four-foot width, halved second dimension into upright two-foot height, increased thickness from1.2in to1.5in, revised origin/front and fine edge bevel. The source paver is not changed.'},
      'source':{'kind':'original-variation','generator':'tools/library/publish_limestone_wall_panel.py','command':'Blender --background --python tools/library/publish_limestone_wall_panel.py','software':bpy.app.version_string},
      'license':'CC-BY-4.0','rights':'Original Homes project contributors geometry and material; attribution Homes project contributors. Not a commercial product or approved wall system.',
      'files':{'blender':PATH.name,'preview':'preview.png','validation':'validation.json'}}
    save_json(FOLDER/'asset.json',meta)
    (FOLDER.parent/'AGENTS.md').write_text('# Shared limestone wall panel\n\n- Preserve adopted versions and link full panels at scale1. Read the manifest for back-plane origin, front and physical dimensions.\n- Host-specific perimeter cuts may trim the source panel mesh while keeping meter-scale texture and thickness. Record those cuts explicitly; do not stretch full modules.\n- Provide engineered backing, anchor/cavity space, movement joints and weather details separately. This shared appearance asset does not establish a cladding product specification.\n')
    print('PUBLISHED',NAME,meta['dimensions_m'],flush=True)

def verify(render):
    bpy.ops.wm.open_mainfile(filepath=str(PATH));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(PATH),link=True) as (source,target):target.collections=[NAME]
    c=target.collections[0];bpy.context.scene.collection.children.link(c);bpy.context.view_layer.update();lo,hi=bounds(c)
    assert all(Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
    meta=json.loads((FOLDER/'asset.json').read_text());assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3));assert abs(lo[1])<1e-5 and abs(lo[2])<1e-5
    if render:
        g.collection('Isolated vertical wall-panel studio');s=bpy.context.scene
        s.camera=g.camera('Wall panel native preview',(4.3,8.2,4.0),(0,.06,.95),52)
        floor=g.material('Neutral studio',(.38,.39,.37),.88);g.box('Preview ground',(0,0,-.045),(100,100,.08),floor)
        g.area('Broad neutral grazing light',(-3,4,5),(0,0,1),260,4,(1,.96,.91));g.area('Soft fill',(4,3,2),(0,0,1),75,3,(.93,.96,1))
        s.world=bpy.data.worlds.new('Neutral studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
        s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=720;s.render.resolution_y=560;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(FOLDER/'preview.png');s.view_settings.view_transform='AgX';bpy.ops.render.render(write_still=True)
    save_json(FOLDER/'validation.json',{'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'bounds_m':{'min':lo,'max':hi},'dimensions_m':[hi[i]-lo[i] for i in range(3)],'back_plane_y_zero':True,'bottom_z_zero':True,'preview_rendered':(FOLDER/'preview.png').exists(),'preview_settings':{'renderer':'Cycles CPU','samples':32,'color_management':'AgX','exposure':0},'host_installation_checked':False})
    print('VERIFIED',NAME,flush=True)
if __name__=='__main__':
    if '--verify' in sys.argv:verify('--render' in sys.argv)
    else:publish()
