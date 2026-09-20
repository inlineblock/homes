"""Render coordinated metric-source concept floor/site plans as SVG, PNG and PDF.

Furniture polygons come from the actual native-build placement manifest; without
that manifest the sheet is explicitly an unfurnished draft. No independent room
or furniture geometry is silently substituted into the final floor plan.
"""
from pathlib import Path
from html import escape
import argparse
import json
import math
import textwrap
import cairosvg
from design import *

ROOT = Path(__file__).resolve().parents[2]
BG='#f7f5ef'; INK='#2f423a'; MUTED='#6b786d'; WALL='#344b3f'

class Sheet:
    def __init__(self, title, subtitle, scale, ox, oy):
        self.width,self.height=1760,1280
        self.scale,self.ox,self.oy=scale/FT,ox,oy
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1760" height="1280" viewBox="0 0 1760 1280">']
        self.rect(0,0,1760,1280,BG)
        self.text(72,63,'H O M E S   /   A T R I U M   0 1',17)
        self.text(72,115,title,35,bold=True)
        self.text(72,152,subtitle,16,MUTED)
        self.line(72,177,1688,177,'#b0bba9')
    def xy(self,x,y): return self.ox+x*self.scale,self.oy-y*self.scale
    def text(self,x,y,value,size=14,color=INK,anchor='start',bold=False):
        self.svg.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(str(value))}</text>')
    def line(self,x1,y1,x2,y2,color=INK,sw=1,dash=None):
        self.svg.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def rect(self,x,y,w,h,fill='none',stroke='none',sw=1):
        self.svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def region(self, bounds, fill, stroke='none',sw=1):
        x1,y1,x2,y2=bounds;x,y=self.xy(x1,y2)
        self.rect(x,y,(x2-x1)*self.scale,(y2-y1)*self.scale,fill,stroke,sw)
    def poly(self, points, fill, stroke=INK, sw=1):
        coords=' '.join(f'{x:.2f},{y:.2f}' for x,y in [self.xy(*q[:2]) for q in points])
        self.svg.append(f'<polygon points="{coords}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def ln(self,a,b,color=INK,sw=1,dash=None): self.line(*self.xy(*a),*self.xy(*b),color,sw,dash)
    def label(self,x,y,value,size=12,bold=False,color=INK): self.text(*self.xy(ft(x),ft(y)),value,size,color,'middle',bold)
    def dim(self,a,b,label,vertical=False):
        self.ln(a,b,MUTED,.9)
        for q in (a,b): self.ln((q[0]-ft(.18),q[1]-ft(.18)),(q[0]+ft(.18),q[1]+ft(.18)),MUTED,1)
        x,y=self.xy((a[0]+b[0])/2,(a[1]+b[1])/2)
        if vertical:
            self.rect(x-30,y-12,60,22,BG)
            self.text(x,y+4,label,13,MUTED,'middle')
        else:self.text(x,y-8,label,13,MUTED,'middle')
    def note(self,y,heading,paragraph):
        self.text(1240,y,heading,16,bold=True)
        for i,line in enumerate(textwrap.wrap(paragraph,47)):
            self.text(1240,y+30+i*23,line,14,MUTED)
    def finish(self,out,name,number):
        self.line(72,1178,1688,1178,'#b0bba9')
        self.text(72,1213,f'{number}  /  '+name.replace('-',' ').upper(),15,bold=True)
        self.text(72,1244,'Concept study · Dimensions govern · Not for construction or permit use',13,MUTED)
        self.text(1688,1244,'ATRIUM 01',13,MUTED,'end')
        self.svg.append('</svg>'); data='\n'.join(self.svg).encode()
        out.mkdir(parents=True,exist_ok=True)
        (out/f'{name}.svg').write_bytes(data)
        cairosvg.svg2png(bytestring=data,write_to=str(out/f'{name}.png'))
        cairosvg.svg2pdf(bytestring=data,write_to=str(out/f'{name}.pdf'))
        print('PLAN_SAVED',out/name)


def walls(s):
    for name,a,b,t,opens in WALLS:
        length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length
        def point(d):return (a[0]+ux*d,a[1]+uy*d)
        cursor=0;door_index=0
        for off,width,sill,head,kind in sorted(opens):
            if off>cursor:s.ln(point(cursor),point(off),WALL,t*s.scale)
            if kind in ('window','glass','slider'):
                for delta in [-t*.3,t*.3]:
                    pa,pb=point(off),point(off+width)
                    s.ln((pa[0]-uy*delta,pa[1]+ux*delta),(pb[0]-uy*delta,pb[1]+ux*delta),'#669595',1.3)
                if kind=='slider':
                    pa,pb=point(off),point(off+width/2)
                    s.ln((pa[0]+uy*ft(.22),pa[1]-ux*ft(.22)),(pb[0]+uy*ft(.22),pb[1]-ux*ft(.22)),'#4f7b76',2.5)
                    mid=point(off+width*.25); start=(mid[0]-ux*ft(1),mid[1]-uy*ft(1)); end=(mid[0]+ux*ft(1),mid[1]+uy*ft(1))
                    start=(start[0]+uy*ft(.6),start[1]-ux*ft(.6));end=(end[0]+uy*ft(.6),end[1]-ux*ft(.6))
                    s.ln(start,end,'#4f7b76',1)
                    s.ln(end,(end[0]-ux*ft(.3)+uy*ft(.15),end[1]-uy*ft(.3)-ux*ft(.15)),'#4f7b76',1)
                    s.ln(end,(end[0]-ux*ft(.3)-uy*ft(.15),end[1]-uy*ft(.3)+ux*ft(.15)),'#4f7b76',1)
            elif kind in ('door','entry'):
                direction=DOOR_SWINGS.get((name,door_index),90)
                if direction=='pocket':
                    pocket_direction=POCKET_DIRECTIONS.get((name,door_index),1)
                    pocket_a,pocket_b=(off-width,off) if pocket_direction<0 else (off+width,off+2*width)
                    s.ln(point(pocket_a),point(pocket_b),'#a18b6d',1.5,'4 3')
                    s.ln(point(off),point(off+width),'#b6a58c',.8,'3 3')
                else:
                    hinge_end=DOOR_HINGES.get((name,door_index))=='end'
                    start=point(off+width if hinge_end else off);sign=1 if direction>0 else -1
                    tx,ty=(-ux,-uy) if hinge_end else (ux,uy)
                    nx,ny=-uy*sign,ux*sign
                    s.ln(start,(start[0]+nx*width,start[1]+ny*width),'#95836a',1.3)
                    prev=point(off if hinge_end else off+width)
                    for j in range(1,17):
                        angle=math.pi/2*j/16
                        q=(start[0]+width*(tx*math.cos(angle)+nx*math.sin(angle)),start[1]+width*(ty*math.cos(angle)+ny*math.sin(angle)))
                        s.ln(prev,q,'#b2a58e',.7);prev=q
                door_index+=1
            cursor=off+width
        if cursor<length:s.ln(point(cursor),b,WALL,t*s.scale)
    for name,a,b in COURTYARD_GLAZING:
        s.ln(a,b,'#669595',2.2)
        length=math.dist(a,b); n=round(length/ft(4));ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length
        for i in range(n+1):
            q=(a[0]+ux*length*i/n,a[1]+uy*length*i/n)
            s.ln((q[0]-ft(.07),q[1]-ft(.07)),(q[0]+ft(.07),q[1]+ft(.07)),WALL,3)
        if name in COURTYARD_SLIDERS:
            off,width=COURTYARD_SLIDERS[name]
            start=(a[0]+ux*off-uy*ft(.2),a[1]+uy*off+ux*ft(.2));end=(start[0]+ux*width/2,start[1]+uy*width/2)
            s.ln(start,end,'#547c77',3)


def furniture(s,layout):
    colors={'cabinetry':'#c4ab87','furniture':'#ded5c3','appliances':'#c4ceca','fixtures':'#edece3'}
    for item in layout.get('placements',[]) + layout.get('host_footprints',[]):
        name=item.get('name','').lower(); kind=item.get('kind','')
        if kind not in colors and not any(k in name for k in ['island','counter','bed','sofa','table','vanity','shower','tub','wardrobe']):continue
        if any(k in name for k in ['light','pendant','handle','pull','faucet','mirror','hood','rug','tile','sconce']):continue
        points=item.get('corners_m')
        if points and len(points)>=3:
            s.poly(points,colors.get(kind,'#d7c6a7'),'#978c77',.85)


def floor(out,layout):
    s=Sheet('A sheltered courtyard ring','3 bedrooms · 3 full baths · 2,400 sq ft gross enclosed · One occupied level',17,130,1036)
    s.region(box(0,0,60,44),'#eeeade')
    for slug,bounds,label in ROOMS:
        if 'bath' in slug or slug=='primary-wc':s.region(bounds,'#e0e8de')
        elif slug in ['bedroom-2','bedroom-3','primary']:s.region(bounds,'#ebe3d4')
    s.region(ATRIUM,'#d9e1c9','#92a383',1)
    s.region(box(27,16,34,25),'#adc095')
    s.region(box(35,14,40,27),'#e9e5d8')
    furniture(s,layout);walls(s)
    labels=[(6.5,12.3,'BEDROOM 02'),(16.5,3.0,'ENSUITE'),(6.5,26.3,'BEDROOM 03'),(16.5,19.8,'LAUNDRY'),(7,31.8,'PRIMARY BEDROOM'),(19.3,38.35,'PRIMARY'),(19.3,37.55,'BATH'),(23.25,36.1,'WC'),(29.6,4.9,'SHARED BATH'),(36.8,6.7,'FOYER'),(45,6.6,'PANTRY'),(54.5,4.4,'UTILITY / BULK'),(50.5,27,'KITCHEN'),(33,42.5,'DINING'),(50.5,42.5,'LIVING'),(33,25.8,'OPEN ATRIUM')]
    for x,y,label in labels:s.label(x,y,label,11.5,True)
    s.label(33,24.5,"16'-0\" × 15'-0\"",11,color=MUTED)
    s.label(33,10.1,'SHELTERED INDOOR ROUTE',10.5,color=MUTED)
    for y,char in zip([19,18,17,16,15,14,13],'GALLERY'):s.label(22.5,y,char,10,color=MUTED)
    s.dim(p(0,-3),p(60,-3),"60'-0\"")
    s.dim(p(-3,0),p(-3,44),"44'-0\"",True)
    for a,b in [(0,25),(25,41),(41,60)]:s.dim(p(a,46),p(b,46),f"{b-a}'-0\"")
    s.dim(p(25,11.5),p(41,11.5),"16'-0\"")
    s.dim(p(39.7,13),p(39.7,28),"15'-0\"",True)
    s.dim(p(20,8.7),p(25,8.7),"5'-0\" nominal")
    s.note(242,'01 / EVERYDAY ROUTES','The foyer connects both wings indoors. A separate laundry serves the bedroom gallery; food pantry and utility storage sit beside the kitchen.')
    s.note(410,'02 / KITCHEN FIRST','A 10 ft island faces the garden. South and east work runs include cooking, extraction, sink, dishwasher, panel-ready refrigeration and a separate oven.')
    s.note(579,'03 / A COMPLETE PRIVATE WING','Each bedroom has its own clothes storage. The primary suite includes two basins, a separate tub and shower, an enclosed toilet and a private entry vestibule.')
    s.note(771,'04 / HEIGHT AND AREA','Finished ceiling: 10 ft 6 in. Principal beams: 9 ft 6 in clear. Service ceilings: 9 ft. Gross enclosed area includes wall thickness; excludes open atrium, carport, canopies and terraces.')
    status='Furniture outlines derive from the current native placement manifest.' if layout else 'UNFURNISHED DRAFT: native placement manifest has not yet been generated.'
    s.note(963,'05 / DRAWING STATUS',status+' Nominal openings and planning zones are shown; final products and local requirements remain unverified.')
    s.finish(out,'floor-plan','A-01')


def site(out):
    s=Sheet('Arrival, parking and garden rooms','Illustrative level site · Orientation and boundaries unassigned · Carport excluded from enclosed area',7.6,265,784)
    s.region(SITE_BOUNDS,'#e4e8d9')
    s.region(box(-14,-48,77,-35),'#d0d1c9')
    s.region(box(0,-35,24,-27),'#d8d2c1')
    s.region(CARPORT,'#d6d0bf','#8c9381',1.4)
    for bay in PARKING_BAYS:
        s.region(bay,'none','#8e998a',1)
        x1,y1,x2,y2=bay
        s.region((x1+ft(1.65),y1+ft(1.5),x2-ft(1.65),y2-ft(1.5)),'#b2bdb2','#788b7b',1)
    s.region(SHELTERED_WALK,'#e9ddc6','#a59378',1)
    s.region(FRONT_LANDING,'#e9ddc6','#a59378',1)
    s.region(REAR_TERRACE,'#e6dcc6','#a59378',1)
    s.region(box(0,0,60,44),'#f0ece1',WALL,2)
    s.region(ATRIUM,'#b7c99c','#819871',1)
    for bounds in [box(-2,-2,62,46)]:
        x1,y1,x2,y2=bounds
        for a,b in [((x1,y1),(x2,y1)),((x2,y1),(x2,y2)),((x2,y2),(x1,y2)),((x1,y2),(x1,y1))]:s.ln(a,b,'#998e78',1,'5 4')
    for a,b in [(p(12,-3),p(36,-3)),(p(36,-3),p(36,10)),(p(36,10),p(22.5,10)),(p(36,10),p(47,10))]:s.ln(a,b,'#99764b',2.5,'6 4')
    for x,y,rad in [(-7,12,5),(-6,37,4),(68,12,5),(69,43,5),(9,55,5),(44,61,4)]:
        cx,cy=s.xy(ft(x),ft(y));s.svg.append(f'<circle cx="{cx}" cy="{cy}" r="{ft(rad)*s.scale}" fill="#bdcba9" stroke="#8c9f7b" stroke-width="1"/>')
    s.label(31,36,'ATRIUM 01',18,True);s.label(32,31,'2,400 sq ft gross enclosed',12)
    s.label(33,20,'OPEN COURT',11,True)
    s.label(12,-16,'TWO-CAR',11,True);s.label(12,-18,'CARPORT',11,True)
    s.label(43,51,'REAR TERRACE',12,True)
    s.label(32,-41,'ILLUSTRATIVE APPROACH / ROAD',11,color=MUTED)
    s.dim(p(0,-29),p(24,-29),"24'-0\"")
    s.dim(p(-3,-27),p(-3,-5),"22'-0\"",True)
    s.dim(p(0,48),p(60,48),"60'-0\" enclosed footprint")
    s.note(244,'01 / SHELTERED ARRIVAL','Two 10 × 18 ft parking reservations sit within a 24 × 22 ft carport. A covered five-foot walk runs behind the parking bays to the entry landing.')
    s.note(436,'02 / INDOOR AND OUTDOOR','The atrium is a garden room, not a required passage. Rear living and dining open to a separate terrace. Dashed lines indicate roof edges and the covered arrival route.')
    s.note(629,'03 / LANDSCAPE AND WATER','Planting locations are illustrative. Reserve roof outlets, accessible courtyard drains and a positive overflow route away from thresholds; final slopes and discharge need site design.')
    s.note(845,'04 / LIMITS OF THIS STUDY','No surveyed boundaries, real road, north orientation, climate or grade are asserted. Vehicle footprints are concept envelopes. Turning, runoff, foundations and accessibility require project-specific checks.')
    s.finish(out,'site-plan','A-02')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=ROOT/'homes/atrium-01/outputs/work/plans');args=parser.parse_args()
    manifest=Path(__file__).with_name('interiors-layout.json')
    layout=json.loads(manifest.read_text()) if manifest.exists() else {}
    floor(args.out,layout);site(args.out)
