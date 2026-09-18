"""Paired dimensioned plans, hillside section and native-render concept booklet."""
import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
from design import *
from common.drawing import Drawing
from pypdf import PdfReader,PdfWriter
HOME=ROOT/'homes'/SLUG;OUT=HOME/'outputs/plans';WORK=HOME/'outputs/work';IMG=HOME/'outputs/images'
INK='#283b32';MUTED='#67736a';PAPER='#f6f4ed';WOOD='#c5a37b';LIGHT='#e5dfd1';BLUE='#72979a';WHITE='#ffffff'

def header(d,n,title,sub):
    d.rect(0,0,d.w,d.h,PAPER);d.text(55,50,'H O M E S   /   0 5',16,MUTED);d.text(55,103,title,39,INK,bold=True);d.text(55,141,sub,17,MUTED)
    d.text(55,d.h-31,'CONCEPT ONLY  /  Original design: Homes project contributors  /  CC BY 4.0',12,MUTED)
    d.text(d.w-55,d.h-31,f'MOUNTAIN HOUSE  /  {n:02d}',13,MUTED,anchor='end')
def dim(d,x1,y1,x2,y2,t):
    d.line(x1,y1,x2,y2,MUTED)
    if y1==y2:
        for x in [x1,x2]:d.line(x,y1-6,x,y1+6,MUTED)
        d.text((x1+x2)/2,y1-10,t,16,INK,anchor='middle')
    else:
        for y in [y1,y2]:d.line(x1-6,y,x1+6,y,MUTED)
        d.text(x1+11,(y1+y2)/2,t,15,INK)

