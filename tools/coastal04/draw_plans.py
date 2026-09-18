"""Dimensioned concept plan and four-page visual booklet from current model renders."""
import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
from design import *
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

# Large printable floor plan, same coordinates and apertures as the model.
d=Drawing(1400,1200,WORK/'plan-page.pdf',OUT/'floor-plan.svg',title='Coastal House dimensioned concept plan')
header(d,2,'A simple plan, open to the coast','68 x 40 ft exterior floor plate  /  2,720 sq ft gross enclosed  /  3 bedrooms + 2 baths')
S=12.3;OX=220;OY=902
X=lambda x:OX+x*S;Y=lambda y:OY-y*S
def rect(x,y,w,h,fill,stroke='none',sw=1):d.rect(X(x),Y(y+h),w*S,h*S,fill,stroke,sw)
def line(a,b,color=INK,sw=4):d.line(X(a[0]),Y(a[1]),X(b[0]),Y(b[1]),color,sw)
def label(x,y,t,size=15,color=INK):d.text(X(x),Y(y),t,size,color,anchor='middle')
rect(-3,40,74,18,SAND);rect(0,0,68,40,WHITE,INK,5)
for x in range(0,69,4):line((x,0),(x,40),'#efede6',.5)
for y in range(0,41,4):line((0,y),(68,y),'#efede6',.5)
# Rear architectural line, then remove apertures with white overdraw.
for a,b in [(10,40),(48,60)]:line((a,40),(b,40),WHITE,7)
for a,b in [(3,15),(24,36),(42,54)]:line((a,0),(b,0),BLUE,4)
line((18,0),(22,0),WHITE,7);line((18.13,.25),(18.13,3.85),OAK,3)
line((0,23),(0,38.2),BLUE,4)
for a,b in [(26,30),(35.5,38.2)]:line((68,a),(68,b),BLUE,3)
for name,a,b,opens in WALLS:
    length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length;cur=0
    for off,w in opens+[(length,0)]:
        line((a[0]+ux*cur,a[1]+uy*cur),(a[0]+ux*off,a[1]+uy*off));cur=off+w
        if w:
            if ux:line((a[0]+off+.09,a[1]),(a[0]+off+.09,a[1]+((w-.16) if name=='Primary bath front' else (-w+.16))),OAK,2)
            else:
                side=-1 if name=='Primary east' else 1
                line((a[0],a[1]+off+.09),(a[0]+side*(w-.16),a[1]+off+.09),OAK,2)
line((60,16),(68,16))
for name,x1,y1,x2,y2 in ROOMS:
    if name in ['LIVING','DINING','KITCHEN','PRIMARY BATH','DRESSING','BATH 02','LAUNDRY']:continue
    label((x1+x2)/2,y2-3,name,12 if x2-x1<11 else 15)
    label((x1+x2)/2,y2-4.5,f'{x2-x1:g} x {y2-y1:g} ft zone',11,MUTED)
# Beds and wardrobes.
for x,y,w in [(8.6,6.9,6.5),(30.5,6.7,5),(47.5,6.7,5)]:
    rect(x-w/2,y-3.5,w,7,SAND,OAK,1);rect(x-w/2+.2,y-3.1,w-.4,1.2,WHITE,OAK,.5)
rect(15.6,17,2.2,6.6,OAK);rect(10.2,21.65,4.9,2.2,OAK)
for x,y in [(0,16),(60,0)]:
    rect(x+.45,y+4.2,4.3,3.6,'#e5edef',BLUE,1);rect(x+5.4,y+5.55,2.2,2.2,OAK);d.circle(X(x+(8.2 if x==0 else 6.5)),Y(y+(2.0 if x==0 else 2.6)),8,WHITE,INK,1)
for x in [61.7,64.7]:rect(x,13.05,2.6,2.5,SAND,INK,1)
# Main living / dining / kitchen, with actual furniture footprints.
rect(3,25.6,20,12,'#f0eee7');rect(7.3,25.95,11.4,3.5,SAND,OAK,1);rect(5.95,28.95,3.5,5.3,SAND,OAK,1);rect(11.1,31,5.8,3.4,OAK)
rect(30.75,27.2,8.5,3.8,OAK)
for x in [32.4,35,37.6]:
    for y in [26.25,31.95]:rect(x-.85,y-.85,1.7,1.7,SAND,OAK,1)
