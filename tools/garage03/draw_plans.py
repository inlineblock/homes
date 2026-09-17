"""Three-page concept book, with editable plan and lift-section SVGs."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from common.drawing import Drawing
from design import *
from pypdf import PdfWriter
HOME=ROOT/'homes/garage-loft-03';OUT=HOME/'outputs/work';OUT.mkdir(parents=True,exist_ok=True)
BG='#f7f5ee';INK='#253b38';MUTED='#657671';WOOD='#bfa083';PITFILL='#d6dddd';TEAL='#285b56'
def header(d,kicker,title,sub):
    d.rect(0,0,d.w,d.h,BG);d.text(80,65,kicker,20,MUTED);d.text(80,120,title,43,INK,bold=True);d.text(80,163,sub,21,MUTED)
def footer(d,page):
    d.line(80,d.h-70,d.w-80,d.h-70,'#c6cec5',1);d.text(80,d.h-35,'CONCEPT ONLY / NOT FOR CONSTRUCTION / ORIGINAL SCHEMATIC EQUIPMENT',16,MUTED);d.text(d.w-80,d.h-35,str(page),16,MUTED,anchor='end')
def plan(d,ox,oy,s,upper):
    def xy(x,y):return ox+x*s,oy-y*s
    def rect(a,b,c,e,fill,stroke='none',sw=1):d.rect(*xy(a,e),(c-a)*s,(e-b)*s,fill,stroke,sw)
    def line(a,b,color=INK,sw=1):d.line(*xy(*a),*xy(*b),color,sw)
    def text(x,y,t,size=17,bold=False,color=INK):d.text(*xy(x,y),t,size,color,anchor='middle',bold=bold)
    rect(0,0,36,34,'#e8e6dd',INK,2)
    for a,b,c,e in [(0,0,.5,34),(35.5,0,36,34),(.5,33.5,35.5,34)]:rect(a,b,c,e,INK)
    # Dimension lines.
    for y in [36]:
        line((0,y),(36,y),MUTED)
        for x in [0,36]:line((x,y-.3),(x,y+.3),MUTED)
        text(18,y+.55,"36'-0\"",20,True)
    line((-1.4,0),(-1.4,34),MUTED);text(-2.4,17,"34'",18)
    rect(28,7,35.5,22,'#ebe3d4',MUTED)
    for j in range(13):
        y=7+j*STAIR_TREAD;line((28.4,y),(31.6,y),MUTED);line((32,y),(35.2,y),MUTED)
    rect(28,18,35.5,22,'#d9c5a9')
    ax=33.65 if upper else 30
    line((ax,8.5),(ax,16.5),TEAL,2);line((ax,16.5),(ax-.4,15.9),TEAL,2);line((ax,16.5),(ax+.4,15.9),TEAL,2)
    text(ax,7.7,'DN' if upper else 'UP',11,True)
    text(31.8,23.5,'ENCLOSED STAIR',14,True)
    text(31.8,22.4,'26 equal risers',13)
    if upper:
        # Front glazing and west windows.
        line((1,.25),(27,.25),'#639995',5);line((.25,.5),(.25,21),'#639995',5)
        rect(28,0,35.5,.5,INK)
        px,py=POOL_CENTER;ew,eh=POOL_ENVELOPE
        rect(px-ew/2,py-eh/2,px+ew/2,py+eh/2,'#d5e4db','#689388',1.5)
        rect(px-POOL_OUTER[0]/2,py-POOL_OUTER[1]/2,px+POOL_OUTER[0]/2,py+POOL_OUTER[1]/2,WOOD,INK,1)
        rect(px-POOL_PLAY[0]/2,py-POOL_PLAY[1]/2,px+POOL_PLAY[0]/2,py+POOL_PLAY[1]/2,TEAL)
        for x in [px-POOL_PLAY[0]/2,px+POOL_PLAY[0]/2]:
            for y in [py-POOL_PLAY[1]/2,py,py+POOL_PLAY[1]/2]:d.circle(*xy(x,y),.13*s,INK)
        text(px,22.1,"13'-4\" x 17'-0\" CUE ZONE",16,True)
        text(px,2.35,'8 FT POOL TABLE / 58 IN CUES',15,True)
        rect(18.1,7.7,26.7,18,'#ded7c9');rect(24.6,8.75,27.4,16.3,'#c4c0ac',MUTED)
        rect(20.55,10.25,24.15,14.75,WOOD,INK)
        text(22.1,19.7,'LOUNGE',18,True)
        rect(3.4,31.1,11,33.4,WOOD,INK);text(7.2,30.1,'REFRESHMENTS',13,True)
        for x in [4.5,7.2,9.9]:d.circle(*xy(x,29.5),.67*s,WOOD,INK)
        rect(17.2,31.5,26.4,33.3,WOOD);text(21.8,30.2,'MEDIA',15,True)
        rect(16.1,33.1,19.9,33.5,'#ffffff',TEAL);text(18,35,'HEAT PUMP HEAD',13,color=TEAL)
        rect(30.1,30.55,34.9,33.05,WOOD);text(32.5,29.4,'GAMING DESK',12,True)
        line((28.05,7),(28.05,22),INK,3)
        line((28,22),(35.5,22),INK,3);line((28,7),(31.65,7),INK,3)
    else:
        rect(27.5,.5,28,1,INK);rect(27.5,4.5,28,33.5,INK)
        rect(28,1,31.4,1.14,WOOD,INK)
        # Dashed conceptual swing, hinge at front jamb; clear of the flight.
        import math
        for a in range(0,90,8):
            line((28+3.4*math.cos(math.radians(a)),1+3.4*math.sin(math.radians(a))),(28+3.4*math.cos(math.radians(a+4)),1+3.4*math.sin(math.radians(a+4))),MUTED)
        rect(*PIT,PITFILL,TEAL,2)
        px,py=LIFT_CENTER;pw,pl=PLATFORM_WIDTH,PLATFORM_LENGTH
        rect(px-pw/2,py-pl/2,px+pw/2,py+pl/2,'#b6c0c0',INK)
        for x in CAR_CENTERS:
            rect(x-CAR_WIDTH/2,py-CAR_LENGTH/2,x+CAR_WIDTH/2,py+CAR_LENGTH/2,'#ebebe5',MUTED)
            rect(x-2.3,py-2.1,x+2.3,py+2.2,'#88a2a0')
        for x in [4.75,23.25]:
            for y in [LIFT_CENTER[1]-1.5,LIFT_CENTER[1]+1.5]:rect(x-.2,y-.25,x+.2,y+.25,INK)
        text(14,30.2,'2 AT GRADE + 2 IN PIT',20,True)
        text(14,28.5,"PIT ALLOWANCE 22' x 19'",15)
        text(14,-1.8,"22'-0\" WIDE GARAGE OPENING",15,True)
        line((3,.2),(25,.2),'#639995',5)
        rect(.5,0,3,.5,INK);rect(25,0,32,.5,INK);rect(35.5,0,36,.5,INK)
        line((32,.2),(35.5,.2),WOOD,5);text(33.75,-1.8,'ENTRY',14,True)
        rect(25.3,29.25,27.2,31.75,INK);text(20.3,32.4,'HYDRAULICS',13)
        # Fixed-floor route stays ahead of the operator bay and the moving equipment.
        rect(1,.75,27,4.25,'#d3e5dd')
        rect(*OPERATOR_ZONE,'#c3dcd1',TEAL,2)
        d.circle(*xy(25.4,5.9),.4*s,TEAL)
        rect(26.22,7,26.97,7.3,INK)
        text(10.7,6.2,"FIXED APRON",13,True)
        text(10.7,5.2,"7'-6\" DEEP",12)
        text(14,1.6,"3'-6\" PEDESTRIAN CROSS AISLE",13,True)
        text(32.7,5.4,'STAIR LOBBY',12,True)
        # Driver-side walk-off paths: selected deck must be stopped and aligned.
        for x in [6.1,15.4]:
            line((x,17),(x,2.8),TEAL,2)
            line((x,2.8),(x-.25,3.5),TEAL,2);line((x,2.8),(x+.25,3.5),TEAL,2)
        line((6.1,2.8),(29.8,2.8),TEAL,2)
        line((29.8,2.8),(29.8,6.5),TEAL,2)
        line((29.8,6.5),(29.5,6),TEAL,2);line((29.8,6.5),(30.1,6),TEAL,2)
        # Supplier access-enclosure line: architectural reservation, not hardware design.
        line((3,7.8),(25,7.8),'#ac673d',3)
        line((2.65,8),(2.65,27),INK,2);line((25.35,8),(25.35,27),INK,2)
        line((3,27.25),(25,27.25),INK,2)
    return xy
# Cover
cover=Drawing(1800,1700,OUT/'cover.pdf',title='Garage Loft 03 | Concept')
header(cover,'03 / GARAGE LOFT','Four cars below. Game night above.','KLAUS-style pit parking / passenger cars and sports cars / conditioned upstairs room')
hero=OUT/'01-exterior.png'
if not hero.exists():hero=HOME/'outputs/images/01-exterior.png'
cover.image(hero,80,210,1640,1184.44)
cover.text(80,1470,"36' x 34' footprint",28,INK,bold=True);cover.text(650,1470,'4 parking spaces',28,INK,bold=True);cover.text(1220,1470,'8 ft pool table',28,INK,bold=True)
cover.text(80,1520,'Cedar, pale plaster and dark metal. Dedicated pedestrian stair and upstairs heat pump.',22,MUTED)
footer(cover,1);cover.save()
# Floor-plan pair + individual editable plan outputs.
d=Drawing(1800,1350,OUT/'plans.pdf',title='Garage Loft 03 | Floor plans')
header(d,'03 / ARRANGEMENT','Garage and game room','Garage footprint 1,224 sq ft / upper slab 1,111.5 sq ft excluding stair opening / dimensions are conceptual')
d.text(120,265,'GROUND / PIT PARKING',25,INK,bold=True);d.text(985,265,'UPPER / GAME ROOM',25,INK,bold=True)
plan(d,120,965,18,False);plan(d,985,965,18,True)
d.text(120,1030,'Teal: fixed-floor stair route and separate 3 x 3 ft operator bay.',19,MUTED)
d.text(120,1062,'Orange: supplier-designed access protection required.',19,MUTED)
d.text(985,1030,'Full cue envelope kept clear of lounge and refreshment area.',19,MUTED)
d.text(985,1062,'Separate heating/cooling; no shared garage return air.',19,MUTED)
d.text(120,1155,'AREA BASIS',18,INK,bold=True);d.text(120,1190,'2,335.5 sq ft total projected floor area, including walls and garage/pit footprint; excludes 112.5 sq ft stair opening.',19,MUTED)
footer(d,2);d.save()
for upper,slug,title in [(False,'ground-plan','Ground / four-car pit parking'),(True,'upper-plan','Upper / game room')]:
    v=Drawing(1100,1100,OUT/(slug+'.pdf'),OUT/(slug+'.svg'),title)
    header(v,'GARAGE LOFT 03',title,'Dimensioned concept / not for construction')
    plan(v,150,965,19,upper)
    if not upper:
        v.text(80,1040,"Teal: walk to internal door / square: operator bay / orange: access protection reservation",16,MUTED)
    v.save()
# Section through a parking bay and pool table above, in both operating states.
d=Drawing(1800,1400,OUT/'section.pdf',OUT/'lift-section.svg','Garage Loft 03 | Lift operation and building section')
header(d,'03 / SECTION','The pit and the overhead clearance','KLAUS MultiBase 2072i-180 DP planning reference / original simplified equipment proxy')
def section(ox,oy,raised):
    s=19
    def xy(y,z):return ox+y*s,oy-z*s
    def r(y1,z1,y2,z2,fill,stroke=INK):d.rect(*xy(y1,z2),(y2-y1)*s,(z2-z1)*s,fill,stroke,1)
    def label(y,z,t,size=16):d.text(*xy(y,z),t,size,INK,anchor='middle')
    def line(a,b,color=MUTED,sw=1):d.line(*xy(*a),*xy(*b),color,sw)
    r(-1,-6.6,8,0,'#cdc5b5');r(27,-6.6,35,0,'#cdc5b5');r(8,-6.65,27,-PIT_FRONT_DEPTH,'#858e89')
    r(7.5,-PIT_FRONT_DEPTH,8,0,'#858e89');r(27,-PIT_FRONT_DEPTH,27.5,0,'#858e89')
    r(0,12,34,UPPER_FLOOR,'#858e89');r(0,22.5,34,23.2,INK)
    r(33.5,0,34,22.5,'#d0b28e');r(0,13.5,.5,15.5,'#d0b28e');r(0,21.8,.5,22.5,'#d0b28e')
    line((.2,15.5),(.2,21.8),'#74a7aa',3)
    for z in [UPPER_FLOOR]:
        r(9,z,9.4,UPPER_FLOOR+2.5,WOOD);r(15.6,z,16,UPPER_FLOOR+2.5,WOOD)
    r(8.3,UPPER_FLOOR+2.5,16.7,UPPER_FLOOR+2.8,WOOD);r(8.85,UPPER_FLOOR+2.8,16.15,UPPER_FLOOR+2.87,TEAL)
    label(13,19.4,'CONDITIONED GAME ROOM',18);label(13,17.9,"9'-0\" clear concept height",15)
    liftz=PLATFORM_SPACING if raised else 0
    for base,color in [(liftz,'#dae3dc'),(liftz-PLATFORM_SPACING,'#be9876')]:
        r(8,base-.2,8+PLATFORM_LENGTH,base,'#727e7c')
        r(LIFT_CENTER[1]-CAR_LENGTH/2,base+.7,LIFT_CENTER[1]+CAR_LENGTH/2,base+2.05,color)
        # Actual coupe height proxy, with sloping glass canopy.
        pts=[(8.4,base+2.05),(10.45,base+CAR_HEIGHT),(14.7,base+CAR_HEIGHT),(16.85,base+2.05)]
        pts=[(y+LIFT_CENTER[1]-12.5,z) for y,z in pts]
        for a,b in zip(pts,pts[1:]):line(a,b,TEAL,3)
        for y in [LIFT_CENTER[1]-4.65,LIFT_CENTER[1]+4.65]:d.circle(*xy(y,base+1.02),1.02*s,INK)
    line((-1,0),(35,0),TEAL,2)
    label(14,-7.8,'PIT: 72.9 IN FRONT / 70.9 IN REAR',15)
    label(14,10.7,"12'-0\" CLEAR GARAGE",17)
    label(14,-9.4,'LOWER PAIR AT DRIVEWAY' if raised else 'UPPER PAIR AT DRIVEWAY',20)
    label(14,-10.7,'Upper cars rise with the carriage' if raised else 'Lower cars stored below grade',16)
    for z1,z2,txt in [(0,12,"12'"),(13.5,22.5,"9'"),(-PIT_FRONT_DEPTH,0,"~6'")]:
        line((36,z1),(36,z2));label(37,(z1+z2)/2,txt,16)
section(120,900,False);section(990,900,True)
d.text(80,1207,'REFERENCE + LIMITS',19,INK,bold=True)
d.text(80,1244,'Based on KLAUS 06/2025 product data; final lift selection and approvals remain open. Movement shown schematically.',18,MUTED)
d.text(80,1275,'Pit structure, waterproofing, drainage, floor span, guards, fire separation, ventilation and HVAC sizing require site-specific design.',17,MUTED)
footer(d,3);d.save()
c=Drawing(1800,1500,OUT/'circulation.pdf',title='Garage Loft 03 | Human access')
header(c,'03 / CIRCULATION','A place to stand. A way upstairs.','Ground-floor access / same fixed-floor route with either parking level selected')
plan(c,140,1140,24,False)
x=1090
for y,title,lines in [
    (290,'01 / Park, stop, get out', ['Drive forward onto the stationary, level deck.', 'Exit on the driver side and walk toward the apron.', 'Passengers unload before parking; check actual doors.']),
    (470,'02 / Stand clear to operate', ['The 3 x 3 ft operator bay is on fixed floor.', 'Face the lift from its front-right corner.', 'No riders; access protection stays closed in motion.']),
    (650,'03 / Walk directly upstairs', ['Cross the fixed apron to the internal door.', 'The leaf opens into a 6 ft 6 in deep lobby.', 'Reach the first stair without crossing the pit.']),
    (830,'04 / Protect the approach', ['Orange marks the access-enclosure reservation.', 'Supplier must resolve guards, interlocks and sightlines.', 'Paint and schematic screens are not certified safeguards.'])]:
    c.text(x,y,title,26,INK,bold=True)
    for i,line in enumerate(lines):c.text(x,y+42+i*30,line,19,MUTED)
c.text(140,1255,'36 x 34 ft footprint / 7 ft 6 in fixed apron / 3 ft 6 in cross aisle / 42 in internal doorway allowance',23,INK,bold=True)
c.text(140,1300,'Walk-off arrows apply only with the deck stopped and aligned. Pause pedestrian crossing while a vehicle drives in or out.',20,MUTED)
c.text(140,1340,'Spatial concept only. Final door clear opening, fire separation, car-door clearance and lift protection remain to be coordinated.',19,MUTED)
footer(c,4);c.save()
writer=PdfWriter()
for name in ['cover','plans','section','circulation']:writer.append(str(OUT/(name+'.pdf')))
writer.write(str(OUT/'garage-loft.pdf'));writer.close()
print('GARAGE_CONCEPT_BOOK_CREATED',flush=True)
