"""Original aged-brass kitchen hardware, fixtures and physical-scale materials.

blender -b --factory-startup --python tools/library/build_brass_kitchen_details.py
blender -b --factory-startup --python tools/library/build_brass_kitchen_details.py -- --verify --render
"""
from pathlib import Path
import bpy, math, json, sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'tools/library'))
from common import geometry as g
from common.hardware_assets import _build as hardware_build, _disk, _rod
from publish_modern_block import box, bounds, linked_mat
GEN='tools/library/build_brass_kitchen_details.py'
CATALOG={'aged-brass':'materials','cream-veined-stone':'materials','bar-pull-aged-brass-6in':'hardware','round-knob-aged-brass-1p125in':'hardware','appliance-pull-aged-brass-24in':'hardware','kitchen-sink-bridge-faucet-brass-650':'fixtures','lighting-brass-picture-light-24in':'fixtures','lighting-brass-shaded-sconce':'fixtures','lighting-brass-double-shade-pendant':'fixtures'}
MATERIAL_NAMES={'aged-brass':'Aged brass | v001','cream-veined-stone':'Cream veined stone | v001'}
def folder(slug):return ROOT/'library'/CATALOG[slug]/slug/'v001'
def cname(slug):return slug+' | shared v001'
def rod(name,a,b,r,mat):return g.rod(name,Vector(a)/g.F,Vector(b)/g.F,r/g.F,mat)
def cyl(name,pos,r,h,mat):return g.cyl(name,Vector(pos)/g.F,r/g.F,h/g.F,mat,64)
def tube(name,points,r,mat):return g.curve(name,[tuple(Vector(p)/g.F) for p in points],r/g.F,mat)
def dep(slug):return {'id':'materials/'+slug,'version':'v001','path':'../../../materials/'+slug+'/v001/'+slug+'.blend'}
def node(n,kind,label=None):
    o=n.new(kind)
    if label:o.label=label
    return o

