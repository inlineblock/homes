"""Photo-informed, approximate Lindon landscape; meter coordinates, not a survey.

House/decks remain owned by architecture. Main grade is Z=0, with a localized
rear walkout court at -3.15 m and stairs back to the lawn. Shared native assets
are linked; only the site's terrain, driveway, steps and fitted fences are local.
"""
import math,random
import bpy
from common import geometry as g
from common.geometry import material
from common.materials import noise_material
from common.library import linked_collection
from utils import box,rod,prism,mesh,instance

ASSET_DEPENDENCIES = [
    ('fixtures','rectangular-pool-6x12m','v001'),
    ('surfaces','pickleball-court-30x60ft','v001'),
    ('furniture','slatted-outdoor-chaise','v001'),
    ('landscape','mountain-conifer','v002'),
    ('landscape','sage-shrub','v002'),
    ('landscape','flowering-perennial-clump','v001'),
    ('landscape','ornamental-grass-clump','v002'),
    ('landscape','olive-tree','v001'),
    ('surfaces','honed-limestone-paver-4ft','v001'),
]
SITE_BOUNDS=(-200,220,-200,220)
WEST_LIGHTWELLS=[(-1.8,0,.6,3.2),(-1.8,0,5.0,7.8)]
POOL_CENTER=(30,28)
COURT_CENTER=(39,4.5)
PATIO_BOUNDS=(8.8,19.3,16.2,23)
STAIR_BOUNDS=(12.8,15.2,23,29.3)

