"""Dimensioned concept plan and eight-page visual booklet from current model renders."""
import sys,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
from design import *
from verandah import (PERGOLA_BOUNDS, PERGOLA_POSTS, PERGOLA_POST_WIDTH,
                      ENTRY_CANOPY_BOUNDS, ENTRY_CANOPY_POSTS, SCREEN_X, SCREEN_Y)
from common.drawing import Drawing
from pypdf import PdfReader,PdfWriter
HOME=ROOT/'homes'/SLUG;OUT=HOME/'outputs/plans';WORK=HOME/'outputs/work';IMG=HOME/'outputs/images';OUT.mkdir(parents=True,exist_ok=True)
REVIEW='--review' in sys.argv
if REVIEW:IMG=WORK
FINAL_PDF=(WORK if REVIEW else OUT)/'design-board.pdf'
INK='#253b40';MUTED='#6c7e7b';SAND='#ede9df';OAK='#c9ad82';BLUE='#58939b';PALE='#f7f6f0';WHITE='#ffffff'

def header(d,n,title,subtitle):
    d.rect(0,0,d.w,d.h,PALE);d.text(55,52,'H O M E S   /   0 4',16,MUTED);d.text(55,105,title,40,INK,bold=True);d.text(55,141,subtitle,17,MUTED)
    d.text(d.w-55,d.h-30,f'COASTAL HOUSE   /   {n:02d}',13,MUTED,anchor='end');d.text(55,d.h-30,'CONCEPT ONLY  /  Original design: Homes project contributors  /  CC BY 4.0',12,MUTED)

def caption(d,x,y,title,text):d.text(x,y,title,23,INK,bold=True);d.text(x,y+29,text,16,MUTED)
def dimension(d,x1,y1,x2,y2,label):
    d.line(x1,y1,x2,y2,MUTED,1)
    if y1==y2:
        for x in [x1,x2]:d.line(x,y1-7,x,y1+7,MUTED,1)
        d.text((x1+x2)/2,y1-9,label,16,INK,anchor='middle')
    else:
        for y in [y1,y2]:d.line(x1-7,y,x1+7,y,MUTED,1)
        d.text(x1+12,(y1+y2)/2,label,16,INK)

def site_features(d,mx,my,scale,labels=False):
    """Clear outline site diagram using the same roof/post coordinates as model."""
    def rr(x,y,w,h,fill,stroke=OAK,sw=.7):d.rect(mx(x),my(y+h),w*scale,h*scale,fill,stroke,sw)
    rr(-3,40,74,18,'#ede9df')
    x1,x2,y1,y2=PERGOLA_BOUNDS
    rr(x1,y1,x2-x1,y2-y1,'none')
    for i in range(8):
        x=x1+i*(x2-x1)/7
        d.line(mx(x),my(y1),mx(x),my(y2),'#c9b99f',.7)
    d.line(mx(x1),my(y1),mx(x2),my(y1),INK,1.6)  # ledger above the glass head
    for x,y in PERGOLA_POSTS:rr(x-PERGOLA_POST_WIDTH/2,y-PERGOLA_POST_WIDTH/2,PERGOLA_POST_WIDTH,PERGOLA_POST_WIDTH,INK,INK)
    x1,x2,y1,y2=ENTRY_CANOPY_BOUNDS
    rr(x1,y1,x2-x1,y2-y1,'#d2bfa4')
    for x,y in ENTRY_CANOPY_POSTS:rr(x-.25,y-.25,.5,.5,INK,INK)
    # Grouped symbols describe planted garden rooms, not a surveyed canopy map.
    for x,y,r in [(8.5,-20.5,4.7),(34,-23,4.5),(10,-32,3),(40,-32,5),
                  (10,-12,2.5),(33,-12,2.8)]:
        d.circle(mx(x),my(y),r*scale,'#bec6aa','#869675',.6)
    if labels:
        d.text(mx((PERGOLA_BOUNDS[0]+PERGOLA_BOUNDS[1])/2),my(59.8),'ATTACHED PERGOLA / SLATTED SHADE',12,INK,anchor='middle')
        d.text(mx(22),my(-5),'PORCH',10,INK,anchor='middle')
        d.text(mx(44),my(-15),'ENTRY GARDEN',12,MUTED,anchor='middle')