def material(slug):
    m=bpy.data.materials.new(MATERIAL_NAMES[slug]);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');geo=node(n,'ShaderNodeNewGeometry');tex=node(n,'ShaderNodeTexNoise');l.new(geo.outputs['Position'],tex.inputs['Vector']);tex.inputs['Detail'].default_value=3
    if slug=='aged-brass':
        tex.inputs['Scale'].default_value=8
        ramp=node(n,'ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.22;ramp.color_ramp.elements[0].color=(.18,.096,.032,1);ramp.color_ramp.elements[1].position=.78;ramp.color_ramp.elements[1].color=(.53,.32,.115,1);l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color']);p.inputs['Metallic'].default_value=.88;p.inputs['Roughness'].default_value=.34;p.inputs['Anisotropic'].default_value=.10
        micro=node(n,'ShaderNodeTexNoise');l.new(geo.outputs['Position'],micro.inputs['Vector']);micro.inputs['Scale'].default_value=950
        bump=node(n,'ShaderNodeBump');bump.inputs['Distance'].default_value=.000025;bump.inputs['Strength'].default_value=.12;l.new(micro.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
        info={'base_color_linear_range':[[.18,.096,.032],[.53,.32,.115]],'roughness':.34,'metallic':.88,'physical_scale':'World meters, gentle patina variation at8cycles/m, microtexture950cycles/m. Restrained warm satin finish, not corroded or mirror-polished.'}
    else:
        # Distorted broad veins with fine branching detail. All coordinates stay in real meters.
        tex.inputs['Scale'].default_value=2.8;tex.inputs['Roughness'].default_value=.62
        distortion=node(n,'ShaderNodeVectorMath');distortion.operation='SCALE';distortion.inputs['Scale'].default_value=.85;l.new(tex.outputs['Color'],distortion.inputs[0]);add=node(n,'ShaderNodeVectorMath');add.operation='ADD';l.new(geo.outputs['Position'],add.inputs[0]);l.new(distortion.outputs['Vector'],add.inputs[1])
        vein=node(n,'ShaderNodeTexVoronoi');vein.feature='DISTANCE_TO_EDGE';vein.inputs['Scale'].default_value=1.65;l.new(add.outputs['Vector'],vein.inputs['Vector'])
        # Irregular narrow mineral boundaries; warped cellular topology avoids parallel stripes.
        ramp=node(n,'ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.002;ramp.color_ramp.elements[0].color=(.39,.31,.21,1);ramp.color_ramp.elements[1].position=.027;ramp.color_ramp.elements[1].color=(.81,.77,.65,1);ramp.color_ramp.elements.new(.009).color=(.64,.57,.43,1);ramp.color_ramp.interpolation='EASE';l.new(vein.outputs['Distance'],ramp.inputs[0]);l.new(ramp.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.27;p.inputs['Specular IOR Level'].default_value=.30
        info={'base_color_linear_range':[[.39,.31,.21],[.81,.77,.65]],'roughness':.27,'physical_scale':'World-meter coordinates, noise-warped irregular narrow mineral boundaries with quiet cream body. Host owns stone slab joints, cutouts, thickness and edge returns. No claim of a specific natural stone species or product.'}
    return m,info

def shade(name,center,zbottom,ztop,rbot,rtop,mat):
    # Thin real open shade, not a solid cone. Top and bottom apertures remain open.
    verts=[];faces=[];N=64
    for r,z in [(rbot,zbottom),(rtop,ztop),(rbot-.002,zbottom),(rtop-.002,ztop)]:
        for i in range(N):
            a=math.tau*i/N;verts.append((center[0]+r*math.cos(a),center[1]+r*math.sin(a),z))
    for i in range(N):
        j=(i+1)%N;faces.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat);o=bpy.data.objects.new(name,me);g.ACTIVE.objects.link(o)
    for p in me.polygons:p.use_smooth=True
    return o

def bulb(name,pos,power):
    emit=g.material(name+' opal glass',(.93,.86,.68),.42);p=emit.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.75,.42,1);p.inputs['Emission Strength'].default_value=1.6
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,radius=.022,location=pos);o=bpy.context.object;o.name=name+' opal bulb';o.data.materials.append(emit)
    for c in list(o.users_collection):c.objects.unlink(o)
    g.ACTIVE.objects.link(o)
    d=bpy.data.lights.new(name+' warm illumination','POINT');d.energy=power;d.color=(1,.77,.49);d.shadow_soft_size=.035;light=bpy.data.objects.new(d.name,d);g.ACTIVE.objects.link(light);light.location=pos

