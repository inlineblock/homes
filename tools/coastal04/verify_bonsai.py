"""Coastal-specific checks after tools/common/verify_bonsai.py imports the IFC.

Run both scripts in a fresh normal Blender startup with Bonsai enabled:
Blender --background --python-exit-code 1 --python tools/common/verify_bonsai.py \
  --python tools/coastal04/verify_bonsai.py -- coastal-house
No scene/model is saved. Only the current Bonsai validation receipt is updated.
"""
import sys,json,hashlib
from pathlib import Path
import bpy,bonsai,bonsai.tool as tool
import ifcopenshell,ifcopenshell.geom,ifcopenshell.util.element
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
from roof_design import (roof_metadata,pavilion_roof_height,front_roof_height,
                        kitchen_roof_height,PAVILION_RIDGE,ROOF_SKIN_THICKNESS,
                        VAULT_ASSEMBLY_DEPTH,FRAME_Y,FRAME_POST_X,FRAME_DEPTH)
from verandah import PERGOLA_POSTS,PERGOLA_LEDGER_BOTTOM,PERGOLA_LEDGER_TOP,PERGOLA_BEAM_BOTTOM,PERGOLA_BEAM_TOP,PERGOLA_SLAT_COUNT
F=.3048
HOME=ROOT/'homes/coastal-house';FOLDER=HOME/'model'
manifest=json.loads((HOME/'project.json').read_text())
model=tool.Ifc.get();assert model is not None and model.schema=='IFC4'
assert manifest['roof_pavilion']==roof_metadata()
settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
cache={}

def product_geometry(entity):
    """Compare actual Bonsai world-space mesh to independent IFC tessellation."""
    if entity.id() in cache:return cache[entity.id()]
    obj=tool.Ifc.get_object(entity)
    assert obj is not None and obj.type=='MESH', ('Missing Bonsai product mesh',entity.Name)
    assert len(obj.data.vertices)>=4 and len(obj.data.polygons)>0, ('Empty import',entity.Name)
    points=[obj.matrix_world@v.co/F for v in obj.data.vertices]
    bounds=[min(p[a] for p in points) for a in range(3)]+[max(p[a] for p in points) for a in range(3)]
    shape=ifcopenshell.geom.create_shape(settings,entity)
    vertices=shape.geometry.verts
    native=[vertices[i:i+3] for i in range(0,len(vertices),3)]
    reference=[min(p[a] for p in native)/F for a in range(3)]+[max(p[a] for p in native)/F for a in range(3)]
    error=max(abs(a-b) for a,b in zip(bounds,reference))
    assert error<.003, ('Bonsai/IFC geometry mismatch',entity.Name,error)
    materials=[slot.material for slot in obj.material_slots if slot.material]
    assert materials, ('Missing actual imported surface material',entity.Name)
    result={'object':obj,'points':points,'bounds':bounds,'materials':materials,'import_bounds_error_ft':error}
    cache[entity.id()]=result
    return result

def bb(e):return product_geometry(e)['bounds']
def one(cls,name):
    found=[e for e in model.by_type(cls) if e.Name==name]
    assert len(found)==1,(cls,name,len(found))
    return found[0]
def matching(cls,prefix):return [e for e in model.by_type(cls) if (e.Name or '').startswith(prefix)]
def appearance(e):
    materials=product_geometry(e)['materials']
    return [{'name':m.name,'rgba':list(m.diffuse_color)} for m in materials]

# Retain and remeasure the attached full-opening pergola and entrance supports.
posts=matching('IfcColumn','Verandah timber column')
ledger=one('IfcBeam','Verandah attached structural header ledger')
outer=one('IfcBeam','Verandah timber-clad steel outer beam')
slats=matching('IfcMember','Verandah open shade slat')
entries=matching('IfcColumn','Entry canopy timber column')
assert len(posts)==2 and len(entries)==2 and len(slats)==PERGOLA_SLAT_COUNT
postbounds=sorted([bb(e) for e in posts],key=lambda b:b[0])
for bounds,(x,y) in zip(postbounds,sorted(PERGOLA_POSTS)):
    assert abs((bounds[0]+bounds[3])/2-x)<.01 and abs((bounds[1]+bounds[4])/2-y)<.01
    assert abs(bounds[5]-PERGOLA_BEAM_BOTTOM)<.01
lb,ob=bb(ledger),bb(outer)
assert abs(lb[2]-PERGOLA_LEDGER_BOTTOM)<.01 and abs(lb[5]-PERGOLA_LEDGER_TOP)<.01
assert abs(ob[2]-PERGOLA_BEAM_BOTTOM)<.01 and abs(ob[5]-PERGOLA_BEAM_TOP)<.01
for e in slats+entries:product_geometry(e)