def plan(lower=False):
    name='walkout-floor' if lower else 'main-floor'
    d=Drawing(1400,1200,WORK/(name+'.pdf'),OUT/(name+'.svg'),title='Mountain House | '+name)
    header(d,3 if lower else 2,'The walkout level' if lower else 'Living at road level','Lower datum -11 ft / 1,824 sq ft gross' if lower else 'Main datum 0 ft / 2,280 sq ft gross including 576 sq ft garage')
    S=12.6;OX=185;OY=925
    X=lambda x:OX+x*S;Y=lambda y:OY-y*S
    def rect(x,y,w,h,fill=WHITE,stroke='none',sw=1):d.rect(X(x),Y(y+h),w*S,h*S,fill,stroke,sw)
    def line(a,b,c=INK,sw=4):d.line(X(a[0]),Y(a[1]),X(b[0]),Y(b[1]),c,sw)
    def lab(x,y,t,size=13,c=INK):d.text(X(x),Y(y),t,max(size,11),c,anchor='middle')
    if lower:
        rect(0,0,24,24,LIGHT);lab(12,13,'UNEXCAVATED',15,MUTED);lab(12,11,'BENEATH GARAGE',12,MUTED)
        for a,b,c,e in LOWER_SLABS:rect(a,b,c-a,e-b,WHITE)
        for a,b in [((24,0),(60,0)),((60,0),(60,40)),((60,40),(0,40)),((0,40),(0,24)),((0,24),(24,24)),((24,24),(24,0))]:line(a,b)
        rect(24,40,36,13,LIGHT,INK,1);lab(42,51,'SHADED WALKOUT PATIO',15)
        for a,b in [(2,16),(20,39),(43,58)]:line((a,40),(b,40),BLUE,3)
        line((35,40),(39,40),WHITE,7)
        for x in [0,60]:line((x,28),(x,38),BLUE,3)
        walls=LOWER_WALLS
    else:
        for a,b,c,e in DECKS:rect(a,b,c-a,e-b,WOOD,INK,1)
        rect(0,0,60,40,WHITE,INK,5);rect(0,0,24,24,LIGHT)
        rect(24,12,8,15,LIGHT,INK,1)
        line((2,0),(22,0),WOOD,5);line((33,0),(39,0),WHITE,7);line((36.7,0),(39,0),BLUE,3)
        for a,b in [(3,21),(24,39),(42,58)]:line((a,40),(b,40),BLUE,3)
        for a,b in [(9,21),(29,39)]:line((a,40),(b,40),WHITE,7)
        line((0,32),(0,38),BLUE,3);line((60,13),(60,23),BLUE,3);line((60,29),(60,33.5),BLUE,3)
        line((60,31),(60,33.5),WHITE,6)
        walls=MAIN_WALLS
    for name,a,b,ops in walls:
        L=math.dist(a,b);ux=(b[0]-a[0])/L;uy=(b[1]-a[1])/L;cur=0
        for off,w in ops+[(L,0)]:
            line((a[0]+ux*cur,a[1]+uy*cur),(a[0]+ux*off,a[1]+uy*off));cur=off+w
            if w:
                p=(a[0]+ux*(off+.1),a[1]+uy*(off+w-.1 if name=='Mudroom east' and off==1.8 else off+.1));q=(p[0]+uy*(w-.18)*(-1 if name=='Primary west' and off==10.3 else 1),p[1]+ux*(w-.18)*(-1 if name in ['Lower utility rear','Primary bath rear','Primary WC rear'] else 1));line(p,q,WOOD,2)
    # The exact two-flight U stair, shown on both levels.
    for i in range(10):
        y=STAIR_START+i*TREAD;line((24.15,y),(27.85,y),MUTED,1);line((28.15,y),(31.85,y),MUTED,1)
    rect(24.15,STAIR_LANDING,7.7,4.4,LIGHT,MUTED,1)
    lab(28,25.8,'U STAIR',10)
    line((26,13),(26,20),BLUE,2);line((30,20),(30,13),BLUE,2)
    def bedshape(x,y,w):rect(x-w/2,y-3.5,w,7,LIGHT,WOOD,1);rect(x-w/2+.2,y-3.0,w-.4,1.25,WHITE,WOOD,.5)
    def storage(x,y,w,h):rect(x,y,w,h,WOOD,INK,.8)
    if lower:
        bedshape(9,32.8,5.2);bedshape(53,32.9,5.2)
        storage(2,24.2,6,2);storage(42.4,28,2,6)
        lab(9,38.0,'BEDROOM 02',13);lab(9,36.7,'18 x 16 ft zone',10,MUTED)
        lab(51,38.0,'BEDROOM 03',13);lab(51,36.7,'18 x 14 ft zone',10,MUTED)
        lab(5,27.5,'6 FT STORAGE',9);lab(46.5,34.8,'6 FT STORAGE',9)
        rect(24.3,27.75,11.4,3.5,LIGHT,WOOD,1);rect(27,32.9,6,3.2,WOOD)
        lab(30,37.8,'LOWER LOUNGE',14)
        rect(43,22.3,3.7,3.3,'#dfebea',BLUE,1);storage(47.2,22.5,2,2);d.circle(X(47.9),Y(19.65),7,WHITE,INK,1)
        lab(47,21,'BATH',11)
        lab(39,8,'MECHANICAL /',12);lab(39,6.6,'WORKSHOP',12)
        rect(33.5,1,5,4,MUTED);rect(39,.75,6,2.5,WOOD)
        for x in [47.7,50.7]:rect(x,.65,2.6,2.7,LIGHT,INK,1)
        storage(54,.5,4,2);lab(53,8,'LAUNDRY + LINEN',11)
        lab(40,16,'LOWER HALL',11,MUTED)
        for x in [47,53]:rect(x-1.4,43.6,2.8,6.8,WHITE,WOOD,1)
        lab(64,24,'SLOPE',12,MUTED)
    else:
        bedshape(54,17.4,6.4);lab(53,24.8,'PRIMARY BEDROOM',12);lab(53,23.5,'14 x 14 ft zone',10,MUTED)
        storage(40.2,13.2,2,8);lab(44.2,20,'CLOSET',11)
        lab(28,4.8,'POWDER',9);storage(25,.4,2,2);d.circle(X(29.8),Y(1.8),7,WHITE,INK,1)
        # Premium primary bath: separate wet fixtures, double vanity and enclosed WC.
        rect(45.6,.25,4.8,4.8,'#dfebea',BLUE,1);lab(48,2.6,'SHOWER',9)
        rect(52.5,.85,6,3,LIGHT,INK,1);rect(53.1,1.35,4.8,2,WHITE,INK,.5);lab(55.5,2.2,'TUB',9)
        storage(52,9.8,6,2)
        for x in [53,57]:d.circle(X(x),Y(10.8),7,WHITE,INK,1)
        d.circle(X(42.5),Y(1.9),7,WHITE,INK,1);lab(42.5,4.9,'WC',9)
        lab(53.4,7.3,'PRIMARY BATH',11);lab(55,9.0,'DOUBLE VANITY',9)
        storage(24.5,9.8,4,2);rect(29.2,10.05,2,1.5,WOOD);lab(27,8,'MUDROOM',10)
        lab(36,5.8,'ENTRY',13);lab(36,4.3,'8 ft zone',10,MUTED)
        for x in [6,17.5]:
            rect(x-3.25,3.5,6.5,15,LIGHT,MUTED,1);lab(x,11,'CAR',11,MUTED)
        lab(12,20,'24 x 24 FT GARAGE',14)
        storage(2,21.6,6,2)
        rect(6.3,25.25,11.4,3.5,LIGHT,WOOD,1);rect(9,31.1,6,3.2,WOOD)
        lab(12,37.6,'LIVING',16)
        rect(29,30.45,8,3.7,WOOD)
        for x in [30.4,33,35.6]:
            for y in [29.5,35.1]:rect(x-.8,y-.8,1.6,1.6,LIGHT,WOOD,.6)
        lab(33,37.8,'DINING',14)
        rect(43.85,30.2,10.3,3.2,WOOD,INK,1);rect(46.5,30.925,3,1.75,INK);lab(48,28.8,'COOKTOP + OVEN',11)
        rect(41.85,37,14.3,2.8,WOOD);rect(50.75,37.575,2.5,1.65,WHITE,INK,1)
        rect(54,37.4,2,2,LIGHT,INK,.8);lab(55,36.3,'DW',11)
        storage(57.5,33,2,4);storage(54.75,26.35,4,2.5);lab(56.75,28.0,'48 IN',11);lab(56.75,27.1,'FRIDGE',11)
        rect(.0,25.2,2,6.6,MUTED);lab(5.5,30,'FIREPLACE',11)
        lab(49,35.5,'KITCHEN',14)
        rect(5.3,42.75,11.4,3.5,LIGHT,INK,1);rect(8.4,47.5,5.2,3,WOOD,INK,1)
        rect(28,45.25,8,3.7,LIGHT,INK,1)
        for x in [29.4,32,34.6]:
            for y in [44.2,50]:rect(x-.8,y-.8,1.6,1.6,WHITE,INK,.6)
        for x in [22,42]:
            for y in [40.8,52.8]:rect(x-.28,y-.28,.56,.56,INK)
        lab(51,48,'OPEN DECK',14);lab(32,52,'PERGOLA',11)
        dim(d,X(71),Y(40),X(71),Y(54),'14 ft deck')
        lab(64,25,'8 FT',12);lab(64,23.5,'RETURN',10)
    dim(d,X(0),Y(-3.2),X(60),Y(-3.2),'60 ft overall')
    dim(d,X(-4),Y(0),X(-4),Y(40),'40 ft')
    d.text(185,1007,'Solid oak blocks indicate usable storage; blue lines indicate glazing. Interior doors shown open.',15,MUTED)
    d.text(185,1036,'Room dimensions are nominal planning zones including wall allowance, not measured net room areas.',15,MUTED)
    d.text(185,1065,'Main stair opening 8 x 15 ft. 20 risers over 11 ft; 6.6 in nominal rise and 11 in tread.',15,MUTED)
    d.text(185,1094,'Concept geometry only. Structure, local egress, waterproofing, energy and site conditions remain unverified.',15,MUTED)
    for i in range(3):d.rect(185+i*10*S,1123,10*S,8,INK if i%2==0 else WHITE,INK,.8)
    d.text(185,1153,'0',12,MUTED);d.text(185+10*S,1153,'10 ft',12,MUTED);d.text(185+20*S,1153,'20 ft',12,MUTED)
    d.save()

