"""Original duplex outlet concept; meter units; wall plane Y=0, front -Y."""
import bpy,sys,math,json,argparse,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];SLUG='duplex-power-outlet-bronze';OUT=ROOT/'library/fixtures'/SLUG/'v001'
DEP='library/hardware/bar-pull-satin-bronze/v001/bar-pull-satin-bronze.blend'
p=argparse.ArgumentParser();p.add_argument('action',choices=['build','verify']);args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);C=None

def own(o,name,mat=None):
    o.name=name
    for c in list(o.users_collection):c.objects.unlink(o)
    C.objects.link(o)
    if mat:o.data.materials.append(mat)
    return o

def box(name,xyz,size,mat=None,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=xyz);o=own(bpy.context.object,name,mat);o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=o.modifiers.new('Soft manufactured perimeter','BEVEL');mod.width=bevel;mod.segments=5;bpy.ops.object.modifier_apply(modifier=mod.name)
    return o

def disk(name,xyz,r,depth,mat=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=xyz,rotation=(math.pi/2,0,0));return own(bpy.context.object,name,mat)

def cut(ob,cutter):
    bpy.context.view_layer.objects.active=ob;mod=ob.modifiers.new('True opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)

def bounds(col):
    bpy.context.view_layer.update();pts=[o.matrix_world@Vector(v) for o in col.objects if o.type=='MESH' for v in o.bound_box];return {'min':[round(min(v[i] for v in pts),7) for i in range(3)],'max':[round(max(v[i] for v in pts),7) for i in range(3)]}

def build():
    global C
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/(SLUG+'.blend')).exists():raise RuntimeError('Published version exists; do not overwrite')
    bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.unit_settings.system='METRIC'
    C=bpy.data.collections.new(SLUG+' | v001');scene.collection.children.link(C)
    with bpy.data.libraries.load(str(ROOT/DEP),link=True) as(src,dst):
        candidates=[n for n in src.materials if n.startswith('Hardware | satin-bronze')];assert len(candidates)==1,candidates;dst.materials=candidates
    bronze=dst.materials[0];assert bronze
    def material(name,color,rough=.5,metal=0):
        m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Roughness'].default_value=rough;n.inputs['Metallic'].default_value=metal;return m
    ivory=material('Outlet | warm ivory polymer',(.55,.50,.40),.37);dark=material('Outlet | unlit cavity',(.009,.011,.010),.85);steel=material('Outlet | concealed yoke',(.23,.24,.22),.45,.75)
    plate=box('2.75 x 4.5 inch satin bronze faceplate',(0,-.0016,0),(.06985,.0032,.1143),bronze,.0014)
    for z in [-.024,.024]:
        cut(plate,box('Plate duplex cutout',(0,-.0016,z),(.035,.012,.0355),None,.008))
        socket=box('Warm ivory duplex receptacle',(0,-.003,z),(.034,.012,.035),ivory,.007)
        for x,length in [(-.0063,.009),(.0063,.007)]:cut(socket,box('True polarized blade aperture',(x,-.004,z+.005),(.0019,.023,length)))
        cut(socket,disk('True ground aperture',(0,-.004,z-.0078),.00235,.023))
        box('Dark deep receptacle cavity',(0,.006,z),(.029,.004,.030),dark,.003)
    screw=disk('Center plate screw',(0,-.0044,0),.0027,.0024,bronze);cut(screw,box('Screwdriver slot',(0,-.0054,0),(.0035,.002,.0007)))
    # Hollow conceptual backbox; +Y is inside the host, never in the room.
    for x in [-.0254,.0254]:box('Recessed backbox side',(x,.025,0),(.0012,.05,.0953),dark)
    for z in [-.04705,.04705]:box('Recessed backbox end',(0,.025,z),(.0508,.05,.0012),dark)
    box('Recessed backbox rear',(0,.0494,0),(.0508,.0012,.0953),dark)
    for z in [-.044,.044]:box('Concealed device mounting yoke',(0,.0015,z),(.018,.002,.010),steel,.001)
    C['asset_id']='fixtures/'+SLUG;C['asset_version']='v001';C['wall_plane']='Y=0; front -Y';C['concept_only']=True
    asset=C;b=bounds(asset)
    C=bpy.data.collections.new('Preview studio (do not instance)');scene.collection.children.link(C)
    wall=material('Preview warm neutral',(.24,.25,.23),.9);box('Preview wall left',(-.18,.006,0),(.305,.012,1),wall);box('Preview wall right',(.18,.006,0),(.305,.012,1),wall)
    for z in [-.28,.28]:box('Preview wall horizontal',(0,.006,z),(.055,.012,.462),wall)
    bpy.ops.object.camera_add(location=(.080,-.24,.042));cam=own(bpy.context.object,'Preview camera');cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.155;scene.camera=cam
    for pos,power,size in [((-.15,-.18,.22),9,.22),((.18,-.12,.03),4,.17)]:
        bpy.ops.object.light_add(type='AREA',location=pos);o=own(bpy.context.object,'Preview area');o.data.energy=power;o.data.size=size;o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
    scene.world=bpy.data.worlds.new('Preview world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[1].default_value=.25
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=480;scene.render.resolution_y=560;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(str(ROOT/DEP),start=str(OUT))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(SLUG+'.blend')));scene.render.filepath=str(OUT/'preview.png');bpy.ops.render.render(write_still=True)
    m={'schema_version':1,'id':'fixtures/'+SLUG,'version':'v001','name':'Original US-styled duplex outlet with satin bronze faceplate','units':'meters','dimensions_m':[round(b['max'][i]-b['min'][i],7) for i in range(3)],'bounds_m':b,'nominal_faceplate_m':[.06985,.0032,.1143],'blender':{'collection':asset.name},'placement':{'origin':'Center of faceplate at finished wall plane Y=0','front':'-Y','up':'+Z','allowed_rotation':'Rotate 90 degrees about local Y for horizontal faceplate; preserves front and cavity axis','allowed_scaling':'None','mounting':'Recessed wall box; remove host finish and backing from required conceptual cavity'},'interfaces':{'host_cutout_m':{'width_x':.054,'height_z':.098,'depth_y':.052,'center_xz':[0,0],'starts_y':0},'box_depth_m':.05,'front_projection_m':round(-b['min'][1],7),'host_requirement':'Do not place into an uncut solid backsplash or cabinet. The opening and service depth rotate with the collection. Keep clear of framing, plumbing and concealed equipment.','horizontal_plate_width_m':.1143,'horizontal_plate_height_m':.06985},'operating_envelope':{'modeled_state':'Unplugged','geometry':'True blade and ground apertures, front plate openings and hollow rear box','plug_clearance':'Provide accessible space in front for selected plug body and cord bend; no plug or cable modeled','host_open_state_checked':False},'limitations':['Original visual power-location concept only: no voltage/current rating, wiring design, electrical listing, GFCI protection or code approval','Connection, wet-location protection, circuiting, box fill, mounting spacing and clearances are unselected','Host cavity and accessible plug/cord space require review'],'source':{'kind':'original','generator':'tools/library/build_kitchen_power_outlet.py','command':'Blender --factory-startup --background --python tools/library/build_kitchen_power_outlet.py -- build','basis':'User-requested nominal 2.75 by 4.5 inch plate. All other geometry original conceptual assumptions; not copied from manufacturer CAD.'},'dependencies':[{'id':'hardware/bar-pull-satin-bronze','version':'v001','path':DEP,'usage':'Pinned linked bronze material only','material':bronze.name}],'files':{'blender':SLUG+'.blend','preview':'preview.png','validation':'validation.json'},'license':'CC-BY-4.0','rights':'Original Homes project contributors geometry; attribution Homes project contributors','software':{'blender':bpy.app.version_string}}
    (OUT/'asset.json').write_text(json.dumps(m,indent=2)+'\n')
    (OUT/'README.md').write_text('# Satin bronze duplex power outlet\n\n![Native preview](preview.png)\n\nOriginal US-styled concept; no manufacturer, electrical rating or certification claim. Nominal faceplate **2.75 × 4.5 inches**. Origin is the wall face center at **Y=0**, front **−Y**. Rotate **90° about local Y** for a horizontal installation: the visible plate becomes 4.5 inches wide × 2.75 inches tall. Do not scale.\n\nLink `'+asset.name+'`; exclude the separate preview studio. The source includes actual socket apertures, separate receptacles, a slotted screw and a hollow 50 mm deep rear box. Cut a conceptual **54 × 98 × 52 mm** host recess, rotating with the asset. Do not bury the box in uncut solids. Provide separate accessible plug and cord space.\n\nSee [asset.json](asset.json) for exact bounds, dependencies and unresolved installation requirements. Appearance and location only: actual wiring, protection, product selection and applicable installation requirements remain to be designed.\n')
    (OUT/'AGENTS.md').write_text('# Duplex outlet v001\n\n- Immutable after adoption; publish a new version for geometry changes.\n- Read asset.json for wall-center origin, −Y front, rotation and rear cavity. Rotate around local Y for horizontal use; never rotate into or away from the wall.\n- Cut the host recess and check framing, services and plug access. Do not hide the backbox in a solid counter, wall or cabinet.\n- This is an unbranded visual location concept, not a listed product or wiring/code approval.\n- Preserve the pinned bronze material dependency and link only the named fixture collection.\n')

def verify():
    bpy.ops.wm.open_mainfile(filepath=str(OUT/(SLUG+'.blend')));m=json.loads((OUT/'asset.json').read_text());col=bpy.data.collections[m['blender']['collection']];b=bounds(col);assert b==m['bounds_m'];assert b['max'][1]<=.050001
    libs=[{'path':l.filepath,'relative':l.filepath.startswith('//'),'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries];assert all(x['relative'] and x['exists'] for x in libs)
    assert len([o for o in col.objects if 'receptacle' in o.name and o.type=='MESH'])==4
    rec={'status':'fresh_reopen_pass','blender':bpy.app.version_string,'collection':col.name,'bounds_m':b,'object_count':len(col.objects),'relative_dependencies':libs,'host_cavity_checked':False,'visual_review':'Pending native preview inspection','native_sha256':hashlib.sha256((OUT/(SLUG+'.blend')).read_bytes()).hexdigest()};(OUT/'validation.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec))
(build if args.action=='build' else verify)()