# Large printable floor plan, same coordinates and apertures as the model.
d=Drawing(1400,1280,WORK/'plan-page.pdf',OUT/'floor-plan.svg',title='Coastal House dimensioned concept plan')
header(d,2,'A warm coastal verandah','68 x 40 ft exterior floor plate  /  2,720 sq ft gross enclosed  /  3 bedrooms + 2 baths')
S=12.3;OX=220;OY=902
X=lambda x:OX+x*S;Y=lambda y:OY-y*S
def rect(x,y,w,h,fill,stroke='none',sw=1):d.rect(X(x),Y(y+h),w*S,h*S,fill,stroke,sw)
def line(a,b,color=INK,sw=4):d.line(X(a[0]),Y(a[1]),X(b[0]),Y(b[1]),color,sw)
def label(x,y,t,size=15,color=INK):d.text(X(x),Y(y),t,size,color,anchor='middle')
rect(-3,40,74,18,SAND)
# Attached open shade: house ledger above the slider head and two outer posts.
# The outline represents overhead slats, not a weatherproof roof.
x1,x2,y1,y2=PERGOLA_BOUNDS
rect(x1,y1,x2-x1,y2-y1,'none',OAK,1.2)
for xx in [x1+i*(x2-x1)/15 for i in range(16)]:line((xx,y1),(xx,y2),'#d9cbb4',.45)
line((x1,y1),(x2,y1),INK,1.8)  # overhead house ledger
for xx,yy in PERGOLA_POSTS:rect(xx-PERGOLA_POST_WIDTH/2,yy-PERGOLA_POST_WIDTH/2,PERGOLA_POST_WIDTH,PERGOLA_POST_WIDTH,INK)
line((SCREEN_X,SCREEN_Y[0]),(SCREEN_X,SCREEN_Y[1]),OAK,3)
x1,x2,y1,y2=ENTRY_CANOPY_BOUNDS
rect(x1,y1,x2-x1,y2-y1,'#e7ddd0',OAK,1)
for xx,yy in ENTRY_CANOPY_POSTS:rect(xx-.25,yy-.25,.5,.5,INK)
rect(17,-9,6,9,WHITE)
label(22,-5,'ENTRY CANOPY',10)
rect(0,0,68,40,WHITE,INK,5)
for x in range(0,69,4):line((x,0),(x,40),'#efede6',.5)
for y in range(0,41,4):line((0,y),(68,y),'#efede6',.5)
# Rear architectural line, then remove apertures with white overdraw.
for a,b in [(10,40),(48,60)]:line((a,40),(b,40),WHITE,7)
for a,b in [(3,15),(28,39),(44,54)]:line((a,0),(b,0),BLUE,4)
line((18,0),(26,0),WHITE,7);line((22,0),(26,0),BLUE,4);line((18.13,.25),(18.13,3.85),OAK,3)
line((0,23),(0,25.8),BLUE,3);line((0,26.2),(0,38.2),BLUE,4)
for a,b in [(26,30),(35.5,38.2)]:line((68,a),(68,b),BLUE,3)
for name,a,b,opens in WALLS:
    length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length;cur=0
    for off,w in opens+[(length,0)]:
        line((a[0]+ux*cur,a[1]+uy*cur),(a[0]+ux*off,a[1]+uy*off));cur=off+w
        if w:
            if name=='Primary WC west':line((13.73,15.35),(13.73,18.19),OAK,2)
            elif name=='Primary bath front':line((a[0]+off,a[1]-.27),(a[0]+off-w+.16,a[1]-.27),OAK,2)
            elif ux:line((a[0]+off+.09,a[1]),(a[0]+off+.09,a[1]-w+.16),OAK,2)
            else:
                side=-1 if name in ['Primary east','Bath closet partition'] else 1
                line((a[0],a[1]+off+.09),(a[0]+side*(w-.16),a[1]+off+.09),OAK,2)
