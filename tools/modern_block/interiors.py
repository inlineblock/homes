"""Modern Block interior placement. Meter coordinates; linked immutable assets.

The layout is an original interpretation. All equipment is conceptual, with
full-size rigid placement; no manufacturer or installation certification.
"""
import json
import math
from pathlib import Path
import bpy
from common import geometry as g
from common.library import linked_collection
from modern_block import utils
import design as d

PI = math.pi
CAMERAS = {
    'interior_living': ((17.8, 6.6, d.GROUND + 1.62), (18.7, 3.3, d.GROUND + 1.25), 20),
    'interior_kitchen': ((14.3, 12.5, d.GROUND + 1.62), (12.8, 17.2, d.GROUND + 1.35), 21),
    'interior_primary': ((16.05, 6.0, d.UPPER + 1.60), (13.3, 2.7 + d.UPPER_FRONT / 2, d.UPPER + 1.05), 24),
}

def box(name, loc, size, mat=None, bevel=0):
    return g.box(name, [v/g.F for v in loc], [v/g.F for v in size], mat, bevel/g.F)

def rod(name, a, b, r, mat):
    return g.rod(name, [v/g.F for v in a], [v/g.F for v in b], r/g.F, mat)

def area(name, loc, target, energy, size, color=(1,.86,.71)):
    return g.area(name, [v/g.F for v in loc], [v/g.F for v in target], energy, size/g.F, color)