# Four actual roof volumes with the correct slope, extent and skin thickness.
roofs=[]
for name,fn,axis,expected_xy in [
    ('Pavilion west 3 in 12 roof',pavilion_roof_height,0,(-3,18,22,43)),
    ('Pavilion east 3 in 12 roof',pavilion_roof_height,0,(22,18,47,43)),
    ('Front wing 1 in 12 roof',front_roof_height,1,(-2,-3.75,70,20)),
    ('Kitchen wing 1 in 12 roof',kitchen_roof_height,0,(44,20,71,43))]:
    entity=one('IfcRoof',name);geometry=product_geometry(entity);bounds=geometry['bounds']
    actual_xy=[bounds[0],bounds[1],bounds[3],bounds[4]]
    assert all(abs(a-b)<.01 for a,b in zip(actual_xy,expected_xy)),(name,actual_xy)
    errors=[min(abs(p.z-fn(p[axis])),abs(p.z-fn(p[axis])+ROOF_SKIN_THICKNESS)) for p in geometry['points']]
    assert max(errors)<.01,(name,max(errors))
    assert max(p.z for p in geometry['points'])-min(p.z for p in geometry['points'])>.5
    roofs.append({'name':name,'bounds_ft':bounds,'maximum_profile_error_ft':max(errors),'material':appearance(entity)})
assert abs(roofs[0]['bounds_ft'][5]-PAVILION_RIDGE)<.01
assert abs(roofs[1]['bounds_ft'][5]-PAVILION_RIDGE)<.01

# Genuine transparent upper panes, not counted empty names.
glass=matching('IfcWindow','Pavilion real upper glazing')
assert len(glass)==13
pane_rows=[]
for entity in glass:
    geometry=product_geometry(entity);bounds=geometry['bounds']
    assert bounds[2]>11 and bounds[5]>bounds[2]+.1
    assert abs(bounds[4]-bounds[1]-.035)<.005
    center_y=(bounds[1]+bounds[4])/2
    assert min(abs(center_y-20.0375),abs(center_y-40.0375))<.01
    assert all(p.z<=pavilion_roof_height(p.x)-VAULT_ASSEMBLY_DEPTH-.099 for p in geometry['points'])
    styles=ifcopenshell.util.element.get_styles(entity)
    transparencies=[item.Transparency for style in styles for item in style.Styles
                    if item.is_a('IfcSurfaceStyleShading') and item.Transparency is not None]
    assert transparencies and min(transparencies)>=.79, ('Upper pane lost transparency',entity.Name)
    pane_rows.append({'name':entity.Name,'bounds_ft':bounds,'surface_transparency':transparencies})
assert sum(' rear' in e.Name for e in glass)==8 and sum(' front' in e.Name for e in glass)==5
assert max(row['bounds_ft'][5] for row in pane_rows)>18

# Exposed frame follows the vault and is supported by six actual columns.
rafters=matching('IfcBeam','Pavilion exposed driftwood sloping rafter')
wood_posts=matching('IfcColumn','Pavilion driftwood structural frame post')
wet_posts=matching('IfcColumn','Pavilion encased wet-zone structural frame post')
ridge=one('IfcBeam','Pavilion exposed driftwood ridge beam')
assert len(rafters)==6 and len(wood_posts)==5 and len(wet_posts)==1
pergola_material=product_geometry(posts[0])['materials'][0]
for entity in rafters+wood_posts+[ridge]:
    geometry=product_geometry(entity)
    assert geometry['materials'][0]==pergola_material, ('Timber style differs from attached pergola',entity.Name)
for entity in rafters:
    b=bb(entity)
    assert b[5]-b[2]>4 and b[3]-b[0]>20
    assert min(abs((b[1]+b[4])/2-y) for y in FRAME_Y)<.01
wet=wet_posts[0];wet_material=product_geometry(wet)['materials'][0]
assert wet_material!=pergola_material
assert 'limestone' in wet_material.name.lower()
assert max(abs(a-b) for a,b in zip(wet_material.diffuse_color,pergola_material.diffuse_color))>.03
frame_bounds=[]
for entity in wood_posts+wet_posts:
    bounds=bb(entity);x=(bounds[0]+bounds[3])/2;y=(bounds[1]+bounds[4])/2
    assert min(abs(x-v) for v in FRAME_POST_X)<.01 and min(abs(y-v) for v in FRAME_Y)<.01
    assert abs(bounds[2])<.01
    expected_top=pavilion_roof_height(x)-VAULT_ASSEMBLY_DEPTH-FRAME_DEPTH
    assert abs(bounds[5]-expected_top)<.01
    mates=[bb(r) for r in rafters if abs((bb(r)[1]+bb(r)[4])/2-y)<.01 and min(bb(r)[3],bounds[3])>max(bb(r)[0],bounds[0])]
    assert any(abs(bounds[5]-b[2])<.03 for b in mates),('Post misses actual sloping rafter',entity.Name)
    frame_bounds.append({'name':entity.Name,'bounds_ft':bounds})