line((60,16),(68,16))
line((63,16),(63,17));line((63,20),(63,21));line((63,21),(68,21));line((63,17.1),(65.8,17.1),OAK,2)
rect(63.3,16.3,4.4,4.4,'#edf0ee');label(65.4,18.8,'SERVICE',9);label(65.4,17.5,'5 x 4.8 ft',8,MUTED)
for name,x1,y1,x2,y2 in ROOMS:
    if name in ['PRIMARY BEDROOM','BEDROOM 02','BEDROOM 03','LIVING','DINING','KITCHEN','PRIMARY BATH','DRESSING','BATH 02','LAUNDRY']:continue
    label((x1+x2)/2,y2-3,name,12 if x2-x1<11 else 15)
    label((x1+x2)/2,y2-4.5,f'{x2-x1:g} x {y2-y1:g} ft zone',11,MUTED)
# Beds and wardrobes.
for name,x,y,w in BEDS:
    if name=='Primary':
        rect(2.35,2.075,7.3,6.85,SAND,OAK,1);rect(2.45,2.25,1.2,6.5,WHITE,OAK,.5);continue
    rect(x-w/2,y-3.5,w,7,SAND,OAK,1);rect(x-w/2+.2,y-3.1,w-.4,1.2,WHITE,OAK,.5)
rect(38.8,2,2,6,OAK,INK,1);rect(49.7,13.75,6,2,OAK,INK,1)
label(39.8,9.0,'STORAGE',8);label(52.7,14.5,'STORAGE',8)
label(32,10.7,'BEDROOM 02',12);label(32,9.5,'15 x 12 ft zone',10,MUTED)
label(47.1,12.1,'BEDROOM 03',12);label(47.1,10.8,'15 x 16 ft zone',10,MUTED)
rect(23.8,9.9,2,2,OAK,INK,1);label(24.7,12.3,'COATS',8)
rect(65.65,11,2,2,OAK,INK,1);label(66.6,10.3,'LINEN',8)
rect(18.2,4.7,.55,2.6,OAK)
rect(.15,12.2,2,4,OAK);rect(3.8,15.8,2,2,OAK)
rect(.45,18.25,5.2,7.4,'#e5edef',BLUE,1);line((5.65,23.5),(5.65,25.65),BLUE,2)
rect(6,22.7,6,3,WHITE,OAK,1);label(9,24,'TUB',10)
rect(15.3,20.125,2.4,5.75,OAK,INK,1)
for y in [21.5,24.5]:d.circle(X(16.4),Y(y),8,WHITE,INK,.6)
rect(15.333,15.25,1.334,2.5,WHITE,INK,1);d.circle(X(16),Y(16.0),7,WHITE,INK,.6)
for x,y in [(60,0)]:
    rect(x+.45,y+4.8,4.3,3.0,'#e5edef',BLUE,1);rect(x+5.4,y+5.55,2.2,2.2,OAK);rect(64.9,2.633,2.5,1.334,WHITE,INK,1);d.circle(X(65.65),Y(3.3),7,WHITE,INK,.6)
for x in [61.7,64.7]:rect(x,13.05,2.6,2.5,SAND,INK,1)
# Main living / dining / kitchen, with actual furniture footprints.
def asset_footprint(slug,loc,angle=0,fill=SAND):
    """Actual pinned asset bounds, rigidly rotated like the native instance."""
    data=json.loads((ROOT/'library/furniture'/slug/'v001/asset.json').read_text())
    lo,hi=data['bounds_m']['min'],data['bounds_m']['max']
    a=math.radians(angle);c,s=math.cos(a),math.sin(a)
    corners=[]
    for u,v in [(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])]:
        u/=0.3048;v/=0.3048
        corners.append((X(loc[0]+u*c-v*s),Y(loc[1]+u*s+v*c)))
    d.svg.append('<polygon points="'+ ' '.join(f'{x},{y}' for x,y in corners)+f'" fill="{fill}" stroke="{OAK}" stroke-width="1"/>')
    from reportlab.lib.colors import HexColor
    d.pdf.setFillColor(HexColor(fill));d.pdf.setStrokeColor(HexColor(OAK));d.pdf.setLineWidth(1)
    path=d.pdf.beginPath();path.moveTo(corners[0][0],d.h-corners[0][1])
    for x,y in corners[1:]:path.lineTo(x,d.h-y)
    path.close();d.pdf.drawPath(path,fill=1,stroke=1)
