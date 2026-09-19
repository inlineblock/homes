"""Shared detailed hardware and a restrained, layered household lighting layout."""
import bpy,math
from mathutils import Vector
from roof_design import ceiling_surface, is_vault, near_exposed_frame
from common.geometry import collection,cyl,F
from common.lighting_assets import load as load_lights,place as place_light
from common.hardware_assets import place as hardware,dependencies as hardware_dependencies
LIGHT_KEYS=['downlight','taskbar']
HARDWARE=[('bar-pull','satin-bronze'),('door-lever','satin-bronze')]

def details(ROOT):
    collection('11 Details | shared hardware and lighting')
    for o in list(bpy.context.scene.objects):
        if o.type!='MESH':continue
        x,y,z=[v/F for v in o.location];dx,dy,dz=[v/F for v in o.dimensions]
        if 'drawer front' in o.name and not o.library:
            if dx<.3:loc=(x-dx/2-.003,y,z);rot=-math.pi/2
            else:
                sign=-1 if o.name.startswith('Interior serving') else 1
                loc=(x,y+sign*(dy/2+.003),z);rot=0 if sign<0 else math.pi
            hardware(ROOT,'bar-pull','satin-bronze',o.name+' shared pull',loc,rotation_z=rot)
        if 'open oak door leaf' in o.name:
            if dx<.3:
                yy=y+dy/2-.35 if o.name.startswith('Primary WC west') else y-dy/2+.35
                for side in [-1,1]:hardware(ROOT,'door-lever','satin-bronze',o.name+' lever',(x+side*(dx/2+.005),yy,3.1),rotation_z=-math.pi/2 if side<0 else math.pi/2)
            else:
                sign=-1 if o.name.startswith(('Primary east','Bath closet partition','Primary bath front')) else 1
                xx=x+sign*(dx/2-.35)
                for side in [-1,1]:hardware(ROOT,'door-lever','satin-bronze',o.name+' lever',(xx,y+side*(dy/2+.005),3.1),rotation_z=0 if side<0 else math.pi)
    lights=load_lights(ROOT,keys=LIGHT_KEYS)
    positions=[(6,28),(20,28),(6,35),(20,35),(29,24),(40,24),(29,35),(40,35),(47,34),(61,34),(62,26),(22,8),(22,16),(9,16),(13.5,19),(9,22),(3,21),(5,5),(33,7),(48,8),(64,4),(63,11),(16,15),(3.5,14),(65,18)]
    cutters_by_ceiling={}
    mat=next(m for m in bpy.data.materials if m.name.startswith('Graphite hardware'))
    for x,y in positions:
        assert not near_exposed_frame(x,y), f'Downlight conflicts with exposed frame: {(x,y)}'
        z,normal,ceiling_name=ceiling_surface(x,y)
        normal=Vector(normal)
        orientation=normal.to_track_quat('Z','Y')
        center=Vector((x,y,z))+normal*.14
        cut=cyl('Temporary downlight ceiling cut',center,1.7/12,.52,mat,32)
        cut.rotation_euler=orientation.to_euler()
        cutters_by_ceiling.setdefault(ceiling_name,[]).append(cut)
        fixture=place_light('Shared recessed downlight',lights['downlight'],'downlight',
                            (x,y,z),power=8 if is_vault(x,y) else 5)
        fixture.rotation_euler=orientation.to_euler()
        fixture['ceiling_mesh']=ceiling_name
        fixture['mounting_height_ft']=z
        fixture['mounting_normal']=list(normal)
        fixture['fixture_direction']='Housing +Z into ceiling; emission -Z into occupied room'
    # Each ceiling receives its own genuine holes. Sloped fixtures and their
    # host-owned lights rotate together; there are no floating flat-level lights.
    for ceiling_name,cutters in cutters_by_ceiling.items():
        ceiling=bpy.data.objects[ceiling_name]
        bpy.ops.object.select_all(action='DESELECT')
        for obj in cutters:obj.select_set(True)
        bpy.context.view_layer.objects.active=cutters[0]
        bpy.ops.object.join();cut=cutters[0]
        mod=ceiling.modifiers.new('Real downlight service openings','BOOLEAN')
        mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
        bpy.context.view_layer.objects.active=ceiling
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(cut,do_unlink=True)
    # Concealed task lighting beneath the east floating shelf, directed at preparation surface.
    place_light('Shared preparation task strip',lights['taskbar'],'taskbar',(66.5,36.8,5.31),rotation=math.pi/2,power=7)

