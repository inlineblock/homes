"""Publish original shared furniture; verify/review through CPU studio previews.

Blender --background --python tools/library/build_lindon_furniture.py
Blender --background --python tools/library/build_lindon_furniture.py -- --verify
The second invocation fresh-links each native asset; add --render for previews.
Existing published native files are never overwritten.
"""
from pathlib import Path
import bpy, json, math, sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.furnishings import soft, sofa, bed, chair, bowl
from common.finish_palette import textured

ASSETS={
 'oak-linen-queen-bed':('Oak and linen queen bed','bed-queen','Headboard toward -Y; foot toward +Y. Mattress nominal 60 × 84 inches.'),
 'oak-linen-king-bed':('Oak and linen king bed','bed-king','Headboard toward -Y; foot toward +Y. Mattress nominal 76 × 84 inches.'),
 'linen-three-seat-sofa':('Linen three-seat sofa','sofa','Front +Y; back -Y. Nominal 11.4-foot overall width.'),
 'oak-upholstered-dining-chair':('Oak upholstered dining chair','chair','Front -Y; back +Y.'),
 'oak-dining-table-8ft':('Eight-foot oak dining table','table','Long axis X. Nominal 8 × 3.7 feet, 30-inch top height.'),
 'oak-rounded-coffee-table':('Rounded oak coffee table','coffee','Long axis X; nominal 5.5 × 2.8 feet.'),
 'oak-open-nightstand':('Oak open nightstand','nightstand','Front -Y; open shelf and tray top; no concealed door.'),
 'oak-writing-desk':('Oak writing desk','desk','Seated front -Y; 1.8 × .75 meter top.'),
 'oak-round-dining-table-1000':('Compact round oak dining table','round-table','Floor center; 1.0 meter diameter, .75 meter top height.'),
 'kitchen-sink-mixer-650':('Stainless sink and mixer','sink','Countertop mounting plane Z=0, front -Y; bowl extends below plane.'),
 'vanity-basin-mixer-mirror':('Vessel basin mixer and mirror','basin','Countertop mounting plane Z=0; wall / mirror toward +Y; front -Y.'),
 'shower-tray-screen-900':('900 mm shower tray and screen','shower','Floor center Z=0; open entry toward -Y; plumbing wall +Y.'),
 'front-loading-laundry-600':('600 mm front-loading laundry module','laundry','Floor center Z=0; drum door faces -Y; generic washer/dryer concept.'),
}
CATEGORIES={'kitchen-sink-mixer-650':'fixtures','vanity-basin-mixer-mirror':'fixtures','shower-tray-screen-900':'fixtures','front-loading-laundry-600':'appliances'}