asset_footprint('woven-oatmeal-rug',(13,32.6),fill='#dbccb1')
asset_footprint('linen-three-seat-sofa',(13,28.7))
rect(5.95,29.95,3.5,5.3,SAND,OAK,1)
asset_footprint('oak-rounded-coffee-table',(14,33.7),fill=OAK)
asset_footprint('oak-dining-table-8ft',(35,29.1),fill=OAK)
for x in [32.4,35,37.6]:
    asset_footprint('oak-upholstered-dining-chair',(x,26.25),180)
    asset_footprint('oak-upholstered-dining-chair',(x,31.95))
rect(49.375,27,10.25,4.4,OAK,INK,1);label(50.4,30.5,'WASTE',7); rect(55.4,28.8,2.25,1.6,WHITE,INK,1)
rect(65.05,26,2.8,12,OAK)
rect(65.15,22,2.5,4,OAK,INK,1);label(66.4,24,'48 IN',8);label(66.4,23,'FRIDGE',7)
rect(65.4,31.9,1.75,3,'#394648',INK,1)
for xx in [65.8,66.75]:
    for yy in [32.55,34.25]:d.circle(X(xx),Y(yy),3,'#394648',WHITE,.5)
label(62.9,35.4,'COOKTOP',7);label(62.9,34.3,'HOOD + OVEN',7);line((63.8,34.3),(65.25,33.4),MUTED,.6)
rect(52.25,28.75,2,2,'#cbd3d2',INK,1);label(53.25,29.7,'DW',8)
rect(43.1,37.3,4,2,OAK,INK,1);label(45.1,36.2,'PANTRY',9)
rect(47.72,37.055,15.66,2.75,OAK,INK,1);rect(47.72,40.235,15.66,3.93,OAK,INK,1)
# Pocket panels at actual open endpoints, unmistakably outside the opening.
for i in range(6):line((4.8,39.625+i*.15),(9.8,39.625+i*.15),BLUE,1)
for i in range(4):line((60.1,39.805+i*.13),(63.1,39.805+i*.13),BLUE,1)
for x in [50.2,53.7,57.2]:d.circle(X(x),Y(45.0),9,WHITE,OAK,1)
for x in [51.2,54.5,57.8]:d.circle(X(x),Y(26.4),9,WHITE,OAK,1)
for name,slug,loc,angle in OUTDOOR_LOUNGE:asset_footprint(slug,loc,angle,OAK if 'coffee' in slug else WHITE)
asset_footprint('oak-dining-table-8ft',(32,51.5),fill=OAK)
for x in [29.7,32,34.3]:
    asset_footprint('oak-upholstered-dining-chair',(x,48.8),180,WHITE)
    asset_footprint('oak-upholstered-dining-chair',(x,54.2),0,WHITE)