rect(49.375,27,10.25,4.4,OAK,INK,1);rect(55.4,28.8,2.25,1.6,WHITE,INK,1)
rect(65.05,22.2,2.8,15.8,OAK)
rect(47.72,37.055,15.66,2.75,OAK,INK,1);rect(47.72,40.235,15.66,3.93,OAK,INK,1)
# Pocket panels at actual open endpoints, unmistakably outside the opening.
for i in range(6):line((4.8,39.625+i*.15),(9.8,39.625+i*.15),BLUE,1)
for i in range(4):line((60.1,39.805+i*.13),(63.1,39.805+i*.13),BLUE,1)
for x in [50.2,53.7,57.2]:d.circle(X(x),Y(45.0),9,WHITE,OAK,1)
for x in [51.2,54.5,57.8]:d.circle(X(x),Y(26.4),9,WHITE,OAK,1)
for x in [10,17]:rect(x-1.5,46,3,7.6,WHITE,OAK,1)
rect(28.5,49.7,7,3.6,OAK)
for x in [29.7,32,34.3]:
    for y in [48.8,54.2]:rect(x-.85,y-.85,1.7,1.7,WHITE,OAK,1)
label(5.2,19.2,'PRIMARY BATH',10);label(13.4,20.0,'DRESSING',10);label(64,3.0,'BATH 02',10);label(64,11.3,'LAUNDRY',10)
label(13,35.9,'LIVING',16);label(35,35.9,'DINING',16);label(55,35.1,'KITCHEN',16)
label(38,18.65,'CONTINUOUS HALL',12,MUTED);label(20,6,'ENTRY',11,MUTED)
label(46,54.8,'SHADED TERRACE',17);label(48,52.8,'Outdoor area excluded from enclosed total',12,MUTED)
dimension(d,X(10),Y(42.9),X(40),Y(42.9),'30 ft pocketing glass wall')
dimension(d,X(48),Y(48.1),X(60),Y(48.1),'12 ft serving window')
dimension(d,X(0),Y(-3),X(68),Y(-3),'68 ft overall')
dimension(d,X(72),Y(0),X(72),Y(40),'40 ft')
# A clear legend and explicit scope, not minute notes mixed into rooms.
d.text(180,973,'Nominal zones: primary bath 10 x 8 ft / bath 02 8 x 8 ft / dressing 8 x 8 ft / laundry 8 x 8 ft',14,MUTED)
d.text(180,1002,'OPENINGS SHOWN FULLY OPEN',17,INK,bold=True)
d.text(180,1025,'Panels store in left door pocket and right window pocket. No panel stack blocks the walk-through.',16,MUTED)
d.text(180,1054,'Room labels show nominal planning zones; they are not measured net floor areas. Interior doors shown open.',16,MUTED)
d.text(180,1083,'No site orientation is assigned. Shore, landscape, drainage and structural details are conceptual.',16,MUTED)
for i in range(3):d.rect(180+i*10*S,1120,10*S,8,INK if i%2==0 else WHITE,INK,.8)
d.text(180,1150,'0',12,MUTED);d.text(180+10*S,1150,'10 ft',12,MUTED);d.text(180+20*S,1150,'20 ft',12,MUTED)
d.save()

if "--plan-only" in sys.argv:
    print("COASTAL_PLAN_SAVED");raise SystemExit(0)

# Booklet cover.
d=Drawing(1400,1120,WORK/'cover-page.pdf',title='Coastal House | Light, glass, open air')
header(d,1,'Coastal House','Light, glass, open air. A modern coastal concept with a kitchen that opens onto the terrace.')
d.image(IMG/'01-terrace-open.png',55,175,1290,806.25)
d.text(55,1022,'2,720 SQ FT  /  ONE STORY  /  THREE BEDROOMS  /  TWO BATHS',18,INK,bold=True)
d.text(55,1055,'Original 3D model render. Illustrative coastal setting; no actual site has been selected.',16,MUTED);d.save()
# Paired kitchen closeups plus a simple counter section.
d=Drawing(1400,1120,WORK/'counter-page.pdf',title='Coastal House | The serving counter')
header(d,3,'One counter, two sides','A separate 12-foot window slides into the wall. Interior and exterior cabinets remain usable.')
d.image(IMG/'03-serving-counter-open.png',55,180,630,393.75);d.image(IMG/'04-serving-counter-closed.png',715,180,630,393.75)
caption(d,55,615,'OPEN / frame 120','All four panels move into the right pocket.')
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
writer=PdfWriter()
for file in ['cover-page.pdf','plan-page.pdf','counter-page.pdf','interior-page.pdf']:writer.append(PdfReader(WORK/file))
writer.add_metadata({'/Title':'Coastal House | Architectural concept','/Author':'Homes project contributors','/Subject':'Bright modern coastal home with pocketing glass wall and indoor outdoor counter'})
with open(FINAL_PDF,'wb') as f:writer.write(f)
assert len(PdfReader(FINAL_PDF).pages)==4
print('COASTAL_PDF_SAVED',FINAL_PDF)
