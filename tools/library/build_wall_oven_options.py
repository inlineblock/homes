"""Original articulated oven columns, derived from the existing 30-inch oven.

blender --background --python tools/library/build_wall_oven_options.py
blender --background --python tools/library/build_wall_oven_options.py -- --verify --render
Existing native versions are immutable. All construction dimensions below are meters.
"""
import bpy, json, math, sys, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.appliances import materials
ASSETS={
 'double-wall-oven-30in':('Original 30-inch double wall oven',[.7112,.7112]),
 'oven-speed-oven-combo-30in':('Original 30-inch oven and compact speed-oven combination',[.7112,.4826]),
}
if '--asset' in sys.argv:
    requested=sys.argv[sys.argv.index('--asset')+1];ASSETS={requested:ASSETS[requested]}
PARENT=ROOT/'library/appliances/built-in-oven-30in/v001/built-in-oven-30in.blend'

def box(name,loc,size,mat,bevel=.002):
    return g.box(name,[x/g.F for x in loc],[x/g.F for x in size],mat,bevel/g.F)

def rod(name,a,b,r,mat):
    return g.rod(name,[x/g.F for x in a],[x/g.F for x in b],r/g.F,mat)

def cylinder(name,loc,r,d,mat):
    return g.cyl(name,[x/g.F for x in loc],r/g.F,d/g.F,mat,40)

def bounds(c):
    bpy.context.view_layer.update()
    pts=[o.matrix_world@Vector(v) for o in c.all_objects if o.type in {'MESH','CURVE','FONT'} for v in o.bound_box]
    return [min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]

def parent_keep(obj,parent):
    bpy.context.view_layer.update();m=obj.matrix_world.copy();obj.parent=parent;obj.matrix_world=m