def build(slug):
    c=g.collection(cname(slug));c['asset_id']=CATALOG[slug]+'/'+slug;c['asset_version']='v001';brass=linked_mat('aged-brass');meta={'dependencies':[dep('aged-brass')],'placement':{'origin':'Host mounting-face center at XY0 Z0','front_direction':'-Y; Z up','allowed_scaling':'Rigid placement and rotation only; keep exact dimensions and fixing centers.'},'operating_envelope':{'state':'Static concept geometry','basis':'Original concept, no commercial product selected','host_open_state_checked':False}}
    if slug.startswith('bar-pull') or slug.startswith('round-knob'):
        kind='bar-pull' if slug.startswith('bar') else 'round-knob';hardware_build(kind,brass)
        meta['derived_from']={'id':'hardware/'+kind+'-satin-bronze','version':'v001','changes':'Preserves exact original shared geometry and mounting origin; substitutes linked aged-brass v001 finish.'}
        meta['mounting'] = 'Origin on host face, projection toward-Y. '+('152.4mm fixing centers, 163.068mm overall bar width,31.75mm projection. Original axisX; rotate localY90degrees for vertical.' if kind=='bar-pull' else '28.575mm head diameter,27.94mm projection, single fixing at face center.')
        meta['clearances']={'basis':'Concept hardware, reserve finger grip and full host door/drawer sweep. Host supplies exact drilling and concealed fasteners.','host_checked':False}
    elif slug.startswith('appliance-pull'):
        for x in [-12,12]:
            _disk('Appliance pull mounting rosette',(x,-.08,0),.48,.16,brass);_rod('Appliance pull standoff',(x,-.10,0),(x,-1.625,0),.26,brass)
        _rod('Appliance pull full-size bar',(-12.75,-1.625,0),(12.75,-1.625,0),.375,brass)
        meta['mounting']='Origin on host face, bar axisX, front-Y. 609.6mm fixing centers,647.7mm overall bar width,50.8mm projection,19.05mm grip diameter. Rotate localY90degrees for vertical. Host supplies through-bolts, door reinforcement and exact appliance clearance.'
        meta['clearances']={'basis':'Dedicated original appliance-scale pull. Do not enlarge cabinet hardware or scale this assembly. Host must check all appliance door swings and hand clearances.','host_checked':False}
    elif slug.startswith('kitchen-sink'):
        native=ROOT/'library/fixtures/kitchen-sink-mixer-650/v002/kitchen-sink-mixer-650.blend'
        with bpy.data.libraries.load(str(native),link=False) as (a,b):b.objects=[x for x in a.objects if 'mixer' not in x.lower()]
        for o in b.objects:
            if o.type=='MESH':c.objects.link(o)
        for x in [-.10,.10]:
            cyl('Bridge tap deck foot',(x,.285,.006),.026,.012,brass);rod('Bridge tap supply leg',(x,.285,.012),(x,.285,.13),.014,brass)
            cyl('Bridge tap valve collar',(x,.285,.143),.019,.026,brass);rod('Bridge tap cross handle',(x-.029,.285,.161),(x+.029,.285,.161),.005,brass)
        rod('Bridge tap crossbar',(-.10,.285,.115),(.10,.285,.115),.013,brass)
        tube('Slender bridge gooseneck',[(0,.285,.115),(0,.285,.34),(0,.17,.43),(0,-.01,.40),(0,-.04,.285)],.012,brass)
        cyl('Downward faucet aerator',(0,-.04,.282),.014,.018,brass)
        meta['derived_from']={'id':'fixtures/kitchen-sink-mixer-650','version':'v002','changes':'Original source bowl and flange geometry appended unchanged; replaces mixer and lever with original brass bridge supply legs, crossbar, valve controls and slender curved gooseneck.'}
        meta['placement']['origin']='Countertop planeZ0, bowl-centerXY0; front-Y, bridgefaucet at rear+Y'
        meta['installation']={'countertop_cutout_m':[.664,.464],'measured_outer_bowl_m':[.654,.454,.218],'below_counter_bowl_depth_m':.218,'faucet_hole_centers_m':[[-.10,.285],[.10,.285]],'concept_faucet_hole_diameter_m':.025,'mounting':'Support flange continuously; 664×464mm bowl opening with separately coordinated rear faucet bores. Exact product and fixing design unresolved.','service_requirements':['Drain/trap and hot/cold routes below bowl.','Removable front access for service; clear rear valve/hand space.'],'operating_envelope':{'basis':'Original concept geometry','reserve_front_standing_depth_m':.80,'host_open_state_checked':False,'modeled_state':'Open bowl, fixed shown faucet position'}}
    else:
        fabric=g.material('Original off-white woven shade',(.82,.78,.67),.82);p=fabric.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.025
        if 'picture' in slug:
            box('Picture light mounting plate',(0,.006,0),(.105,.012,.075),brass,.009)
            tube('Picture light curved arm',[(0,0,0),(0,-.11,.005),(0,-.18,.06)],.008,brass)
            rod('24inch narrow picture-light barrel',(-.3048,-.18,.06),(.3048,-.18,.06),.022,brass)
            emiss=g.material('Picture light warm diffuser',(.87,.79,.58),.5);p=emiss.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.78,.47,1);p.inputs['Emission Strength'].default_value=2
            box('Downward picture light diffuser',(0,-.18,.038),(.56,.020,.004),emiss,.002)
            meta['mounting']='Wall mounting face Y=0. Backplate extends+Y12mm into shallow wall recess; host supplies recess or surface mounting spacer. Light projects toward-Y;24inch barrel axisX; aperture faces downward-Z. Mount above glazing or artwork with independent support and electrical route.'
            meta['clearances']={'projection_m':.202,'service_basis':'Reach diffuser/barrel screws from below; no glazing contact. Fixture output is illustrative, not a photometric specification.','host_checked':False}
        elif 'sconce' in slug:
            o=cyl('Sconce wall rose',(0,.006,0),.062,.012,brass);o.rotation_euler.x=math.pi/2
            tube('Sconce raised arm',[(0,0,-.015),(0,-.21,-.015),(0,-.23,.15)],.009,brass)
            cyl('Sconce lamp socket',(0,-.23,.15),.020,.06,brass);shade('Open tapered fabric sconce shade',(0,-.23),.13,.34,.125,.068,fabric)
            for x in [-.056,.056]:rod('Shade frame spoke',(0,-.23,.31),(x,-.23,.31),.0018,brass)
            bulb('Sconce',(0,-.23,.215),5)
            meta['mounting']='Wall mounting face Y=0 at rosecenterZ0; backplate +Y12mm requires recess or host spacer. Shade centered Y-.23, opens downward; safe electrical connection and support supplied by host.'
            meta['clearances']={'shade_front_projection_m':.355,'service_basis':'Allow bulb removal below open shade and keep shade clear of open doors and heat sources.','host_checked':False}
        else:
            cyl('Pendant ceiling canopy',(0,0,-.012),.08,.024,brass);rod('Pendant central drop',(0,0,-.024),(0,0,-.96),.011,brass)
            rod('Two arm pendant horizontal bar',(-.40,0,-.96),(.40,0,-.96),.010,brass)
            for x in [-.40,.40]:
                rod('Pendant lamp stem',(x,0,-.96),(x,0,-1.14),.008,brass);cyl('Pendant lamp socket',(x,0,-1.12),.023,.07,brass)
                shade('Open tapered fabric pendant shade',(x,0),-1.35,-1.05,.22,.115,fabric)
                for dx in [-.105,.105]:rod('Pendant shade support spoke',(x,0,-1.07),(x+dx,0,-1.07),.002,brass)
                bulb('Pendant',(x,0,-1.20),8)
            meta['placement']['origin']='Ceiling mounting planeZ0 at XYcenter; fixture hangs belowZ0; two-shade axisX'
            meta['mounting']='Ceiling canopy topZ0, hardwired fixed stem. Actual drop1350mm. Host supplies support, ceiling opening, wiring and suitable task/ambient illumination.'
            meta['clearances']={'overall_drop_m':1.35,'shade_diameter_m':.44,'shade_center_spacing_m':.80,'service_basis':'Allow bulb replacement below each open shade, coordinate sightlines/headroom and countertop clearance in host.','host_checked':False}
    return c,meta

