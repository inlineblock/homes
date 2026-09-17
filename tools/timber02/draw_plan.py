"""Exterior presentation board and measured schematic plan."""
import sys,math,random,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from common.drawing import Drawing
from design import *
HOME=ROOT/'homes/timber-courtyard-02';OUT=HOME/'outputs/plans';OUT.mkdir(parents=True,exist_ok=True)
def plan(c,ox,oy,s=20):
    def xy(x,y):return ox+x*s,oy-y*s
    def r(a,b,d,e,fill,stroke='none',sw=1):c.rect(*xy(a,e),(d-a)*s,(e-b)*s,fill,stroke,sw)
    def line(a,b,color='#26372c',sw=1):c.line(*xy(*a),*xy(*b),color,sw)
    def text(x,y,t,size=15,bold=False):c.text(*xy(x,y),t,size,anchor='middle',bold=bold)
    r(0,0,62,48,'#eeece4')
    for slug,coords,name in ROOMS:
        if 'bath' in slug:r(*coords,'#e1e9e3')
        elif 'bedroom' in slug or slug=='primary':r(*coords,'#ece3d1')
    r(*ATRIUM,'#e2e1d5')
    for x in [20.3,35.4]:r(x,10,x+6.4,30,'#b5c29c')
    rng=random.Random(7)
    for i in range(52):
        x=rng.choice([rng.uniform(20.7,26.5),rng.uniform(36,41.5)]);y=rng.uniform(10.5,29.5)
        c.circle(*xy(x,y),rng.uniform(.3,.8)*s,rng.choice(['#859865','#667e55','#9caf83']))
    c.circle(*xy(24.6,21),2.3*s,'#a0775e','#7b654c',1)
    c.circle(*xy(38.5,25),1.7*s,'#80946b','#5e765b',1)
    for y in [11,16,21,26]:r(27.25,y-2.1,34.75,y+2.1,'#f3f0e5','#c2c5b5',.8)
    # Perimeter and the prominent four glass sides of the court.
    for a,b in [((0,0),(19,0)),((43,0),(62,0)),((0,0),(0,48)),((62,0),(62,48)),((0,48),(62,48))]:line(a,b,sw=7)
    for a,b in [((3.4,0),(13.6,0)),((48.4,0),(58.6,0)),((0,3),(0,11)),((0,25),(0,33)),((62,3),(62,18)),((62,25),(62,30)),((62,35),(62,44)),((17,48),(53,48)),((19,0),(43,0)),((19,8),(43,8)),((19,8),(19,32)),((43,8),(43,32)),((19,32),(43,32))]:line(a,b,'#7faaa7',3)
    for name,a,b,opens in WALLS:
        L=math.dist(a,b);ux=(b[0]-a[0])/L;uy=(b[1]-a[1])/L;point=lambda t:(a[0]+ux*t,a[1]+uy*t);start=0
        for off,w in opens:
            line(point(start),point(off),sw=5);p=point(off);direction=-1 if 'west-gallery'==name or 'pantry-west'==name else 1
            line(p,(p[0]+direction*w if uy else p[0],p[1]+w if ux else p[1]),'#ad9370',1.5);start=off+w
        line(point(start),b,sw=5)
    for x,y,w in [(7.5,6.2,5),(7.5,28.6,5),(54.6,9,6.5)]:
        r(x-w/2,y-3.3,x+w/2,y+3.3,'#f9f6ef','#aa987c',1)
        for dx in [-w*.25,w*.25]:r(x+dx-w*.21,y+1.5,x+dx+w*.21,y+3,'#ddd3bf','#b7a78c',.7)
    for x,y,w,d in [(0,14,9,8),(9,14,6,8),(47,24,8,8)]:
        r(x+.25,y+.25,x+3.75,y+3.75,'#f7f6ee','#8da18f',.8)
        r(x+w*.6-1.5,y+d-2,x+w*.6+1.5,y+d-.2,'#bba582','#8e795f',.7)
        c.circle(*xy(x+1,y+d-2.4),.55*s,'#fffdf8','#8da18f',.7)
    r(39,44.95,53.3,47.65,'#b69a70','#8c7658',1)
    r(41.9,35.1,46.3,42.5,'#f3ecda','#9b8a6d',1)
    for y in [36.5,38.8,41.1]:c.circle(*xy(40.85,y),.68*s,'#b59a71','#81714f',.8)
    r(29.9,39.3,36.7,42.7,'#b59970','#81714f',1)
    for x in [30.8,33.3,35.8]:
        for y in [38.5,43.5]:r(x-.7,y-.7,x+.7,y+.7,'#d6cdbb','#a09680',.7)
    r(17.5,34,29.5,46,'#e4dcc9')
    r(18.2,43.4,27.8,46.6,'#d1c7af','#978c73',1)
    c.circle(*xy(24,40),1.5*s,'#b49971','#81714f',1)
    labels=[(7.5,12,'BEDROOM 03'),(7.5,34,'BEDROOM 02'),(4.5,18.4,'BATH 02'),(12,18.4,'BATH 03'),(7.5,43,'LAUNDRY / FLEX'),(54.6,18.4,'PRIMARY SUITE'),(51,28.3,'PRIMARY BATH'),(58.5,28,'DRESSING'),(31,4,'GLAZED ENTRY'),(23,35,'LIVING'),(33.3,35,'DINING'),(44,33.3,'KITCHEN'),(58,41,'PANTRY'),(31,19.8,'COURTYARD'),(31,18.5,"24' x 24'")]
    for x,y,t in labels:text(x,y,t,13.5,True)
    # Board dimension lines use the actual outer footprint.
    for y,t in [(51,"62'-0\"")]:
        line((0,y),(62,y),'#667766',1)
        for x in [0,62]:line((x-.2,y-.3),(x+.2,y+.3),'#667766',1)
        text(31,y+.65,t,18)
    line((65,0),(65,48),'#667766',1)
    for y in [0,48]:line((64.8,y-.3),(65.2,y+.3),'#667766',1)
    xx,yy=xy(65,24);c.rect(xx-30,yy-16,60,32,'#faf8f2');c.text(xx,yy+6,"48'-0\"",17,anchor='middle')
    for i in range(3):r(27.25,-3-i*3,34.75,-1-i*3,'#e3dfd2','#bfbdac',.7)

