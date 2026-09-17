"""Meaningful concept checks; no engineering or manufacturer approval implied."""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
from design import *
HOME=ROOT/'homes/garage-loft-03';scene=bpy.context.scene;F=.3048
links=[]
for lib in bpy.data.libraries:
    assert lib.filepath.startswith('//'),lib.filepath
    path=Path(bpy.path.abspath(lib.filepath)).resolve();assert path.is_relative_to(ROOT) and path.is_file(),path
    links.append(lib.filepath)
assert len(links)==6,links
floors=list(bpy.data.collections['02 Architecture | floors'].objects)
area=sum(o.dimensions.x*o.dimensions.y/F**2 for o in floors)
assert abs(area-GROSS_AREA)<.02,(area,GROSS_AREA)
upper_area=sum(o.dimensions.x*o.dimensions.y/F**2 for o in floors if o.get('ifc_storey')=='Game room')
assert abs(upper_area-UPPER_SLAB_AREA)<.02
cars=[o for o in scene.objects if o.name.startswith('Car ') and o.name.endswith(' body')];assert len(cars)==4
roof_heights=[]
for i in range(1,5):
    members=[o for o in scene.objects if o.name.startswith(f'Car {i} ')];zmax=max((o.matrix_world@Vector(v)).z/F for o in members for v in o.bound_box)
    roof_heights.append(zmax)
assert max(roof_heights)+PLATFORM_SPACING<GARAGE_CLEAR-.75
assert PLATFORM_SPACING-.2-CAR_HEIGHT>.7
assert PIT_REAR_DEPTH-PLATFORM_SPACING-.2>0
# Table envelope is calculated from actual linked playing surface, not its nominal name.
table=bpy.data.objects['Eight foot pool table'];playing=next(o for o in table.instance_collection.objects if o.name=='Billiard playing field')
width=playing.dimensions.x/F+2*CUE;length=playing.dimensions.y/F+2*CUE
assert abs(width-POOL_ENVELOPE[0])<.01 and abs(length-POOL_ENVELOPE[1])<.01
x,y=POOL_CENTER;cuebox=(x-width/2,y-length/2,x+width/2,y+length/2)
assert cuebox[0]>.5 and cuebox[1]>.5 and cuebox[2]<27.5 and cuebox[3]<27.5
# Check lounge and refreshment furniture projections do not intrude into cue envelope.
for o in bpy.data.collections['13 Game room | furnishings'].objects:
    if any(k in o.name for k in ['Lounge','Refreshment','Shared walnut']):
        if o.instance_collection:
            pts=[o.matrix_world@child.matrix_world@Vector(v) for child in o.instance_collection.objects if child.type=='MESH' for v in child.bound_box]
        else:pts=[o.matrix_world@Vector(v) for v in o.bound_box]
        a=min(p.x/F for p in pts);b=min(p.y/F for p in pts);c=max(p.x/F for p in pts);d=max(p.y/F for p in pts)
        assert c<=cuebox[0] or a>=cuebox[2] or d<=cuebox[1] or b>=cuebox[3],o.name
# Area-bearing upper floor pieces must leave the real stairwell void clear.
for o in floors:
    if o.get('ifc_storey')!='Game room':continue
    pts=[o.matrix_world@Vector(v) for v in o.bound_box]
    a,b=min(p.x/F for p in pts),min(p.y/F for p in pts);c,d=max(p.x/F for p in pts),max(p.y/F for p in pts)
    vx1,vy1,vx2,vy2=STAIR_VOID
    assert c<=vx1+.01 or a>=vx2-.01 or d<=vy1+.01 or b>=vy2-.01,o.name
report={'native_model_reopened':True,'relative_library_count':len(links),'relative_libraries':links,'car_proxies':len(cars),'projected_floor_area_sqft':round(area,2),'upper_slab_sqft':round(upper_area,2),'cue_envelope_ft':[round(width,3),round(length,3)],'max_raised_car_top_ft':round(max(roof_heights)+PLATFORM_SPACING,3),'garage_clear_height_ft':GARAGE_CLEAR,'pit_front_depth_in':PIT_FRONT_DEPTH*12,'pit_rear_depth_in':PIT_REAR_DEPTH*12,'stair_opening_clear':True,'status':'Concept geometry checks only; engineering and manufacturer coordination unresolved'}
(HOME/'model/model-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('GARAGE_VERIFIED',json.dumps(report),flush=True)