def site_materials():
    mats={
        'concrete':noise_material('Lindon driveway | pale aggregate',(.38,.37,.33),(.59,.58,.52),70,.78,.0015),
        'stone':noise_material('Lindon retaining stone | warm gray',(.28,.26,.22),(.54,.51,.43),12,.86,.012),
        'soil':noise_material('Lindon planted soil',(.032,.022,.012),(.085,.066,.035),38,.96,.007),
        'black':material('Lindon fence black metal',(.022,.027,.022),.5,.5),
        'joint':material('Lindon driveway contraction joint',(.19,.18,.16),.9),
        'arrival':noise_material('Arrival warm ivory concrete',(.40,.385,.355),(.47,.45,.42),90,.80,.0007),
    }
    lawn=material('Lindon lawn | physical-scale turf',(.095,.14,.075),.92)
    n=lawn.node_tree.nodes;l=lawn.node_tree.links;p=n.get('Principled BSDF');coord=n.new('ShaderNodeTexCoord')
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.065;noise.inputs['Detail'].default_value=2
    l.new(coord.outputs['Object'],noise.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.085,.125,.070,1);ramp.color_ramp.elements[1].color=(.115,.160,.085,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
    fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=340;fine.inputs['Detail'].default_value=2;l.new(coord.outputs['Object'],fine.inputs['Vector'])
    bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.006;bump.inputs['Strength'].default_value=.22;l.new(fine.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    mats['lawn']=lawn
    return mats

def lawn_with_excavations(mat):
    # Shared vertices and continuous object-space shader avoid seams between cells.
    xs=sorted(set([-200,-50,-32,-20,-10,-1.8,0,8.45,8.8,12.8,15.2,19.3,19.65,24,26.79,33.21,36,45,56,80,220]))
    ys=sorted(set([-200,-60,-37,-20,-8,0,.6,3.2,5.0,7.8,16.19,16.2,19,21.79,23,29.3,34.21,37,43,51,75,220]))
    verts=[(x,y,-.018) for y in ys for x in xs];faces=[]
    for j in range(len(ys)-1):
        for i in range(len(xs)-1):
            x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2
            inside_house=0<x<19.3 and 0<y<16.19
            inside_patio=8.45<x<19.65 and 16.19<y<23
            inside_stairs=12.8<x<15.2 and 23<y<29.3
            inside_pool=26.79<x<33.21 and 21.79<y<34.21
            inside_lightwell=any(xa<x<xb and ya<y<yb for xa,xb,ya,yb in WEST_LIGHTWELLS)
            if inside_house or inside_patio or inside_stairs or inside_pool or inside_lightwell:continue
            a=j*len(xs)+i;faces.append((a,a+1,a+1+len(xs),a+len(xs)))
    terrain=mesh('Approximate lawn grade | excavations for pool and walkout',verts,faces,mat)
    terrain['grade_datum_m']=0.;terrain['surveyed']=False
    return terrain

def railing(name,a,b,height,mat,pickets=True,spacing=.115):
    dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
    if length<.01:return
    count=max(1,math.ceil(length/2.1))
    for i in range(count+1):
        t=i/count;x=a[0]+dx*t;y=a[1]+dy*t;z=a[2]+(b[2]-a[2])*t
        box(name+' post',(x,y,z+height/2),(.065,.065,height),mat,.009)
    rod(name+' top rail',(a[0],a[1],a[2]+height),(b[0],b[1],b[2]+height),.027,mat)
    rod(name+' lower rail',(a[0],a[1],a[2]+.12),(b[0],b[1],b[2]+.12),.018,mat)
    if pickets:
        for i in range(1,math.ceil(length/spacing)):
            t=i/math.ceil(length/spacing);x=a[0]+dx*t;y=a[1]+dy*t;z=a[2]+(b[2]-a[2])*t
            rod(name+' vertical infill',(x,y,z+.10),(x,y,z+height-.02),.009,mat)

def build_site(root,M):
    """Build the coordinated approximate site; M accepted but no keys required."""
    mats=site_materials();rng=random.Random(61026)
    linked={slug:linked_collection(root,cat,slug,version) for cat,slug,version in ASSET_DEPENDENCIES}
    g.collection('Lindon 90 | Site terrain and circulation')
    lawn_with_excavations(mats['lawn'])
    # Vehicle apron stays open from the lane to the angled garage. The unused
    # left forecourt is removed from paving and becomes a planted arrival garden.
    drivepoly=[(-2,-14),(10,-16),(19,-18),(30,-15),(33,-9),(29,-1),(23.27,-5.97),(19.87,-2.54),(19.32,-3.07),(14.6,1.7),(9,-1),(4.5,-1),(4.5,-6.2),(3.6,-8.7),(-2.4,-9.2)]
    prism('Approximate concrete arrival court',drivepoly,-.15,.018,mats['arrival'])
    lanepoly=[(18,-18),(23,-37),(28,-37),(24,-22),(31,-15),(30,-11),(25,-14)]
    prism('Private approach lane | approximate route',lanepoly,-.16,.012,mats['arrival'])
    # Restrained joints are clipped away from the planting notch and entry.
    for x in [9,14]:box('Driveway contraction joint',(x,-7.5,.021),(.007,11,.002),mats['joint'])
    for y in [-4,-8]:box('Driveway contraction joint',(11,y,.021),(13,.007,.002),mats['joint'])
    box('Driveway contraction joint',(8,-12,.021),(17,.007,.002),mats['joint'])
    # A full 2.4 m clear route reaches the recessed doorway. No garden objects
    # enter x4.8..7.2, and its far end follows the traced entry setback.
    box('Recessed front-door connecting walk',(6,(-3+2.747)/2,-.0275),(2.4,5.747,.105),mats['arrival'])
    for y in [-1.8,-.6,.6,1.8]:box('Entry walk fine joint',(6,y,.026),(2.4,.006,.002),mats['joint'])
    # Narrow arrival landing joins the drive only on the door side; the old
    # broad left-hand branch has been replaced by a layered planted island.
    box('Main entry pedestrian walk',(7.6,-2.4,.006),(1.4,1.2,.038),mats['arrival'])
    island=[(-2,-7.5),(.6,-8.05),(3.2,-7.9),(3.95,-6.25),(4,-1.05),(.0,-1.05),(-2.35,-3.2)]
    prism('Layered arrival garden island',island,-.018,.022,mats['soil'])
    for a,b in zip(island,island[1:]+island[:1]):rod('Arrival garden thin charcoal edging',(*a,.027),(*b,.027),.012,mats['black'])
    # Grounded low planting in irregular drifts, not isolated billboard shrubs.
    arrival_rng=random.Random(610913)
    for ci,(cx,cy) in enumerate([(-1.1,-3.1),(-.3,-5.5),(1.3,-6.9),(1.25,-3.9),(2.6,-1.9)]):
        instance('Arrival shared sage anchor %02d'%ci,linked['sage-shrub'],(cx,cy,.024),arrival_rng.uniform(0,math.tau),arrival_rng.uniform(.90,1.15))
        for k in range(7):
            a=k*math.tau/7+arrival_rng.uniform(-.15,.15);r=arrival_rng.uniform(.52,.77)
            slug='flowering-perennial-clump' if k%3 else 'ornamental-grass-clump'
            x=cx+math.cos(a)*r;y=cy+math.sin(a)*r
            if 1.70<x<3.70 and -5.44<y<-2.19:continue  # clear paver footprint plus foliage setback
            instance('Arrival shared flowering drift %02d %02d'%(ci,k),linked[slug],(x,y,.024),arrival_rng.uniform(0,math.tau),arrival_rng.uniform(.82,1.08))
    # Slim foundation borders sit forward of fixed glazing, below view height;
    # the recessed front door and both west-side light wells stay open.
    for bi,(x0,x1,y) in enumerate([(0.15,3.8,-.90),(7.72,11.5,-1.22)]):
        box('Front foundation border %d'%bi,((x0+x1)/2,y,.006),(x1-x0,.84,.036),mats['soil'],.035)
        for i in range(7):
            x=x0+.24+i*(x1-x0-.48)/6
            slug='flowering-perennial-clump' if i%3 else 'ornamental-grass-clump'
            instance('Front shared low border %d %d'%(bi,i),linked[slug],(x,y,.025),arrival_rng.uniform(0,math.tau),.82 if slug=='flowering-perennial-clump' else .85)
    # Two genuine unscaled library slabs form a small garden maintenance landing,
    # entirely left of the door route and outside the garage approach.
    for i in range(2):instance('Shared arrival garden paver %d'%i,linked['honed-limestone-paver-4ft'],(2.70,-3.20-i*1.23,.026))
    prism('East garden and court access',[(20,8),(29,8),(29,3.65),(30,3.65),(30,9.5),(20,9.5)],-.08,.025,mats['concrete'])
    # Approximate open west light wells for the two basement glazing bays.
    # The parent owns wall openings/glazing; no soil face remains in these holes.
    for wi,(xa,xb,ya,yb) in enumerate(WEST_LIGHTWELLS,1):
        width=xb-xa;length=yb-ya;cx=(xa+xb)/2;cy=(ya+yb)/2
        box('West lightwell %d floor'%wi,(cx,cy,-3.205),(width,length,.11),mats['concrete'],.012)
        box('West lightwell %d retaining back'%wi,(xa-.15,cy,-1.56),(.3,length+.6,3.18),mats['stone'],.016)
        for y in [ya-.15,yb+.15]:
            box('West lightwell %d retaining end'%wi,(cx,y,-1.56),(width,.3,3.18),mats['stone'],.016)
        for a,b in [((xa-.18,ya-.3,.03),(xa-.18,yb+.3,.03)),((xa-.18,ya-.3,.03),(0,ya-.3,.03)),((xa-.18,yb+.3,.03),(0,yb+.3,.03))]:
            railing('West lightwell %d guard'%wi,a,b,1.05,mats['black'])
    # Walkout floor/retaining shell, outside the deck structure owned by parent.
    box('Sunken rear walkout patio',(14.05,19.6,-3.235),(10.5,6.8,.17),mats['concrete'],.02)
    for x in [8.6,19.5]:box('Walkout court side retaining wall',(x,19.6,-1.575),(.4,6.8,3.15),mats['stone'],.03)
    for x,w in [(10.8,4),(17.25,4.1)]:box('Walkout rear retaining wall',(x,23.15,-1.575),(w,.3,3.15),mats['stone'],.03)
    for i in range(18):
        top=-3.15+(i+1)*.175
        box('Garden stair tread %02d'%(i+1),(14,23+.35*(i+.5),(-3.15+top)/2),(2.4,.35,top+3.15),mats['stone'],.009)
    for x in [12.68,15.32]:
        box('Garden stair retaining side',(x,26.15,-1.575),(.24,6.3,3.15),mats['stone'],.015)
        railing('Garden stair handrail',(x,23,-2.975),(x,29.3,0),.95,mats['black'],False)
    for a,b in [((8.4,16.25,0),(8.4,23.3,0)),((19.7,16.25,0),(19.7,23.3,0)),((8.4,23.3,0),(12.55,23.3,0)),((15.45,23.3,0),(19.7,23.3,0))]:
        railing('Walkout retaining-edge guard',a,b,1.05,mats['black'])
    # Two levels of planted bands emphasize the local excavation while avoiding
    # a misleading sloped whole lot. Retaining shell dimensions are not engineering.
    for x in [7.65,20.45]:box('Walkout edge planting bed',(x,20.5,.02),(1.2,6.6,.08),mats['soil'],.06)
    # Shared paving modules: unscaled, exactly 1.2192 m square.
    for i in range(6):instance('Shared rear lawn stepping stone %02d'%i,linked['honed-limestone-paver-4ft'],(14,30+i*1.53,.015))
    for i in range(7):
        instance('Shared pool approach paver %02d'%i,linked['honed-limestone-paver-4ft'],(15.6+i*1.55,30 if i==0 else 29.2,.015))
    g.collection('Lindon 91 | Shared pool and outdoor furniture')
    instance('Shared swimming pool',linked['rectangular-pool-6x12m'],(30,28,0))
    # Four deck strips leave the actual pool excavation open.
    for x in [25.65,34.35]:box('Pool deck long side',(x,28,-.06),(2.10,16.8,.12),mats['concrete'],.018)
    for y in [20.70,35.30]:box('Pool deck end',(30,y,-.06),(6.6,2.2,.12),mats['concrete'],.018)
    for x in [27,28.5,30,31.5,33]:instance('Shared pool chaise',linked['slatted-outdoor-chaise'],(x,35.2,.01),math.pi)
    for x in [10.5,17.65]:instance('Shared walkout chaise',linked['slatted-outdoor-chaise'],(x,21,-3.15),math.pi)
    # Fitted site-specific barrier; gate is represented closed, not safety certified.
    fence_segments=[((24,19,0),(36,19,0)),((36,19,0),(36,37,0)),((36,37,0),(24,37,0)),((24,37,0),(24,30,0)),((24,28.4,0),(24,19,0))]
    for a,b in fence_segments:railing('Pool perimeter barrier',a,b,1.4,mats['black'])
    railing('Pool access gate | closed',(24,28.4,0),(24,30,0),1.4,mats['black'])
    box('Pool gate latch',(23.96,29.9,1.27),(.12,.1,.08),mats['black'],.018)
    g.collection('Lindon 92 | Shared sport court')
    instance('Shared blue pickleball court',linked['pickleball-court-30x60ft'],(39,4.5,.025))
    for a,b in [((29.65,-.3,0),(48.35,-.3,0)),((48.35,-.3,0),(48.35,9.3,0)),((48.35,9.3,0),(29.65,9.3,0)),((29.65,9.3,0),(29.65,5.35,0)),((29.65,3.65,0),(29.65,-.3,0))]:
        railing('Court perimeter fence',a,b,2.5,mats['black'],False)
        # Fine open welded mesh represented as one curve per direction segment.
        length=math.hypot(b[0]-a[0],b[1]-a[1])
        for i in range(1,int(length/.22)):
            t=i*.22/length;x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t
            rod('Court mesh vertical',(x,y,.12),(x,y,2.45),.002,mats['black'])
        for i in range(1,12):rod('Court mesh horizontal',(a[0],a[1],i*.21),(b[0],b[1],i*.21),.002,mats['black'])
    g.collection('Lindon 93 | Shared planting')
    tree_positions=[(-13,-8,.85),(-18,8,1.08),(-14,26,1.12),(-5,40,.88),(8,46,1.04),(23,44,.9),(40,42,1.10),(48,28,.98),(51,13,.86),(-24,-23,.95)]
    for i,(x,y,s) in enumerate(tree_positions):instance('Shared conifer boundary %02d'%i,linked['mountain-conifer'],(x,y,0),rng.uniform(0,math.tau),s)
    for i,(x,y) in enumerate([(-7,5),(-7,18),(-1,30),(5,35),(20,35),(39,18),(45,32),(47,41),(-12,-17)]):instance('Shared ornamental tree %02d'%i,linked['olive-tree'],(x,y,0),rng.uniform(0,math.tau),rng.uniform(.95,1.25))
    # Generic off-site context, not inferred property lines or measured species.
    # Clusters stay behind/beside the whole project: clear house, pool, court and
    # front camera corridor, while avoiding isolated specimen spacing in aerials.
    far_rng=random.Random(61209)
    far_clusters=[(-29,8),(-32,32),(-15,52),(7,58),(29,55),(49,48),(61,28),(65,9)]
    for ci,(cx,cy) in enumerate(far_clusters):
        for j in range(6):
            angle=far_rng.uniform(0,math.tau);radius=far_rng.uniform(2,9)
            x=cx+math.cos(angle)*radius;y=cy+math.sin(angle)*radius
            instance('Shared background conifer %02d %02d'%(ci,j),linked['mountain-conifer'],(x,y,0),far_rng.uniform(0,math.tau),far_rng.uniform(.82,1.28))
        for j in range(6):
            x=cx+far_rng.uniform(-10,10);y=cy+far_rng.uniform(-10,10)
            instance('Shared background ornamental %02d %02d'%(ci,j),linked['olive-tree'],(x,y,0),far_rng.uniform(0,math.tau),far_rng.uniform(.95,1.35))
        for j in range(14):
            x=cx+far_rng.uniform(-11,11);y=cy+far_rng.uniform(-10,10)
            slug='sage-shrub' if j%2 else 'ornamental-grass-clump'
            instance('Shared meadow edge planting %02d %02d'%(ci,j),linked[slug],(x,y,0),far_rng.uniform(0,math.tau),far_rng.uniform(.85,1.25))
    # Beds deliberately stay off the drive, pool deck, court and clear rear steps.
    beds=[(-3,8,2.0,12),(-7,28,3.0,10),(7.65,20.5,.8,6),(20.45,20.5,.8,6),(40,30,3,11),(31,40,10,2),(-8,-3,3,4),(25,12,6,1.4)]
    for bi,(cx,cy,w,d) in enumerate(beds):
        box('Site-specific planted bed %02d'%bi,(cx,cy,-.007),(w,d,.018),mats['soil'],.015)
        count=max(5,int(w*d*.75))
        for k in range(count):
            x=cx+rng.uniform(-w*.43,w*.43);y=cy+rng.uniform(-d*.43,d*.43)
            slug='sage-shrub' if k%3==0 else 'ornamental-grass-clump'
            instance('Shared understory %02d %03d'%(bi,k),linked[slug],(x,y,.006),rng.uniform(0,math.tau),rng.uniform(.85,1.25))
    notes={'units':'meters','grade_datum_m':0,'site_surveyed':False,'generic_context_bounds_xy_m':list(SITE_BOUNDS),'west_lightwells':{'bounds_xy_m':WEST_LIGHTWELLS,'floor_z_m':-3.15,'dimensions_status':'Approximate/unverified; daylight and maintenance concept, not certified escape openings or drained/engineered retaining design'},'front_entry_walk':{'bounds_xy_m':[4.8,7.2,-3,2.747],'top_z_m':.025},'arrival_styling':{'left_forecourt':'Paving notch replaced with planted island, wholly outside garage approach','entry_clear_width_m':2.4,'foreground_asset':'landscape/flowering-perennial-clump/v001','status':'Proposed styling inspired by user reference; no surveyed landscape claim'},'pool_center_m':[30,28,0],'pool_water_footprint_m':[6,12],'court_center_m':[39,4.5,.025],'court_surface_m':[18.288,9.144],'walkout_patio_bounds_xy_m':list(PATIO_BOUNDS),'walkout_patio_z_m':-3.15,'garden_stairs':{'riser_count':18,'riser_m':.175,'tread_m':.35,'clear_width_m':2.4},'site_limitations':'Photo-informed spatial approximation; not surveyed. Pool barrier/gate, retaining structures, drainage, utilities, access and grading need site-specific design. Generic existing tree assets are illustrative, not identified listing species.','asset_dependencies':[{'id':cat+'/'+slug,'version':ver} for cat,slug,ver in ASSET_DEPENDENCIES]}
    bpy.context.scene['lindon_site_grade_datum_m']=0.
    return notes