def dependencies():
    return hardware_dependencies(HARDWARE)+[{'id':'fixtures/'+slug,'version':'v001','path':'../../library/fixtures/'+slug+'/v001/'} for slug in ['lighting-recessed-downlight-3in','lighting-undercabinet-bar-4ft']]


def verify_saved(scene):
    """Measure reopened fixture geometry, supports and cutouts without edits.

    Rays target only the evaluated ceiling mesh, so a fixture's own housing
    cannot masquerade as roof support. A clear center plus four present collar
    samples verifies each opening rather than accepting a missing ceiling.
    """
    import json
    from pathlib import Path
    from roof_design import ceiling_height, ceiling_slope, roof_metadata

    assert bpy.data.filepath, 'Lighting verification requires a reopened saved model'
    project_path=Path(bpy.data.filepath).parent.parent/'project.json'
    project=json.loads(project_path.read_text())
    assert project['roof_pavilion']==roof_metadata(), 'Saved project roof metadata differs from current geometry rules'
    graph=bpy.context.evaluated_depsgraph_get()
    objects=scene.objects
    fixtures=[o for o in objects if o.instance_type=='COLLECTION' and o.instance_collection
              and o.get('shared_asset')=='fixtures/lighting-recessed-downlight-3in/v001']
    assert len(fixtures)==25, ('Expected 25 actual linked downlights',len(fixtures))
    groups={'vault':0,'flat':0}
    records=[]

    def ceiling_ray(name,point,normal,before=.12,span=.55):
        target=objects[name].evaluated_get(graph)
        inverse=target.matrix_world.inverted()
        start=point-normal*(before*F)
        finish=start+normal*(span*F)
        local_start=inverse@start
        local_delta=inverse@finish-local_start
        hit,location,local_normal,face=target.ray_cast(local_start,local_delta.normalized(),distance=local_delta.length)
        if not hit:return None
        hit_normal=(target.matrix_world.to_3x3().inverted().transposed()@local_normal).normalized()
        return target.matrix_world@location,hit_normal

    for fixture in fixtures:
        assert fixture.instance_collection.library, ('Downlight is not linked',fixture.name)
        position=fixture.matrix_world.translation
        x,y,z=position/F
        wanted_z,normal,mesh_name=ceiling_surface(x,y)
        normal=Vector(normal)
        assert abs(z-wanted_z)<.0001, ('Downlight canopy misses ceiling',fixture.name,z,wanted_z)
        axis=(fixture.matrix_world.to_quaternion()@Vector((0,0,1))).normalized()
        assert (axis-normal).length<1e-5, ('Downlight housing normal mismatch',fixture.name)
        assert not near_exposed_frame(x,y), ('Downlight intersects frame zone',fixture.name)
        assert fixture.get('ceiling_mesh')==mesh_name
        assert abs(fixture.get('mounting_height_ft')-wanted_z)<.0001
        assert (Vector(fixture.get('mounting_normal'))-normal).length<1e-5
        assert max(abs(v-1) for v in fixture.scale)<1e-6, 'Linked downlight scaled'
        sources=[child for child in fixture.children if child.type=='LIGHT']
        assert len(sources)==1
        emission=(sources[0].matrix_world.to_quaternion()@Vector((0,0,-1))).normalized()
        assert (emission+normal).length<1e-5, ('Downlight emission does not follow ceiling',fixture.name)
        expected_source=position-normal*(.022*F)
        assert (sources[0].matrix_world.translation-expected_source).length<.0001*F
        assert ceiling_ray(mesh_name,position,normal) is None, ('Downlight ceiling is not actually cut',fixture.name)
        sx,sy=ceiling_slope(x,y)
        tangents=[Vector((1,0,sx)).normalized(),Vector((0,1,sy)).normalized()]
        collar_errors=[]
        for tangent in tangents:
            for sign in [-1,1]:
                sample=position+tangent*(sign*.20*F)
                hit=ceiling_ray(mesh_name,sample,normal)
                assert hit is not None, ('Missing ceiling beside downlight opening',fixture.name)
                location,hit_normal=hit
                error=(location-sample).length/F
                assert error<.001, ('Ceiling collar not at mounting plane',fixture.name,error)
                assert abs(hit_normal.dot(normal))>.9999
                collar_errors.append(error)
        kind='vault' if is_vault(x,y) else 'flat';groups[kind]+=1
        records.append({'fixture':fixture.name,'region':kind,'ceiling':mesh_name,
                        'mounting_height_ft':round(z,6),'normal_error':float((axis-normal).length),
                        'open_center_ray':True,'solid_collar_rays':4,
                        'maximum_collar_contact_error_ft':max(collar_errors)})
    assert groups=={'vault':8,'flat':17}, ('Unexpected vault/flat fixture distribution',groups)

    pendants=[o for o in objects if o.instance_type=='COLLECTION' and o.instance_collection
              and o.get('shared_asset_id')=='fixtures/lighting-linear-pendant-4ft-vault-3in12']
    assert len(pendants)==1, ('Expected one linked sloped-ceiling pendant',len(pendants))
    pendant=pendants[0]
    assert pendant.instance_collection.library
    assert max(abs(v-1) for v in pendant.scale)<1e-6, 'Pendant asset was stretched'
    contact_errors=[];mounts=0
    for obj in pendant.instance_collection.all_objects:
        if not obj.get('ceiling_contact_top_vertices'):continue
        mounts+=1
        transform=pendant.matrix_world@obj.matrix_world
        for vertex in obj.data.vertices[:4]:
            point=transform@vertex.co
            x,y,z=point/F
            height,normal,mesh_name=ceiling_surface(x,y)
            error=abs(z-height)
            assert error<.0001, ('Pendant mounting plate misses designed ceiling',obj.name,error)
            assert not near_exposed_frame(x,y,.35), ('Pendant mounting plate overlaps exposed beam',obj.name)
            hit=ceiling_ray(mesh_name,point,Vector(normal),before=.06,span=.20)
            assert hit is not None, ('No actual ceiling supporting pendant',obj.name)
            actual_error=(hit[0]-point).length/F
            assert actual_error<.001, ('Pendant plate misses actual ceiling',obj.name,actual_error)
            contact_errors.append(actual_error)
    assert mounts==3 and len(contact_errors)==12
    lens=next(o for o in pendant.instance_collection.all_objects if 'level opal diffuser' in o.name)
    lens_matrix=pendant.matrix_world@lens.matrix_world
    lens_points=[lens_matrix@Vector(v) for v in lens.bound_box]
    lens_bottom=min(p.z for p in lens_points)/F
    assert abs(lens_bottom-8.55)<.0001, ('Dining diffuser height changed',lens_bottom)
    for axis in [(1,0,0),(0,1,0)]:
        assert abs((lens_matrix.to_3x3()@Vector(axis)).normalized().z)<1e-6, 'Dining lightbar is not horizontal'
    px,py,pz=pendant.matrix_world.translation/F
    assert abs(pz-ceiling_height(px,py))<.0001
    assert abs(pendant.get('diffuser_height_ft')-lens_bottom)<.0001
    lights=[child for child in pendant.children if child.type=='LIGHT']
    assert len(lights)==1
    assert ((lights[0].matrix_world.to_quaternion()@Vector((0,0,-1)))-Vector((0,0,-1))).length<1e-6
    assert abs(lights[0].matrix_world.translation.z/F-(lens_bottom-.005))<.0001
    return {'reopened_native_geometry_checked':True,'roof_metadata_matches_current_design':True,
            'downlights':groups,'total_actual_ceiling_openings':len(records),
            'opening_evidence':'Each center ray passes through, four collar rays hit the actual ceiling mounting plane',
            'fixtures':records,'pendant':{'linked_variant':'lighting-linear-pendant-4ft-vault-3in12/v001',
            'mounting_faces':mounts,'actual_ceiling_contact_vertices':len(contact_errors),
            'maximum_contact_error_ft':max(contact_errors),'level_diffuser_height_ft':lens_bottom,
            'vertical_emission':True,'unscaled_asset':True},
            'limits':'Native geometry and placement checks; no rated photometry, electrical or structural approval.'}