d=Drawing(1800,1450,Path(tempfile.gettempdir())/'timber-floor-plan.pdf',OUT/'floor-plan.svg','Timber Courtyard 02 | Schematic plan')
d.rect(0,0,1800,1450,'#faf8f2');d.text(100,69,'TIMBER COURTYARD 02 / SCHEMATIC PLAN',30,bold=True)
d.text(100,109,'3 bedrooms / 3 baths / 2,400 sq ft gross enclosed / Interior layout is flexible',18,'#647563')
plan(d,220,1160,20);d.text(100,1415,'Concept only. Includes walls; excludes courtyard, garden and roof overhangs. Dimensions govern; do not scale.',15,'#647563');d.save()
render=HOME/'outputs/images/01-exterior.png'
if render.exists():
    board=Drawing(1800,2700,OUT/'design-board.pdf',title='Timber Courtyard 02 | Exterior and plan')
    board.rect(0,0,1800,2700,'#faf8f2');board.text(900,74,'02 / T I M B E R   C O U R T Y A R D',36,anchor='middle')
    board.text(900,115,'An exterior-led study in warm timber, dark metal and garden light',18,'#647563',anchor='middle')
    board.image(render,0,150,1800,1200)
    plan(board,220,2460,20)
    board.text(900,2670,'CONCEPT ONLY / 2,400 SQ FT GROSS ENCLOSED / 3 BEDROOMS / 3 BATHS',16,'#647563',anchor='middle');board.save()
print('TIMBER_DRAWINGS_SAVED')