def module(c,M,z,h,index,speed=False):
    tag=('Upper compact speed oven' if speed else ('Lower full oven' if index==0 else 'Upper full oven'))
    body_w=.7239;body_d=.5969;front=-body_d/2
    # Discrete insulated panels enclose an empty cavity. No solid body behind glass.
    for x in [-.34195,.34195]:box(tag+' insulated side',(x,0,z+h/2),(.04,body_d,h-.012),M['dark'])
    box(tag+' insulated back',(0,.27845,z+h/2),(.6439,.04,h-.012),M['dark'])
    for zz in [z+.016,z+h-.016]:box(tag+' insulated top bottom',(0,0,zz),(.6439,body_d,.020),M['dark'])
    for x in [-.3695,.3695]:box(tag+' mounting flange',(x,front-.008,z+h/2),(.023,.018,h),M['steel'])
    control_z=z+h-.066
    box(tag+' brushed control fascia',(0,front-.019,control_z),(.716,.038,.112),M['steel'],.004)
    box(tag+' black control display',(0,front-.040,control_z),(.266,.009,.055),M['dark'],.004)
    # Restrained readable numerals, and etched controls; no commercial logo.
    txt=bpy.data.curves.new(tag+' display text','FONT');txt.body='12:00';txt.size=.025;txt.extrude=.0001
    ob=bpy.data.objects.new(tag+' display text',txt);c.objects.link(ob);ob.location=(-.046,front-.046,control_z-.009);ob.rotation_euler=(math.pi/2,0,0);ob.data.materials.append(M['marks'])
    for x in [-.284,.284]:
        dial=cylinder(tag+' selector dial',(x,front-.050,control_z),.024,.018,M['dark']);dial.rotation_euler.x=math.pi/2
        box(tag+' dial index',(x,front-.060,control_z+.014),(.002,.002,.008),M['steel'],.0005)
    # Continuous viewing aperture bounded by real gasket, stiles and window.
    bottom=z+.042;top=z+h-.136;dh=top-bottom;cy=(bottom+top)/2
    hinge=bpy.data.objects.new(tag+' bottom hinge',None);c.objects.link(hinge);hinge.location=(0,front-.038,bottom)
    hinge['role']='oven_door_hinge';hinge['open_axis']='local X';hinge['open_degrees']=90;hinge['cavity_z_m']=cy
    before=set(c.objects)
    for x in [-.349,.349]:box(tag+' door stile',(x,front-.041,cy),(.032,.045,dh),M['dark'])
    for zz in [bottom+.02,top-.02]:box(tag+' door rail',(0,front-.041,zz),(.666,.045,.04),M['dark'])
    # Real transmissive thin glass, not an opaque facade over an enclosed block.
    box(tag+' inner glass',(0,front-.043,cy),(.650,.006,dh-.070),M['glass'],.003)
    rod(tag+' door handle',(-.286,front-.110,top-.060),(.286,front-.110,top-.060),.009,M['steel'])
    for x in [-.279,.279]:rod(tag+' handle mount',(x,front-.061,top-.060),(x,front-.109,top-.060),.010,M['steel'])
    for x in [-.313,.313]:
        o=cylinder(tag+' hinge pin',(x,front-.038,bottom),.010,.035,M['steel']);o.rotation_euler.y=math.pi/2
    for o in set(c.objects)-before:parent_keep(o,hinge)
    # Gasket stays on stationary cavity flange.
    for x in [-.318,.318]:box(tag+' cavity gasket',(x,front-.003,cy),(.013,.009,dh-.03),M['rubber'])
    for zz in [bottom+.017,top-.017]:box(tag+' cavity gasket',(0,front-.003,zz),(.63,.009,.014),M['rubber'])
    rack_levels=[bottom+.12,bottom+.30] if not speed else [bottom+.075]
    for rz in rack_levels:
        for x in [-.293,.293]:rod(tag+' rack side',(x,-.242,rz),(x,.224,rz),.004,M['steel'])
        for j in range(13):
            yy=-.232+j*.037
            rod(tag+' rack crossbar',(-.293,yy,rz),(.293,yy,rz),.0025,M['steel'])
        for x in [-.307,.307]:box(tag+' rack runner',(x,0,rz-.008),(.012,.465,.014),M['steel'])
    # Exposed rear convection grille, visible through the hollow oven.
    fan=cylinder(tag+' convection fan shield',(0,.253,cy),.093,.01,M['steel']);fan.rotation_euler.x=math.pi/2
    for xx in [-.06,-.04,-.02,0,.02,.04,.06]:box(tag+' fan louver',(xx,.244,cy),(.007,.008,.11),M['dark'],.001)
    if speed:
        # Compact cavity shielding represented as narrow wire grid inside door glass.
        before=set(c.objects)
        for j in range(81):
            x=-.30+j*.0075
            rod(tag+' illustrative window grid',(x,front-.048,bottom+.05),(x,front-.048,top-.05),.00018,M['dark'])
        for j in range(31):
            zz=bottom+.055+j*(dh-.11)/30
            rod(tag+' illustrative window grid',(-.30,front-.048,zz),(.30,front-.048,zz),.00018,M['dark'])
        for o in set(c.objects)-before:parent_keep(o,hinge)
    for j in range(6):box(tag+' bottom front vent',(0,front-.013,z+.007+j*.004),(.61,.007,.0016),M['steel'],.0003)

def build(slug):
    name,levels=ASSETS[slug];c=g.collection(name);c['asset_id']='appliances/'+slug;c['asset_version']='v001';M=materials()
    glass=M['glass'].node_tree.nodes.get('Principled BSDF');glass.inputs['Base Color'].default_value=(.08,.095,.11,1);glass.inputs['Transmission Weight'].default_value=.72;glass.inputs['Roughness'].default_value=.09
    z=0
    for i,h in enumerate(levels):module(c,M,z,h,i,speed=(h<.6));z+=h
    bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
    return c

