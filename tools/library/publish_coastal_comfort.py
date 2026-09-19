"""Publish immutable coastal seating/textiles; fresh-process verify and CPU previews.

Blender --background --python tools/library/publish_coastal_comfort.py
Blender --background --python tools/library/publish_coastal_comfort.py -- --verify --render
"""
from pathlib import Path
import bpy, json, math, sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.furnishings import soft
from common.timber_materials import grain_uv

FURNITURE={
 'coastal-outdoor-sofa':'Coastal outdoor sofa',
 'coastal-outdoor-lounge-chair':'Coastal outdoor lounge chair',
 'woven-oatmeal-rug':'Woven oatmeal rug',
 'olive-linen-cushion':'Olive linen cushion',
}
TEXTILES={'woven-oatmeal':((.40,.34,.25),(.64,.57,.44)), 'olive-linen':((.115,.145,.072),(.255,.29,.155))}
GENERATOR='tools/library/publish_coastal_comfort.py'

def folder(category,slug):return ROOT/'library'/category/slug/'v001'
def write_json(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def base_meta(category,slug,name):
    return {'schema_version':1,'id':category+'/'+slug,'version':'v001','name':name,'units':'meters',
      'license':'CC-BY-4.0','rights':'Original concept; attribution Homes project contributors; no commercial product or outdoor durability rating asserted.',
      'source':{'kind':'original','generator':GENERATOR,'software':bpy.app.version_string},'derived_from':None,
      'files':{'blender':slug+'.blend','preview':'preview.png','validation':'validation.json'}}

def weave(slug):
    c1,c2=TEXTILES[slug];m=g.material(slug.replace('-',' ').title()+' | physical weave | v001',c1,.89)
    n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Sheen Weight'].default_value=.22
    tc=n.new('ShaderNodeTexCoord');waves=[]
    for axis in ['X','Z']:
        w=n.new('ShaderNodeTexWave');w.wave_type='BANDS';w.bands_direction=axis;w.inputs['Scale'].default_value=230 if slug=='woven-oatmeal' else 620;w.inputs['Distortion'].default_value=.7;w.inputs['Detail Scale'].default_value=1.8;l.new(tc.outputs['Object'],w.inputs['Vector']);waves.append(w)
    mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY';l.new(waves[0].outputs['Fac'],mult.inputs[0]);l.new(waves[1].outputs['Fac'],mult.inputs[1])
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=110;noise.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],noise.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*c1,1);ramp.color_ramp.elements[1].color=(*c2,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
    bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00045;bump.inputs['Strength'].default_value=.24;l.new(mult.outputs[0],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    return m

def link_mat(slug):
    p=folder('materials',slug)/(slug+'.blend')
    with bpy.data.libraries.load(str(p),link=True) as (a,b):b.materials=[a.materials[0]]
    return b.materials[0]

def seam(name,x,y,z,w,d,mat):
    # Closed beveled polyline around the padded seat, avoiding loose tube ends.
    pts=[(x-w/2+.06,y-d/2,z),(x+w/2-.06,y-d/2,z),(x+w/2,y-d/2+.06,z),(x+w/2,y+d/2-.06,z),(x+w/2-.06,y+d/2,z),(x-w/2+.06,y+d/2,z),(x-w/2,y+d/2-.06,z),(x-w/2,y-d/2+.06,z)]
    o=g.curve(name,pts,.009,mat);o.data.splines[0].use_cyclic_u=True

def seating(slug,oak,linen,olive):
    w,d,n=(8,3.1,3) if slug=='coastal-outdoor-sofa' else (3,3.2,1)
    for x in [-w/2+.20,w/2-.20]:
        for y in [-d/2+.22,d/2-.22]:soft('Rounded timber foot',(x,y,.50),(.22,.22,1.0),oak,.06)
    for y in [-d/2+.10,d/2-.10]:soft('Continuous timber apron',(0,y,.91),(w,.20,.30),oak,.08)
    # Individual longitudinal slats read as real construction through the base.
    for i in range(9):g.box('Seat support slat',(0,-d/2+.24+i*(d-.48)/8,1.03),(w-.28,.18,.12),oak,.025)
    for x in [-w/2+.095,w/2-.095]:
        soft('Round edged timber arm',(x,0,2.0),(.19,d,.16),oak,.07)
        for y in [-d/2+.22,d/2-.22]:soft('Timber arm upright',(x,y,1.48),(.15,.15,1.02),oak,.035)
    soft('Upper back rail',(0,-d/2+.09,2.70),(w,.18,.20),oak,.07)
    for i in range(int(w/.33)):
        x=-w/2+.22+i*(w-.44)/(int(w/.33)-1);soft('Individual back slat',(x,-d/2+.10,1.93),(.17,.12,1.43),oak,.03)
    inner=w-.55;cw=inner/n-.045
    for i in range(n):
        x=-inner/2+(i+.5)*inner/n
        soft('Ivory boxed seat cushion',(x,.05,1.34),(cw,d-.52,.50),linen,.18)
        seam('Seat cushion tailored welt',x,.05,1.46,cw-.07,d-.60,linen)
        b=soft('Ivory plump back cushion',(x,-d/2+.48,2.04),(cw,.48,1.34),linen,.18);b.rotation_euler.x=math.radians(-8)
    # Small olive lumbar pillows are included, not a substitute for the separate cushion option.
    for x in ([-w/2+.90,w/2-.90] if n==3 else [0]):
        p=soft('Olive lumbar cushion',(x,-.53,1.79),(1.18,.38,.70),olive,.16);p.rotation_euler.x=-.13

def build(slug):
    c=g.collection(FURNITURE[slug]);c['asset_id']='furniture/'+slug;c['asset_version']='v001'
    oatmeal=link_mat('woven-oatmeal');olive=link_mat('olive-linen')
    deps=['woven-oatmeal','olive-linen']
    if slug.startswith('coastal-outdoor'):
        oak=link_mat('smoked-oak');deps+=['smoked-oak'];seating(slug,oak,oatmeal,olive)
        for o in c.all_objects:
            if o.type=='MESH' and oak in list(o.data.materials):grain_uv(o)
    elif slug=='woven-oatmeal-rug':
        deps=['woven-oatmeal']
        soft('Woven field',(0,0,.014),(20,12,.028),oatmeal,.025)
        edge=g.material('Original darker oatmeal bound edge',(.235,.205,.158),.97)
        for y in [-5.955,5.955]:soft('Long bound selvage',(0,y,.028),(20,.09,.014),edge,.012)
        for x in [-9.955,9.955]:soft('Short bound selvage',(x,0,.028),(.09,11.82,.014),edge,.012)
    else:
        deps=['olive-linen'];w=20/12
        soft('Olive linen removable cushion',(0,0,w/2),(w,5/12,w),olive,.20)
        # Welt follows perimeter on the upright +Y face.
        pts=[(-w/2+.10,.17,.10),(w/2-.10,.17,.10),(w/2-.045,.17,.20),(w/2-.045,.17,w-.20),(w/2-.10,.17,w-.10),(-w/2+.10,.17,w-.10),(-w/2+.045,.17,w-.20),(-w/2+.045,.17,.20)]
        p=g.curve('Cushion perimeter piping',pts,.009,olive);p.data.splines[0].use_cyclic_u=True
    bpy.context.view_layer.update();return c,deps

def bounds(c):
    pts=[o.matrix_world@Vector(v) for o in c.all_objects for v in o.bound_box];return [min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]

def publish():
    for slug in TEXTILES:
        f=folder('materials',slug);path=f/(slug+'.blend')
        if path.exists():continue
        bpy.ops.wm.read_factory_settings(use_empty=True);m=weave(slug);f.mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(path),{m},fake_user=True)
        meta=base_meta('materials',slug,m.name);meta.update(dependencies=[],texture_scale={'coordinates':'Local object coordinates in meters','weave_nominal_scale_m':.00435 if slug=='woven-oatmeal' else .00161,'bump_distance_m':.00045},limitations='Appearance only: select tested upholstery/rug material for actual outdoor exposure, cleaning and fire requirements.');write_json(f/'asset.json',meta)
    for slug in FURNITURE:
        f=folder('furniture',slug);path=f/(slug+'.blend')
        if path.exists():continue
        bpy.ops.wm.read_factory_settings(use_empty=True);c,deps=build(slug);lo,hi=bounds(c);f.mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap='RELATIVE_ALL')
        meta=base_meta('furniture',slug,FURNITURE[slug]);meta.update(dimensions_m=[hi[i]-lo[i] for i in range(3)],bounds_m={'min':lo,'max':hi},blender={'collection':c.name},dependencies=[{'id':'materials/'+s,'version':'v001','path':'../../../materials/'+s+'/v001/'+s+'.blend'} for s in deps],placement={'origin':'Centered XY at support plane Z=0','front_direction':'+Y; long dimension along X','up':'Z','allowed_scaling':'Rigid placement/rotation only; no nonuniform scale. Cushion may tilt in host; keep support contact.'},installation={'mounting':'Level supported floor' if slug!='olive-linen-cushion' else 'Upholstered seat or bed support, local bottom Z=0','operating_envelope':{'state':'Fixed furniture; no articulated mechanism','front_access_m':.90 if slug.startswith('coastal-outdoor') else None,'side_access_m':.60 if slug.startswith('coastal-outdoor') else None,'basis':'Original concept allowance, not a code or product claim','host_open_state_checked':False},'service_requirements':['Remove cushions for cleaning; confirm outdoor upholstery/timber suitability and anchoring for actual wind exposure.'] if slug.startswith('coastal-outdoor') else ['Keep floor rugs outside moving-door tracks and wet outdoor exposure; confirm edges remain trip-resistant.'] if slug=='woven-oatmeal-rug' else ['Do not reduce usable seating depth or obstruct circulation.']})
        write_json(f/'asset.json',meta)
        (f.parent/'AGENTS.md').write_text('# Coastal comfort asset\n\n- Link the exact collection version at its recorded meter scale. Preserve published versions.\n- Read the manifest for support plane, front direction and clearances. Furniture geometry does not prove access or weather performance.\n- Publish reusable dimensional variations separately and explicitly record adoption and host review.\n')
        print('PUBLISHED',slug,c.name,meta['dimensions_m'],flush=True)