def installation(kind):
    """Component-specific interfaces; allowances are concepts, not code minima."""
    base={'basis':'Original concept geometry; no manufacturer selected','host_open_state_checked':False}
    if kind=='sink':
        return {'mounting':'Countertop mounting plane Z=0. Provide a 650 × 450 mm opening, support the metal flange continuously, and leave the bowl unobstructed below the top.',
          'countertop_cutout_m':[.65,.45], 'below_counter_bowl_depth_m':.218,
          'operating_envelope':dict(base,modeled_state='Open bowl and static mixer; mixer movement not articulated',
              reserve_front_standing_depth_m=.80,notes='Keep the approach clear of open appliance doors; allow hand movement around the rear mixer and lever. Standing allowance is a project starting point, not an accessibility or code claim.'),
          'service_requirements':['Provide drain/trap and hot/cold routes below bowl; the model does not include a functioning drain or trap.',
            'Reserve removable cabinet-front access to connections; coordinate selected faucet fixing, countertop thickness and splash protection.']}
    if kind=='basin':
        return {'mounting':'Vessel bowl sits on countertop plane Z=0. Rear mixer requires countertop fixing; separate mirror/backing requires a structural wall at local +Y. Mirror back is approximately 0.3475 m behind the mounting origin.',
          'operating_envelope':dict(base,modeled_state='Open vessel bowl; static mixer; wall-mounted mirror',reserve_front_standing_depth_m=.80,
            notes='Verify basin height, faucet reach and handwashing space in host. Mirror is not supported by the basin; no reach or mobility compliance is asserted.'),
          'service_requirements':['Provide basin waste opening, trap, supply connections and service access below counter. Drain rough-ins are not modeled.',
             'Coordinate mirror attachment, wet-area electrical interfaces and splash-resistant wall finish; no product rating supplied.']}
    if kind=='shower':
        return {'mounting':'900 × 900 mm nominal tray on a continuous supported waterproof floor. Fixed screen attaches along local -X; mixer/riser and head arm require a wall and supply connections at local +Y. Entry is open toward -Y.',
          'operating_envelope':dict(base,modeled_state='Fixed screen and open front; no swinging shower door',reserve_front_approach_depth_m=.80,
             notes='Host must keep dry approach clear, check actual standing space and control reach, and contain water at the open entry. This concept screen layout is not a tested watertight assembly.'),
          'service_requirements':['Connect the rear drainage-slot allowance to a properly designed drain, waterproofing and slope system.',
             'Resolve tray threshold, screen anchorage, safety glass, slip resistance, temperature controls, ventilation and product clearances.']}
    if kind=='laundry':
        return {'mounting':'Freestanding front-loading appliance on a continuous level floor. Body is 600 mm wide and 640 mm deep; front drum/handle increases modeled overall depth. Front is -Y.',
          'operating_envelope':dict(base,modeled_state='Door closed; hinge motion is not rigged',intended_open_angle_degrees=110,reserve_front_depth_m=.70,
             notes='Opening angle and 700 mm front allowance are concept assumptions. Check door swing, operator and laundry basket together against the selected appliance; do not count the same floor space as a permanently clear passage.'),
          'service_requirements':['Reserve rear hose/connection space and an accessible shutoff/drain arrangement; exact clearances depend on the selected washer or dryer.',
             'Resolve dryer exhaust or condensate drainage, vibration, leak management, electrical requirements and whole-appliance replacement access.']}
    return {'mounting':'Freestanding floor-supported original furniture concept.',
      'operating_envelope':dict(base,modeled_state='Fixed furniture, no opening mechanism',
         notes='Host must reserve actual chair pullback, seated/bedside approach and passage; bounds are furniture geometry, not circulation clearance.')}

def palette():
    path=ROOT/'library/materials/coastal-white-oak/v001/coastal-white-oak.blend'
    with bpy.data.libraries.load(str(path),link=True) as (a,b): b.materials=[a.materials[0]]
    M={'oak':b.materials[0],
      'linen':textured('Original warm ivory upholstery',(.55,.535,.49),(.73,.71,.66),420,.9,.0001),
      'blue':textured('Original muted flax accent',(.26,.23,.18),(.39,.35,.29),350,.9,.0001),
      'porcelain':g.material('Original warm white pillows',(.78,.77,.73),.9),
      'steel':g.material('Original brushed stainless',(.48,.50,.51),.24,.85),
      'dark':g.material('Original charcoal accents',(.025,.028,.03),.35),
      'ceramic':g.material('Original satin sanitary ceramic',(.78,.78,.74),.24),
      'glass':g.material('Original fixture clear glass',(.94,.98,.99),.06)}
    bs=M['glass'].node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.45
    return M

