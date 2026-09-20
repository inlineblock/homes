"""Original gas and induction counter-mounted cooktops, dimensional concept assets.

Blender --background --python tools/library/build_cooktop_options.py
Blender --background --python tools/library/build_cooktop_options.py -- --verify --render
Uses meter-valued wrappers around the repository's shared geometry helpers.
"""
from pathlib import Path
import bpy, json, math, sys, hashlib
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common import geometry as g
GENERATOR = 'tools/library/build_cooktop_options.py'
ASSETS = {'gas-cooktop-36in': (.9144, .5334, .876, .494), 'induction-cooktop-30in': (.762, .5334, .724, .494)}

def folder(slug): return ROOT / 'library/appliances' / slug / 'v001'
def js(path, data): path.write_text(json.dumps(data, indent=2) + '\n')
def ft(v): return [n/g.F for n in v]
def box(n, p, s, m, b=.001): return g.box(n, ft(p), ft(s), m, b/g.F)
def cyl(n, p, r, h, m): return g.cyl(n, ft(p), r/g.F, h/g.F, m, 48)
def rod(n, a, b, r, m): return g.rod(n, ft(a), ft(b), r/g.F, m)
def ring(n, x, y, z, r, thick, mat):
    bpy.ops.mesh.primitive_torus_add(major_segments=72, minor_segments=8, major_radius=r, minor_radius=thick, location=(x,y,z))
    o=g.move(bpy.context.object);o.name=n;o.data.materials.append(mat)
    for face in o.data.polygons: face.use_smooth=True
    return o

def bounds(c):
    bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get(); pts=[]
    for o in c.all_objects:
        if o.type!='MESH': continue
        ev=o.evaluated_get(dg);me=ev.to_mesh();pts.extend(ev.matrix_world@v.co for v in me.vertices);ev.to_mesh_clear()
    return [min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)]

def mats():
    return {k:g.material(n,col,rough,metal) for k,n,col,rough,metal in [
        ('steel','Cooktop satin stainless original',(.38,.40,.415),.30,.86),
        ('dark','Cooktop powder-coated casing original',(.025,.029,.030),.48,.20),
        ('iron','Cooktop cast-iron grates original',(.022,.025,.024),.70,.32),
        ('cap','Cooktop black burner enamel original',(.025,.029,.03),.30,.45),
        ('brass','Cooktop burner distributor original',(.24,.18,.085),.40,.74),
        ('mark','Cooktop understated etched marks original',(.40,.43,.44),.40,.3),
        ('rubber','Cooktop support gasket original',(.011,.012,.012),.85,0),
    ]}

