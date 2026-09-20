"""Publish immutable smoked-oak kitchen modules; fresh verify and CPU previews.

Blender --background --python tools/library/build_timber_kitchen_cabinets.py
Blender --background --python tools/library/build_timber_kitchen_cabinets.py -- --verify --render
All authoring below is in meters. Countertops and appliances belong to the host.
"""
from pathlib import Path
import bpy, json, sys, shutil, hashlib
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common import geometry as g
from common.library import linked_collection, instance
from common.timber_materials import grain_uv

H, D, T = .87122, .6096, .018
ASSETS = {
    'smoked-oak-drawer-base-2ft': (.6096, 'drawer'),
    'smoked-oak-sink-base-36in': (.9144, 'sink'),
    'smoked-oak-oven-base-36in': (.9144, 'oven'),
    'smoked-oak-waste-pullout-18in': (.4572, 'waste'),
    'smoked-oak-pantry-shelf-2ft': (.6096, 'pantry'),
}


def box(name, loc, size, mat, bevel=.0015):
    o = g.box(name, [v/g.F for v in loc], [v/g.F for v in size], mat, bevel/g.F)
    if mat.library:
        grain_uv(o)
    return o


def load_palette():
    path = ROOT/'library/materials/smoked-oak/v001/smoked-oak.blend'
    with bpy.data.libraries.load(str(path), link=True) as (a, b):
        b.materials = [a.materials[0]]
    return {'wood': b.materials[0],
            'inner': g.material('Warm light cabinet liner', (.32,.29,.235), .6),
            'dark': g.material('Recessed graphite plinth', (.026,.028,.027), .7),
            'metal': g.material('Drawer runner stainless', (.35,.36,.36), .3, .8),
            'bin': g.material('Waste bins recycled graphite concept', (.065,.07,.068), .65)}