def publish():
    for slug,cat in CATALOG.items():
        if '--asset' in sys.argv and slug!=sys.argv[sys.argv.index('--asset')+1]:continue
        f=folder(slug);native=f/(slug+'.blend')
        if native.exists():print('PRESERVE',slug,flush=True);continue
        bpy.ops.wm.read_factory_settings(use_empty=True);f.mkdir(parents=True,exist_ok=True)
        base={'schema_version':1,'id':cat+'/'+slug,'version':'v001','units':'meters','license':'CC-BY-4.0','rights':'Original Homes project contributor geometry and procedural appearance; attribution Homes project contributors.','source':{'kind':'original','generator':GEN,'command':'blender -b --factory-startup --python '+GEN+' -- --asset '+slug},'software':{'blender':bpy.app.version_string},'files':{'blender':native.name,'preview':'preview.png','validation':'validation.json'},'limitations':'Original concept appearance and geometry, not a commercial product, certified electrical/plumbing assembly, code approval or construction specification.'}
        if cat=='materials':
            mat,info=material(slug);bpy.data.libraries.write(str(native),{mat},fake_user=True,path_remap='RELATIVE_ALL');base.update(name=MATERIAL_NAMES[slug],blender={'material':MATERIAL_NAMES[slug]},dependencies=[],placement='Material-only asset, world-coordinate physical-meter shader. Host owns geometry.',texture_scale=info)
        else:
            c,meta=build(slug);lo,hi=bounds(c);bpy.data.libraries.write(str(native),{c},fake_user=True,path_remap='RELATIVE_ALL');base.update(meta);base.update(name=cname(slug),dimensions_m=[hi[i]-lo[i] for i in range(3)],bounds_m={'min':lo,'max':hi},blender={'collection':cname(slug)})
        (f/'asset.json').write_text(json.dumps(base,indent=2)+'\n');print('PUBLISHED',slug,flush=True)