plan();plan(True)
# Section diagrams show actual floor, road and downhill profile, rather than a third floor.
d=Drawing(1400,1120,WORK/'section.pdf',OUT/'hillside-section.svg',title='Mountain House | Slope and outdoor rooms')
header(d,5,'Two levels, one descending site','Road and garage at the main floor. A broad timber deck replaces an impractical steep lawn.')
S=9;X=lambda y:500+y*S;Z=lambda z:410-z*S
for y in range(-45,94):
    if not 0 <= y < 40:d.line(X(y),Z(grade(42,y)),X(y+1),Z(grade(42,y+1)),MUTED,3)
d.rect(X(-48),Z(-.28),20*S,4,INK)
d.text(X(-38),Z(1),'FRONT ROAD',15,INK,anchor='middle')
for z in [0,-11]:d.rect(X(0),Z(z),40*S,7,WOOD,INK,1)
d.line(X(0),Z(roof_z(0)),X(40),Z(roof_z(40)),INK,5)
for y in [0,40]:d.line(X(y),Z(-11),X(y),Z(roof_z(y)),INK,3)
d.line(X(40),Z(0),X(54),Z(0),WOOD,8);d.line(X(53.4),Z(-.7),X(53.4),Z(grade(42,53.4)),WOOD,7)
d.line(X(40),Z(-11.14),X(53),Z(-11.14),BLUE,5)
d.text(X(20),Z(5),'MAIN LIVING  /  0 FT',19,INK,anchor='middle')
d.text(X(20),Z(-6),'WALKOUT  /  -11 FT',19,INK,anchor='middle')
d.text(X(57),Z(.5),'14 ft deck',16,INK)
d.text(X(55),Z(-10),'Shaded patio',16,INK)
d.text(55,670,'A usable outdoor sequence',26,INK,bold=True)
for y,t in [(714,'Main living opens to a 1,128 sq ft rear deck and side return.'),(749,'A partial pergola shades dining; the lounge retains open sky.'),(784,'Posts and knee braces express the elevated deck structure.'),(819,'The lower lounge opens to a graded patio bench before the hill falls away.'),(881,'Area: 4,104 sq ft gross including garage; 3,528 sq ft conditioned gross.'),(916,'The lower floor is L-shaped: there is no occupied room beneath the front garage.'),(970,'Illustrative grading only: cut/fill, retaining, snow loads and drainage require site engineering.')]:d.text(55,y,t,18,MUTED)
d.save()
if '--plan-only' in sys.argv:print('MOUNTAIN_PLANS_SAVED');raise SystemExit
pages=[]
def imagepage(file,n,title,sub):
    path=WORK/(file+'-page.pdf');d=Drawing(1400,1120,path,title='Mountain House | '+title);header(d,n,title,sub)
    d.image(IMG/(file+'.png'),55,175,1290,806.25)
    d.text(55,1021,'Original native 3D model render. Forest, road and terrain are illustrative.',17,MUTED);d.save();return path
