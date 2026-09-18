"""Fresh-open native receipts; no claim of engineering or full code compliance."""
import bpy,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
import design
from interiors import FURNITURE,FIXTURES
HOME=ROOT/'homes/lindon-brick-house'
native=HOME/'model/lindon-brick-house.blend'
assert native.read_bytes()[:7]==b'BLENDER'
bpy.ops.wm.open_mainfile(filepath=str(native))
bpy.context.view_layer.update()
deps=[]
for library in bpy.data.libraries:
    assert library.filepath.startswith('//'),library.filepath
    p=Path(bpy.path.abspath(library.filepath)).resolve();assert p.is_relative_to(ROOT) and p.is_file(),p
    manifest=p.parent/'asset.json'
    if manifest.exists():
        m=json.loads(manifest.read_text());entry={'id':m['id'],'version':m['version'],'path':'../../'+str(p.parent.relative_to(ROOT))+'/'}
        if entry not in deps:deps.append(entry)
floor_areas={}
for o in bpy.context.scene.objects:
    if o.get('floor_area_role'):
        area=sum(p.area for p in o.data.polygons if p.normal.z>.9)
        floor_areas[o.get('level_key','garage')]=round(area/.3048**2,3)
assert all(k in floor_areas for k in ['main','upper','basement','garage'])
assert all(v>500 for v in floor_areas.values())
beds=[o for o in bpy.context.scene.objects if o.get('bed_count')==1]
assert len(beds)==7
evaluated_beds=[]
dg=bpy.context.evaluated_depsgraph_get()
for bed in beds:
    parts=[i for i in dg.object_instances if i.is_instance and i.parent and i.parent.original==bed and i.object.type=='MESH']
    assert parts,bed.name
    evaluated_beds.append({'name':bed.name,'evaluated_mesh_parts':len(parts)})
windows=[o for o in bpy.context.scene.objects if o.get('ifc_class')=='IfcWindow']
assert len(windows)>=15
brick=[]
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.library is None and any(m and m.name.startswith('Warm red brick |') for m in o.data.materials):
        assert o.data.uv_layers.get('Brick meters'),o.name
        brick.append(o.name)
assert len(brick)>40
cameras=[o.name for o in bpy.context.scene.objects if o.type=='CAMERA']
assert len(cameras)>=8
# Check the assembled appliance and roof geometry that previously produced
# visible defects, rather than only the presence of named host objects.
cooktops=[]
for name,counter_z in [('Main induction cooktop',.9565),('Second kitchen induction',-2.1935)]:
    host=bpy.data.objects[name]
    glass=[max((i.matrix_world@v.co).z for v in i.object.data.vertices) for i in dg.object_instances if i.is_instance and i.parent and i.parent.original==host and 'ceramic glass surface' in i.object.name]
    assert glass,name
    top=max(glass)
    assert .003<top-counter_z<.012,(name,top,counter_z)
    cooktops.append({'name':name,'glass_above_worktop_mm':round((top-counter_z)*1000,2)})
garagecap=bpy.data.objects['Garage setback roof and ceiling']
assert sum(p.area for p in garagecap.data.polygons if p.normal.z>.9)>1
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.modifiers.get('Folded roof thickness'):
        assert all(p.normal.z>0 for p in o.data.polygons),o.name
receipt={'native_reopened':True,'blender':bpy.app.version_string,'relative_asset_dependencies':sorted(deps,key=lambda d:d['id']),
 'measured_horizontal_floor_surfaces_sqft':floor_areas,'area_basis':'Top horizontal mesh faces after stair-void cuts; includes walls, excludes terrace/patio/site, garage listed separately.',
 'listing_area_sqft':6807,'measured_model_area_matches_listing':False,'source_registration':'Nondimensioned listing plans; modeled areas deliberately not forced to match unverified listing totals.',
 'bedroom_count':7,'evaluated_bed_instances':evaluated_beds,'window_assemblies':len(windows),'physical_brick_uv_meshes':len(brick),'cameras':cameras,
 'cooktop_host_checks':cooktops,'roof_face_orientation':'Upward; solidify extends beneath visible roof surfaces','garage_setback_cap':'Present; excludes upper occupied footprint',
 'unresolved':['Measured as-built dimensions and floor-area reconciliation','Engineering and building-envelope specifications','Product window performance and egress selection','Detailed full-home operating clearances and service routing','Existing solar and accessory pool structures not yet modeled']}
(HOME/'model/native-validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('LINDON_NATIVE_VERIFIED',json.dumps({k:v for k,v in receipt.items() if k not in ['relative_asset_dependencies','evaluated_bed_instances']}),flush=True)