label(10.2,18.4,'PRIMARY BATH',11);label(3.8,14.3,'DRESSING',9);label(16,13.2,'WC',10);label(9,10.5,'PRIMARY BEDROOM',13);label(9,9.2,'18 x 12 ft zone',10,MUTED);label(63,1.65,'BATH 02',10);label(64,11.3,'LAUNDRY',10)
label(13,35.9,'LIVING',16);label(35,35.9,'DINING',16);label(55,35.1,'KITCHEN',16)
label(38,18.65,'CONTINUOUS HALL',12,MUTED);label(22,4,'8 FT ENTRY',11,MUTED)
label((PERGOLA_BOUNDS[0]+PERGOLA_BOUNDS[1])/2,60.0,'ATTACHED PERGOLA / SHADE ONLY',12);label((PERGOLA_BOUNDS[0]+PERGOLA_BOUNDS[1])/2,58.8,f'{PERGOLA_BOUNDS[1]-PERGOLA_BOUNDS[0]:g} ft wide / two terrace-edge posts',10,MUTED);label(56.5,56.1,'OPEN TERRACE',13);label(55.7,54.4,'Outdoor area excluded',10,MUTED);label(55.7,53.0,'from enclosed total',10,MUTED)
label(-8,44.0,'LEDGER ABOVE',9,MUTED);label(-8,42.7,'SLIDING WALL',9,MUTED)
line((-3,43.4),(PERGOLA_BOUNDS[0],PERGOLA_BOUNDS[2]),MUTED,.65)
dimension(d,X(10),Y(42.9),X(40),Y(42.9),'30 ft pocketing glass wall')
dimension(d,X(48),Y(48.1),X(60),Y(48.1),'12 ft serving window')
dimension(d,X(0),Y(-10),X(68),Y(-10),'68 ft overall')
dimension(d,X(72),Y(0),X(72),Y(40),'40 ft')
# A clear legend and explicit scope, not minute notes mixed into rooms.
d.text(180,1050,'Primary suite: 18 x 12 ft bedroom / 6 x 6 ft dressing / L-shaped bath with separate tub, shower, WC and dual vanity',14,MUTED)
d.text(180,1080,'OPENINGS SHOWN FULLY OPEN',17,INK,bold=True)
d.text(180,1105,'Panels store in left door pocket and right window pocket. No panel stack blocks the walk-through.',16,MUTED)
d.text(180,1132,'Room labels show nominal planning zones; they are not measured net floor areas. Interior doors shown open.',16,MUTED)
d.text(180,1158,'No site orientation is assigned. Shore, landscape, drainage and structural details are conceptual.',16,MUTED)
for i in range(3):d.rect(180+i*10*S,1190,10*S,8,INK if i%2==0 else WHITE,INK,.8)
d.text(180,1220,'0',12,MUTED);d.text(180+10*S,1220,'10 ft',12,MUTED);d.text(180+20*S,1220,'20 ft',12,MUTED)
d.save()

if "--plan-only" in sys.argv:
    print("COASTAL_PLAN_SAVED");raise SystemExit(0)