def gas(slug):
    c=g.collection(slug+' | v001');m=mats()
    box('Gas stainless support flange at counter plane',(0,0,.0025),(.9144,.5334,.005),m['steel'],.003)
    box('Gas inset enamel burner deck',(0,.048,.0065),(.884,.400,.007),m['cap'],.008)
    box('Gas under-counter service enclosure',(0,0,-.039),(.870,.486,.078),m['dark'],.007)
    # Gasket remains below the supporting flange, with a real central opening.
    for x in [-.446,.446]: box('Gas side support gasket',(x,0,-.0015),(.012,.519,.003),m['rubber'])
    for y in [-.256,.256]: box('Gas front/rear support gasket',(0,y,-.0015),(.88,.010,.003),m['rubber'])
    burners=[(-.303,-.050,.045),(-.303,.153,.038),(.303,-.050,.038),(.303,.153,.045),(0,.065,.059)]
    for i,(x,y,r) in enumerate(burners,1):
        cyl(f'Burner {i} stainless removable drip cup',(x,y,.011),r+.015,.006,m['steel'])
        cyl(f'Burner {i} gas distributor',(x,y,.020),r,.013,m['brass'])
        # Individual radial ports show the burner as a manufactured part.
        for j in range(28):
            a=2*math.pi*j/28
            o=box(f'Burner {i} port {j+1}',(x+math.cos(a)*(r-.001),y+math.sin(a)*(r-.001),.024),(.008,.0028,.005),m['dark'],.0004);o.rotation_euler.z=a
        cyl(f'Burner {i} enamel cap',(x,y,.031),r+.004,.010,m['cap'])
        cyl(f'Burner {i} ceramic ignition electrode',(x+r+.009,y,.024),.003,.020,m['mark'])
    # Three removable grate assemblies, each has four contact feet and a perimeter.
    for idx,x in enumerate([-.303,0,.303],1):
        w=.282;front=-.141;back=.251
        for yy in [front,back]: box(f'Grate {idx} transverse frame',(x,yy,.055),(w,.014,.014),m['iron'],.004)
        for xx in [x-w/2,x+w/2]:
            box(f'Grate {idx} longitudinal frame',(xx,.055,.055),(.014,back-front,.014),m['iron'],.004)
            for yy in [front+.012,back-.012]:
                box(f'Grate {idx} contact foot',(xx,yy,.031),(.019,.022,.044),m['iron'],.003)
        relevant=[b for b in burners if abs(b[0]-x)<.01]
        if len(relevant)==2:box(f'Grate {idx} structural middle crossbar',(x,.052,.055),(w,.014,.014),m['iron'],.004)
        for bx,by,r in relevant:
            for dx in [-1,1]:
                box(f'Grate {idx} pot support horizontal',(bx+dx*.091,by,.056),(.096,.016,.014),m['iron'],.004)
            for dy in [-1,1]:
                inner=by+dy*.040
                outer=(front if dy<0 else back) if len(relevant)==1 else (front if by<0 and dy<0 else back if by>0 and dy>0 else .052)
                box(f'Grate {idx} connected vertical finger',(bx,(inner+outer)/2,.056),(.016,abs(inner-outer),.014),m['iron'],.004)
    for i,x in enumerate([-.26,-.13,0,.13,.26],1):
        ring('Knob escutcheon',x,-.211,.010,.023,.002,m['steel'])
        cyl(f'Gas control {i} turned metal knob',(x,-.211,.022),.019,.025,m['steel'])
        box(f'Gas control {i} index',(x,-.217,.035),(.0025,.013,.001),m['dark'],.0005)
        for j in [-1,0,1]:
            a=math.pi/2+j*.65
            cyl('Etched burner control index',(x+math.cos(a)*.030,-.211+math.sin(a)*.030,.006),.0015,.0008,m['mark'])
    cyl('Gas supply stub at rear underside',(.29,.18,-.100),.011,.050,m['brass'])
    box('Gas ignition connection cover',(-.30,.15,-.080),(.050,.048,.012),m['dark'],.004)
    return c

def induction(slug):
    parent=folder('induction-cooktop-36in')/'induction-cooktop-36in.blend'
    with bpy.data.libraries.load(str(parent),link=False) as (src,dst): dst.collections=[src.collections[0]]
    c=dst.collections[0];c.name=slug+' | v001';bpy.context.scene.collection.children.link(c);g.ACTIVE=c
    # Actual parent surface/casing and palette retained, re-engineered to a distinct size.
    surface=None;casing=None
    for o in list(c.all_objects):
        if o.name.startswith('Induction ceramic glass surface'):surface=o
        elif o.name.startswith('Cooktop below-counter casing'):casing=o
        else:bpy.data.objects.remove(o,do_unlink=True)
    assert surface and casing
    surface.name='30in ceramic-glass support flange';surface.dimensions=(.762,.5334,.006);surface.location=(0,0,.003)
    casing.name='30in ventilated under-counter enclosure';casing.dimensions=(.716,.486,.060);casing.location=(0,0,-.030)
    for o in [surface,casing]:
        bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        for mod in o.modifiers:
            if mod.type=='BEVEL':mod.width=.002;mod.segments=4
    m=mats();ceramic=surface.data.materials[0]
    ceramic.name='30in neutral black ceramic | derived original palette'
    cp=ceramic.node_tree.nodes.get('Principled BSDF');cp.inputs['Base Color'].default_value=(.003,.0035,.004,1);cp.inputs['Metallic'].default_value=0;cp.inputs['Roughness'].default_value=.13;cp.inputs['Coat Weight'].default_value=.30
    for x in [-.369,.369]:box('Induction lateral under-glass support gasket',(x,0,-.001),(.012,.51,.002),m['rubber'])
    for y in [-.255,.255]:box('Induction front/rear gasket',(0,y,-.001),(.732,.012,.002),m['rubber'])
    zones=[(-.193,-.085,.092),(-.193,.142,.077),(.193,-.085,.080),(.193,.142,.098)]
    for i,(x,y,r) in enumerate(zones,1):
        ring(f'Zone {i} fine ceramic engraving',x,y,.0065,r,.00065,m['mark'])
        for axis in range(2):
            size=(.013,.0012,.0005) if axis==0 else (.0012,.013,.0005)
            box(f'Zone {i} center registration',(x,y,.0065),size,m['mark'],.0002)
        # Four distinct control groups, not one generic featureless stripe.
        cx=-.246+(i-1)*.164
        box(f'Zone {i} status display',(cx,-.203,.0063),(.036,.019,.0005),m['dark'],.002)
        for j in range(7):
            box(f'Zone {i} slider tick {j+1}',(cx-.031+j*.0103,-.229,.0065),(.0016,.006 if j%3 else .010,.0005),m['mark'],.0002)
        ring(f'Zone {i} off-state display',cx,-.203,.0068,.004,.00045,m['mark'])
    ring('Power touch symbol',.330,-.214,.0065,.008,.00065,m['mark'])
    box('Power symbol index',(.330,-.207,.0068),(.001,.009,.0005),m['mark'],.0001)
    # Visible cooling intake and separate electric connection cover below the deck.
    for j in range(18):box('Underbody ventilation fin',(-.30+j*.035,.244,-.033),(.018,.003,.028),m['steel'],.001)
    box('Electrical junction access cover',(.26,.17,-.064),(.082,.08,.008),m['dark'],.003)
    return c

