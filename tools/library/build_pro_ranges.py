"""Original representative range families; meters, front -Y, no product claims.
Run Blender --background --python tools/library/build_pro_ranges.py -- build
Then ... -- verify --slug gas-range-36in (and dual-fuel-range-48in).
"""
import argparse, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
ARGS=argparse.ArgumentParser(); ARGS.add_argument('action',choices=['build','verify']); ARGS.add_argument('--slug',choices=['gas-range-36in','dual-fuel-range-48in']); A=ARGS.parse_args(sys.argv[sys.argv.index('--')+1:])
SLUGS=['gas-range-36in','dual-fuel-range-48in']
DEP='library/appliances/built-in-oven-30in/v001/built-in-oven-30in.blend'
M={}; C=None

def move(o,name,mat=None):
    o.name=name
    for c in list(o.users_collection):c.objects.unlink(o)
    C.objects.link(o)
    if mat:o.data.materials.append(mat)
    return o

def box(name,xyz,size,mat,bevel=.002):
    bpy.ops.mesh.primitive_cube_add(size=1,location=xyz);o=move(bpy.context.object,name,mat);o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel: m=o.modifiers.new('Manufactured softened edges','BEVEL');m.width=bevel;m.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o

def rod(name,a,b,r,mat):
    v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=v.length,location=(Vector(a)+Vector(b))/2)
    o=move(bpy.context.object,name,mat);o.rotation_euler=v.to_track_quat('Z','Y').to_euler()
    for p in o.data.polygons:p.use_smooth=True
    return o

def cyl(name,xyz,r,h,mat):return rod(name,(xyz[0],xyz[1],xyz[2]-h/2),(xyz[0],xyz[1],xyz[2]+h/2),r,mat)

def bounds(objects):
    pts=[o.matrix_world@Vector(v) for o in objects if o.type=='MESH' for v in o.bound_box]
    return {'min':[round(min(v[i] for v in pts),6) for i in range(3)],'max':[round(max(v[i] for v in pts),6) for i in range(3)]}

def swept_bounds(objects,hinges):
    previous=[h.rotation_euler.x for h in hinges]; samples=[]
    for angle in range(0,91,2):
        for h in hinges:h.rotation_euler.x=math.radians(angle)
        bpy.context.view_layer.update();samples.append(bounds(objects))
    for h,a in zip(hinges,previous):h.rotation_euler.x=a
    bpy.context.view_layer.update()
    b={'min':[min(s['min'][i] for s in samples) for i in range(3)],'max':[max(s['max'][i] for s in samples) for i in range(3)]}
    b['min'][1]=round(b['min'][1]-.001,6)
    return b

def cavity(x,w,label):
    # Real opening with rear, base, ceiling, side insulation and internal racks.
    lo,hi=.18,.725
    for sx in [x-w/2+.018,x+w/2-.018]:box(label+' enamel cavity side',(sx,.01,(lo+hi)/2),(.025,.61,hi-lo),M['dark'])
    box(label+' enamel rear',(x,.31,(lo+hi)/2),(w-.045,.022,hi-lo),M['dark'])
    for z in [lo,hi]:box(label+' enamel cavity horizontal',(x,.01,z),(w-.045,.61,.022),M['dark'])
    for z in [.30,.49]:
        for sx in [x-w/2+.05,x+w/2-.05]:rod(label+' rack side',(sx,-.27,z),(sx,.265,z),.003,M['steel'])
        for j in range(15):rod(label+' rack crossbar',(x-w/2+.05,-.26+j*.036,z),(x+w/2-.05,-.26+j*.036,z),.0026,M['steel'])
    for z in [.26,.34,.42,.50,.58]:
        for sx in [x-w/2+.032,x+w/2-.032]:rod(label+' rack guide',(sx,-.255,z),(sx,.26,z),.003,M['steel'])
    # Rear fan guard rings visually grounded in cavity.
    for r in [.04,.07,.095]:
        bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=.0025,major_segments=32,minor_segments=6,location=(x,.292,.46),rotation=(math.pi/2,0,0));move(bpy.context.object,label+' convection guard',M['steel'])
    hinge=bpy.data.objects.new(label+' door hinge - rotate X +90 degrees',None);C.objects.link(hinge);hinge.location=(x,-.361,.175);hinge['open_angle_degrees']=90
    before=set(C.objects)
    for sx in [x-w/2+.038,x+w/2-.038]:box(label+' door stainless stile',(sx,-.365,.444),(.069,.052,.54),M['steel'])
    for z in [.198,.690]:box(label+' door stainless rail',(x,-.365,z),(w-.014,.052,.071),M['steel'])
    for sx in [x-w/2+.080,x+w/2-.080]:box(label+' viewing gasket',(sx,-.374,.447),(.019,.028,.419),M['rubber'])
    for z in [.24,.65]:box(label+' viewing gasket',(x,-.374,z),(w-.155,.028,.019),M['rubber'])
    box(label+' transparent viewing glass',(x,-.372,.445),(w-.17,.009,.40),M['glass'],.001)
    for sx in [x-w*.32,x+w*.32]:rod(label+' handle standoff',(sx,-.392,.66),(sx,-.427,.66),.009,M['steel'])
    rod(label+' brushed handle',(x-w*.38,-.430,.66),(x+w*.38,-.430,.66),.013,M['steel'])
    bpy.context.view_layer.update()
    for ob in set(C.objects)-before:ob.parent=hinge;ob.matrix_parent_inverse=hinge.matrix_world.inverted()
    return hinge