def build(slug,kind):
    M=palette(); c=g.collection(ASSETS[slug][0]); c['asset_id']=CATEGORIES.get(slug,'furniture')+'/'+slug; c['asset_version']='v001'
    def box(name,loc,size,mat,bevel=.005):return g.box(name,[v/g.F for v in loc],[v/g.F for v in size],mat,bevel/g.F)
    def rod(name,a,b,r,mat):return g.rod(name,[v/g.F for v in a],[v/g.F for v in b],r/g.F,mat)
    if kind.startswith('bed'):
        bed('Queen' if kind=='bed-queen' else 'King',0,0,5 if kind=='bed-queen' else 76/12,M)
        for o in list(c.objects):
            if 'bedside' in o.name:bpy.data.objects.remove(o,do_unlink=True)
        for x in [-1.8,1.8]:
            for y in [-2.7,2.7]:g.cyl('Bed recessed supporting foot',(x,y,.12),.13,.24,M['oak'])
    elif kind=='sofa': sofa('Three-seat sofa',0,0,M)
    elif kind=='chair': chair('Dining chair',0,0,0,M)
    elif kind=='table':
        soft('Rounded dining top',(0,0,2.4),(8,3.7,.2),M['oak'],.32)
        for x in [-2.65,2.65]:g.box('Dining trestle',(x,0,1.15),(.36,2.7,2.3),M['oak'],.06)
        g.box('Dining lower stretcher',(0,0,.55),(5.6,.28,.28),M['oak'],.04)
    elif kind=='coffee':
        soft('Coffee top',(0,0,1.18),(5.5,2.8,.18),M['oak'],.28)
        for x in [-1.9,1.9]:g.box('Coffee support',(x,0,.55),(.3,2,1.1),M['oak'],.05)
    elif kind=='nightstand':
        for z in [.18,1.76]:g.box('Nightstand horizontal shelf',(0,0,z),(1.7,1.6,.13),M['oak'],.025)
        for x in [-.8,.8]:g.box('Nightstand side',(x,0,.93),(.1,1.6,1.73),M['oak'],.025)
        g.box('Nightstand back',(0,.75,.93),(1.65,.1,1.73),M['oak'],.015)
    elif kind=='desk':
        box('Writing desk top',(0,0,.735),(1.8,.75,.035),M['oak'],.025)
        for x in [-.76,.76]:box('Desk trestle',(x,0,.36),(.045,.62,.72),M['oak'],.012)
        box('Desk rear stretcher',(0,.23,.26),(1.54,.035,.05),M['oak'])
    elif kind=='round-table':
        g.cyl('Round dining top',(0,0,.73/g.F),.50/g.F,.04/g.F,M['oak'],96)
        g.cyl('Round table pedestal',(0,0,.36/g.F),.11/g.F,.72/g.F,M['oak'],48)
        g.cyl('Round table stable base',(0,0,.025/g.F),.33/g.F,.05/g.F,M['oak'],64)
    elif kind=='sink':
        box('Stainless sink bowl bottom',(0,0,-.208),(.64,.44,.02),M['steel'],.014)
        for x in [-.32,.32]:box('Sink end',(x,0,-.105),(.014,.45,.21),M['steel'])
        for y in [-.22,.22]:box('Sink side',(0,y,-.105),(.65,.014,.21),M['steel'])
        for x in [-.335,.335]:box('Sink flange',(x,0,.004),(.045,.49,.008),M['steel'])
        for y in [-.235,.235]:box('Sink flange',(0,y,.004),(.65,.04,.008),M['steel'])
        g.curve('High arch kitchen mixer',[(0,.285/g.F,0),(0,.285/g.F,.34/g.F),(0,.06/g.F,.39/g.F),(0,-.03/g.F,.28/g.F)],.015/g.F,M['steel'])
        rod('Mixer lever',(.08,.285,0),(.08,.285,.15),.012,M['steel'])
    elif kind=='basin':
        bowl('Vessel porcelain basin',0,0,0,.75,M['ceramic'])
        g.curve('Vanity mixer',[(0,.27/g.F,0),(0,.27/g.F,.25/g.F),(0,.06/g.F,.28/g.F)],.012/g.F,M['steel'])
        box('Mirror backing',(0,.335,.76),(.55,.025,.75),M['dark'],.025)
        mirror=g.material('Original polished mirror',(.80,.80,.80),.025,1)
        box('Vanity mirror face',(0,.316,.76),(.52,.009,.72),mirror,.015)
    elif kind=='shower':
        box('Shower tray',(0,0,.025),(.90,.90,.05),M['ceramic'],.015)
        box('Shower recessed drainage slot',(0,.36,.052),(.35,.025,.008),M['dark'])
        box('Fixed left shower screen',(-.44,0,1.03),(.009,.89,2.0),M['glass'],.003)
        rod('Shower screen post',(-.44,-.44,.04),(-.44,-.44,2.05),.012,M['dark'])
        rod('Shower rail',(0,.43,.85),(0,.43,1.90),.012,M['steel'])
        rod('Shower head arm',(0,.43,1.90),(0,.12,1.90),.012,M['steel'])
        g.cyl('Rain shower head',(0,.12/g.F,1.90/g.F),.12/g.F,.025/g.F,M['steel'])
        box('Mixer plate',(0,.437,1.05),(.15,.03,.18),M['steel'],.014)
    elif kind=='laundry':
        box('Laundry appliance enclosure',(0,0,.425),(.60,.64,.85),M['ceramic'],.025)
        box('Laundry control band',(0,-.326,.73),(.56,.016,.13),M['dark'],.008)
        o=g.cyl('Laundry glazed circular door',(0,-.34/g.F,.40/g.F),.225/g.F,.035/g.F,M['dark'],64);o.rotation_euler.x=math.pi/2
        o=g.cyl('Laundry drum glass',(0,-.366/g.F,.40/g.F),.178/g.F,.012/g.F,M['glass'],64);o.rotation_euler.x=math.pi/2
        o=g.cyl('Laundry control knob',(.18/g.F,-.347/g.F,.735/g.F),.024/g.F,.02/g.F,M['steel'],32);o.rotation_euler.x=math.pi/2
        box('Laundry door grip',(.19,-.39,.40),(.025,.025,.14),M['steel'])
    for o in c.all_objects:
        if o.type=='CURVE':o.data.use_fill_caps=True
    bpy.context.view_layer.update()
    # A real supporting foot / side reaches the placement plane.
    lowest=min((o.matrix_world@Vector(v)).z for o in c.all_objects for v in o.bound_box)
    if kind not in ['sink','basin']:
        for o in c.all_objects:o.location.z-=lowest
    bpy.context.view_layer.update();return c

