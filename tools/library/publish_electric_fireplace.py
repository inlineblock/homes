"""Original slim electric fireplace concept; publish once, then fresh-link/preview."""
import bpy, json, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
SLUG='slim-electric-fireplace-48in'
NAME='Slim electric fireplace 48in'
FOLDER=ROOT/'library/fixtures'/SLUG/'v001'
PATH=FOLDER/(SLUG+'.blend')

def measured(c):
    bpy.context.view_layer.update()
    pts=[o.matrix_world@Vector(v) for o in c.all_objects for v in o.bound_box]
    lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
    return lo,hi

def publish():
    if PATH.exists(): raise RuntimeError('Published version is immutable')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    c=g.collection(NAME);c['asset_id']='fixtures/'+SLUG;c['asset_version']='v001'
    black=g.material('Electric insert | matte graphite',(.018,.022,.025),.32,.55)
    dark=g.material('Electric insert | dark display',(.012,.016,.020),.18,.15)
    ember=g.material('Electric insert | amber simulated ember',(.22,.045,.008),.55)
    bs=ember.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(.7,.09,.004,1);bs.inputs['Emission Strength'].default_value=.45
    g.box('Electric insert rear case',(0,.365,.75),(4,.57,1.5),black,.01)
    g.box('Electric insert display',(0,.075,.75),(3.80,.02,1.25),dark,.004)
    for x in [-1.96,1.96]:g.box('Electric insert side bezel',(x,.04,.75),(.08,.08,1.5),black,.006)
    for z in [.045,1.455]:g.box('Electric insert top bottom bezel',(0,.04,z),(3.84,.08,.09),black,.006)
    # An illustrative ember display, not a flame or combustion device.
    for i in range(17):
        x=-1.65+i*.205
        g.box('Electric simulated ember segment',(x,.055,.22),(.16,.025,.035+.012*(i%3)),ember,.012)
    for x in [-1.7,-1.4,-1.1,-.8,-.5,-.2,.2,.5,.8,1.1,1.4,1.7]:
        g.box('Electric front ventilation slot',(x,.003,1.41),(.19,.007,.018),dark,.003)
    for o in c.all_objects:o['ifc_class']='IfcBuildingElementProxy'
    lo,hi=measured(c);FOLDER.mkdir(parents=True,exist_ok=True)
    bpy.data.libraries.write(str(PATH),{c},fake_user=True,path_remap='RELATIVE_ALL')
    meta={'schema_version':1,'id':'fixtures/'+SLUG,'version':'v001','name':NAME,'units':'meters',
      'dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'blender':{'collection':NAME},
      'placement':{'origin':'Width center, front bezel at Y=0, bottom Z=0','front_direction':'-Y','up':'Z','allowed_scaling':'Rigid placement only'},
      'installation':{'type':'Original electric display concept; no combustion or flue','nominal_size_in':[48,7.8,18],
        'required_host_checks':['Real recess with no opaque geometry through insert','Rear service reservation and electrical route','Front removal approach','Manufacturer thermal clearances and ventilation remain unselected'],
        'operating_envelope':{'state':'Fixed front with illustrative dim ember display','front_removal_reservation_m':.9144,'basis':'Concept planning assumption, not a listed product','host_installation_checked':False}},
      'source':{'kind':'original','generator':'tools/library/publish_electric_fireplace.py','command':'Blender --background --factory-startup --python tools/library/publish_electric_fireplace.py','software':bpy.app.version_string},
      'license':'CC-BY-4.0','rights':'Original Homes project contributors geometry; not a specified commercial product.',
      'dependencies':[],'files':{'blender':SLUG+'.blend','preview':'preview.png','validation':'validation.json'}}
    (FOLDER/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')

def verify():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(PATH),link=True) as (src,dst):dst.collections=[NAME]
    c=dst.collections[0];bpy.context.scene.collection.children.link(c)
    lo,hi=measured(c)
    for a,b in zip([hi[i]-lo[i] for i in range(3)],[4*g.F,.6505*g.F,1.5*g.F]):assert abs(a-b)<.0001
    assert abs(lo[1]+.0005*g.F)<.0001 and abs(lo[2])<.0001
    g.collection('Preview studio');s=bpy.context.scene
    s.camera=g.camera('Electric insert preview',(5,-8,3.2),(0,.25,.65),52)
    neutral=g.material('Studio neutral',(.36,.37,.35),.85);g.box('Ground',(0,0,-.04),(100,100,.08),neutral)
    g.area('Softbox',(-3,-4,6),(0,0,.6),250,4,(1,.94,.87));g.area('Fill',(4,-1,3),(0,0,.6),90,3,(.9,.95,1))
    s.world=bpy.data.worlds.new('Studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4
    s.render.resolution_x=960;s.render.resolution_y=600;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(FOLDER/'preview.png');s.view_settings.view_transform='AgX'
    bpy.ops.render.render(write_still=True)
    (FOLDER/'validation.json').write_text(json.dumps({'fresh_link':True,'measured_bounds_m':{'min':lo,'max':hi},'dimensions_match':True,'preview_rendered':True,'blender_version':bpy.app.version_string,'host_installation_checked':False},indent=2)+'\n')

if __name__=='__main__':
    verify() if '--verify' in sys.argv else publish()