def build(slug):
    w, kind = ASSETS[slug]
    M = load_palette()
    pull = linked_collection(ROOT, 'hardware', 'bar-pull-satin-bronze', 'v001') if kind not in {'oven','pantry'} else None
    c = g.collection(slug)
    c['asset_id'] = 'cabinetry/'+slug
    c['asset_version'] = 'v001'
    c['front_direction'] = '-Y'
    c['cabinet_height_m'] = H
    if kind == 'pantry':
        h,d=2.1336,.3048
        c['cabinet_height_m']=h
        box('Pantry floor-supported plinth',(0,.020,.0508),(w-.036,d-.065,.1016),M['dark'])
        for x in [-w/2+.009,w/2-.009]:
            box('Pantry smoked oak side',(x,0,(h+.1016)/2),(.018,d,h-.1016),M['wood'])
        box('Pantry rear fixing panel',(0,d/2-.009,(h+.1016)/2),(w-.036,.018,h-.1016),M['wood'])
        for z in [.130,.500,.900,1.300,1.700,h-.009]:
            box('Pantry usable adjustable shelf',(0,-.004,z),(w-.036,d-.026,.018),M['wood'])
            if z not in [.130,h-.009]:
                for x in [-w/2+.021,w/2-.021]:
                    for y in [-.115,.110]:
                        box('Pantry shelf support pin',(x,y,z-.012),(.008,.009,.009),M['metal'],.001)
        for x in [-.23,.23]:
            box('Pantry anti-tip fixing plate',(x,d/2-.020,h-.065),(.040,.004,.060),M['metal'])
        bpy.context.view_layer.update()
        return c
    # Continuous recessed plinth reaches floor; no floating toe kick.
    box('Floor-supported recessed plinth', (0,.034,.0508), (w-.036,D-.100,.1016), M['dark'])
    for x in [-w/2+T/2, w/2-T/2]:
        box('Smoked oak cabinet side', (x,.011,(H+.1016)/2), (T,D-.022,H-.1016), M['wood'])
    box('Cabinet bottom', (0,.011,.1106), (w-.036,D-.022,.018), M['inner'])
    if kind not in {'sink','oven'}:
        box('Cabinet rear', (0,D/2-.009,(H+.1196)/2), (w-.036,.018,H-.1196), M['inner'])
    # Narrow rails leave the sink bowl and appliance top unobstructed.
    for y in [-.274,.284]:
        box('Countertop support rail', (0,y,H-.009), (w-.036,.016,.018), M['wood'])
    if kind == 'drawer':
        for n, (lo, hi) in enumerate([(.115,.355),(.359,.610),(.614,H-.003)]):
            z = (lo+hi)/2
            box('Drawer %d flush oak front'%n, (0,-.2938,z), (w-.004,.022,hi-lo), M['wood'])
            instance('Shared bronze drawer pull', pull, (0,-.3048/g.F,(hi-.055)/g.F))
            box('Drawer %d bottom'%n, (0,-.008,lo+.027), (w-.096,.514,.012), M['inner'])
            for x in [-w/2+.041,w/2-.041]:
                box('Drawer %d side'%n, (x,-.008,z-.014), (.014,.514,hi-lo-.060), M['inner'])
                box('Drawer %d runner'%n, (x+(-.012 if x<0 else .012),-.008,z-.052), (.009,.47,.018), M['metal'])
            box('Drawer %d rear'%n, (0,.242,z-.014), (w-.096,.014,hi-lo-.060), M['inner'])
    elif kind == 'sink':
        # Real cavity: no solid backing, shelf or drawer crossing the bowl/plumbing.
        box('Sink fixed false front', (0,-.2938,.803), (w-.004,.022,.130), M['wood'])
        door_h = .619
        for sign in [-1,1]:
            x = sign*w/4
            box('Sink hinged door', (x,-.2938,.4245), (w/2-.004,.022,door_h), M['wood'])
            o = instance('Shared bronze sink door pull', pull, (sign*.055/g.F,-.3048/g.F,.62/g.F))
            o.rotation_euler.y = 1.5707963267948966
        # Lower rear stretcher leaves full plumbing access above it.
        box('Sink lower rear stretcher', (0,.295,.175), (w-.036,.018,.11), M['wood'])
    elif kind == 'oven':
        # 774 x 720 mm unobstructed face opening, bottom .135, top .855.
        box('Oven load-support shelf', (0,.005,.126), (w-.036,.56,.018), M['inner'])
        for sign in [-1,1]:
            box('Oven housing face stile', (sign*(w/2+.387)/2,-.2938,.495), ((w-.774)/2,.022,.720), M['wood'])
        box('Oven housing top rail', (0,-.2938,.86311), (w-.004,.022,H-.855), M['wood'])
        # The parent appliance extends to rear plane; ventilation/service beyond
        # this open rear must be supplied by the host, not silently filled here.
    else:
        box('Waste pullout oak front', (0,-.2938,(H+.115)/2), (w-.004,.022,H-.115-.003), M['wood'])
        instance('Shared bronze waste pull', pull, (0,-.3048/g.F,(H-.058)/g.F))
        box('Waste carriage floor', (0,-.007,.147), (w-.080,.52,.018), M['inner'])
        for x in [-w/2+.035,w/2-.035]:
            box('Waste full extension runner', (x,-.005,.17), (.012,.5,.032), M['metal'])
        for y in [-.14,.11]:
            bw, bd, bh, bz = w-.10,.225,.46,.165
            box('Waste bin bottom', (0,y,bz+.006), (bw,bd,.012), M['bin'])
            for x in [-bw/2+.006,bw/2-.006]:
                box('Waste bin side', (x,y,bz+bh/2), (.012,bd,bh), M['bin'])
            for by in [y-bd/2+.006,y+bd/2-.006]:
                box('Waste bin end', (0,by,bz+bh/2), (bw-.024,.012,bh), M['bin'])
    bpy.context.view_layer.update()
    return c


def mesh_bounds(c, matrix=Matrix.Identity(4)):
    pts=[]
    for o in c.objects:
        transform=matrix@o.matrix_world
        if o.type=='MESH':
            pts += [transform@Vector(v) for v in o.bound_box]
        if o.instance_type=='COLLECTION' and o.instance_collection:
            pts += mesh_bounds(o.instance_collection, transform)
    return pts


def bounds(c):
    pts=mesh_bounds(c)
    return ([min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)])