# Booklet cover.
d=Drawing(1400,1120,WORK/'cover-page.pdf',title='Coastal House | A warm coastal verandah')
header(d,1,'Coastal House','A warm coastal verandah: attached slatted shade across the glass wall, with dining and garden seating.')
d.image(IMG/'01-terrace-open.png',55,175,1290,806.25)
d.text(55,1022,'2,720 SQ FT  /  ONE STORY  /  THREE BEDROOMS  /  TWO BATHS',18,INK,bold=True)
d.text(55,1055,'Original 3D model render. Illustrative coastal setting; no actual site has been selected.',16,MUTED);d.save()
# Paired kitchen closeups plus a simple counter section.
d=Drawing(1400,1120,WORK/'counter-page.pdf',title='Coastal House | The serving counter')
header(d,3,'One counter, two sides','A separate 12-foot window slides into the wall. Interior and exterior cabinets remain usable.')
d.image(IMG/'03-serving-counter-open.png',55,180,630,393.75);d.image(IMG/'04-serving-counter-closed.png',715,180,630,393.75)
caption(d,55,615,'OPEN / frame 120','All four panels retract into the side pocket.')
caption(d,715,615,'CLOSED / frame 1','Glass closes above the continuous stone surface.')
d.text(55,710,'COUNTER SECTION  /  schematic, not to scale',19,INK,bold=True)
# Cross-section y-z: wide stone bridge, cabinets both sides and recessed tracks.
d.rect(125,790,385,17,OAK);d.rect(130,817,160,152,SAND,INK,2);d.rect(345,817,160,152,SAND,INK,2)
d.rect(301,758,29,32,BLUE);d.line(315,740,315,790,BLUE,3)
d.text(55,1007,'INTERIOR',16,INK);d.text(432,1007,'TERRACE',16,INK)
d.text(560,767,'Approximately 37-inch counter height',23,INK,bold=True)
d.text(560,805,'Aligned stone surfaces join beneath the recessed track zone.',17,MUTED)
d.text(560,838,'Separate drawer cabinets face inward and outward.',17,MUTED)
d.text(560,871,'Window sill: about 38 inches; head: 8 ft 6 in.',17,MUTED)
d.text(560,926,'Product selection must resolve water drainage, seals,',17,MUTED)
d.text(560,955,'thermal separation and access to pocketed panels.',17,MUTED)
d.text(560,999,'This is original concept geometry, not manufacturer CAD.',16,MUTED);d.save()
# Interior image and concentrated practical notes.
d=Drawing(1400,1120,WORK/'interior-page.pdf',title='Coastal House | Great room')
header(d,4,'Daylight all the way in','Kitchen, dining and living share the terrace, with separate work and walking routes.')
d.image(IMG/'02-great-room.png',55,178,1290,806.25)
d.text(55,1022,'Explore the editable model: frame 1 closed / frame 120 open.',18,INK,bold=True)
d.text(55,1055,'Native Blender + classified IFC concept. Structure, weather performance and site conditions remain unverified.',16,MUTED);d.save()
# Complete front arrival and roof/site concept sheet.
d=Drawing(1400,1120,WORK/'arrival-page.pdf',title='Coastal House | Arrival and pitched roof')
header(d,5,'A complete arrival','A timber entry porch, planted approach, two covered parking spaces and a low pitched metal roof.')
d.image(IMG/'06-front-arrival.png',55,176,820,512.5)
d.image(IMG/'07-roof-and-parking.png',910,176,435,271.875)
d.text(910,490,'ROOF + RAIN',21,INK,bold=True)
for y,t in [(526,'House: 2:12 low gable.'),(557,'Carport: 1:12 mono-pitch.'),(588,'Sloped gutters / downpipes.'),(619,'Roof system and outfall'),(648,'require site-specific design.')]:d.text(910,y,t,17,MUTED)
# Site diagram uses the same feet coordinates as model. Front road below.
SS=2.5;xx=lambda x:85+x*SS;yy=lambda y:840-y*SS
for x,y,w,h,c in [(0,0,68,40,SAND),(73,-27,26,24,OAK),(73,-45,26,18,'#ccccbf'),(-10,-67,120,22,'#8f9996'),(17,-45,6,45,WHITE),(17,-4.25,69,4,WHITE)]:d.rect(xx(x),yy(y+h),w*SS,h*SS,c,INK,.6)
site_features(d,xx,yy,SS)
d.text(xx(34),yy(18),'HOUSE',14,INK,anchor='middle');d.text(xx(86),yy(-13),'2 CARS',12,INK,anchor='middle')
d.text(xx(48),yy(-58),'ILLUSTRATIVE FRONT ROAD',12,WHITE,anchor='middle')
d.text(550,772,'26 x 24 ft carport / two nominal 12 ft bays',21,INK,bold=True)
d.text(550,810,'6 ft entry walk and 4 ft crosswalk behind parked cars.',18,MUTED)
d.text(550,848,'Timber porch and planted garden frame the entry.',18,MUTED)
d.text(550,886,'Attached pergola: open slats; only two terrace-edge posts.',18,MUTED)
d.text(550,924,'Turning radii, flood level and stormwater design unverified.',18,MUTED)
d.text(550,986,'Enclosed area stays 2,720 sq ft; carport is excluded.',18,INK,bold=True);d.save()
d=Drawing(1400,1120,WORK/'entry-page.pdf',title='Coastal House | A generous entry and usable storage')
header(d,6,'Room to arrive','An 8-foot entry opens after 12 feet; every bedroom now has usable storage.')
d.image(IMG/'09-entry-hall.png',55,178,820,512.5)
d.image(IMG/'08-west-garden.png',910,178,435,271.875)
d.text(910,490,'BEDROOM STORAGE',21,INK,bold=True)
for y,t in [(528,'Primary: walk-in dressing.'),(562,'Guest 02: 6 ft wardrobe.'),(596,'Guest 03: 6 ft wardrobe.'),(644,'Guest wardrobes are'),(676,'24 inches deep with'),(708,'paired oak doors.')]:d.text(910,y,t,17,MUTED)
d.text(55,766,'A timber porch, warm mirror wall and coat storage make arrival feel considered.',23,INK,bold=True)
d.text(55,810,'The daylight foyer preserves its 8-foot planning width and direct view through to the terrace.',18,MUTED)
d.text(55,852,'The oak drop shelf and wall-mounted mirror leave the bedroom door and hall approach clear.',18,MUTED)
d.text(55,906,'Entry coat storage and drop shelf, laundry linen cabinet and kitchen waste pullout are modeled.',18,INK)
d.text(55,942,'A 5 x 4.8 ft service closet reserves plant and maintenance space; equipment remains unengineered.',18,MUTED)
d.text(55,970,'Cabinet, plant and paving components use versioned library assets where adopted.',18,MUTED);d.save()
d=Drawing(1400,1120,WORK/'suite-page.pdf',title='Coastal House | Complete primary suite')
header(d,7,'A complete private suite','Separate bathing, dressing and sleeping zones in an expanded 18 x 26 ft primary wing.')
d.image(IMG/'10-primary-bath.png',55,178,1290,806.25)
d.text(55,1022,'Double vanity / separate soaking tub / generous shower / enclosed toilet / walk-in dressing',18,INK,bold=True)
d.text(55,1055,'Fixture spacing and walking routes checked; waterproofing, ventilation and final fixture specifications unverified.',16,MUTED);d.save()
d=Drawing(1400,1120,WORK/'living-page.pdf',title='Coastal House | Warm living retreat')
header(d,8,'A place to settle in','Warm oak, woven oatmeal, olive linen and original wall art frame an unhurried coastal living room.')
d.image(IMG/'11-living-retreat.png',55,178,1290,806.25)
d.text(55,1022,'Linked shared furniture / a tactile rug / soft color / the same generous terrace opening',18,INK,bold=True)
d.text(55,1055,'A house ledger spans the glass wall; two outer posts support open slatted shade, not a rainproof roof.',16,MUTED);d.save()
writer=PdfWriter()
for file in ['cover-page.pdf','plan-page.pdf','counter-page.pdf','interior-page.pdf','arrival-page.pdf','entry-page.pdf','suite-page.pdf','living-page.pdf']:writer.append(PdfReader(WORK/file))
writer.add_metadata({'/Title':'Coastal House | Warm coastal verandah concept','/Author':'Homes project contributors','/Subject':'Warm coastal verandah, garden arrival, pocketing glass wall and indoor outdoor counter'})
with open(FINAL_PDF,'wb') as f:writer.write(f)
assert len(PdfReader(FINAL_PDF).pages)==8
print('COASTAL_PDF_SAVED',FINAL_PDF)

