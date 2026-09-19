"""Original fixed angled cedar privacy screen; metric, immutable library asset.

blender -b --factory-startup --python tools/library/publish_angled_cedar_screen.py
blender -b --factory-startup --python tools/library/publish_angled_cedar_screen.py -- --verify --render
"""
from pathlib import Path
import bpy, json, math, sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'tools/library'))
from common import geometry as g
from common.timber_materials import grain_uv
from publish_modern_block import box, bounds, linked_mat
SLUG='angled-cedar-privacy-screen-2000x2800'
ID='openings/'+SLUG
NAME='Angled cedar privacy screen 2000x2800 | shared v001'
FOLDER=ROOT/'library'/ID/'v001'
NATIVE=FOLDER/(SLUG+'.blend')
GEN='tools/library/publish_angled_cedar_screen.py'

def publish():
    if NATIVE.exists():
        print('PRESERVE existing immutable asset',flush=True);return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    c=g.collection(NAME);c['asset_id']=ID;c['asset_version']='v001'
    wood=linked_mat('warm-vertical-cedar','v003')
    metal=linked_mat('bronze-gray-standing-seam','v001')
    for x in [-.98,.98]:box('Fixed frame perimeter stile',(x,0,1.4),(.04,.30,2.8),metal,.002)
    for z in [.025,2.775]:box('Fixed frame top bottom rail',(0,0,z),(1.92,.30,.05),metal,.002)
    for i in range(23):
        x=-.925+i*1.85/22
        o=box('Angled solid cedar fin %02d'%i,(x,0,1.4),(.12,.025,2.70),wood,.0015)
        grain_uv(o);o.rotation_euler.z=math.radians(45)
        o['fixed_fin_angle_degrees']=45
    bpy.context.view_layer.update();lo,hi=bounds(c)
    FOLDER.mkdir(parents=True,exist_ok=True)
    bpy.data.libraries.write(str(NATIVE),{c},fake_user=True,path_remap='RELATIVE_ALL')
    meta={'schema_version':1,'id':ID,'version':'v001','name':NAME,'units':'meters','dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'blender':{'collection':NAME},'license':'CC-BY-4.0','rights':'Original Homes project contributor geometry; attribution Homes project contributors. No commercial product or third-party source geometry.','source':{'kind':'original','generator':GEN,'command':'blender -b --factory-startup --python '+GEN},'software':{'blender':bpy.app.version_string},'files':{'blender':NATIVE.name,'preview':'preview.png','validation':'validation.json'},'dependencies':[{'id':'materials/warm-vertical-cedar','version':'v003','path':'../../../materials/warm-vertical-cedar/v003/warm-vertical-cedar.blend'},{'id':'materials/bronze-gray-standing-seam','version':'v001','path':'../../../materials/bronze-gray-standing-seam/v001/bronze-gray-standing-seam.blend'}],'placement':{'origin':'XY center of frame depth and width at bottom Z=0; bounds X -1 to +1, Y -.15 to +.15, Z 0 to 2.8 meters','front_direction':'-Y; width X; Z up','allowed_scaling':'Rigid placement and Z rotation only. Do not scale fins, frame or fittings.'},'mounting':'Fixed perimeter frame supported by host at top and bottom rails. Solid vertical cedar fins captured by continuous rails. Host provides engineered brackets, fasteners, drainage and isolated metal/timber connections. No pivot or moving leaf.','modeled_state':'Fixed 23 solid cedar fins 120x25mm, 2700mm high, rotated +45 degrees around local Z, at 84.09mm pitch. Four slim bronze-gray perimeter frame members.','privacy_geometry':{'fin_width_m':.12,'fin_thickness_m':.025,'fin_angle_degrees':45,'fin_pitch_m':1.85/22,'normal_view_projected_fin_width_m':(.12+.025)/math.sqrt(2),'normal_view_projection_overlap_m':(.12+.025)/math.sqrt(2)-1.85/22,'basis':'Actual geometric normal-view overlap. Oblique viewpoints can see between fins; no universal privacy or solar-performance claim.'},'clearances':{'rear_frame_to_glass_min_m':.30,'cleaning_basis':'Concept reach/service gap only, not a walkable passage. Host must provide accessible glazing and demountable frame fixings or separate safe maintenance access.','host_checked':False},'operating_envelope':{'state':'Fixed','moving_parts':False,'host_open_state_checked':False,'basis':'Host must separately verify any operable window does not swing into screen or supports.'},'product_status':'Original reusable architectural privacy screen concept. No certified structural, wind, weathering, fire or maintenance system.'}
    (FOLDER/'asset.json').write_text(json.dumps(meta,indent=2)+'\n');print('PUBLISHED',meta['dimensions_m'],flush=True)

def preview(c):
    g.collection('Preview scene only');m=g.material('Neutral preview ground',(.3,.31,.29),.9)
    box('Neutral ground',(0,0,-.045),(300,300,.08),m)
    s=bpy.context.scene;target=Vector((0,0,1.4));campos=Vector((3,-6,3.1));s.camera=g.camera('Privacy screen native preview',campos/g.F,target/g.F,55)
    g.area('Large soft daylight',Vector((-3,-4,6))/g.F,target/g.F,1400,4/g.F,(1,.97,.92))
    g.area('Gentle fill',Vector((3,2,4))/g.F,target/g.F,650,3/g.F,(.91,.96,1))
    s.world=bpy.data.worlds.new('Neutral world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=760;s.render.resolution_y=760;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(FOLDER/'preview.png');s.view_settings.view_transform='AgX';s.view_settings.exposure=0;bpy.ops.render.render(write_still=True)

def verify(render):
    bpy.ops.wm.open_mainfile(filepath=str(NATIVE));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(NATIVE),link=True) as (a,b):b.collections=[NAME]
    c=b.collections[0];bpy.context.scene.collection.children.link(c);lo,hi=bounds(c)
    assert all(abs((hi[i]-lo[i])-v)<1e-5 for i,v in enumerate([2,.3,2.8]))
    assert abs(lo[2])<1e-6
    assert all(Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
    fins=[o for o in c.all_objects if o.name.startswith('Angled solid')];assert len(fins)==23
    assert all(abs(o.rotation_euler.z-math.pi/4)<1e-5 for o in fins)
    assert (.12+.025)/math.sqrt(2)>1.85/22
    if render:preview(c)
    report={'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'bounds_m':{'min':lo,'max':hi},'actual_dimensions_m':[hi[i]-lo[i] for i in range(3)],'objects':len(c.all_objects),'solid_angled_fins':len(fins),'normal_view_geometric_overlap_checked':True,'origin_at_base':True,'preview_rendered':(FOLDER/'preview.png').exists(),'preview_settings':{'renderer':'Cycles CPU','threads':4,'samples':24,'resolution_px':[760,760]},'host_integration_checked':False}
    (FOLDER/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('VERIFIED fixed angled privacy screen',flush=True)
if __name__=='__main__':
    if '--verify' in sys.argv:verify('--render' in sys.argv)
    else:publish()
