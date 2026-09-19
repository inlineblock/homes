"""Publish coordinated original brick, black metal, oak and slim bronze glazing.

All geometry and UVs are meters. Existing adopted versions remain untouched.
Commands: -- publish | previews | verify. Native previews use Cycles CPU.
"""
from pathlib import Path
import json, math, sys
import bpy
from mathutils import Vector, Euler

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from library.build_lindon_assets import cube, material, apply_brick_uv
from common.timber_materials import timber, grain_uv

BRICK = 'Iron red brick | running bond | v002'
MODULE = 'Iron red brick | 225 x 75 mm module | v002'
ROOF = 'Charcoal roof | warm matte | v002'
OAK = 'Smoked oak | warm umber | v001'
PLASTER = 'Warm limestone plaster | v001'
PANEL = 'Charcoal facade panel | v001'
WINDOW = 'Slim bronze window | 2400 x 2400 mm | v002'
SPECS = {
    'brick': ('materials', 'warm-red-brick', 'v002', BRICK),
    'roof': ('materials', 'charcoal-standing-seam', 'v002', ROOF),
    'oak': ('materials', 'smoked-oak', 'v001', OAK),
    'plaster': ('materials', 'warm-limestone-plaster', 'v001', PLASTER),
    'panel': ('materials', 'charcoal-facade-panel', 'v001', PANEL),
    'window': ('openings', 'slim-dark-window', 'v002', WINDOW),
}

def folder(key):
    category, slug, version, _ = SPECS[key]
    return ROOT / 'library' / category / slug / version

def native(key):
    return folder(key) / (SPECS[key][1] + '.blend')