# A separate fully vector site overview remains useful outside the image booklet.
d=Drawing(1080,1060,WORK/'site-vector.pdf',OUT/'site-plan.svg',title='Coastal House | Concept site plan')
header(d,9,'Arrival and roof plan','Garden arrival, two-car parking, timber porch and slatted pergola / no surveyed parcel')
SITE_SCALE=5.7
SX=lambda x:150+(x+10)*SITE_SCALE;SY=lambda y:200+(58-y)*SITE_SCALE
for x,y,w,h,c in [(0,0,68,40,SAND),(73,-27,26,24,OAK),(73,-45,26,18,'#ccccbf'),(-10,-67,120,22,'#8f9996'),(17,-45,6,45,WHITE),(17,-4.25,69,4,WHITE)]:d.rect(SX(x),SY(y+h),w*SITE_SCALE,h*SITE_SCALE,c,INK,1)
site_features(d,SX,SY,SITE_SCALE,labels=True)
d.line(SX(0),SY(20),SX(68),SY(20),INK,1.5)
d.text(SX(34),SY(29),'HOUSE / 68 x 40 ft',19,INK,anchor='middle')
d.text(SX(34),SY(25),'2:12 roof planes',16,MUTED,anchor='middle')
d.text(SX(34),SY(12),'ENTRY / 8 ft planning width',16,INK,anchor='middle')
for x in [79.5,92.5]:
    d.rect(SX(x-3.15),SY(-6.5),6.3*SITE_SCALE,16*SITE_SCALE,'#e8ece9',INK,1)
d.text(SX(86),SY(-30),'26 x 24 ft carport',16,INK,anchor='middle')
d.text(SX(86),SY(-34),'1:12 mono-pitch',14,MUTED,anchor='middle')
d.text(SX(21),SY(-23),'6 ft walk',14,INK)
d.text(SX(49),SY(-58),'ILLUSTRATIVE FRONT ROAD',20,WHITE,anchor='middle')
d.text(90,953,'Road width 22 ft / driveway 26 ft / rear parking crosswalk 4 ft.',18,INK)
d.text(90,988,'No setbacks, grades, turning sweeps or lawful drainage outfall are established.',16,MUTED)
d.save()