def bounds(c):
    pts=[o.matrix_world@Vector(v) for o in c.all_objects for v in o.bound_box]
    lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
    return lo,hi

def publish():
    for slug,(name,kind,front) in ASSETS.items():
        category=CATEGORIES.get(slug,'furniture');folder=ROOT/'library'/category/slug/'v001'; path=folder/(slug+'.blend')
        if path.exists():print('IMMUTABLE_EXISTING',slug,flush=True);continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        c=build(slug,kind);lo,hi=bounds(c);folder.mkdir(parents=True,exist_ok=True)
        bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap='RELATIVE_ALL')
        meta={'schema_version':1,'id':category+'/'+slug,'version':'v001','name':name,'units':'meters',
          'dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},
          'placement':{'origin':'Floor center at Z=0; centered nominal plan footprint','front_direction':front,'up':'Z','allowed_scaling':'Rigid placement and Z rotation only. Publish a dimensional sibling instead of nonuniform scaling.'},
          'installation':installation(kind),
          'dependencies':[{'id':'materials/coastal-white-oak','version':'v001','path':'../../../materials/coastal-white-oak/v001/coastal-white-oak.blend'}],
          'source':{'kind':'original','generator':'tools/library/build_lindon_furniture.py','primitives':'tools/common/furnishings.py','software':bpy.app.version_string},
          'derived_from':None,'license':'CC-BY-4.0','rights':'Original geometry; attribution Homes project contributors',
          'files':{'blender':path.name,'preview':'preview.png','validation':'validation.json'}}
        if kind.startswith('bed'):meta['bed_count']=1
        if kind in ['sink','basin','shower','laundry']:meta['dependencies']=[]
        if kind in ['sink','basin']:
            meta['placement']['origin']='Countertop mounting center Z=0'
        (folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
        (folder.parent/'AGENTS.md').write_text('# Shared original component\n\n- Read the version manifest for actual dimensions, front direction and mounting origin.\n- Link and instance the collection at scale 1. Preserve adopted versions; publish another size as a distinct sibling.\n- Provide all host mounting, opening, standing and service interfaces listed in the manifest. A closed or isolated preview does not verify installation.\n- Record actual adoption and host review; component bounds alone are not a circulation or product-approval check.\n')
        print('PUBLISHED',slug,flush=True)

def verify(render=False):
    for slug,(name,kind,front) in ASSETS.items():
        if '--asset' in sys.argv and slug!=sys.argv[sys.argv.index('--asset')+1]:continue
        folder=ROOT/'library'/CATEGORIES.get(slug,'furniture')/slug/'v001';path=folder/(slug+'.blend')
        # Direct native opening reveals stored relative paths. On subsequent
        # linking into another file Blender normalizes nested paths in memory.
        bpy.ops.wm.open_mainfile(filepath=str(path))
        assert all(lib.filepath.startswith('//') for lib in bpy.data.libraries)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        with bpy.data.libraries.load(str(path),link=True) as (a,b):b.collections=[a.collections[0]]
        c=b.collections[0];bpy.context.scene.collection.children.link(c);bpy.context.view_layer.update()
        lo,hi=bounds(c);meta=json.loads((folder/'asset.json').read_text())
        assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3))
        if kind not in ['sink','basin']:assert abs(lo[2])<1e-5
        assert all(Path(bpy.path.abspath(lib.filepath,library=lib.parent)).exists() for lib in bpy.data.libraries)
        if kind.startswith('bed'):assert sum(' bed frame' in o.name for o in c.all_objects)==1
        receipt={'fresh_link':True,'dimensions_m':[hi[i]-lo[i] for i in range(3)],'floor_contact':None if kind in ['sink','basin'] else True,'objects':len(c.all_objects),'relative_material_dependencies':True,'preview_rendered':(folder/'preview.png').exists()}
        if render:
            g.collection('Preview studio');center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))/g.F
            target=[v/g.F for v in center];loc=[target[0]+span*1.15,target[1]+span*1.6,target[2]+span*1.12]
            if kind in ['chair','nightstand','sink','basin','shower','laundry','desk']:loc[1]=target[1]-span*1.7
            if kind=='nightstand':loc=[target[i]+(loc[i]-target[i])*1.25 for i in range(3)]
            cam=g.camera('Original furniture preview',loc,target,50);bpy.context.scene.camera=cam
            floor=g.material('Studio floor',(.55,.57,.58),.9);g.box('Studio ground',(0,0,lo[2]/g.F-.07),(span*200,span*200,.12),floor)
            g.area('Soft key',(span,-span,span*2),target,span*span*18,span*1.5,(1,.93,.85));g.area('Soft fill',(-span,span,span),target,span*span*6,span*1.5,(.85,.93,1))
            s=bpy.context.scene;s.world=bpy.data.worlds.new('Studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
            s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=6
            s.render.resolution_x=800;s.render.resolution_y=650;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(folder/'preview.png');s.view_settings.view_transform='AgX';s.view_settings.exposure=-.4
            bpy.ops.render.render(write_still=True);receipt['preview_rendered']=True
        (folder/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print('VERIFIED',slug,flush=True)

if __name__=='__main__':
    if '--metadata-only' in sys.argv:
        for slug,(_,kind,_) in ASSETS.items():
            folder=ROOT/'library'/CATEGORIES.get(slug,'furniture')/slug/'v001';p=folder/'asset.json'
            meta=json.loads(p.read_text());meta['installation']=installation(kind);p.write_text(json.dumps(meta,indent=2)+'\n')
            if kind in ['sink','basin','shower','laundry']:
                (folder.parent/'AGENTS.md').write_text('# Shared fixture or appliance\n\n- Preserve the versioned native model; use its exact meter scale, front and mounting origin.\n- Provide the manifest-defined host support, connections, opening and service access. Counter-mounted and wall-mounted parts are not freestanding furniture.\n- Keep standing/door-swing allowances separate from permanent routes. Mark product and regulatory checks unresolved until the specific installation is verified.\n')
    elif '--verify' in sys.argv:verify('--render' in sys.argv)
    else:publish()