def publish():
    assert PARENT.exists(),'Real parent asset is required for honest derivation'
    for slug,(name,levels) in ASSETS.items():
        folder=ROOT/'library/appliances'/slug/'v001';path=folder/(slug+'.blend')
        if path.exists():print('IMMUTABLE_EXISTING',slug,flush=True);continue
        bpy.ops.wm.read_factory_settings(use_empty=True);c=build(slug);lo,hi=bounds(c);folder.mkdir(parents=True,exist_ok=True)
        bpy.context.scene['primary_collection']=c.name
        bpy.ops.wm.save_as_mainfile(filepath=str(path))
        height=sum(levels)
        meta={'schema_version':1,'id':'appliances/'+slug,'version':'v001','name':name,'units':'meters',
          'dimensions_m':[round(hi[i]-lo[i],6) for i in range(3)],'bounds_m':{'min':lo,'max':hi},
          'placement':{'origin':'Bottom center of appliance body at Z=0; body centered about X=0,Y=0','front_direction':'-Y','up':'Z','allowed_scaling':'Rigid translation and rotation about Z only; never scale a standard-size appliance.'},
          'nominal_dimensions_inches':{'face_width':30,'body_width':28.5,'body_depth':23.5,'overall_height':height/.0254},
          'installation':{'basis':'Original generic concept geometry, not a manufacturer specification or code minimum. No commercial product selected.',
            'body_dimensions_m':[.7239,.5969,height-.012],'face_width_m':.762,'face_plane_y_m':-.29845,
            'concept_cabinet_opening_m':[.730,height-.004,.625],
            'opening_axis_order':'width X, height Z, clear depth Y; reserve at least this concept envelope pending selected appliance instructions',
            'cabinet_front_y_m':-.29845,'opening_bottom_z_m':.002,'support_platform_z_m':.006,
            'mounting':'Support both ovens on a continuous structurally sized cabinet platform. Keep cavity clear behind fronts; side flanges overlap opening. Provide removable fixing points; brackets/load rating not engineered.',
            'ventilation':'Preserve visible front ventilation slots. Real cooling airflow, rear clearances and heat separation remain manufacturer-specific.',
            'electrical':'Reserve accessible rear connection/service space; dedicated circuits, voltage, conductor size and load must follow selected equipment. This model does not specify wattage or circuitry.',
            'operating_envelope':{'modeled_state':'Both doors closed; separate bottom-hinge empties permit +90 degrees about local X','angle_degrees':90,'measurement':'Fresh-process validation.json measures both doors open and samples 0-90 degree swept bounds at five-degree increments','reserve_below_origin_front_clearance_m':.045,'reserve_operator_depth_beyond_open_door_m':.60,'host_open_state_checked':False},
            'service':'Entire column removes toward -Y. Reserve clear frontal replacement route and support access; host height, operator reach and passage with doors open must be checked separately.'},
          'derived_from':{'id':'appliances/built-in-oven-30in','version':'v001','source_sha256':hashlib.sha256(PARENT.read_bytes()).hexdigest(),'method':'Original sibling geometry adapts the real parent hollow-cavity, rack and stainless/glass design; adds two compartments, mounting flange interfaces and articulated doors. Not a scaled or linked duplicate.','changed_interfaces':'56-inch double column or 47-inch full/compact column; 28.5-inch body behind 30-inch flange; compact compartment is a new original concept.'},
          'dependencies':[],'source':{'kind':'original','generator':'tools/library/build_wall_oven_options.py','software':bpy.app.version_string,'command':'Blender --background --python tools/library/build_wall_oven_options.py'},
          'license':'CC-BY-4.0','rights':'Original geometry; attribution Homes project contributors. Derived from the project original 30-inch built-in oven.',
          'files':{'blender':slug+'.blend','preview':'preview.png','open_preview':'preview-open.png','validation':'validation.json'},
          'limitations':['No tested thermal, electromagnetic, electrical or structural performance.','Compact speed-oven window grid is illustrative geometry, not certified microwave shielding.','Isolated asset checks do not establish usable host installation.']}
        (folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
        (folder/'README.md').write_text('# '+name+'\n\n![Closed native preview](preview.png)\n\n![Doors open native preview](preview-open.png)\n\nOriginal concept appliance, not a commercial product specification. Read `asset.json` for body versus flange, placement and operating interfaces, and `validation.json` for measured door motion. Link the named collection at scale 1. A cabinet opening, platform, electrical services, cooling allowances and operator space are supplied by the adopting home. No host has been checked by this asset-only review.\n')
        print('PUBLISHED',slug,flush=True)

def studio(c,folder,isopen=False):
    lo,hi=bounds(c);h=hi[2];g.collection('Preview studio');M=g.material('Warm neutral studio',(.25,.265,.28),.82)
    box('Studio floor',(0,0,-.20),(200,200,.05),M)
    box('Studio support pedestal',(0,0,-.084),(.720,.570,.180),M)
    target=(0,-.08,h*.50);loc=(h*.70,-h*2.1,h*1.12)
    cam=g.camera('Native appliance studio',[v/g.F for v in loc],[v/g.F for v in target],52);bpy.context.scene.camera=cam
    for name,loc,power,color in [('Key',(h,-h,h*2),500,(1,.94,.87)),('Fill',(-h,-h,h),350,(.87,.94,1)),('Rim',(0,h,h*2),500,(1,1,1))]:
        g.area(name,[v/g.F for v in loc],[v/g.F for v in target],power,h*1.5/g.F,color)
    s=bpy.context.scene;s.world=bpy.data.worlds.new('Studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=48;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4
    s.render.resolution_x=600;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX'
    for opened in [False,True]:
        for o in c.objects:
            if o.get('role')=='oven_door_hinge':o.rotation_euler.x=math.pi/2 if opened else 0
        if opened:
            a,b=bounds(c);aim=Vector([(a[i]+b[i])/2 for i in range(3)]);cam.location=Vector((h*.80,aim.y-h*2.55,h*1.20));cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
        s.render.filepath=str(folder/('preview-open.png' if opened else 'preview.png'));bpy.ops.render.render(write_still=True)

def verify(render=False):
    for slug in ASSETS:
        folder=ROOT/'library/appliances'/slug/'v001';path=folder/(slug+'.blend');bpy.ops.wm.open_mainfile(filepath=str(path));meta=json.loads((folder/'asset.json').read_text())
        c=bpy.data.collections[ASSETS[slug][0]];hinges=[o for o in c.objects if o.get('role')=='oven_door_hinge'];assert len(hinges)==2
        lo,hi=bounds(c);assert abs(lo[2])<1e-5;assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3));assert not bpy.data.libraries
        bodypts=[o.matrix_world@Vector(v) for o in c.all_objects if 'insulated' in o.name for v in o.bound_box]
        bodylo=[min(p[i] for p in bodypts) for i in range(3)];bodyhi=[max(p[i] for p in bodypts) for i in range(3)]
        bodydim=[bodyhi[i]-bodylo[i] for i in range(3)]
        assert all(abs(bodydim[i]-meta['installation']['body_dimensions_m'][i])<1e-5 for i in range(3))
        # Rays through each viewing aperture must reach rear cavity rather than a solid cabinet.
        deps=bpy.context.evaluated_depsgraph_get();rays=[]
        for hinge in hinges:
            center=hinge['cavity_z_m'];hits=[]
            origin=Vector((.19,-.27,center+.023));direction=Vector((0,1,0))
            hit,loc,normal,idx,obj,matrix=bpy.context.scene.ray_cast(deps,origin,direction,distance=1)
            assert hit and loc.y>.20,(slug,obj.name if obj else None,loc[:]);rays.append({'origin_m':list(origin),'first_hit':obj.name,'hit_y_m':loc.y})
        all_bounds=[]
        for angle in range(0,91,5):
            for hinge in hinges:hinge.rotation_euler.x=math.radians(angle)
            a,b=bounds(c);all_bounds.append((a,b))
        swept={'min':[min(v[0][i] for v in all_bounds) for i in range(3)],'max':[max(v[1][i] for v in all_bounds) for i in range(3)]}
        a,b=bounds(c)
        for hinge in hinges:hinge.rotation_euler.x=0
        # Verify portability by linking the same collection in a fresh empty scene too.
        bpy.ops.wm.read_factory_settings(use_empty=True)
        with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=[ASSETS[slug][0]]
        bpy.context.scene.collection.children.link(dst.collections[0]);la,lb=bounds(dst.collections[0]);assert all(abs(lb[i]-la[i]-meta['dimensions_m'][i])<1e-5 for i in range(3))
        bpy.ops.wm.open_mainfile(filepath=str(path));c=bpy.data.collections[ASSETS[slug][0]]
        receipt={'fresh_native_reopen':True,'fresh_link':True,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions_m':meta['dimensions_m'],'origin_bottom_z_zero':True,'front_direction':'-Y','objects':len(c.all_objects),'dependencies':'No external files; all materials original and embedded','hollow_cavity_rays':rays,'measured_body_dimensions_m':bodydim,'door_hinges':2,'door_open_degrees':90,'door_open_bounds_m':{'min':a,'max':b},'sampled_swept_bounds_m':swept,'swept_sample_step_degrees':5,'required_front_projection_from_cabinet_m':round(-.29845-swept['min'][1],6),'operator_reservation_beyond_swing_m':.60,'host_installation_checked':False,'visual_review':'pending','preview_cpu_samples':48 if render else None}
        if render:studio(c,folder)
        (folder/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print('VERIFIED',slug,receipt['dimensions_m'],receipt['required_front_projection_from_cabinet_m'],flush=True)

if __name__=='__main__':
    verify('--render' in sys.argv) if '--verify' in sys.argv else publish()