def publish():
    for slug,(w,d,cw,cd) in ASSETS.items():
        target=folder(slug);path=target/(slug+'.blend')
        if path.exists():print('PRESERVED',slug);continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        c=gas(slug) if slug.startswith('gas') else induction(slug)
        c['asset_id']='appliances/'+slug;c['asset_version']='v001';c['mount_plane_z_m']=0.0;c['front_direction']='-Y'
        lo,hi=bounds(c);target.mkdir(parents=True,exist_ok=True)
        bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap='RELATIVE_ALL')
        gas_type=slug.startswith('gas')
        parent=folder('induction-cooktop-36in')/'induction-cooktop-36in.blend'
        meta={'schema_version':1,'id':'appliances/'+slug,'version':'v001','name':'Original '+slug.replace('-',' '),'units':'meters',
            'dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'blender':{'collection':c.name},
            'placement':{'origin':'XY center of overall flange at countertop support plane Z=0','front_direction':'-Y','up':'+Z','allowed_scaling':'Rigid placement and rotation only. Do not scale an appliance to fit a cabinet.'},
            'installation':{'overall_flange_m':[w,d],'countertop_cutout_concept_m':[cw,cd],'cutout_center_m':[0,0],'cutout_corner_radius_concept_m':.006,'cutout_basis':'Original concept allowance; select actual appliance and verify its installation template before fabrication. Not a manufacturer dimension.',
            'mounting':'Drop into separate host countertop cutout; continuous flange support/gasket at Z=0. No opaque countertop or cabinet geometry through the casing.',
            'underbody_clear_depth_from_counter_m':.15 if gas_type else .10,'underside_service_access_m':.20,'rear_and_side_heat_clearance':'Unspecified until selected product, backsplash material and hood are coordinated; no zero-clearance claim.',
            'services':['Accessible gas shutoff, regulator, flexible gas connection and grounded electrical ignition supply; gas type/load/pressure unselected.' if gas_type else 'Dedicated correctly rated electrical circuit, accessible junction and unobstructed cooling airflow; voltage/current unselected.','Separate overhead extraction with actual duct route and product-specific mounting height; no downdraft fan implied.','No oven is included. Coordinate separate wall oven or an explicitly compatible under-counter oven without blocking cooling/services.'],
            'operating_envelope':{'modeled_state':'Off, fixed installation; removable grates/caps' if gas_type else 'Off, fixed installation','clear_working_space_front_m':1.067,'basis':'Concept planning allowance only; selected product and household determine final arrangement.','host_open_state_checked':False},'host_integration_checked':False},
            'dependencies':[],'source':{'kind':'original' if gas_type else 'original derivative','generator':GENERATOR,'command':'Blender --background --python '+GENERATOR},
            'license':'CC-BY-4.0','rights':'Original Homes project contributors geometry and materials. Attribution required. Generic concept, not a commercial product or certified installation.',
            'files':{'blender':slug+'.blend','preview':'preview.png','service_preview':'service-preview.png','validation':'validation.json'},'software':{'blender':bpy.app.version_string}}
        if not gas_type:meta['derived_from']={'id':'appliances/induction-cooktop-36in','version':'v001','path':'../../induction-cooktop-36in/v001/induction-cooktop-36in.blend','source_sha256':hashlib.sha256(parent.read_bytes()).hexdigest(),'method':'Append actual published collection, preserve ceramic surface and enclosure meshes/materials, rebuild to 30in nominal flange dimensions and 4-zone arrangement. All published source files unchanged.','changes':'Distinct 30in option; neutral black ceramic finish, four circular heating zones, independent sliders, power icon, gasket, ventilation fins and electric service cover. New cutout and mounting plane recorded explicitly.'}
        js(target/'asset.json',meta)
        (target/'README.md').write_text('# '+meta['name']+'\n\n![Native asset preview](preview.png)\n\n![Underbody and service access](service-preview.png)\n\nOriginal generic concept equipment; CC BY 4.0, Homes project contributors. Link the named collection in `'+slug+'.blend`, centered on the countertop mounting plane with controls toward −Y. Preserve its real dimensions.\n\nRead `asset.json` before installation: the flange is larger than its concept cutout, the underbody needs a real opening and access, and separate extraction and an oven must be provided. These allowances are not manufacturer specifications.\n\nRebuild and fresh-process verify using `'+GENERATOR+'`; published versions are immutable. Native preview includes a temporary neutral support counter, not part of the asset. Host integration is pending.\n')
        print('PUBLISHED',slug,meta['dimensions_m'],flush=True)

