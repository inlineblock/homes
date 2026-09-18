"""Reopened-geometry checks. Does not certify construction or commercial systems."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
from design import *
F=.3048;s=bpy.context.scene;HOME=ROOT/'homes'/SLUG

def bounds(o):
    pts=[o.matrix_world@Vector(v) for v in o.bound_box]
    return tuple(min(getattr(p,a)/F for p in pts) for a in 'xyz')+tuple(max(getattr(p,a)/F for p in pts) for a in 'xyz')
def intersects(a,b,tol=.002):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>tol for i in range(3))
links=[]
for lib in bpy.data.libraries:
    assert lib.filepath.startswith('//'),lib.filepath
    p=Path(bpy.path.abspath(lib.filepath)).resolve();assert p.is_file() and p.is_relative_to(ROOT);links.append(lib.filepath)
assert len(links)==4
floor=bpy.data.objects['Gross enclosed floor'];area=floor.dimensions.x*floor.dimensions.y/F**2;assert abs(area-AREA)<.02
assert len([o for o in s.objects if ' bed frame' in o.name])==3
# Test every panel component against actual pocket/wall solids through its travel.
statics=[o for o in s.objects if o.type=='MESH' and o.get('ifc_class')=='IfcWall']
panels=[o for o in s.objects if o.get('opening_system')]
checks=0
for f in [1,20,40,60,80,100,120]:
    s.frame_set(f);bpy.context.view_layer.update()
    for o in panels:
        a=bounds(o)
        for other in statics:
            assert not intersects(a,bounds(other)),(f,o.name,other.name,'panel/wall collision')
        checks+=1
s.frame_set(120);bpy.context.view_layer.update()
for name,spec in [('Great room',DOOR),('Serving window',WINDOW)]:
    group=[bounds(o) for o in panels if o['opening_system']==name]
    if spec['pocket_center']<spec['start']:assert max(bb[3] for bb in group)<spec['start']-.10
    else:assert min(bb[0] for bb in group)>spec['end']+.05
# A swept 30-inch diameter route checks actual room/hall furniture and walls.
# 30 inches is a concept sanity check, not an accessible route or code finding.
obstacles=[]
for o in s.objects:
    if o.type!='MESH':continue
    groups=[c.name for c in o.users_collection]
    if not any(c.startswith(('01 Architecture','03 Kitchen','04 Furnishings')) for c in groups):continue
    bb=bounds(o)
    if bb[2]<6 and bb[5]>.30:obstacles.append((o.name,bb))
# Centerline paths deliberately continue into the room, not just to a wall label.
routes={
 'entry to dining terrace':[(20,-2),(20,18.7),(25,18.7),(42,18.7),(42,34),(36,36),(36,42),(39,46)],
 'primary bedroom':[(20,10),(20,13.2),(13.45,13.2),(13.45,10.9)],
 'primary bath':[(13.45,13.2),(5.5,13.2),(5.5,18.1)],
 'bedroom 02':[(26.65,18.7),(26.65,14),(26.65,12)],
 'bedroom 03':[(44.65,18.7),(44.65,14),(44.65,12)],
 'guest bath':[(58,18.7),(58,2.25),(62,2.25)],
 'laundry':[(58,18.7),(58,11.65),(62,11.65)],
 'kitchen work aisle':[(42,34),(47,34),(62,34),(62,29)],
}
for name,points in routes.items():
    for a,b in zip(points,points[1:]):
        n=max(1,math.ceil(math.dist(a,b)/.12))
        for i in range(n+1):
            x=a[0]+(b[0]-a[0])*i/n;y=a[1]+(b[1]-a[1])*i/n
            for obj,bb in obstacles:
                dx=max(bb[0]-x,0,x-bb[3]);dy=max(bb[1]-y,0,y-bb[4])
                assert math.hypot(dx,dy)>=1.25-.02,(name,obj,round(x,2),round(y,2),'walking route obstructed')
# Counter continuity and serving aperture remain separate from stone.
bridge=bounds(bpy.data.objects['Continuous stone sill serving bridge']);s.frame_set(1);bpy.context.view_layer.update()
windowbottom=min(bounds(o)[2] for o in panels if o['opening_system']=='Serving window')
assert windowbottom>bridge[5]
outer_top=bounds(bpy.data.objects['Exterior serving stone counter'])
outer_front=max(bounds(o)[4] for o in s.objects if o.name.startswith('Exterior serving drawer front'))
overhang=outer_top[4]-outer_front
assert overhang>=1.0,('insufficient counter knee overhang',overhang)
report={'native_model_reopened':True,'gross_enclosed_area_sqft':round(area,2),'modeled_beds':3,'relative_libraries':links,'opening_travel':{'sampled_frames':[1,20,40,60,80,100,120],'panel_component_checks':checks,'no_panel_wall_collisions':True,'both_clear_openings_unobstructed_by_panels':True},'circulation':{'swept_diameter_inches':30,'routes':list(routes),'actual_geometry_checked':True},'counter':{'stone_top_ft':round(bridge[5],3),'closed_window_bottom_ft':round(windowbottom,3),'no_glass_stone_intersection':True,'outdoor_knee_overhang_inches':round(overhang*12,2)},'limits':'Concept geometry only. No weatherproofing, thermal, structural, impact/flood or accessibility approval.'}
(HOME/'model/model-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('COASTAL_VERIFIED',json.dumps(report),flush=True)
# IFC exporter can follow this script: leave scene at closed frame, do not save blend.