def build_interiors(root, M):
    root=Path(root)
    ground_ceiling = d.GROUND + d.GROUND_CLEAR
    upper_ceiling = d.UPPER + d.UPPER_CLEAR
    ground_roof = getattr(d, 'GROUND_ROOF_Z', ground_ceiling + .13)
    flue_bottom = d.GROUND + 1.15
    flue_top = d.UPPER_ROOF_Z + .36
    # Move the primary sleeping group into the enlarged front half of the room.
    # Wet fixtures retain their supported footprint at Y >= 0.
    primary_front_shift = d.UPPER_FRONT / 2
    cache={}
    usage={}
    plan=[]
    def asset(category,slug,name,loc,rotation=0):
        key=(category,slug)
        if key not in cache: cache[key]=linked_collection(root,category,slug)
        o=bpy.data.objects.new(name,None)
        o.instance_type='COLLECTION';o.instance_collection=cache[key]
        g.ACTIVE.objects.link(o);o.location=loc;o.rotation_euler.z=rotation
        o['asset_id']=f'{category}/{slug}';o['asset_version']='v001';o['version']='v001'
        if 'bed' in slug and category=='furniture': o['bed_count']=1
        usage_entry=usage.setdefault(f'{category}/{slug}',{'id':f'{category}/{slug}','version':'v001','instances':[]})
        usage_entry['instances'].append(name)
        if category in ('furniture','cabinetry','appliances','fixtures') and 'lighting-' not in slug:
            meta=json.loads((root/'library'/category/slug/'v001'/'asset.json').read_text())
            bounds=meta.get('bounds_m')
            if bounds:
                x0,y0,_=bounds['min']; x1,y1,_=bounds['max']
            else:
                w,h,_=meta['dimensions_m'];x0,y0,x1,y1=-w/2,-h/2,w/2,h/2
            cs,sn=math.cos(rotation),math.sin(rotation)
            corners=[[round(loc[0]+x*cs-y*sn,4),round(loc[1]+x*sn+y*cs,4)] for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]]
            plan.append({'name':name,'kind':category,'asset_id':f'{category}/{slug}','level':'upper' if loc[2]>=d.UPPER-.01 else 'ground','x':loc[0],'y':loc[1],'z':loc[2],'rotation_rad':rotation,'corners_m':corners})
        return o
    def mat(key,slug):
        if key in M:return M[key]
        p=root/'library'/'materials'/slug/'v001'/f'{slug}.blend'
        with bpy.data.libraries.load(str(p),link=True) as (src,dst):dst.materials=[src.materials[0]]
        usage[f'materials/{slug}']={'id':f'materials/{slug}','version':'v001','instances':['Interior host millwork and finishes']}
        return dst.materials[0]
    oak=mat('oak','coastal-white-oak')
    stone=mat('stone','coastal-honed-limestone')
    dark=mat('dark','charcoal-facade-panel')
    plaster=mat('plaster','warm-limestone-plaster')
    def base(name,x,y,z=d.GROUND,rotation=0):return asset('cabinetry','oak-drawer-base-2ft',name,(x,y,z),rotation)
    def wardrobe(name,x,y,z=d.GROUND,rotation=0):return asset('cabinetry','oak-wardrobe-2ft',name,(x,y,z),rotation)
    def shelving(name,x,y,z=d.GROUND,rotation=0):return asset('cabinetry','oak-shelving-2ft',name,(x,y,z),rotation)
    def furniture(slug,name,loc,rotation=0):return asset('furniture',slug,name,loc,rotation)
    def fixture(slug,name,loc,rotation=0):return asset('fixtures',slug,name,loc,rotation)
    def counter_hole(name,x0,x1,y0,y1,hx0,hx1,hy0,hy1,z=d.GROUND+.93,th=.05):
        # Four separate solid pieces form a true rectangular mounting aperture.
        for label,a,b,c,d in [('west',x0,hx0,y0,y1),('east',hx1,x1,y0,y1),('south',hx0,hx1,y0,hy0),('north',hx0,hx1,hy1,y1)]:
            if b>a and d>c:box(f'{name} | {label}',((a+b)/2,(c+d)/2,z-th/2),(b-a,d-c,th),stone,.008)
    def vanity(name,x,y,z=d.GROUND,rotation=0,count=1,pitch=.96,width=None):
        # Counter/basins sit over real linked drawer modules; vessel basin is above its mounting plane.
        for i in range(count):
            xx=x+(i-(count-1)/2)*pitch
            base(f'{name} drawer {i+1}',xx,y,z,rotation)
            fixture('vanity-basin-mixer-mirror',f'{name} basin {i+1}',(xx,y,z+.92),rotation)
        box(f'{name} continuous counter',(x,y,z+.895),(width or count*pitch,.65,.05),stone,.012)
    def bed(name,kind,loc,rotation=0):
        furniture(f'oak-linen-{kind}-bed',name,loc,rotation)
        half=1.43 if kind=='king' else 1.23
        # Nightstands towards the head, transformed with the linked bed.
        for side in [-1,1]:
            dx=side*half;dy=-.72
            x=loc[0]+dx*math.cos(rotation)-dy*math.sin(rotation)
            y=loc[1]+dx*math.sin(rotation)+dy*math.cos(rotation)
            furniture('oak-open-nightstand',f'{name} bedside {side}',(x,y,loc[2]),rotation+PI)
    g.collection('Interior | ground living and dining')
    furniture('woven-oatmeal-rug','Living woven rug',(17.7,3.55,d.GROUND+.012),PI/2)
    furniture('linen-three-seat-sofa','Living ivory sofa',(16.65,3.55,d.GROUND+.028),-PI/2)
    furniture('oak-rounded-coffee-table','Living low oak table',(18.25,3.55,d.GROUND+.026),PI/2)
    for y in [2.55,4.5]:
        c=furniture('olive-linen-cushion','Living olive cushion',(16.27,y,d.GROUND+.40),-PI/2)
        c.rotation_euler.x=-.16
    for xx in [18.0,19.3]:furniture('coastal-outdoor-lounge-chair','Living oak lounge chair',(xx,1.1,d.GROUND+.02))
    # A one-off masonry fire surround with the firebox opening left genuinely empty.
    fixture('closed-glass-fireplace-48in','Living closed glass hearth',(21.56,3.55,d.GROUND+.28),-PI/2)
    box('Living limestone hearth',(21.5,3.55,d.GROUND+.16),(.95,3.3,.24),stone,.035)
    pier_bottom = d.GROUND + 1.18
    box('Living masonry upper pier',(21.65,3.55,(pier_bottom+ground_ceiling)/2),(.70,3.3,ground_ceiling-pier_bottom),dark,.018)
    for yy in [2.44,4.66]:box('Living masonry firebox jamb',(21.65,yy,d.GROUND+.74),(.70,.99,.92),stone,.01)
    # Continuous conceptual non-combustible flue, within the exterior masonry bay.
    box('Living conceptual concealed flue',(22.42,3.55,(flue_bottom+flue_top)/2),(.24,.24,flue_top-flue_bottom),dark)
    box('Living conceptual flue offset',(22.08,3.55,d.GROUND+1.45),(.92,.24,.24),dark)
    furniture('oak-dining-table-8ft','Dining oak table',(13.0,9.8,d.GROUND+.02),PI/2)
    for yy in [9.0,9.8,10.6]:
        furniture('oak-upholstered-dining-chair','Dining east chair',(13.95,yy,d.GROUND+.02),-PI/2)
        furniture('oak-upholstered-dining-chair','Dining west chair',(12.05,yy,d.GROUND+.02),PI/2)
    furniture('oak-upholstered-dining-chair','Dining south end chair',(13.0,8.1,d.GROUND+.02),PI)
    furniture('oak-upholstered-dining-chair','Dining north end chair',(13.0,11.5,d.GROUND+.02))
    fixture('lighting-linear-pendant-4ft','Dining linear pendant',(13,9.8,ground_ceiling),PI/2)
    area('Dining warm pool',(13,9.8,ground_ceiling-.85),(13,9.8,d.GROUND+.75),130,1.2)
    # Entry coat storage is tucked onto the eastern service wall, outside stair access.
    for yy in [8.0,8.61]:wardrobe('Foyer coats',18.35,yy,d.GROUND,-PI/2)

    g.collection('Interior | kitchen and service')
    # North wall run. Full-size appliance bays interrupt cabinetry.
    for x in [10.65,11.26,13.19,13.80]:base('Kitchen north drawer',x,19.43)
    asset('appliances','built-in-oven-30in','Kitchen built-in oven',(12.22,19.43,d.GROUND+.11))
    for x in [11.78,12.66]:box('Kitchen oven bay side',(x,19.43,d.GROUND+.455),(.045,.65,.87),oak)
    counter_hole('Kitchen rear stone top',10.33,14.13,19.06,19.78,11.78,12.66,19.175,19.685)
    asset('appliances','induction-cooktop-36in','Kitchen induction cooktop',(12.22,19.43,d.GROUND+.934))
    asset('appliances','wall-hood-36in','Kitchen wall hood',(12.22,19.55,d.GROUND+1.68))
    hood_duct_bottom = d.GROUND + 2.34
    hood_duct_top = ground_roof + .35
    box('Kitchen hood exhaust to roof',(12.22,19.7,(hood_duct_bottom+hood_duct_top)/2),(.29,.26,hood_duct_top-hood_duct_bottom),dark)
    asset('appliances','panel-ready-fridge-48in','Kitchen wide refrigeration',(15.08,19.31,d.GROUND+.02))
    # Project-specific refrigerator niche, no solid obstruction in the appliance volume.
    for xx in [14.4,15.76]:box('Kitchen refrigerator niche cheek',(xx,19.4,d.GROUND+1.32),(.055,.83,2.64),oak)
    box('Kitchen refrigerator overhead',(15.08,19.4,d.GROUND+2.43),(1.30,.83,.42),oak,.01)
    # True under-mount sink hole in the long island; sink working face is east.
    counter_hole('Kitchen island top',12.4,13.85,14.0,18.10,12.955,13.445,16.665,17.335)
    fixture('kitchen-sink-mixer-650','Kitchen island sink',(13.2,17.0,d.GROUND+.934),PI/2)
    asset('appliances','dishwasher-24in','Kitchen integrated dishwasher',(13.48,16.08,d.GROUND+.02),PI/2)
    for yy in [14.36,14.97,17.76]:base('Kitchen island drawer',13.48,yy,d.GROUND,PI/2)
    # Closed sink cabinet front belongs to this bespoke island; interior recess remains empty.
    box('Kitchen sink false apron',(13.81,17.0,d.GROUND+.50),(.035,.74,.73),oak,.008)
    for yy in [16.62,17.37]:box('Kitchen sink cabinet cheek',(13.44,yy,d.GROUND+.445),(.70,.04,.87),oak)
    box('Kitchen island continuous back',(12.80,16.05,d.GROUND+.44),(.045,4.02,.85),oak)
    for yy in [14.035,18.065]:box('Kitchen stone waterfall',(13.125,yy,d.GROUND+.47),(1.45,.07,.92),stone,.012)
    for yy in [14.5,15.5,16.5,17.5]:furniture('coastal-oak-counter-stool','Kitchen oak stool',(12.05,yy,d.GROUND+.02),PI/2)
    # Linked task-light bars are mounted beneath the shelf rather than buried in it.
    box('Kitchen floating display shelf',(11.05,19.65,d.GROUND+1.59),(1.48,.29,.05),oak,.01)
    fixture('lighting-undercabinet-bar-4ft','Kitchen task bar',(11.05,19.49,d.GROUND+1.555))
    area('Kitchen task light',(11.05,19.45,d.GROUND+1.54),(11.05,19.42,d.GROUND+.93),45,1.1)
    for x in [16.48,17.09,17.70]:shelving('Pantry storage',x,15.52)
    for yy in [14.13,14.8]:asset('appliances','front-loading-laundry-600','Laundry washer' if yy<14.5 else 'Laundry dryer',(21.48,yy,d.GROUND+.02),-PI/2)
    box('Laundry work surface',(21.45,14.465,d.GROUND+.92),(.76,1.41,.05),stone,.012)
    shelving('Laundry tall linen',19.45,15.48)
    vanity('Ground powder vanity',16.95,19.52)
    fixture('toilet-elongated','Ground powder WC',(18.3,19.4,d.GROUND+.02))
    for yy in [13.72,14.33]:shelving('Pantry side shelf',18.5,yy,d.GROUND,-PI/2)

    g.collection('Interior | upper bedrooms')
    bed('Primary king bed','king',(13.45,2.05+primary_front_shift,d.UPPER+.02))
    furniture('woven-oatmeal-rug','Primary rug',(13.5,3.4+primary_front_shift,d.UPPER+.011))
    furniture('oak-writing-desk','Primary window desk',(11.16,5.94,d.UPPER+.02))
    furniture('oak-upholstered-dining-chair','Primary desk chair',(11.16,5.08,d.UPPER+.02),PI)
    for x in [19.18,19.79,20.40,21.01]:wardrobe('Primary dressing wardrobe',x,6.51,d.UPPER)
    bed('Upper west queen bed','queen',(12.45,14.75,d.UPPER+.02),PI)
    for x in [10.98,11.59,12.20,12.81]:wardrobe('Upper west wardrobe',x,11.47,d.UPPER,PI)
    bed('Upper east queen bed','queen',(20.35,15.35,d.UPPER+.02),PI/2)
    for y in [15.0,15.61,16.22]:wardrobe('Upper east wardrobe',17.48,y,d.UPPER,PI/2)

    for xx in [17.5,18.11]:shelving('Upper landing linen',xx,12.52,d.UPPER)

    g.collection('Interior | upper bathing')
    vanity('Primary double vanity',18.40,4.55,d.UPPER,count=2,pitch=1.05,width=2.4)
    fixture('freestanding-tub-72in','Primary freestanding tub',(19.05,1.03,d.UPPER+.02))
    # Bespoke tub filler is plumbing geometry, not a claimed product.
    rod('Primary tub filler riser',(19.95,1.04,d.UPPER),(19.95,1.04,d.UPPER+.79),.018,dark)
    rod('Primary tub filler spout',(19.95,1.04,d.UPPER+.79),(19.67,1.04,d.UPPER+.79),.018,dark)
    fixture('shower-tray-screen-1500x1200','Primary separate shower',(21.0,.78,d.UPPER+.02),PI)
    fixture('toilet-elongated','Primary enclosed WC',(21.08,4.43,d.UPPER+.02))
    vanity('Upper shared vanity',11.25,10.52,d.UPPER,count=2)
    fixture('toilet-elongated','Upper shared WC',(13.1,10.45,d.UPPER+.02))
    fixture('shower-tray-screen-900','Upper shared shower',(14.24,10.35,d.UPPER+.02))

    g.collection('Interior | guest pavilion')
    furniture('oak-writing-desk','Pavilion office desk',(-7.25,2.3,d.GROUND+.02),PI/2)
    furniture('oak-upholstered-dining-chair','Pavilion office chair',(-6.38,2.3,d.GROUND+.02),-PI/2)
    for yy in [.68,1.29]:wardrobe('Pavilion office closed storage',-2.45,yy,d.GROUND,-PI/2)
    furniture('oak-round-dining-table-1000','Pavilion reading table',(-3.9,3.4,d.GROUND+.02))
    furniture('oak-upholstered-dining-chair','Pavilion reading chair',(-3.9,2.55,d.GROUND+.02),PI)
    bed('Guest queen bed','queen',(-4.7,7.42,d.GROUND+.02),PI)
    for yy in [5.85,6.46,7.07]:wardrobe('Guest wardrobe',-7.48,yy,d.GROUND,PI/2)
    vanity('Guest bathroom vanity',-5.7,11.56,d.GROUND,count=2)
    fixture('toilet-elongated','Guest bathroom WC',(-3.85,11.42,d.GROUND+.02))
    fixture('shower-tray-screen-900','Guest bathroom shower',(-7.22,11.43,d.GROUND+.02))
    # Area sources complement architectural ceiling fittings from the host builder.
    for name,loc,target,power,size in [
        ('Living soft daylight',(11.1,3.1,ground_ceiling-.60),(18,3.5,d.GROUND+1),400,4),
        ('Kitchen soft daylight',(10.7,16.3,ground_ceiling-.70),(14.3,17,d.GROUND+1),300,3),
        ('Primary soft daylight',(11.0,1.5+primary_front_shift,upper_ceiling-.50),(14,3+primary_front_shift,d.UPPER+.60),180,2.5),
        ('Guest soft fill',(-5,8,ground_ceiling-.40),(-5,8,d.GROUND),75,2),
    ]:area(name,loc,target,power,size,(1,.93,.84))
    (root/'tools/modern_block/interiors-layout.json').write_text(json.dumps({'units':'meters','floor_datums_m':{'ground':d.GROUND,'upper':d.UPPER},'clear_ceiling_heights_m':{'ground':d.GROUND_CLEAR,'upper':d.UPPER_CLEAR},'placements':plan},indent=2)+'\n')
    return list(usage.values())