def preview(c,target,lo,hi):
    g.collection('Temporary neutral studio; excluded from library')
    m=g.material('Studio honed pale gray',(.31,.32,.31),.82)
    # Honest real opening: four separate worktop strips, leaving underbody unobstructed.
    w,d,cw,cd=ASSETS[target.parent.name]
    for x in [-1,1]:box('Preview counter side',(x*(cw/2+.115),0,-.015),(.23,.80,.030),m,.003)
    for y in [-1,1]:box('Preview counter front/back',(0,y*(cd/2+.06),-.015),(cw,.12,.030),m,.003)
    s=bpy.context.scene;s.camera=g.camera('Native cooktop view',ft((1.15,-1.60,1.35)),ft((0,0,0)),55)
    g.area('Large warm studio key',ft((-.7,-.7,1.8)),(0,0,0),180,1.4/g.F,(1,.96,.90))
    g.area('Broad cool studio fill',ft((1,.6,1.2)),(0,0,0),95,1.0/g.F,(.91,.95,1))
    s.world=bpy.data.worlds.new('Soft studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=40;s.cycles.use_denoising=True
    s.render.threads_mode='FIXED';s.render.threads=3;s.render.resolution_x=900;s.render.resolution_y=650;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(target/'preview.png');s.view_settings.view_transform='AgX'
    bpy.ops.render.render(write_still=True)
    for o in list(g.ACTIVE.objects):
        if o.name.startswith('Preview counter'):o.hide_render=True
    s.camera=g.camera('Native underside service view',ft((1.1,-1.4,-.85)),ft((0,0,-.025)),55)
    g.area('Underbody inspection light',ft((-.7,-.9,-1.2)),ft((0,0,-.03)),100,1.2/g.F,(1,.96,.90))
    g.area('Underbody side fill',ft((.8,.6,-.8)),ft((0,0,-.03)),65,.8/g.F,(.91,.95,1))
    s.render.filepath=str(target/'service-preview.png');bpy.ops.render.render(write_still=True)

def verify(render):
    for slug in ASSETS:
        target=folder(slug);path=target/(slug+'.blend');meta=json.loads((target/'asset.json').read_text())
        bpy.ops.wm.open_mainfile(filepath=str(path));assert not bpy.data.libraries
        bpy.ops.wm.read_factory_settings(use_empty=True)
        with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=[meta['blender']['collection']]
        c=dst.collections[0];bpy.context.scene.collection.children.link(c);lo,hi=bounds(c)
        assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3))
        assert c['mount_plane_z_m']==0 and c['front_direction']=='-Y'
        assert all(o.type=='MESH' and all(abs(s-1)<1e-5 for s in o.scale) for o in c.all_objects)
        assert lo[2]<0<hi[2]
        if 'derived_from' in meta:
            parent=folder('induction-cooktop-36in')/'induction-cooktop-36in.blend';assert hashlib.sha256(parent.read_bytes()).hexdigest()==meta['derived_from']['source_sha256']
        if render:preview(c,target,lo,hi)
        js(target/'validation.json',{'fresh_native_reopen':True,'fresh_collection_link':True,'evaluated_dimensions_m':[hi[i]-lo[i] for i in range(3)],'evaluated_bounds_m':{'min':lo,'max':hi},'object_count':len(c.all_objects),'unit_scale_checked':True,'counter_mount_origin_checked':True,'relative_dependencies':'No runtime external dependencies; induction source provenance hash verified.','preview_rendered':(target/'preview.png').exists(),'preview_visually_reviewed':False,'host_integration_checked':False,'native_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'software':bpy.app.version_string})
        print('VERIFIED',slug,len(c.all_objects),flush=True)

if __name__=='__main__':
    if '--verify' in sys.argv:verify('--render' in sys.argv)
    else:publish()