def preview(c,f,lo,hi):
    g.collection('Isolated asset preview');center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))/g.F;target=[v/g.F for v in center]
    if f.parent.name=='coastal-outdoor-lounge-chair':span*=1.16
    cam=g.camera('Native asset studio',[target[0]+span*1.28,target[1]+span*1.89,target[2]+span*1.485],target,50);s=bpy.context.scene;s.camera=cam
    m=g.material('Neutral studio ground',(.39,.40,.38),.91);g.box('Ground',(0,0,lo[2]/g.F-.045),(span*100,span*100,.08),m)
    g.area('Broad daylight',(-span,span,span*2),target,span*span*13,span*1.7,(1,.96,.90));g.area('Cool fill',(span,-span,span),target,span*span*5,span*1.6,(.90,.95,1))
    s.world=bpy.data.worlds.new('Neutral studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.55,.57,.60,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=720;s.render.resolution_y=560;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(f/'preview.png');s.view_settings.view_transform='AgX';s.view_settings.exposure=0;bpy.ops.render.render(write_still=True)

def verify(render):
    for category,slugs in [('materials',TEXTILES),('furniture',FURNITURE)]:
        for slug in slugs:
            if '--asset' in sys.argv and slug!=sys.argv[sys.argv.index('--asset')+1]:continue
            f=folder(category,slug);path=f/(slug+'.blend');bpy.ops.wm.open_mainfile(filepath=str(path));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
            bpy.ops.wm.read_factory_settings(use_empty=True)
            if category=='furniture':
                with bpy.data.libraries.load(str(path),link=True) as (a,b):b.collections=[a.collections[0]]
                c=b.collections[0];bpy.context.scene.collection.children.link(c)
            else:
                m=link_mat(slug);c=g.collection('Native textile swatch');soft('Upholstery swatch',(0,0,.12),(3,2,.24),m,.12)
            bpy.context.view_layer.update();lo,hi=bounds(c)
            assert all(Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
            if category=='furniture':
                meta=json.loads((f/'asset.json').read_text());assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3));assert abs(lo[2])<1e-5
            if render:preview(c,f,lo,hi)
            write_json(f/'validation.json',{'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'bounds_m':{'min':lo,'max':hi},'objects':len(c.all_objects),'preview_rendered':(f/'preview.png').exists(),'preview_settings':{'renderer':'Cycles CPU','samples':24,'color_management':'AgX','exposure':0},'host_integration_checked':False})
            print('VERIFIED',category,slug,flush=True)

if __name__=='__main__':
    if '--verify' in sys.argv:verify('--render' in sys.argv)
    else:publish()