def save(key, blocks):
    path = native(key)
    if path.exists():
        raise FileExistsError(f'Immutable published asset exists: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.data.libraries.write(str(path), set(blocks), path_remap='RELATIVE', fake_user=True, compress=True)

def noise(nodes, links, position, scale, detail=3):
    n = nodes.new('ShaderNodeTexNoise')
    n.inputs['Scale'].default_value = scale
    n.inputs['Detail'].default_value = detail
    links.new(position, n.inputs['Vector'])
    return n

def brick():
    deep = SPECS['brick'][2] == 'v003'
    first = (.185,.052,.045,1) if deep else (.245,.071,.052,1)
    second = (.105,.029,.027,1) if deep else (.135,.037,.029,1)
    joint_color = (.19,.165,.145,1) if deep else (.225,.195,.163,1)
    mid = (.145,.0405,.036) if deep else (.18,.055,.040)
    m = material(BRICK, mid, .82)
    n, l = m.node_tree.nodes, m.node_tree.links
    p = n.get('Principled BSDF'); p.inputs['Specular IOR Level'].default_value = .26
    uv = n.new('ShaderNodeUVMap'); uv.uv_map = 'Brick meters'
    b = n.new('ShaderNodeTexBrick'); b.offset = .5; b.offset_frequency = 2
    for name, value in {'Scale':1., 'Mortar Size':.004, 'Mortar Smooth':.001, 'Bias':0., 'Brick Width':.225, 'Row Height':.075}.items():
        b.inputs[name].default_value = value
    b.inputs['Color1'].default_value = first
    b.inputs['Color2'].default_value = second
    b.inputs['Mortar'].default_value = joint_color
    l.new(uv.outputs[0], b.inputs['Vector'])
    geo = n.new('ShaderNodeNewGeometry')
    broad = noise(n,l,geo.outputs['Position'],38,3)
    fine = noise(n,l,geo.outputs['Position'],620,2)
    color = n.new('ShaderNodeMixRGB'); color.blend_type = 'MULTIPLY'; color.inputs[0].default_value=.12
    l.new(b.outputs['Color'],color.inputs[1]); l.new(broad.outputs['Fac'],color.inputs[2]);l.new(color.outputs[0],p.inputs['Base Color'])
    invert=n.new('ShaderNodeMath');invert.operation='SUBTRACT';invert.inputs[0].default_value=1;l.new(b.outputs['Fac'],invert.inputs[1])
    joint=n.new('ShaderNodeBump');joint.inputs['Strength'].default_value=.58;joint.inputs['Distance'].default_value=.003
    l.new(invert.outputs[0],joint.inputs['Height'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.24;bump.inputs['Distance'].default_value=.00045
    l.new(fine.outputs['Fac'],bump.inputs['Height']);l.new(joint.outputs['Normal'],bump.inputs['Normal']);l.new(bump.outputs['Normal'],p.inputs['Normal'])
    rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.76;rough.inputs['To Max'].default_value=.9
    l.new(fine.outputs['Fac'],rough.inputs['Value']);l.new(rough.outputs[0],p.inputs['Roughness'])
    col=bpy.data.collections.new(MODULE)
    clay=material('Iron red clay unit | '+SPECS['brick'][2],mid,.82)
    mortar=material('Warm gray recessed mortar | '+SPECS['brick'][2],joint_color[:3],.9)
    cube('Clay unit | 217 x 67 x 102.5 mm',(0,0,.0375),(.217,.1025,.067),clay,col,.0013)
    cube('Eight millimeter mortar pitch | 3 mm recessed',(0,.0015,.0375),(.225,.0995,.075),mortar,col,.0004)
    save('brick',[m,col])

def mineral(name,dark,light,scale,rough,metal=0,bump=.00006):
    m=material(name,dark,rough,metal);n,l=m.node_tree.nodes,m.node_tree.links;p=n.get('Principled BSDF')
    p.inputs['Specular IOR Level'].default_value=.28
    geo=n.new('ShaderNodeNewGeometry');t=noise(n,l,geo.outputs['Position'],scale,2)
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*dark,1);ramp.color_ramp.elements[1].color=(*light,1)
    l.new(t.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
    b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.15;b.inputs['Distance'].default_value=bump
    l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
    return m

def window():
    col=bpy.data.collections.new(WINDOW)
    frame=material('Blackened bronze window frame | v002',(.027,.023,.019),.46,.22)
    frame.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.30
    seal=material('Neutral glazing gasket | v002',(.010,.010,.009),.75)
    glass=material('Neutral double glazing | v002',(1,1,1),.018)
    p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.46
    def bar(name,x,z,w,h,y=.065,d=.13,mat=frame):
        return cube(name,(x,y,z),(w,d,h),mat,col,.0008)
    for x in [-1.18,1.18]:bar('40 mm outer jamb',x,1.2,.04,2.4)
    for z in [.02,2.38]:bar('40 mm outer head / sill',0,z,2.32,.04)
    for x in [-.60,.60]:bar('40 mm vertical mullion',x,1.2,.04,2.32)
    for i,(a,b) in enumerate([(-1.16,-.62),(-.58,.58),(.62,1.16)]):
        low,high=.04,2.36
        if i!=1:
            t,inset=.021,.005
            for x in [a+inset+t/2,b-inset-t/2]:bar('21 mm casement sash stile',x,1.2,t,high-low-2*inset,.072,.094)
            for z in [low+inset+t/2,high-inset-t/2]:bar('21 mm casement sash rail',(a+b)/2,z,b-a-2*inset-2*t,t,.072,.094)
            a+=inset+t;b-=inset+t;low+=inset+t;high-=inset+t
        for x in [a+.0025,b-.0025]:bar('Five millimeter gasket',x,(high+low)/2,.005,high-low,.062,.009,seal)
        for z in [low+.0025,high-.0025]:bar('Five millimeter gasket',(a+b)/2,z,b-a-.01,.005,.062,.009,seal)
        for y in [.077,.098]:
            cube(('Fixed center' if i==1 else 'Closed side casement')+' | 4 mm glass',((a+b)/2,y,(high+low)/2),(b-a-.01,.004,high-low-.01),glass,col,.00035)
    bar('Slim sill drip',0,.013,2.4,.014,.058,.15)
    hp=ROOT/'library/hardware/bar-pull-matte-black/v001/bar-pull-matte-black.blend'
    with bpy.data.libraries.load(str(hp),link=True,relative=True) as (src,dst):dst.collections=[src.collections[0]]
    for x in [-.65,.65]:
        obj=bpy.data.objects.new('Shared concept interior casement grip',None);obj.instance_type='COLLECTION';obj.instance_collection=dst.collections[0]
        obj.location=(x,.133,1.10);obj.rotation_euler=Euler((0,math.pi/2,math.pi));col.objects.link(obj)
    save('window',[col])

def publish(keys=None):
    keys=set(keys or SPECS)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if 'brick' in keys and not native('brick').exists():brick()
    if 'roof' in keys and not native('roof').exists():save('roof',[mineral(ROOF,(.017,.016,.015),(.029,.027,.025),120,.58,.15)])
    if 'oak' in keys and not native('oak').exists():save('oak',[timber(OAK,(.022,.014,.009),(.061,.039,.023),(.13,.091,.054))])
    if 'plaster' in keys and not native('plaster').exists():save('plaster',[mineral(PLASTER,(.58,.545,.482),(.68,.645,.580),180,.87,bump=.00018)])
    if 'panel' in keys and not native('panel').exists():save('panel',[mineral(PANEL,(.018,.019,.018),(.027,.028,.026),180,.67,.08)])
    if 'window' in keys and not native('window').exists():window()
    for key,(category,slug,version,name) in SPECS.items():
        if key not in keys:continue
        meta={'schema_version':1,'id':category+'/'+slug,'version':version,'name':name,'units':'meters','license':'CC-BY-4.0','rights':'Original Homes project contributors asset; attribution Homes project contributors','source':{'kind':'original','generator':'tools/library/build_lindon_palette.py','command':'Blender --background --python tools/library/build_lindon_palette.py -- publish'},'files':{'blender':native(key).name,'preview':'preview.png'},'dependencies':[],'software':{'blender':bpy.app.version_string},'host_integration':{'checked':False,'required':'Inspect adopted sunny/shaded facade, opening geometry and clearances; material preview is not installation verification.'},'preview_settings':{'renderer':'Cycles CPU','samples':48,'color_management':'AgX Medium High Contrast','exposure':0,'illumination':'Neutral area lights and neutral gray environment'},'limitations':'Original concept appearance, not a manufacturer product or weather/structural certification.'}
        if key in ('brick','roof','window'):meta['derived_from']={'id':category+'/'+slug,'version':'v002' if key=='brick' and version=='v003' else 'v001'}
        if key=='oak':meta['derived_from']={'id':'materials/warm-vertical-cedar','version':'v003','basis':'Shared original meter-grain algorithm and revised oak/umber palette'}
        if key=='window':
            meta.update({'dimensions_m':[2.4,.18175,2.4],'nominal_opening_m':[2.4,2.4],'frame_sightline_m':.04,'blender':{'collection':WINDOW},'placement':'Bottom-center origin, front -Y, Z-up. Main frame Y0..0.13; sill reaches -0.017; concept grips reach Y0.16475.','variation':'Keep scale 1 for nominal 40 mm frames. Host resizing changes sightlines and remains an explicitly approximate study; publish dimensional variants for resolved openings.','operating_clearance':{'state':'Closed','type':'Fixed center, two casement-style side panels','assumed_outward_angle_degrees':90,'assumed_outward_sweep_m':.54,'basis':'Generic concept side-opening width, no engineered hinges','host_checked':False},'service_clearance':'Host resolves shims, drainage, flashing, sill slope, safe glazing, operating/cleaning access and actual product selection.','dependencies':[{'id':'hardware/bar-pull-matte-black','version':'v001','path':'../../../hardware/bar-pull-matte-black/v001/','blender':'bar-pull-matte-black.blend'}],'changes_from_parent':'40 mm main sightlines, 21 mm sash, neutral untinted 4 mm glazing with IOR 1.46 and warm dark bronze frames; original concept grips retained.'})
        elif key=='brick':
            meta.update({'dimensions_m':[.225,.1025,.075],'unit_dimensions_m':[.217,.1025,.067],'joint_m':.008,'mortar_recess_m':.003,'blender':{'material':BRICK,'collection':MODULE},'placement':'Use Brick meters UV; call library.build_lindon_assets.apply_brick_uv(obj) after final mesh and world transforms. Module bottom-center, front -Y, Z-up.','texture_scale':{'uv_map':'Brick meters','horizontal_pitch_m':.225,'course_pitch_m':.075,'bump_recess_m':.003,'micropore_scale_per_m':620},'variation':'Fixed physical course scale, half-running bond; subtle internal per-unit red variation. No arbitrary object scaling of the physical module.','changes_from_parent':'Muted iron-red unit colors, 8 mm quieter warm-gray joint, restrained 3 mm recess and fine microporosity; retained conventional brick proportion.'})
            if version=='v003':
                meta['changes_from_parent']='Deeper, less orange iron-red body colors and slightly darker warm-gray mortar after neutral host sun/shade review. v002 remains an available lighter russet option. Same physical bond, joints and bump.'
                meta['linear_rgb']={'clay_light':[.185,.052,.045],'clay_dark':[.105,.029,.027],'mortar':[.19,.165,.145]}
                meta['source']['command']='Blender --factory-startup --background --python tools/library/build_lindon_palette.py -- deep-publish'
        else:
            meta['blender']={'material':name}
            meta['placement']='Material-only asset; no placement or operating envelope. Host supplies the actual assembly geometry.'
            if key=='oak':meta['texture_scale']={'uv_map':'Timber meters','across_grain_m':.025,'fiber_width_m':.003,'mapping':'Apply common.timber_materials.grain_uv after transforms; longest local mesh axis defines grain.'};meta['variation']='Seeded per-board phase and .72–1.24 tone variation. Inspect both horizontal and vertical boards.'
            else:meta['texture_scale']={'coordinates':'World position in meters','noise_scale_per_m':120 if key=='roof' else 180};meta['variation']='Fixed subtle physical texture; host supplies seams, joints and flashing geometry.'
            if key=='roof':meta['metallic']=.15;meta['roughness']=.58;meta['changes_from_parent']='Much darker warm charcoal coated metal, reduced color variation and matte response; host seam layout is independent of material.'
        folder(key).mkdir(parents=True,exist_ok=True)
        (folder(key)/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
        (folder(key)/'README.md').write_text('# '+name+'\n\n![Native preview](preview.png)\n\n'+meta['placement']+'\n\n'+meta.get('variation','')+'\n\n'+meta['limitations']+' Host integration is reviewed separately.\n\nOriginal by Homes project contributors, CC BY 4.0. Regenerate and verify with `tools/library/build_lindon_palette.py` (MIT). Existing adopted parent versions are immutable. Read `asset.json` for exact pinned dependencies, dimensions and operating assumptions.\n')
        (folder(key)/'AGENTS.md').write_text('# '+name+'\n\n- Preserve this adopted version; publish the next version for changes.\n- Read asset.json and parent library guidance before placement. Use the named linked native material or collection.\n- Review actual neutral preview and sunny/shaded host views; do not correct palette faults with excessive exposure.\n- Keep physical texture scale and frame sightlines. A source preview does not establish host fit or performance.\n')

def load(key):
    with bpy.data.libraries.load(str(native(key)),link=True,relative=True) as (src,dst):
        if key=='window':dst.collections=[WINDOW]
        else:dst.materials=[SPECS[key][3]]
    return dst.collections[0] if key=='window' else dst.materials[0]

def inst(col,name,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=col;bpy.context.scene.collection.objects.link(o);o.location=loc;return o

def setup_preview():
    bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=48;s.cycles.use_denoising=True
    s.render.resolution_x=1100;s.render.resolution_y=950;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
    s.world=bpy.data.worlds.new('Neutral palette review');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.6,.6,.6,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.32
    return s

def previews(keys=None):
    for key in SPECS:
        if keys and key not in keys:continue
        s=setup_preview();c=s.collection;m=load(key)
        floor_mat=material('Neutral review floor',(.34,.33,.31),.85);cube('Floor',(0,0,-.07),(200,200,.12),floor_mat,c)
        target=(0,0,1.15);eye=(3.7,-6.7,3.1)
        if key=='window':
            inst(m,'Actual linked window')
            wall=load('plaster')
            for x in [-1.43,1.43]:cube('Plaster wall jamb',(x,.13,1.2),(.46,.4,2.9),wall,c,.004)
            for z in [-.13,2.55]:cube('Plaster wall head / sill',(0,.13,z),(2.4,.4,.3),wall,c,.004)
            back=material('Quiet interior wall',(.38,.355,.32),.87);cube('Backdrop',(0,3.2,1.2),(4,.1,3),back,c)
            cube('Interior shelf',(0,1.9,.74),(2.1,.6,.05),load('oak'),c,.01)
        elif key=='oak':
            for i in range(11):
                ob=cube('Individually seeded vertical oak board',((i-5)*.205,0,1.25),(.198,.15,2.5),m,c,.002);grain_uv(ob)
            ob=cube('Horizontal oak sample',(0,-.14,.28),(2.5,.18,.26),m,c,.004);grain_uv(ob)
        elif key=='roof':
            ob=cube('Coated roof plane',(0,0,1.2),(2.8,.075,2.4),m,c,.002)
            for i in range(7):cube('Raised seam',((i-3)*.42,-.052,1.2),(.014,.026,2.4),m,c,.001)
        elif key=='panel':
            for x in [-.61,.61]:cube('Matte panel with fine joint',(x,0,1.2),(1.216,.1,2.4),m,c,.002)
        else:
            ob=cube('Actual material sample',(0,.12,1.2),(2.7,.24,2.4),m,c,.003)
            if key=='brick':apply_brick_uv(ob)
        for name,loc,energy,size in [('Neutral broad light',(-3,-4,5),420,4),('Soft grazing light',(3,-2,4),170,2.5)]:
            d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;ob=bpy.data.objects.new(name,d);c.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
        cam=bpy.data.cameras.new('Native palette inspection');ob=bpy.data.objects.new(cam.name,cam);c.objects.link(ob);ob.location=eye;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();cam.lens=55;s.camera=ob
        s.render.filepath=str(folder(key)/'preview.png');bpy.ops.render.render(write_still=True);print('PALETTE_PREVIEW',key,flush=True)

def verify(keys=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats={key:load(key) for key in SPECS if key!='window'};col=load('window');inst(col,'Window bounds check')
    bpy.context.view_layer.update();points=[]
    for item in bpy.context.evaluated_depsgraph_get().object_instances:
        if item.is_instance and item.object.type=='MESH':points.extend(item.matrix_world@Vector(v) for v in item.object.bound_box)
    bounds={'min':[min(v[i] for v in points) for i in range(3)],'max':[max(v[i] for v in points) for i in range(3)]}
    sizes=[bounds['max'][i]-bounds['min'][i] for i in range(3)]
    assert abs(sizes[0]-2.4)<1e-5 and abs(sizes[2]-2.4)<1e-5,sizes
    jambs=[o for o in col.objects if '40 mm outer jamb' in o.name]
    assert len(jambs)==2 and all(abs(o.dimensions.x-.04)<1e-5 for o in jambs)
    missing=[];dependencies=[]
    for lib in bpy.data.libraries:
        # An unsaved inspection scene resolves linked paths to absolute paths.
        # Check portability in the saved native library below, not this host.
        absolute=Path(bpy.path.abspath(lib.filepath,library=lib.parent)).resolve()
        assert absolute.is_relative_to(ROOT/'library'),absolute
        if not absolute.exists():missing.append(str(absolute))
        dependencies.append(str(absolute.relative_to(ROOT)))
    assert not missing,missing
    sample=cube('Brick physical UV test',(0,0,0),(2.25,.24,1.5),mats['brick'],bpy.context.scene.collection)
    sample.rotation_euler.z=math.pi/4;sample.scale=(1.15,.9,1.1);uv=apply_brick_uv(sample)
    errors=[]
    for face in sample.data.polygons:
        ids=list(face.loop_indices)
        for a,b in zip(ids,ids[1:]+ids[:1]):
            wa=sample.matrix_world@sample.data.vertices[sample.data.loops[a].vertex_index].co;wb=sample.matrix_world@sample.data.vertices[sample.data.loops[b].vertex_index].co
            errors.append(abs((wa-wb).length-(uv.data[a].uv-uv.data[b].uv).length))
    assert max(errors)<1e-5
    bpy.ops.wm.open_mainfile(filepath=str(native('window')))
    stored_dependencies=[]
    for lib in bpy.data.libraries:
        assert lib.filepath.startswith('//'), lib.filepath
        resolved=Path(bpy.path.abspath(lib.filepath)).resolve()
        assert resolved.exists() and resolved.is_relative_to(ROOT/'library'),resolved
        stored_dependencies.append(lib.filepath)
    if not keys or 'window' in keys:
        meta_path=folder('window')/'asset.json';meta=json.loads(meta_path.read_text());meta['dimensions_m']=sizes;meta['bounds_m']=bounds;meta_path.write_text(json.dumps(meta,indent=2)+'\n')
    receipt={'verification_scope':'Coordinated palette batch. Window metrics describe the separate window asset; dependencies lists files checked in the batch. Each asset manifest controls its own adoption dependencies.','native_linked_in_fresh_process':True,'blender':bpy.app.version_string,'window_bounds_m':bounds,'window_dimensions_m':sizes,'main_sightline_m':.04,'brick_rotated_nonuniform_transform_uv_error_m':max(errors),'missing_dependencies':missing,'dependencies':dependencies,'window_saved_relative_dependencies':stored_dependencies,'host_integration_checked':False,'visual_preview_review':'Pending actual PNG inspection'}
    for key in SPECS:
        if keys and key not in keys:continue
        path=folder(key)/'verification.json'
        row=dict(receipt)
        if path.exists():
            previous=json.loads(path.read_text())
            row['visual_preview_review']=previous.get('visual_preview_review',row['visual_preview_review'])
        path.write_text(json.dumps(row,indent=2)+'\n')
    print('PALETTE_FRESH_LINK_VERIFIED',json.dumps(receipt),flush=True)

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['publish']
    command=args[0]
    keys=None
    if command.startswith('deep-'):
        BRICK='Deep iron red brick | running bond | v003'
        MODULE='Deep iron red brick | 225 x 75 mm module | v003'
        SPECS['brick']=('materials','warm-red-brick','v003',BRICK)
        keys={'brick'};command=command.removeprefix('deep-')
    {'publish':publish,'previews':previews,'verify':verify}[command](keys)
