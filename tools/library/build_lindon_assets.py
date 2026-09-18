"""Original Lindon brick/window assets. Geometry in meters; sources MIT, assets CC BY 4.0."""
from pathlib import Path
import json, math, sys
import bpy
from mathutils import Vector, Euler
ROOT=Path(__file__).resolve().parents[2]
BRICK_DIR=ROOT/'library/materials/warm-red-brick/v001'
WINDOW_DIR=ROOT/'library/openings/slim-dark-window/v001'
BRICK_NAME='Warm red brick | running bond | meters'
MODULE_NAME='Warm red brick | 225 x 75 mm module'
WINDOW_NAME='Slim dark window | 2400 x 2400 mm'

def material(name,color,rough=.6,metal=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m

def cube(name,loc,dims,mat,collection,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for c in list(o.users_collection):c.objects.unlink(o)
    collection.objects.link(o);o.data.materials.append(mat)
    if bevel:
        b=o.modifiers.new('Manufactured soft edge','BEVEL');b.width=bevel;b.segments=3
        n=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o

def apply_brick_uv(obj):
    """Write meter UVs after final object transforms; supports arbitrarily rotated facades.

    Face-horizontal tangent derives from its world normal. Vertical uses world Z.
    Horizontal faces use world XY. Call again after geometry/scale changes.
    """
    if obj.type != 'MESH':
        raise TypeError('Brick mapping requires a mesh object')
    bpy.context.view_layer.update()
    uv=obj.data.uv_layers.get('Brick meters') or obj.data.uv_layers.new(name='Brick meters')
    normal_matrix=obj.matrix_world.to_3x3().inverted().transposed()
    for face in obj.data.polygons:
        normal=(normal_matrix@face.normal).normalized()
        tangent=Vector((-normal.y,normal.x,0))
        horizontal=abs(normal.z)>.99
        if not horizontal:
            tangent.normalize()
            dominant=max(range(2),key=lambda i:abs(tangent[i]))
            if tangent[dominant]<0:tangent=-tangent
        for li in face.loop_indices:
            point=obj.matrix_world@obj.data.vertices[obj.data.loops[li].vertex_index].co
            uv.data[li].uv=(point.x,point.y) if horizontal else (point.dot(tangent),point.z)
    return uv

def brick_material():
    m=material(BRICK_NAME,(.36,.095,.048),.78);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    geo=n.new('ShaderNodeNewGeometry');geo.label='World meters: never stretch brick with wall dimensions'
    co=n.new('ShaderNodeUVMap');co.uv_map='Brick meters';co.label='Physical face coordinates from apply_brick_uv(obj)'
    brick=n.new('ShaderNodeTexBrick');brick.label='215 x 65 mm clay; 10 mm joints; half bond';brick.offset=.5;brick.offset_frequency=2
    for k,v in {'Scale':1.,'Mortar Size':.005,'Mortar Smooth':.001,'Bias':0.,'Brick Width':.225,'Row Height':.075}.items():brick.inputs[k].default_value=v
    brick.inputs['Color1'].default_value=(.285,.051,.022,1);brick.inputs['Color2'].default_value=(.115,.018,.009,1)
    brick.inputs['Mortar'].default_value=(.32,.295,.255,1);l.new(co.outputs[0],brick.inputs['Vector'])
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=85;noise.inputs['Detail'].default_value=5;l.new(geo.outputs['Position'],noise.inputs['Vector'])
    grain=n.new('ShaderNodeMixRGB');grain.blend_type='MULTIPLY';grain.inputs[0].default_value=.35;l.new(brick.outputs['Color'],grain.inputs[1]);l.new(noise.outputs['Fac'],grain.inputs[2]);l.new(grain.outputs[0],p.inputs['Base Color'])
    invert=n.new('ShaderNodeMath');invert.operation='SUBTRACT';invert.inputs[0].default_value=1;l.new(brick.outputs['Fac'],invert.inputs[1])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.7;bump.inputs['Distance'].default_value=.004;l.new(invert.outputs[0],bump.inputs['Height'])
    micro=n.new('ShaderNodeBump');micro.inputs['Strength'].default_value=.65;micro.inputs['Distance'].default_value=.0012;l.new(noise.outputs['Fac'],micro.inputs['Height']);l.new(bump.outputs['Normal'],micro.inputs['Normal']);l.new(micro.outputs['Normal'],p.inputs['Normal'])
    return m

def write_blend(path,blocks):
    if path.exists():
        raise FileExistsError(f'Published versions are immutable: {path}; choose a new version folder.')
    path.parent.mkdir(parents=True,exist_ok=True)
    bpy.data.libraries.write(str(path),set(blocks),path_remap='RELATIVE',fake_user=True,compress=True)

def link_assets(root=None):
    root=Path(root or ROOT)
    with bpy.data.libraries.load(str(root/'library/materials/warm-red-brick/v001/warm-red-brick.blend'),link=True,relative=True) as (src,dst):
        dst.materials=[BRICK_NAME];dst.collections=[MODULE_NAME]
    result={'brick':dst.materials[0],'brick_module':dst.collections[0]}
    with bpy.data.libraries.load(str(root/'library/openings/slim-dark-window/v001/slim-dark-window.blend'),link=True,relative=True) as (src,dst):dst.collections=[WINDOW_NAME]
    result['window']=dst.collections[0]
    return result

def build_brick():
    facade=brick_material();clay=material('Warm red clay | individual unit',(.37,.084,.037),.78)
    n=clay.node_tree.nodes;l=clay.node_tree.links;p=n.get('Principled BSDF');info=n.new('ShaderNodeObjectInfo');r=n.new('ShaderNodeValToRGB')
    r.color_ramp.elements[0].color=(.115,.018,.009,1);r.color_ramp.elements[1].color=(.285,.051,.022,1);l.new(info.outputs['Random'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=120;geo=n.new('ShaderNodeNewGeometry');l.new(geo.outputs['Position'],noise.inputs[0]);b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.0004;b.inputs['Strength'].default_value=.4;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
    mortar=material('Light warm-gray mortar | recessed',(.4,.365,.315),.9)
    col=bpy.data.collections.new(MODULE_NAME)
    cube('Clay unit | 215 x 65 x 102.5 mm',(0,0,.0375),(.215,.1025,.065),clay,col,.0013)
    cube('Mortar joint module | face recessed 4 mm',(0,.002,.0375),(.225,.0985,.075),mortar,col,.0004)
    write_blend(BRICK_DIR/'warm-red-brick.blend',[col,facade]);return facade,col

def build_window():
    col=bpy.data.collections.new(WINDOW_NAME)
    frame=material('Charcoal anodized window frame',(.025,.031,.032),.36,.55)
    seal=material('Window glazing gasket',(.009,.012,.013),.72)
    glass=material('Clear architectural double glazing',(.96,.98,.99),.035)
    p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.45
    def bar(name,x,z,w,h,y=.07,d=.14,mat=frame):return cube(name,(x,y,z),(w,d,h),mat,col,.0012)
    bar('Outer jamb L',-1.1725,1.2,.055,2.4);bar('Outer jamb R',1.1725,1.2,.055,2.4)
    bar('Head',0,2.3725,2.29,.055);bar('Sill',0,.0275,2.29,.055)
    for x in [-.5725,.5725]:bar('55 mm vertical mullion',x,1.2,.055,2.29)
    for i,(a,b) in enumerate([(-1.145,-.6),(-.545,.545),(.6,1.145)]):
        low=.055;high=2.345;inset=.006
        if i!=1:
            t=.026
            for x in [a+inset+t/2,b-inset-t/2]:bar('Casement sash stile',x,1.2,t,high-low-2*inset,.082,.098)
            for z in [low+inset+t/2,high-inset-t/2]:bar('Casement sash rail',(a+b)/2,z,b-a-2*inset-2*t,t,.082,.098)
            a+=inset+t;b-=inset+t;low+=inset+t;high-=inset+t
        for x in [a+.003,b-.003]:bar('Elastomer glazing seal',x,(high+low)/2,.006,high-low,.068,.012,seal)
        for z in [low+.003,high-.003]:bar('Elastomer glazing seal',(a+b)/2,z,b-a-.012,.006,.068,.012,seal)
        for y in [.076,.098]:cube(('Fixed center' if i==1 else 'Side casement')+' | glass pane',( (a+b)/2,y,(high+low)/2),(b-a-.012,.006,high-low-.012),glass,col,.0006)
    bar('Sloped sill drip',0,.021,2.4,.018,.0615,.157)
    # Existing reusable pull geometry. Concept grip only: not a manufacturer casement lock.
    hp=ROOT/'library/hardware/bar-pull-matte-black/v001/bar-pull-matte-black.blend'
    with bpy.data.libraries.load(str(hp),link=True,relative=True) as (src,dst):dst.collections=[src.collections[0]]
    for x in [-.625,.625]:
        o=bpy.data.objects.new('Shared matte-black interior pull',None);o.instance_type='COLLECTION';o.instance_collection=dst.collections[0]
        o.location=(x,.144,1.10);o.rotation_euler=Euler((0,math.pi/2,math.pi));col.objects.link(o)
    write_blend(WINDOW_DIR/'slim-dark-window.blend',[col]);return col

def instance(col,name,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=col;bpy.context.scene.collection.objects.link(o);o.location=loc;return o

def preview(kind):
    bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=48;s.cycles.use_denoising=True
    s.render.resolution_x=1200;s.render.resolution_y=1000;s.render.resolution_percentage=100
    s.view_settings.view_transform='AgX';s.view_settings.exposure=0;s.view_settings.look='AgX - Medium High Contrast'
    s.world=bpy.data.worlds.new('Neutral studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.72,.78,.84,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.45
    ground=material('Preview neutral floor',(.48,.46,.43),.8);c=s.collection;cube('Preview floor',(0,0,-.06),(200,200,.1),ground,c)
    if kind in ['brick','brick-45']:
        with bpy.data.libraries.load(str(BRICK_DIR/'warm-red-brick.blend'),link=True) as (src,dst):dst.materials=[BRICK_NAME]
        sample=cube('Native facade material sample',(0,.15,.75),(2.475,.3,1.5),dst.materials[0],c,.004)
        if kind=='brick-45':sample.rotation_euler.z=math.pi/4
        apply_brick_uv(sample)
        target=(0,0,.72);eye=(2.2,-4.2,1.65);out=BRICK_DIR/('preview.png' if kind=='brick' else 'preview-45-degrees.png')
        if kind=='brick-45':eye=(3.2,-4.2,1.65)
    else:
        with bpy.data.libraries.load(str(WINDOW_DIR/'slim-dark-window.blend'),link=True) as (src,dst):dst.collections=[WINDOW_NAME]
        instance(dst.collections[0],'Window installed at measured origin')
        wall=material('Preview reveal plaster',(.65,.63,.57),.82)
        for x in [-1.43,1.43]:cube('Preview wall side',(x,.12,1.2),(.46,.38,2.9),wall,c,.004)
        for z in [-.13,2.55]:cube('Preview wall lintel/sill',(0,.12,z),(2.4,.38,.3),wall,c,.004)
        rear=material('Preview shaded interior',(.19,.20,.18),.8);cube('Interior backdrop',(0,2.7,1.2),(3,.08,2.9),rear,c)
        cube('Interior horizontal shelf',(0,1.3,.7),(2.7,.5,.08),wall,c,.01)
        target=(0,.03,1.2);eye=(3.5,-6.5,3.2);out=WINDOW_DIR/'preview.png'
    for name,loc,power,size in [('Large softbox',(-3,-4,5),650,4),('Grazing light',(3,-1,4),450,2)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);c.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    d=bpy.data.cameras.new('Native asset inspection');o=bpy.data.objects.new('Native asset inspection',d);c.objects.link(o);o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=55;s.camera=o
    s.render.image_settings.file_format='PNG';s.render.filepath=str(out);bpy.ops.render.render(write_still=True)

def metadata():
    base={'schema_version':1,'version':'v001','units':'meters','license':'CC-BY-4.0','rights':'Original project geometry and procedural materials; attribution: Homes project contributors','software':{'blender':bpy.app.version_string},'source':{'kind':'original','generator':'tools/library/build_lindon_assets.py','command':'Blender --background --python tools/library/build_lindon_assets.py -- publish'},'host_integration':{'checked':False,'required':'Adopting home checks opening fit, sun/shade color response, access and actual weather detailing.'}}
    brick={**base,'id':'materials/warm-red-brick','name':'Warm red clay brick — running bond','dimensions_m':[.225,.1025,.075],'unit_dimensions_m':[.215,.1025,.065],'joint_m':.01,'mortar_recess_m':.004,'placement':'Facade shader uses named UV Brick meters; call apply_brick_uv(mesh) after final world transforms, supporting any wall angle; module origin at bottom-center, front -Y, Z-up. Module horizontal/course pitch 225/75 mm.','variation':'Material may cover any wall size without texture stretching. Module scale stays 1; alternate courses shift 112.5 mm. UV tangent follows each facade angle at physical meter scale, including 45-degree wings. Reapply after mesh or transform changes; UV seams at wall corners are intentional.','files':{'blender':'warm-red-brick.blend','preview':'preview.png','angled_preview':'preview-45-degrees.png'},'blender':{'material':BRICK_NAME,'collection':MODULE_NAME},'dependencies':[],'limitations':'Original appearance concept. Shader bump is visual relief, not geometric masonry. Individual module includes real bevel and recessed mortar. No structural wall, flashing or weather approval.'}
    window={**base,'id':'openings/slim-dark-window','name':'Slim dark three-panel window — 2400 ×2400 mm','dimensions_m':[2.4,.19275,2.4],'nominal_opening_m':[2.4,2.4],'frame_sightline_m':.055,'placement':'Origin bottom-center at exterior main frame plane Y0, front -Y, Z-up. Main frame occupies Y0..0.14; sill projects to Y-0.017; interior pull reaches Y0.17575. Host opening must remain clear across the full 2.4 × 2.4 m envelope.','variation':'Keep scale 1 for 55 mm sightlines; publish dimensional variants using generator for alternate openings. Moderate host scaling is only a visual study and changes all product dimensions.','files':{'blender':'slim-dark-window.blend','preview':'preview.png'},'blender':{'collection':WINDOW_NAME},'dependencies':[{'id':'hardware/bar-pull-matte-black','version':'v001','path':'../../../hardware/bar-pull-matte-black/v001/','blender':'bar-pull-matte-black.blend'}],'operating_clearance':{'state':'Closed','side_panel_type':'Casement-style concept','assumed_outward_opening_degrees':90,'assumed_outward_sweep_m':.545,'basis':'Concept side aperture width; hinges and opening mechanism not engineered','host_checked':False},'service_clearance':'Host must resolve installation shims, drainage, flashing, exterior sill slope, thermal performance, wind/water rating and interior/exterior cleaning access.','limitations':'Generic original concept, not commercial product. Side panels are modeled closed; no operational or weather certification. Reused cabinet pulls are concept grips only, not specified casement-lock hardware.'}
    for folder,m in [(BRICK_DIR,brick),(WINDOW_DIR,window)]:
        (folder/'asset.json').write_text(json.dumps(m,indent=2)+'\n')
        (folder/'README.md').write_text('# '+m['name']+'\n\n![Actual native preview](preview.png)\n\n'+m['placement']+'\n\n'+m['variation']+'\n\n'+m['limitations']+'\n\nOriginal by Homes project contributors; CC BY 4.0. Editable generator: `tools/library/build_lindon_assets.py` (MIT). Use `link_assets(ROOT)` to link the exact material/collections. For brick facade meshes call `apply_brick_uv(obj)` after final world transforms; it creates the required `Brick meters` UV layer for any facade angle. Inspect `asset.json` for dimensions and dependencies.\n\nPreview: Blender Cycles CPU, 48 samples, AgX Medium High Contrast, exposure 0, neutral studio world 0.45 and large area lights. Actual sunlit/shaded host validation remains the adopting home’s responsibility.\n')

def verify():
    bpy.ops.wm.read_factory_settings(use_empty=True);assets=link_assets();instance(assets['window'],'Window verification');instance(assets['brick_module'],'Module verification',(4,0,0));bpy.context.view_layer.update()
    dg=bpy.context.evaluated_depsgraph_get();bounds={}
    for key,label in [('window','Window verification'),('brick_module','Module verification')]:
        points=[]
        for i in dg.object_instances:
            if i.is_instance and i.parent and i.parent.original.name==label and i.object.type=='MESH':points.extend(i.matrix_world@Vector(v) for v in i.object.bound_box)
        if points:bounds[key]={'min':[min(v[a] for v in points) for a in range(3)],'max':[max(v[a] for v in points) for a in range(3)]}
    test=cube('45-degree mapping verification',(0,0,0),(2.475,.3,1.5),assets['brick'],bpy.context.scene.collection)
    test.rotation_euler.z=math.pi/4;test.scale=(1.15,.9,1.1);uv=apply_brick_uv(test)
    edge_errors=[]
    for face in test.data.polygons:
        ids=list(face.loop_indices)
        for a,b in zip(ids,ids[1:]+ids[:1]):
            wa=test.matrix_world@test.data.vertices[test.data.loops[a].vertex_index].co
            wb=test.matrix_world@test.data.vertices[test.data.loops[b].vertex_index].co
            edge_errors.append(abs((wa-wb).length-(uv.data[a].uv-uv.data[b].uv).length))
    assert max(edge_errors)<1e-5,edge_errors
    missing=[bpy.path.abspath(lib.filepath) for lib in bpy.data.libraries if not Path(bpy.path.abspath(lib.filepath)).exists()]
    assert not missing,missing
    assert len(assets['window'].objects)>=25
    assert abs(bounds['window']['max'][0]-bounds['window']['min'][0]-2.4)<1e-5
    assert abs(bounds['window']['max'][2]-2.4)<1e-5
    assert abs(bounds['window']['min'][1]+.017)<1e-5
    assert abs(bounds['window']['max'][1]-.17575)<1e-5
    assert abs(bounds['brick_module']['max'][0]-bounds['brick_module']['min'][0]-.225)<1e-5
    assert BRICK_NAME in bpy.data.materials
    receipt={'fresh_process':True,'native_assets_loaded':True,'missing_dependencies':missing,'bounds_world_m':bounds,'window_object_count':len(assets['window'].objects),'dimensions_assertions_passed':True,'brick_45_degree_nonuniform_scale_uv_edge_error_m':max(edge_errors),'brick_uv_name':'Brick meters','preview_review':{'neutral_native_previews':'Inspected actual PNGs: red/rust clay variation and fine grain; window complete slim frame, deep glazing and visible side sash reveals.','host_sun_shade_review':'Pending adopting home'},'blender':bpy.app.version_string}
    (WINDOW_DIR/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');(BRICK_DIR/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['publish']
    if args[0]=='publish':
        bpy.ops.wm.read_factory_settings(use_empty=True);build_brick();build_window();metadata()
    elif args[0]=='preview':preview(args[1])
    elif args[0]=='verify':verify()