pages.append(imagepage('01-forest-rear',1,'Mountain House','Timber, forest and a broad deck overlooking the downhill landscape.'))
pages += [WORK/'main-floor.pdf',WORK/'walkout-floor.pdf']
pages.append(imagepage('02-road-arrival',4,'A quiet arrival at the road','Integrated two-car garage, sheltered entry and a low timber profile.'))
pages.append(WORK/'section.pdf')
pages.append(imagepage('03-deck-living',6,'Living among the trees','Outdoor dining beneath a partial pergola; open-air lounge and an eight-foot side return.'))
pages.append(imagepage('04-walkout-patio',7,'The shaded lower terrace','The walkout lounge opens directly beneath the deck onto a locally graded patio.'))
pages.append(imagepage('06-kitchen',8,'A complete integrated kitchen','Shared appliances, cabinet-matched 48-inch refrigeration, induction cooking and separate extraction.'))
pages.append(imagepage('07-primary-bath',9,'Primary vanity and soaking tub','The plan locates the separate shower, enclosed toilet room and walk-in dressing room.'))
pages.append(imagepage('08-kitchen-appliances',10,'Equipment belongs in the plan','A reverse kitchen view shows the oven and the wide cabinet-matched refrigerator.'))
writer=PdfWriter()
for p in pages:writer.append(PdfReader(p))
writer.add_metadata({'/Title':'Mountain House | Architectural concept','/Author':'Homes project contributors'})
with open(OUT/'design-board.pdf','wb') as f:writer.write(f)
assert len(PdfReader(OUT/'design-board.pdf').pages)==10
print('MOUNTAIN_BOOKLET_SAVED')