def preview(slug,c,lo,hi):
    s=bpy.context.scene;g.collection('Preview only');span=max(hi[i]-lo[i] for i in range(3));center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);mat=g.material('Neutral preview support',(.31,.32,.30),.92)
    cat=CATALOG[slug]
    if cat=='hardware':
        box('Mounting backing',(0,.025,0),(span*1.40,.05,max(span*.8,.06)),mat,.002);cam=center+Vector((span*.8,-span*3.3,span*1.4));target=center
    else:
        box('Neutral ground',(0,0,lo[2]-.055),(max(span,1)*200,max(span,1)*200,.08),mat)
        target=center;cam=center+Vector((span*.90,-span*1.6,span*.8))
        if 'sink' in slug:cam=center+Vector((span*.70,-span*1.4,span*1.5))
    s.camera=g.camera('Native component preview',cam/g.F,target/g.F,48);s.camera.data.clip_start=.001
    g.area('Large soft neutral key',(center+Vector((-span,-span,span*2)))/g.F,target/g.F,span*span*350,span*1.3/g.F,(1,.97,.92));g.area('Fill',(center+Vector((span,span,span)))/g.F,target/g.F,span*span*90,span/g.F,(.9,.95,1))
    s.world=bpy.data.worlds.new('Neutral preview world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.40,.43,.47,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=760;s.render.resolution_y=650;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(folder(slug)/'preview.png');s.view_settings.view_transform='AgX';s.view_settings.exposure=0;bpy.ops.render.render(write_still=True)

def verify(render):
    for slug,cat in CATALOG.items():
        if '--asset' in sys.argv and slug!=sys.argv[sys.argv.index('--asset')+1]:continue
        f=folder(slug);native=f/(slug+'.blend');meta=json.loads((f/'asset.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(native));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        if cat=='materials':
            with bpy.data.libraries.load(str(native),link=True) as (a,b):b.materials=[MATERIAL_NAMES[slug]]
            c=g.collection('Material preview sample');m=b.materials[0]
            if slug=='aged-brass':
                cyl('Brass disc',(0,0,.055),.12,.11,m);box('Brass plate',(.24,0,.014),(.17,.27,.028),m,.004)
            else:box('Cream stone sample',(0,0,.03),(1.8,1.2,.06),m,.006)
        else:
            with bpy.data.libraries.load(str(native),link=True) as (a,b):b.collections=[cname(slug)]
            c=b.collections[0];bpy.context.scene.collection.children.link(c)
        lo,hi=bounds(c)
        if cat!='materials':assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3))
        assert all(Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
        if 'sink' in slug:
            assert abs(lo[2]+.218)<1e-5;assert not any('mixer' in o.name.lower() for o in c.all_objects)
            assert sum('Sink flange' in o.name for o in c.all_objects)==4
        if render:preview(slug,c,lo,hi)
        receipt={'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'objects':len(c.all_objects),'actual_bounds_m':{'min':lo,'max':hi},'dimensions_match_manifest':True if cat!='materials' else None,'dimension_check_scope':'Measured collection bounds compared against manifest' if cat!='materials' else 'Not applicable: material-only asset; rendered swatch dimensions are illustrative and are not a product-size contract','preview_rendered':(f/'preview.png').exists(),'preview_settings':{'renderer':'Cycles CPU','threads':4,'samples':24,'resolution_px':[760,650]},'host_integration_checked':False}
        (f/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print('VERIFIED',slug,flush=True)
if __name__=='__main__':
    if '--verify' in sys.argv:verify('--render' in sys.argv)
    else:publish()