def build(slug):
    global C,M
    out=ROOT/'library/appliances'/slug/'v001';out.mkdir(parents=True,exist_ok=True)
    if (out/(slug+'.blend')).exists():raise RuntimeError('Immutable existing version: '+str(out))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    C=bpy.data.collections.new(slug+' | v001');bpy.context.scene.collection.children.link(C)
    names={'steel':'Original appliance brushed stainless','dark':'Original appliance graphite enamel','rubber':'Original appliance graphite enamel','glass':'Original appliance low-tint glass','marks':'Original appliance etched control marks'}
    with bpy.data.libraries.load(str(ROOT/DEP),link=True) as (src,dst):dst.materials=list(dict.fromkeys(names.values()))
    M={key:bpy.data.materials.get(name) for key,name in names.items()};assert all(M.values())
    wide=slug.startswith('dual');w=1.2192 if wide else .9144
    for x in [-w/2+.012,w/2-.012]:box('Brushed steel side shell',(x,0,.487),(.024,.70,.814),M['steel'])
    box('Rear service and heat shield',(0,.34,.49),(w-.04,.022,.82),M['steel'])
    box('Undercarriage',(0,.01,.11),(w-.055,.62,.07),M['dark'])
    for x in [-w/2+.08,w/2-.08]:
        for y in [-.27,.26]:cyl('Adjustable foot',(x,y,.05),.026,.10,M['steel'])
    box('Recessed toe grille',(0,-.302,.118),(w-.08,.025,.05),M['dark'])
    for i in range(int(w/.032)-3):box('Toe grille vent',(i*.032-w/2+.063,-.318,.12),(.014,.004,.021),M['rubber'],.001)
    box('Control fascia',(0,-.337,.799),(w,.07,.137),M['steel'])
    box('Sealed cooktop tray',(0,0,.875),(w,.70,.021),M['steel'])
    box('Low rear riser',(0,.335,.91),(w,.031,.07),M['steel'])
    # Six independent burner pans, caps, support fingers and continuous grate frame.
    xs=[-w/2+.16,0,w/2-.16] if not wide else [-.454,-.164,.166]
    for i,x in enumerate(xs):
        for j,y in enumerate([-.177,.153]):
            rad=.052 if i==1 else .045
            cyl('Recessed burner well',(x,y,.891),.091,.014,M['dark']);cyl('Gas burner brass-colored ring',(x,y,.903),rad,.014,M['marks']);cyl('Gas burner cap',(x,y,.915),rad+.008,.014,M['dark'])
            for k in range(8):
                a=k*math.tau/8
                box('Burner port',(x+rad*math.cos(a),y+rad*math.sin(a),.904),(.003,.003,.005),M['rubber'],0)
            for ang in [0,math.pi/2,math.pi,3*math.pi/2]:
                a=(x+.041*math.cos(ang),y+.041*math.sin(ang),.944);b=(x+.118*math.cos(ang),y+.118*math.sin(ang),.944)
                rod('Cast-iron pot support',a,b,.0075,M['dark'])
            for dx in [-.123,.123]:box('Cast-iron grate longitudinal',(x+dx,y,.938),(.012,.28,.018),M['dark'])
            for dy in [-.14,.14]:box('Cast-iron grate crossrail',(x,y+dy,.938),(.256,.012,.018),M['dark'])
    if wide:
        box('Separate steel griddle plate',(.458,-.01,.912),(.24,.55,.018),M['steel'])
        for x in [.335,.581]:box('Griddle rim',(x,-.01,.922),(.007,.55,.017),M['dark'])
        box('Griddle front grease trough',(.458,-.293,.9),(.235,.024,.014),M['dark'])
    knobxs=[-w*.43+i*(w*.86/(8 if wide else 6)) for i in range(9 if wide else 7)]
    for i,x in enumerate(knobxs):
        rod('Control dial bezel',(x,-.374,.8),(x,-.385,.8),.034,M['dark']);rod('Control dial',(x,-.387,.8),(x,-.414,.8),.025,M['steel'])
        box('Knob off pointer',(x,-.429,.816),(.0025,.003,.011),M['rubber'],.0006)
        for k in range(5):
            a=math.pi*.2+k*math.pi*.15
            box('Engraved dial scale',(x+.040*math.cos(a),-.374,.8+.040*math.sin(a)),(.002,.002,.003),M['marks'],0)
    hinges=[]
    if wide:
        # Two independently hinged true cavities, 30/18-inch conceptual split.
        hinges=[cavity(-.220,.738,'Main electric oven'),cavity(.370,.418,'Companion electric oven')]
    else:hinges=[cavity(0,w-.043,'Gas oven')]
    bpy.context.view_layer.update();b=bounds(C.objects);dims=[round(b['max'][i]-b['min'][i],6) for i in range(3)]
    C['asset_id']='appliances/'+slug;C['asset_version']='v001';C['front_direction']='-Y';C['concept_only']=True
    scene=bpy.context.scene;scene.unit_settings.system='METRIC'
    # Non-asset preview rig stays outside published collection.
    stage=bpy.data.collections.new('Preview studio (do not instance)');scene.collection.children.link(stage);Casset=C;C=stage
    floor=bpy.data.materials.new('Preview neutral');floor.diffuse_color=(.15,.17,.18,1)
    box('Preview floor',(0,0,-.032),(200,200,.06),floor,0)
    bpy.ops.object.camera_add(location=(1.75,-2.35,1.65));cam=move(bpy.context.object,'Preview camera');cam.rotation_euler=(Vector((0,0,.49))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.83 if wide else 1.50;scene.camera=cam
    for xyz,power,size in [((1,-2,3),450,3),((-2,-.6,2),300,2),((0,2,2.5),400,2)]:
        bpy.ops.object.light_add(type='AREA',location=xyz);o=move(bpy.context.object,'Studio area');o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
    scene.world=bpy.data.worlds.new('Neutral studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.18,.18,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.4
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=3;scene.render.resolution_x=600;scene.render.resolution_y=600;scene.render.resolution_percentage=100
    scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(str(ROOT/DEP),start=str(out))
    bpy.ops.wm.save_as_mainfile(filepath=str(out/(slug+'.blend')))
    scene.render.filepath=str(out/'preview.png');bpy.ops.render.render(write_still=True)
    for hinge in hinges:hinge.rotation_euler.x=math.pi/2
    bpy.context.view_layer.update();openbounds=bounds(Casset.objects);sweep=swept_bounds(Casset.objects,hinges)
    cam.data.ortho_scale*=1.30;cam.rotation_euler=(Vector((0,-.20,.43))-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/'open-preview.png');bpy.ops.render.render(write_still=True)
    manifest={'schema_version':1,'id':'appliances/'+slug,'version':'v001','name':('48-inch dual-fuel range — six burners, griddle, two ovens' if wide else '36-inch gas range — six burners, single oven'),'units':'meters','dimensions_m':dims,'bounds_m':b,'nominal_case_m':{'width':w,'depth':.70,'cooktop_tray_height':.8855,'pot_support_height':.9515},'blender':{'collection':Casset.name},'placement':{'origin':'Floor-center XY, Z=0 at foot bottoms','front':'-Y','up':'+Z','mounting':'Freestanding level floor; side panels do not replace a cabinet opening','allowed_scaling':'None; create a new dimensional variant instead'},'operating_envelope':{'modeled_state':'Closed native source; open-preview renders hinged doors at +90 degrees around X','opening_basis':'Measured original concept geometry, not manufacturer clearance','door_angle_degrees':90,'open_bounds_m':openbounds,'conservative_swept_bounds_m':sweep,'sweep_basis':'Door hinges sampled every 2 degrees from 0 to 90, unioned with fixed case; 1 mm front padding exceeds angular sampling error. Add operating-person space separately.','front_clearance_from_case_m':round(-.35-openbounds['min'][1],4),'required_host_checks':['Door swing and handle sweep','Usable passage with oven door open','Landing counters on both sides','No carcass or drawer obscuring cavities'],'host_open_state_checked':False},'installation':{'concept_only':True,'suggested_rough_opening_width_m':w+.012,'rear_service_reserve_m':.06,'service_access':'Pull-out access after safe isolation; provide selected-product shutoffs and receptacles outside hot/obstructed zones','fuel':'Gas cooking surface with two electric ovens and electric griddle' if wide else 'Gas cooking surface and gas oven; electrical ignition and light assumption','electrical':'Supply rating, dedicated circuit and connection unselected; actual product determines requirements','ventilation':'Externally ducted capture hood concept required; width, height, airflow, make-up air and combustion compatibility remain unselected','heat_clearances':'No certified combustible clearances; coordinate exact listed appliance, hood, backsplash and adjacent tall cabinetry','anti_tip':'Host must provide the selected product anti-tip restraint; not certified or modeled here'},'design_basis':{'kind':'Original nominal-size concept','dimensions_basis':'36 or 48 inch nominal width converted at 0.0254 meters/inch. All other geometry authored as an original visualization assumption; no manufacturer product copied.','commercial_specification':False},'source':{'kind':'original','generator':'tools/library/build_pro_ranges.py','command':'Blender --background --python tools/library/build_pro_ranges.py -- build --slug '+slug},'license':'CC-BY-4.0','rights':'Original geometry by Homes project contributors; attribution Homes project contributors','dependencies':[{'id':'appliances/built-in-oven-30in','version':'v001','path':DEP,'usage':'Pinned linked steel, graphite (also used for gaskets), glass and marks materials; no object geometry copied'}],'files':{'blender':slug+'.blend','preview':'preview.png','open_preview':'open-preview.png','validation':'validation.json'},'software':{'blender':bpy.app.version_string},'limitations':['No certification, installation drawing, thermal performance or appliance recommendation','Control markings illustrative; no branded interface','Preview is asset-only; host installation and circulation not checked']}
    (out/'asset.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'README.md').write_text('# '+manifest['name']+'\n\nOriginal generic concept, not a purchasable or certified appliance. Floor-centered, front **−Y**, meters; do not scale.\n\n![Closed native preview](preview.png)\n\n![Hinged open native preview](open-preview.png)\n\nLink collection `'+Casset.name+'` from `'+slug+'.blend`. The preview studio is separate and should not be instanced. Actual cavities, racks, support grates and independently hinged oven doors are modeled. Door pivot empties carry the opening angle. The closed model is the saved default; the open preview is generated from the same geometry.\n\nSee [asset.json](asset.json) for measured closed/open bounds, the suggested concept recess, exact material dependency, unresolved services and ventilation. Host open-door passage, adjacent combustible surfaces, extraction and anti-tip installation still require review.\n\nGenerate only while unpublished with `Blender --background --python tools/library/build_pro_ranges.py -- build --slug '+slug+'`; fresh reopen with `... -- verify --slug '+slug+'`. Published versions are immutable.\n')

def verify(slug):
    out=ROOT/'library/appliances'/slug/'v001';m=json.loads((out/'asset.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(out/(slug+'.blend')))
    col=bpy.data.collections[m['blender']['collection']];bpy.context.view_layer.update();b=bounds(col.objects);assert b==m['bounds_m'],(b,m['bounds_m'])
    libs=[{'path':l.filepath,'relative':l.filepath.startswith('//'),'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries];assert all(l['relative'] and l['exists'] for l in libs)
    assert len([o for o in col.objects if 'rack crossbar' in o.name])>=30
    hinges=[o for o in col.objects if o.type=='EMPTY' and 'door hinge' in o.name];assert len(hinges)==(2 if slug.startswith('dual') else 1)
    for hinge in hinges:assert abs(hinge.rotation_euler.x)<1e-6;hinge.rotation_euler.x=math.pi/2
    bpy.context.view_layer.update();ob=bounds(col.objects);assert ob==m['operating_envelope']['open_bounds_m']
    sweep=swept_bounds(col.objects,hinges);assert sweep==m['operating_envelope']['conservative_swept_bounds_m']
    scene=bpy.context.scene;cam=scene.camera;cam.data.ortho_scale*=1.30;cam.rotation_euler=(Vector((0,-.20,.43))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(out/'open-preview.png');bpy.ops.render.render(write_still=True)
    receipt={'status':'fresh_reopen_pass','blender':bpy.app.version_string,'collection':col.name,'object_count':len(col.objects),'closed_bounds_m':b,'open_bounds_m':ob,'conservative_swept_bounds_m':sweep,'oven_cavities':len(hinges),'door_rotation_checked_degrees':90,'relative_dependencies':libs,'host_integration_checked':False,'visual_review':'Pending actual preview inspection'}
    (out/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
for slug in ([A.slug] if A.slug else SLUGS):
    (build if A.action=='build' else verify)(slug)