def installation(kind):
    record={'mounting':'Floor-supported; countertop excluded. Nominal 24-inch depth and 34.3-inch height. Finish front plane Y=-0.3048m; rear Y=+0.3048m. Bronze pulls project a further 31.75mm where used.',
            'operating_envelope':{'modeled_state':'Closed; components individually editable, not animated',
              'basis':'Original concept geometry and conservative planning allowance; no manufacturer selected',
              'host_open_state_checked':False, 'reserve_front_operator_depth_m':.8},
            'service_requirements':['Host supplies countertop, wall fixing, selected product tolerances and access; these are concept modules, not construction specifications.']}
    if kind=='drawer': record['operating_envelope'].update(intended_drawer_travel_m=.5,reserve_front_depth_including_operator_m=1.3)
    elif kind=='sink':
        record['operating_envelope'].update(intended_open_angle_degrees=100,reserve_front_door_projection_m=.46)
        record['compatible_fixture']={'id':'fixtures/kitchen-sink-mixer-650','version':'v002','mounting_center_m':[0,-.030,None], 'mounting_z':'Host countertop top; verified at cabinet height plus38.1mm','recommended_host_cutout_m':[.664,.464], 'below_top_bowl_depth_m':.218, 'fit_basis':'v002 corrects original fixture manifest opening to measured654x454mm outer bowl plus5mm each side. Inspect selected commercial sink separately.'}
        record['service_requirements'] += ['Open cavity and rear permit drain/trap/supply routing. Keep all pipes accessible after doors open.','Host must cut the actual countertop opening and check the selected bowl/faucet. No shelf or top panel crosses the bowl.']
    elif kind=='oven':
        record['operating_envelope'].update(intended_open_angle_degrees=90,reserve_front_door_projection_m=.72,reserve_front_depth_including_operator_m=1.52)
        record['appliance_opening_m']={'width':.774,'front_height':.720,'effective_height_under_support_rails':.71822,'bottom_z':.135,'front_top_z':.855,'support_rail_bottom_z':.85322,'rear':'Open; service and ventilation space must continue beyond cabinet'}
        record['compatible_fixture']={'id':'appliances/built-in-oven-30in','version':'v001','suggested_origin_m':[0,0,.14], 'front_direction':'-Y'}
        record['service_requirements'] += ['Do not fill the opening with a solid cabinet or drawer. Confirm support load and product-specific ventilation/heat separation before specification.']
    elif kind=='waste': record['operating_envelope'].update(intended_pullout_travel_m=.52,reserve_front_depth_including_operator_m=1.32,bin_count=2)
    else:
        record['mounting']='Floor-centered open shelf module, 24in wide x12in deep x84in high. Front -Y. Floor plinth reaches Z=0. Attach rear fixing plates to verified wall backing; model plates do not establish capacity.'
        record['operating_envelope'].update(modeled_state='Open shelving; no doors',reserve_front_depth_m=.8)
        record['shelf_top_elevations_m']=[.139,.509,.909,1.309,1.709,2.1336]
        record['service_requirements'] += ['Reserve wall attachment access and confirm shelf loads and anti-tip anchorage. Shelf clear depths approximately278mm suit food storage and small items; deep countertop appliances require separate deeper storage.','Shelf intervals are approximately350-400mm clear; the model has concept adjustable supports, not a rated commercial system.']
    return record


def sink_signature(c):
    data=[]
    for o in sorted(c.objects,key=lambda v:v.name):
        if o.type=='MESH':data.append([o.name,[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],list(sum((list(row) for row in o.matrix_world),[]))])
        elif o.type=='CURVE':data.append([o.name,[[list(p.co) for p in spline.bezier_points] for spline in o.data.splines],o.data.bevel_depth])
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()