assert abs(bb(ridge)[5]-(PAVILION_RIDGE-VAULT_ASSEMBLY_DEPTH))<.01

# Full modules and perimeter cuts retain actual panel dimensions and joint rows.
schedule=manifest['facade_panel_schedule']
full=matching('IfcCovering','Shared limestone facade full panel')
cuts=matching('IfcCovering','Limestone facade bespoke perimeter cut')
assert len(full)==schedule['full_linked_panels']==5 and len(cuts)==schedule['bespoke_edge_cuts']==31
panel_manifest=json.loads((ROOT/'library'/schedule['asset']/schedule['version']/'asset.json').read_text())
expected_full=[v/F for v in panel_manifest['dimensions_m']]
for entity in full:
    bounds=bb(entity)
    assert all(abs(bounds[i+3]-bounds[i]-expected_full[i])<.005 for i in range(3))
for entity in full+cuts:
    bounds=bb(entity);w= bounds[3]-bounds[0];h=bounds[5]-bounds[2]
    assert .1<w<=4.005 and .1<h<=2.005
    assert abs(bounds[1]-40.63)<.005 and abs(bounds[4]-bounds[1]-.125)<.005
    assert product_geometry(entity)['materials'][0]==wet_material
panel_rows=[]
for x1,x2 in [(0.,4.5),(40.3,47.7),(63.4,68.)]:
    pier=[e for e in full+cuts if bb(e)[0]>=x1-.005 and bb(e)[3]<=x2+.005]
    assert len(pier)==12
    for row in range(6):
        bottom=.02+row*(schedule['nominal_course_height_ft']+schedule['joint_ft'])
        pair=sorted([bb(e) for e in pier if abs(bb(e)[2]-bottom)<.005],key=lambda b:b[0])
        assert len(pair)==2
        assert abs(pair[0][0]-x1)<.005 and abs(pair[1][3]-x2)<.005
        assert abs(pair[1][0]-pair[0][3]-schedule['joint_ft'])<.005
        panel_rows.append({'pier_x_ft':[x1,x2],'course':row,'bottom_ft':bottom,'panel_widths_ft':[b[3]-b[0] for b in pair]})

receipt=json.loads((FOLDER/'bonsai-validation.json').read_text())
receipt.update({'blender_version':bpy.app.version_string,'bonsai_version':'.'.join(map(str,bonsai.bl_info['version'])) if hasattr(bonsai,'bl_info') else '0.8.5',
 'ifcopenshell_version':ifcopenshell.version,'ifc_sha256':hashlib.sha256((FOLDER/'coastal-house.ifc').read_bytes()).hexdigest(),
 'source_blend_sha256':hashlib.sha256((FOLDER/'coastal-house.blend').read_bytes()).hexdigest(),'closed_envelope_frame':1,
 'attached_pergola':{'seaward_posts':2,'house_side_posts':0,'post_bounds_ft':postbounds,'header_ledger_bounds_ft':lb,'outer_beam_bounds_ft':ob,'open_slats':len(slats),'actual_bonsai_member_objects_checked':True},
 'entry_canopy_supports':2,'roof_pavilion':{'metadata_matches_current_design':True,'actual_roof_planes':roofs,'upper_glazing':pane_rows,
 'sloping_rafters':len(rafters),'frame_columns':frame_bounds,'stone_encased_wet_zone_posts':1,'wet_zone_material':appearance(wet),'timber_matches_pergola':True},
 'facade_panels':{'source_schedule':schedule,'actual_full_panel_meshes':len(full),'actual_perimeter_cut_meshes':len(cuts),'module_dimensions_ft':expected_full,'checked_courses':panel_rows,'limestone_material_matches_wet_post':True},
 'actual_import_geometry':{'checked_product_meshes':len(cache),'maximum_bonsai_vs_ifc_bounds_error_ft':max(v['import_bounds_error_ft'] for v in cache.values())},
 'limits':'Actual IFC tessellation and Bonsai mesh geometry, material appearance and source hashes checked; original classified concept geometry is not engineered construction documentation.'})
(FOLDER/'bonsai-validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('COASTAL_PAVILION_BONSAI_VERIFIED',json.dumps({'mesh_checks':len(cache),'roofs':len(roofs),'upper_glazing':len(glass),'facade_full':len(full),'facade_cuts':len(cuts)}),flush=True)