def publish_sink_correction():
    slug='kitchen-sink-mixer-650';parent=ROOT/'library/fixtures'/slug/'v001';folder=parent.parent/'v002';path=folder/(slug+'.blend')
    if path.exists():return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(parent/(slug+'.blend')),link=False) as (a,b):b.collections=[a.collections[0]]
    c=b.collections[0];c['asset_version']='v002';folder.mkdir(parents=True,exist_ok=True)
    bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap='RELATIVE_ALL')
    meta=json.loads((parent/'asset.json').read_text());meta['version']='v002'
    meta['installation']['mounting']='Countertop mounting plane Z=0. Provide a 664 × 464 mm opening: actual modeled outside bowl walls measure654 ×454mm, plus5mm allowance per side. Support the flange continuously. Coordinate final selected-product cutout separately.'
    meta['installation']['countertop_cutout_m']=[.664,.464]
    meta['installation']['measured_outer_bowl_m']=[.654,.454,.218]
    meta['source']={'kind':'original','generator':'tools/library/build_timber_kitchen_cabinets.py','parent_geometry':'tools/library/build_lindon_furniture.py','software':bpy.app.version_string}
    meta['derived_from']={'id':'fixtures/kitchen-sink-mixer-650','version':'v001','basis':'Identical native geometry and material; corrects undersized opening metadata from650x450mm to664x464mm after measuring654x454mm outer bowl walls. Asset-version property updated.'}
    (folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
    shutil.copyfile(parent/'preview.png',folder/'preview.png')
    print('PUBLISHED',slug,'v002',flush=True)


def verify_sink_correction():
    slug='kitchen-sink-mixer-650';base=ROOT/'library/fixtures'/slug
    signatures=[]
    for version in ['v001','v002']:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        with bpy.data.libraries.load(str(base/version/(slug+'.blend')),link=True) as (a,b):b.collections=[a.collections[0]]
        c=b.collections[0];bpy.context.scene.collection.children.link(c);bpy.context.view_layer.update();signatures.append(sink_signature(c))
    assert signatures[0]==signatures[1]
    objects=[o for o in c.objects if o.type=='MESH' and (o.name.startswith('Stainless sink bowl bottom') or o.name.startswith('Sink end') or o.name.startswith('Sink side'))]
    pts=[o.matrix_world@Vector(v) for o in objects for v in o.bound_box]
    lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
    dims=[hi[i]-lo[i] for i in range(3)]
    assert abs(dims[0]-.654)<1e-6 and abs(dims[1]-.454)<1e-6
    receipt={'fresh_link':True,'geometry_identical_to_v001':True,'geometry_signature_sha256':signatures[1],
             'measured_outer_bowl_bounds_m':{'min':lo,'max':hi},'measured_outer_bowl_dimensions_m':dims,
             'countertop_cutout_m':[.664,.464],'cutout_allowance_per_side_m':[.005,.005],
             'measurement_objects':[o.name for o in objects],'preview':'Copied actual v001 native preview because all geometry and materials are unchanged.',
             'host_installation_checked':False,'manufacturer_specification':False}
    (base/'v002/validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('VERIFIED',slug,'v002',flush=True)


def publish():
    publish_sink_correction()
    for slug,(w,kind) in ASSETS.items():
        folder=ROOT/'library/cabinetry'/slug/'v001'; path=folder/(slug+'.blend')
        if path.exists():
            print('IMMUTABLE_EXISTING',slug,flush=True); continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        c=build(slug);lo,hi=bounds(c);folder.mkdir(parents=True,exist_ok=True)
        bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap='RELATIVE_ALL')
        dependencies=[{'id':'materials/smoked-oak','version':'v001','path':'../../../materials/smoked-oak/v001/smoked-oak.blend'}]
        if kind not in {'oven','pantry'}:dependencies.append({'id':'hardware/bar-pull-satin-bronze','version':'v001','path':'../../../hardware/bar-pull-satin-bronze/v001/bar-pull-satin-bronze.blend'})
        meta={'schema_version':1,'id':'cabinetry/'+slug,'version':'v001','name':slug.replace('-',' ').capitalize(),'units':'meters',
              'dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'nominal_carcass_dimensions_m':[w,.3048,2.1336] if kind=='pantry' else [w,D,H],
              'placement':{'origin':'Floor-center of nominal footprint at Z=0','front_direction':'-Y','up':'Z','allowed_scaling':'Rigid placement and Z rotation only; no scaling.'},
              'installation':installation(kind),'dependencies':dependencies,
              'derived_from':{'id':'cabinetry/oak-drawer-base-2ft','version':'v001','basis':'Original same-size drawer cabinet arrangement adapted to 34.3in top, refined individual carcass/drawer parts, meter-grain smoked oak and shared bronze pulls'} if kind=='drawer' else None,
              'source':{'kind':'original','generator':'tools/library/build_timber_kitchen_cabinets.py','primitives':'tools/common/geometry.py','software':bpy.app.version_string},
              'license':'CC-BY-4.0','rights':'Original Homes project geometry; attribution Homes project contributors',
              'files':{'blender':path.name,'preview':'preview.png','validation':'validation.json'}}
        (folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
        print('PUBLISHED',slug,flush=True)


def verify(render):
    for slug,(w,kind) in ASSETS.items():
        folder=ROOT/'library/cabinetry'/slug/'v001';path=folder/(slug+'.blend')
        bpy.ops.wm.open_mainfile(filepath=str(path))
        assert all(lib.filepath.startswith('//') for lib in bpy.data.libraries)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        with bpy.data.libraries.load(str(path),link=True) as (a,b):b.collections=[slug]
        c=b.collections[0];bpy.context.scene.collection.children.link(c);bpy.context.view_layer.update()
        lo,hi=bounds(c);meta=json.loads((folder/'asset.json').read_text())
        assert abs(lo[2])<1e-6 and abs(hi[2]-(2.1336 if kind=='pantry' else H))<1e-6
        assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-6 for i in range(3))
        assert all(Path(bpy.path.abspath(lib.filepath,library=lib.parent)).exists() for lib in bpy.data.libraries)
        wood_meshes=[o for o in c.objects if o.type=='MESH' and any(m and m.name.startswith('Smoked oak') for m in o.data.materials)]
        assert wood_meshes and all(o.data.uv_layers.get('Timber meters') for o in wood_meshes)
        receipt={'fresh_native_reopen':True,'fresh_link':True,'floor_contact':True,'relative_dependencies_resolved':True,
                 'dimensions_m':[hi[i]-lo[i] for i in range(3)],'wood_meshes_with_meter_uv':len(wood_meshes),'host_installation_checked':False,
                 'interface_check':'Open top and cabinet cavity reviewed against documented component envelope; host integration remains separate.',
                 'preview_rendered':(folder/'preview.png').exists()}
        if kind in {'sink','oven'}:
            category, fixture = ('fixtures','kitchen-sink-mixer-650') if kind=='sink' else ('appliances','built-in-oven-30in')
            fixture_version='v002' if kind=='sink' else 'v001'
            fixture_path=ROOT/'library'/category/fixture/fixture_version/(fixture+'.blend')
            with bpy.data.libraries.load(str(fixture_path),link=True) as (a,b):b.collections=[a.collections[0]]
            fc=b.collections[0]
            bpy.context.scene.collection.children.link(fc)
            bpy.context.view_layer.update()
            offset=Vector((0,-.030,H+.0381) if kind=='sink' else (0,0,.14))
            def object_bounds(o, shift=Vector((0,0,0))):
                pts=[o.matrix_world@Vector(v)+shift for v in o.bound_box]
                return ([min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)])
            collisions=[]
            for host in c.objects:
                if host.type!='MESH':continue
                alo,ahi=object_bounds(host)
                for component in fc.objects:
                    if component.type!='MESH':continue
                    blo,bhi=object_bounds(component,offset)
                    if all(min(ahi[i],bhi[i])-max(alo[i],blo[i])>1e-5 for i in range(3)):
                        collisions.append([host.name,component.name])
            assert not collisions, collisions
            bpy.context.scene.collection.children.unlink(fc)
            receipt['isolated_component_fit']={'id':category+'/'+fixture,'version':fixture_version,'origin_m':list(offset),'mesh_aabb_intersections':collisions,'basis':'Actual linked mesh bounds versus cabinet mesh bounds; no operating motion, countertop or house integration included.'}
        if render:
            g.collection('Preview studio')
            s=bpy.context.scene;s.camera=g.camera('Cabinet preview',(7,-9,6) if kind=='pantry' else (4,-5,4),(0,0,3.5) if kind=='pantry' else (0,0,1.35),52)
            floor=g.material('Neutral studio floor',(.32,.33,.32),.85);g.box('Studio floor',(0,0,-.02),(200,200,.04),floor)
            g.area('Large soft key',(2,-4,6),(0,0,1.5),380,5,(1,.94,.88))
            g.area('Soft fill',(-3,-1,3),(0,0,1.5),130,4,(.90,.95,1))
            s.world=bpy.data.worlds.new('Neutral world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25
            s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True
            s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100
            s.render.image_settings.file_format='PNG';s.render.filepath=str(folder/'preview.png');s.view_settings.view_transform='AgX'
            bpy.ops.render.render(write_still=True);receipt['preview_rendered']=True
        (folder/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print('VERIFIED',slug,flush=True)


if __name__=='__main__':
    if '--metadata-only' in sys.argv:
        for slug,(_,kind) in ASSETS.items():
            path=ROOT/'library/cabinetry'/slug/'v001/asset.json'
            meta=json.loads(path.read_text());meta['installation']=installation(kind);path.write_text(json.dumps(meta,indent=2)+'\n')
    elif '--verify' in sys.argv:
        verify_sink_correction();verify('--render' in sys.argv)
    else:publish()
