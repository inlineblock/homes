"""Draw reviewed concept plans from Twin Gables' shared dimensional records.

Drafts stay in outputs/work/plans. No model edits or GPU rendering are performed.
The plan-data.json receipt is exported by build.py from the same wall, opening,
and furnishing records used for the native scene; no separate layout lives here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
import platform
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common.drawing import Drawing
import design
HOME = ROOT / 'homes' / design.SLUG
INK, MUTED, PAPER = '#263b35', '#63756c', '#faf9f3'
WOOD, WET, GLASS = '#c8b79a', '#dce8e3', '#79a6a3'
WC_FILL, DOOR = '#e8e0cc', '#61482f'


class Plan:
    def __init__(self, drawing, origin, scale, label_scale=1):
        self.d, self.ox, self.oy, self.s = drawing, *origin, scale
        self.label_scale=label_scale
        self.clip_bounds=None

    def xy(self, x, y):
        return self.ox + x * self.s, self.oy - y * self.s

    def rect(self, rect, fill, stroke='none', sw=1):
        x1, y1, x2, y2 = rect
        self.d.rect(*self.xy(x1, y2), (x2-x1)*self.s, (y2-y1)*self.s, fill, stroke, sw)

    def line(self, a, b, color=INK, sw=1):
        self.d.line(*self.xy(*a), *self.xy(*b), color, sw)

    def text(self, x, y, value, size=13, bold=False, color=INK):
        if self.clip_bounds:
            x1,y1,x2,y2=self.clip_bounds
            if not (x1+.15<x<x2-.15 and y1+.5<y<y2-.3):return
        self.d.text(*self.xy(x,y), value, size*self.label_scale, color, anchor='middle', bold=bold)

    def circle(self, x, y, r, fill, stroke='none', sw=1):
        self.d.circle(*self.xy(x,y), r*self.s, fill, stroke, sw)

    def ellipse(self, x, y, rx, ry, fill, stroke=INK, sw=1):
        cx,cy=self.xy(x,y)
        self.d.svg.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*self.s}" ry="{ry*self.s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        from reportlab.lib.colors import HexColor
        self.d.pdf.setFillColor(HexColor(fill));self.d.pdf.setStrokeColor(HexColor(stroke));self.d.pdf.setLineWidth(sw)
        self.d.pdf.ellipse(cx-rx*self.s,self.d.h-cy-ry*self.s,cx+rx*self.s,self.d.h-cy+ry*self.s,fill=1,stroke=1)

    def arrow(self, a, b, color=DOOR, sw=1.2):
        self.line(a,b,color,sw)
        angle=math.atan2(b[1]-a[1],b[0]-a[0]);head=.3
        for offset in (-.5,.5):self.line(b,(b[0]-head*math.cos(angle+offset),b[1]-head*math.sin(angle+offset)),color,sw)

    def arc(self, origin, radius, start, end, color='#ac9678', sw=.8):
        pts = [(origin[0]+radius*math.cos(a), origin[1]+radius*math.sin(a))
               for a in [start+(end-start)*i/30 for i in range(31)]]
        for a,b in zip(pts, pts[1:]): self.line(a,b,color,sw)

    def polygon(self, coords, fill, stroke=INK, sw=1):
        # Paired SVG and PDF polygon primitive, preserving source coordinates.
        pts = [self.xy(*p) for p in coords]
        self.d.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+
                          f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        from reportlab.lib.colors import HexColor
        path = self.d.pdf.beginPath()
        path.moveTo(pts[0][0], self.d.h-pts[0][1])
        for x,y in pts[1:]: path.lineTo(x,self.d.h-y)
        path.close()
        self.d.pdf.setFillColor(HexColor(fill))
        self.d.pdf.setStrokeColor(HexColor(stroke))
        self.d.pdf.setLineWidth(sw)
        self.d.pdf.drawPath(path,fill=1,stroke=1)

    def dimension(self, a, b, text, axis='x'):
        self.line(a,b,MUTED,.8)
        for x,y in (a,b): self.line((x-.2,y-.25),(x+.2,y+.25),MUTED,1)
        x,y=(a[0]+b[0])/2,(a[1]+b[1])/2
        px,py=self.xy(x,y)
        width=max(48,len(text)*8)
        self.d.rect(px-width/2,py-13,width,22,PAPER)
        self.d.text(px,py+3,text,14,MUTED,anchor='middle')


def ft(v):
    inch=round(v*12); whole,rem=divmod(inch,12)
    return f'{whole}\'-{rem}"'


def header(d, title, subtitle):
    d.rect(0,0,d.w,d.h,PAPER)
    d.text(75,60,'T W I N   G A B L E S   C O U R T Y A R D',25,INK,bold=True)
    d.text(75,95,title,20,INK)
    d.text(75,123,subtitle,14,MUTED)
    d.line(75,145,d.w-75,145,'#c7cfc2',1)


def footer(d, page):
    d.line(75,d.h-67,d.w-75,d.h-67,'#c7cfc2',1)
    d.text(75,d.h-39,'CONCEPT DESIGN  /  Dimensions govern; do not scale. Site, products and engineering unverified.',12,MUTED)
    d.text(d.w-75,d.h-39,page,12,MUTED,anchor='end')


def room_labels(data):
    labels=[]
    for name,rect,height in data['rooms']:
        x1,y1,x2,y2=rect; x,y=(x1+x2)/2,(y1+y2)/2
        title=name.upper()
        if 'Primary suite' in name: x=x1+(x2-x1)*(.7 if x1==0 else .3);y=y1+3.2;title='PRIMARY WEST' if x1==0 else 'PRIMARY EAST'
        elif 'dressing' in name:title='WALK-IN';y=y1+6.2
        elif 'ensuite' in name:title='ENSUITE';y=y1+6.2
        elif 'Office' in name:title='OFFICE / GUEST';x=x1+6.5;y=y2-4.7
        elif 'Guest bath' in name:title='BATH 3';x=x1+4.2;y=y1+4.6
        elif 'gallery' in name:title='GALLERY';y=(y1+y2)/2;
        elif 'bookcase' in name.lower() or 'library wall' in name.lower():title=''
        elif 'primary sleeping' in name.lower():title='PRIMARY WEST' if x1==0 else 'PRIMARY EAST';y=y1+4
        elif 'laundry' in name.lower():title='LAUNDRY';y=y1+4.5
        elif 'mechanical' in name.lower():title='MECH'
        elif 'household storage' in name.lower():title='STORAGE'
        elif name=='Kitchen':y=y1+1.5; x=x1+7
        elif name=='Living':y=y1+1.5
        elif name=='Dining':y=y1+1.5
        elif 'pantry' in name.lower():y=y1+4.8;title='BUTLER PANTRY' if 'butler' in name.lower() else name.upper()
        elif name=='Laundry':y=y1+5.2
        labels.append({'at':[x,y],'text':title,'size':8 if 'gallery' in name else 11 if name=='Guest bath' else 13})
    return labels

def toilet_symbol(p, obj, rect):
    """Conventional tank and bowl, oriented inside the actual exported footprint."""
    points=obj.get('footprint')
    if not points:
        x1,y1,x2,y2=rect;points=[(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
        quarter=round(obj.get('rotation',0)/(math.pi/2))%4
        points=points[quarter:]+points[:quarter]
    a,b,_,d=points
    def local(u,v):return (a[0]+u*(b[0]-a[0])+v*(d[0]-a[0]),a[1]+u*(b[1]-a[1])+v*(d[1]-a[1]))
    p.polygon([local(u,v) for u,v in ((.05,.73),(.95,.73),(.95,.97),(.05,.97))],'#fafbf7','#697f72',1.1)
    width,depth=math.dist(a,b),math.dist(a,d)
    rx,ry=width*.40,depth*.35
    if abs(b[1]-a[1])>abs(b[0]-a[0]):rx,ry=ry,rx
    p.ellipse(*local(.5,.39),rx,ry,'#ffffff','#697f72',1.1)
    p.ellipse(*local(.5,.38),rx*.62,ry*.63,'#dce8e3','#94a79a',.7)


def room_clear_dimension(value):
    # Retain quarter-inch precision rather than invent a clean dimension.
    from fractions import Fraction
    quarter=round(value*12*4);feet,rem=divmod(quarter,48);inches,fraction=divmod(rem,4)
    suffix='' if not fraction else ' '+str(Fraction(fraction,4))
    return f"{feet}'-{inches}{suffix}\""


def draw_wc_annotations(p, data):
    for wc in data.get('wc_rooms',[]):
        x1,y1,x2,y2=wc['rect']
        at=wc.get('label_at')
        if at is None:
            toilets=[o for o in data.get('furnishings',[]) if 'toilet' in o.get('name','').lower() and o.get('rect') and x1<=(o['rect'][0]+o['rect'][2])/2<=x2 and y1<=(o['rect'][1]+o['rect'][3])/2<=y2]
            front=not toilets or (toilets[0]['rect'][1]+toilets[0]['rect'][3])/2>(y1+y2)/2
            at=[(x1+x2)/2,y1+.8 if front else y2-1.7]
        p.text(at[0],at[1]+.7,'TOILET',10.5,True)
        p.text(at[0],at[1],f"{room_clear_dimension(x2-x1)} x {room_clear_dimension(y2-y1)}",8.5,True)



def draw_layout(p,data):
    p.rect((0,0,design.WIDTH,design.DEPTH),'#eae8de')
    for name,rect,height in design.ROOMS:
        color=WET if any(x in name.lower() for x in ('bath','ensuite','laundry')) else '#eae8de'
        if 'dressing' in name.lower():color='#e3d9c8'
        if 'Primary suite' in name:color='#eee6d7'
        p.rect(rect,color)
    for wc in data.get('wc_rooms',[]):p.rect(wc['rect'],WC_FILL,'#af9c7e',.7)
    p.rect(design.COURT,'#dce4d3','#b3c1a6',1)
    # Exported site extents establish paving and planted beds; no invented furniture.
    for obj in data.get('site',[]):
        if 'rect' not in obj:continue
        if obj.get('kind')=='planting':
            p.rect(obj['rect'],'#c0cdaa','#a5b693',.6)
            x1,y1,x2,y2=obj['rect']
            for y in range(math.ceil(y1)+1,math.floor(y2),3):p.circle((x1+x2)/2,y,.9,'#a4b88c','#92a57b',.7)
    for tree in data.get('plan_trees',[]):
        p.circle(*tree['at'],tree['radius'],'#a1b68a','#7f986d',1)
        p.circle(*tree['at'],tree['radius']*.76,'#b0c29b','#93aa7f',.7)
    for obj in sorted(data.get('furnishings',[]),key=lambda o: 0 if 'rug' in o.get('name','').lower() else 2 if o.get('kind')=='counter' else 3 if o.get('kind') in ('appliances','fixtures') else 1):
        if obj.get('plan_visibility')=='overhead':continue
        name=obj.get('name','').lower();rect=obj.get('rect')
        footprint=obj.get('footprint')
        if rect is None and footprint:
            rect=[min(q[0] for q in footprint),min(q[1] for q in footprint),max(q[0] for q in footprint),max(q[1] for q in footprint)]
        if rect is None:continue
        if rect[1]>=design.DEPTH or rect[3]<=0:continue
        if any(t in name for t in ('light','hood','tap','faucet','pull','lever')) or ('mirror' in name and 'basin' not in name):continue
        fill=WOOD
        if any(t in name for t in ('bed','sofa','chair','stool')) or any(t in name.split() for t in ('king','queen')):fill='#f9f5e9'
        if any(t in name for t in ('basin','sink','toilet','tub','shower')):fill='#f8fbf8'
        if any(t in name for t in ('cooktop','oven','fridge','washer','dryer','dishwasher')):fill='#8f9990'
        if obj.get('plan_label')=='W/D':fill='#8f9990'
        if 'rug' in name:fill='#ded7c7'
        if 'toilet' not in name:
            if footprint:p.polygon(footprint,fill,'#9b9c8d',.85)
            else:p.rect(rect,fill,'#9b9c8d',.85)
        x1,y1,x2,y2=rect
        if ('bed' in name and 'bedside' not in name) or any(t in name.split() for t in ('king','queen')):
            # Shared bed families define the headboard toward local -Y.
            side=obj.get('headboard_side') or ['south','east','north','west'][round(obj.get('rotation',0)/(math.pi/2))%4]
            if side in ('west','east'):
                bx=x1+.25 if side=='west' else x2-1.3
                p.rect((bx,y1+.3,bx+1.05,y2-.3),'#dcd4c2','#b8b2a1',.6)
                edge=x1 if side=='west' else x2;p.line((edge,y1),(edge,y2),'#8c7655',2.3)
            else:
                by=y1+.25 if side=='south' else y2-1.3
                p.rect((x1+.3,by,x2-.3,by+1.05),'#dcd4c2','#b8b2a1',.6)
                edge=y1 if side=='south' else y2;p.line((x1,edge),(x2,edge),'#8c7655',2.3)
        if 'toilet' in name:toilet_symbol(p,obj,rect)
        if 'tub' in name:
            p.ellipse((x1+x2)/2,(y1+y2)/2,(x2-x1)*.39,(y2-y1)*.39,'#eef3ee','#a8b6ae',.7)
            if p.label_scale>1:p.text((x1+x2)/2,(y1+y2)/2,'TUB',8,True)
        if 'sofa' in name:
            if x2-x1<y2-y1:
                p.line((x1+.35,y1+.2),(x1+.35,y2-.2),'#b8b2a1',.8)
                for i in (1,2):p.line((x1+.4,y1+(y2-y1)*i/3),(x2-.15,y1+(y2-y1)*i/3),'#b8b2a1',.65)
            else:
                p.line((x1+.2,y2-.35),(x2-.2,y2-.35),'#b8b2a1',.8)
                for i in (1,2):p.line((x1+(x2-x1)*i/3,y1+.15),(x1+(x2-x1)*i/3,y2-.4),'#b8b2a1',.65)
        if obj.get('kind')=='appliances' or any(t in name for t in ('induction','cooktop',' hob')):
            if 'induction' in name or 'cooktop' in name or 'range' in name:
                p.rect(rect,'#3d4842','#26372d',.7)
                for dx in (.3,.7):
                    for dy in (.25,.75):p.circle(x1+(x2-x1)*dx,y1+(y2-y1)*dy,.21,'#707b73','#c0c9c0',.6)
            label=obj.get('plan_label')
            if label:
                pass
            elif ('washer' in name and 'dryer' in name) or 'laundry tower' in name:label='W/D STACK'
            elif 'refrigerator' in name:
                label='FRIDGE'
                p.text((x1+x2)/2,(y1+y2)/2+.7,'48 in',10,True)
            elif 'dishwasher' in name:label='DW'
            elif 'oven' in name:label='OVEN'
            elif 'washer' in name:label='W'
            elif 'dryer' in name:label='D'
            elif 'induction' in name or 'cooktop' in name:label='HOB'
            if 'induction' in name and not obj.get('plan_label'):p.text(x1-1.2,(y1+y2)/2,'HOB',9,True)
            if 'induction' in name and not obj.get('plan_label'):p.text(x1-1.2,(y1+y2)/2-.7,'OVEN',8,True)
            if 'induction' in name and not obj.get('plan_label'):p.text(x1-1.2,(y1+y2)/2+.7,'HOOD',8,True)
            if label:p.text((x1+x2)/2,(y1+y2)/2,label,10,True,'#24382f')
        if 'basin' in name:
            p.circle((x1+x2)/2,(y1+y2)/2,min(x2-x1,y2-y1)*.35,'#e2eae5','#82958a',.8)
            if 'laundry' in name or 'stain' in name:p.text((x1+x2)/2,y1-.5,'STAIN SINK',9,True)
        if 'sink' in name and obj.get('kind')=='fixtures':
            p.rect((x1+.12,y1+.2,x2-.2,y2-.2),'#e2eae5','#82958a',.8)
            if 'stain' in name or 'laundry' in name:p.text((x1+x2)/2,y1-.5,'STAIN SINK',9,True)
            elif 'pantry' in name or 'prep' in name:p.text((x1+x2)/2,y1-.5,'PREP SINK',9,True)
        if 'shower' in name:
            p.line((x1,y1),(x2,y2),'#bac9c0',.7)
            p.line((x1,y2),(x2,y1),'#bac9c0',.7)

        if 'linen' in name and any(t in name for t in ('closet','bath','cabinet')):p.text((x1+x2)/2,(y1+y2)/2,'LINEN',10,True)
        module=(obj.get('storage_module_type') or '').lower()
        if module and not any(t in module for t in ('hang','drawer','shoe','shel','book','hamper')):
            module='drawers' if 'drawer' in name else 'shelves' if 'storage' in name else 'bookcase' if 'bookcase' in name else ''
        if 'hang' in module:module='hanging'
        elif 'drawer' in module:module='drawers'
        elif 'shoe' in module:module='shoes'
        elif 'book' in module:module='bookcase'
        elif 'shel' in module:module='shelves'
        elif 'hamper' in module:module='hamper'
        if not module:
            aid=obj.get('asset','').lower()
            if 'bookcase' in aid or 'bookcase' in name:module='bookcase'
            elif 'shoe' in aid or 'shoe' in name:module='shoes'
            elif 'hanging' in aid or 'hanging' in name:module='hanging'
            elif 'closet' in name or 'wic' in name:
                if 'drawer' in aid or 'drawer' in name:module='drawers'
                elif 'shelf' in aid or 'shelf' in name:module='shelves'
        if module:
            along_y=(y2-y1)>(x2-x1)
            if module in ('drawers','shoes','shelves','bookcase'):
                count=4 if module=='shoes' else 3
                for i in range(1,count+1):
                    if along_y:p.line((x1+.08,y1+(y2-y1)*i/(count+1)),(x2-.08,y1+(y2-y1)*i/(count+1)),'#8f8169',.75)
                    else:p.line((x1+(x2-x1)*i/(count+1),y1+.08),(x1+(x2-x1)*i/(count+1),y2-.08),'#8f8169',.75)
            elif module=='hanging':
                if along_y:p.line(((x1+x2)/2,y1+.1),((x1+x2)/2,y2-.1),'#8f8169',1.1)
                else:p.line((x1+.1,(y1+y2)/2),(x2-.1,(y1+y2)/2),'#8f8169',1.1)
            if module=='bookcase':p.text((x1+x2)/2,(y1+y2)/2,'BOOKS',9,True)
            elif p.label_scale>1:p.text((x1+x2)/2,(y1+y2)/2,{'hanging':'HANG','drawers':'DRAWERS','shoes':'SHOES','shelves':'SHELVES'}.get(module,module.upper()),7,True)


    for wall in data['walls']:
        a,b=wall['a'],wall['b'];length=math.dist(a,b)
        ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length
        point=lambda t:(a[0]+ux*t,a[1]+uy*t)
        cursor=0;sw=5.8 if wall.get('exterior') or 'WC' in wall['name'] else 4
        for opening in sorted(wall.get('openings',[]),key=lambda item:item['offset']):
            off,w=opening['offset'],opening['width']
            p.line(point(cursor),point(off),INK,sw)
            if opening.get('type') in ('opening','cased opening','cased-opening','passage','cased','open passage'):
                pass
            elif opening.get('type')=='window':
                p.line(point(off),point(off+w),GLASS,2.3)
            elif opening.get('type')=='pocket':
                direction=opening.get('pocket_direction')
                if direction not in (-1,1):
                    if data.get('proposed'):raise ValueError(f"Missing proposed pocket direction: {wall['name']}")
                    # Legacy native receipts did not export travel direction: preserve
                    # the closed-leaf symbol rather than inventing a pocket cavity.
                    p.line(point(off),point(off+w),'#907957',2)
                    cursor=off+w
                    continue
                # Keep the doorway blank; show the recessed leaf beyond its jamb and travel arrow.
                end=off+w if direction==1 else off
                stored=point(end+direction*w*.85)
                p.line(point(end),stored,DOOR,2.1)
                normal=(-uy*.4,ux*.4)
                q1=point(off+w*.5);q2=point(end+direction*w*.5)
                p.arrow((q1[0]+normal[0],q1[1]+normal[1]),(q2[0]+normal[0],q2[1]+normal[1]),DOOR,1.1)
            elif opening.get('type') in ('slider','sliding','glazing','sliding glazing','fixed glazing'):
                color='#907957' if opening.get('type')=='pocket' else GLASS
                p.line(point(off),point(off+w),color,2)
                mid=point(off+w/2);p.line(mid,point(off+w),color,3.2)
            elif opening.get('type') in ('removable panels','closed door') or opening.get('state')=='closed':
                p.line(point(off),point(off+w),'#907957',3.5)
            else:
                hinge=point(off);base=math.atan2(uy,ux)
                sign=opening.get('swing',1)
                angle=base+math.radians(opening.get('angle_degrees',55))*sign
                leaf=(hinge[0]+math.cos(angle)*w,hinge[1]+math.sin(angle)*w)
                p.line(hinge,leaf,'#907957',1.4)
                p.arc(hinge,w,base,angle)
            cursor=off+w
        p.line(point(cursor),b,INK,sw)
    draw_wc_annotations(p,data)
    # Label anchors are supplied alongside source room records; avoid furniture overlaps.
    for item in (room_labels(data)+data.get('labels',[]) if data.get('proposed') else data.get('labels',[]) or room_labels(data)):
        x,y=item['at'];p.text(x,y,item['text'],item.get('size',12),item.get('bold',True))
    for name,(x1,y1,x2,y2),height in design.ROOMS:
        if 'dressing' in name:p.text((x1+x2)/2,(y1+y2)/2-1,'HANG / SHELF',8,color=MUTED)
        if 'Primary suite' in name:
            p.text(x1+(x2-x1)*(.7 if x1==0 else .3),y1+1.9,f'{ft(x2-x1)} x {ft(y2-y1)} gross',10,color=MUTED)
        if name in ('Living','Dining','Kitchen'):
            p.text((x1+x2)/2,y1+.35,f'{ft(x2-x1)} x {ft(y2-y1)} gross',10,color=MUTED)


def draw_floor(out, data):
    """Plan linework is source geometry; furnishing silhouettes are exported bounds."""
    d=Drawing(1900,1960,out/'floor-plan.pdf',out/'floor-plan.svg','Twin Gables | Furnished concept floor plan')
    header(d,data.get('title','One level / furnished concept plan'),
           ('PROPOSED 2D LAYOUT / ' if data.get('proposed') else '')+f"Two primary suites + office / three baths / {design.AREA:,.0f} sq ft enclosed, excluding courtyard")
    scale=min(1394/design.WIDTH,1230/design.DEPTH)
    p=Plan(d,((1900-design.WIDTH*scale)/2,1540),scale)
    draw_layout(p,data)
    p.dimension((0,design.DEPTH+4),(design.WIDTH,design.DEPTH+4),ft(design.WIDTH))
    p.dimension((design.WIDTH+4,0),(design.WIDTH+4,design.DEPTH),ft(design.DEPTH),'y')
    c1,cy1,c2,cy2=design.COURT
    p.text((c1+c2)/2,cy2-5,'OPEN COURTYARD',16,True)
    p.text((c1+c2)/2,cy2-6.5,f"{c2-c1:g}' x {cy2-cy1:g}' / {(c2-c1)*(cy2-cy1):,.0f} sq ft",13)
    p.text(design.WIDTH/2,-2,'4 ft SOLID ENTRY DOOR',11,True)
    p.text(design.WIDTH/2,-4,'OPAQUE ENTRY / FRONT',13,True)
    p.text(design.WIDTH/2,-6,'FRONT ARRIVAL / ROAD SIDE' if data.get('proposed') else 'ROAD + PARKING: SEE ARRIVAL DIAGRAM',10,color=MUTED)
    d.text(100,1725,'EVERYDAY COMFORT',17,INK,bold=True)
    notes=[
       'Both primary suites: king bedroom, walk-in dressing, double vanity, separate tub + shower, enclosed WC and bath linen.',
       'Full kitchen: 36-in induction cooking, built-in oven + hood, 48-in panel-ready fridge, dishwasher, sink, drawers and walk-in pantry.',
       'Three full baths total: two ensuites (each with an enclosed toilet room) plus one hall bath. Toilet rooms are not additional bathrooms.',
       'Door arcs show hinge swings; brown arrows show pocket-door travel. Toilet-room dimensions are measured clear inside faces.',
       'Area is gross planning-grid area including wall allowances, not a measured exterior-cladding footprint. Product/engineering review remains.',
    ]
    if not data.get('proposed') and not data.get('wc_rooms'):
        notes[3]='Door arcs show source opening states. Legacy pocket-door receipts omit cavity travel and clear toilet-room dimensions.'
    if data.get('proposed'):
        import textwrap
        notes=[]
        for text in [data.get('summary',''),*data.get('tradeoffs',[])]:
            notes.extend(textwrap.wrap(text,145))
        notes=(notes[:4]+[f'Overall envelope: {ft(design.WIDTH)} x {ft(design.DEPTH)}; open court: {(c2-c1)*(cy2-cy1):,.0f} sq ft; enclosed: {design.AREA:,.0f} sq ft.',
                                  'Proposed 2D arrangement for selection; no native model has been rebuilt or engineering confirmed.'])
    for i,t in enumerate(notes):d.text(100,1760+i*25,t,14,MUTED)
    footer(d,('OPTION '+data['option_key'].upper()+' / FURNISHED PLAN') if data.get('proposed') else '01 / MAIN FLOOR')
    d.save()


def draw_details(out,data):
    d=Drawing(1900,1960,out/'interior-details-page.pdf',out/'interior-details.svg','Twin Gables | Bathroom, dressing and kitchen details')
    header(d,data.get('title','Interior details')+' / storage + privacy',
           ('PROPOSED 2D LAYOUT / ' if data.get('proposed') else '')+'Two ensuite baths and one hall bath; enclosed WCs remain part of their ensuites.')
    rooms={name:rect for name,rect,height in data['rooms']}
    def bounds(names):
        rects=[rooms[name] for name in names]
        return min(r[0] for r in rects),min(r[1] for r in rects),max(r[2] for r in rects),max(r[3] for r in rects)
    def panel(title,rect,left,top,scale,key):
        x1,y1,x2,y2=rect;w,h=(x2-x1)*scale,(y2-y1)*scale
        d.text(left,top-26,title,min(18,900/max(len(title),1)),INK,bold=True)
        d.rect(left-12,top-12,w+24,h+24,'#f5f3eb','#ccd2c5',.8)
        path=d.pdf.beginPath();path.rect(left,d.h-top-h,w,h)
        d.pdf.saveState();d.pdf.clipPath(path,stroke=0,fill=0)
        d.svg.append(f'<defs><clipPath id="{key}"><rect x="{left}" y="{top}" width="{w}" height="{h}"/></clipPath></defs><g clip-path="url(#{key})">')
        view=Plan(d,(left-x1*scale,top+y2*scale),scale,label_scale=1.25)
        view.clip_bounds=rect
        draw_layout(view,data)
        d.svg.append('</g>');d.pdf.restoreState()
    for side,left in [('West',110),('East',1050)]:
        custom=data.get('detail_views',[])
        r=custom[0 if side=='West' else 1]['rect'] if len(custom)>=2 else bounds([n for n in rooms if side.lower() in n.lower() and any(k in n.lower() for k in ('dressing','ensuite'))])
        scale=min(720/(r[2]-r[0]),490/(r[3]-r[1]))
        title=custom[0 if side=='West' else 1].get('short_title',custom[0 if side=='West' else 1]['title']) if len(custom)>=2 else side.upper()+' SUITE / DRESSING + ENSUITE'
        panel(title,r,left,240,scale,side.lower()+'-suite-detail')
        if len(custom)>=2 and custom[0 if side=='West' else 1].get('note'):
            d.text(left,240+(r[3]-r[1])*scale+38,custom[0 if side=='West' else 1]['note'],14,MUTED)
    kitchen_names=[n for n in rooms if n in ('Kitchen','Laundry','Mechanical') or 'pantry' in n.lower() or 'bookcase' in n.lower()]
    kitchen_bounds=data['detail_views'][2]['rect'] if len(data.get('detail_views',[]))>=3 else bounds(kitchen_names)
    kitchen_scale=min(780/(kitchen_bounds[2]-kitchen_bounds[0]),850/(kitchen_bounds[3]-kitchen_bounds[1]))
    panel(data['detail_views'][2].get('short_title',data['detail_views'][2]['title']) if len(data.get('detail_views',[]))>=3 else 'KITCHEN / BUTLER PANTRY / HOUSEHOLD SUPPORT',kitchen_bounds,110,910,kitchen_scale,'kitchen-detail')
    d.text(1030,950,'READING THE DETAILS',19,INK,bold=True)
    notes=[
        'Warm shaded compartments are private toilet rooms.',
        'Printed WC dimensions are clear inside faces.',
        'Premium bidet toilets are intended; fixture models remain unselected.',
        'Brown arrows show pocket-door retraction direction.',
        'Curved arcs indicate hinged-door movement.',
                'Closet rails, drawers, shoe racks and shelves use distinct marks.',
                'Two W/D labels denote two stacked washer/dryer pairs.',
        'The stain sink and pantry prep sink flank their shared wall.',
        'The bookcase strip is separate from the laundry footprint.',
    ]
    for i,t in enumerate(notes):d.text(1030,1000+i*36,t,15,MUTED)
    y=1445
    for wc in data.get('wc_rooms',[]):
        rect=wc['rect'];label=wc.get('name','Toilet room')
        d.text(1030,y,label.upper(),15,INK,bold=True)
        d.text(1030,y+26,f"Clear inside: {room_clear_dimension(rect[2]-rect[0])} x {room_clear_dimension(rect[3]-rect[1])}.",14,MUTED)
        if wc.get('clear_passage_ft') is not None:
            d.text(1030,y+52,f"Door passage in shown state: {room_clear_dimension(wc['clear_passage_ft'])}.",14,MUTED)
        y+=100
    d.text(1030,1735,'Fixture models and final hardware remain to be selected.',13,MUTED)
    footer(d,('OPTION '+data['option_key'].upper()+' / INTERIOR DETAILS') if data.get('proposed') else '02 / INTERIOR DETAILS')
    d.save()


def draw_roof(out, data=None):
    d=Drawing(1700,1810,out/'roof-and-section.pdf',out/'roof-and-section.svg','Twin Gables | Roof and clear-height concept')
    header(d,'Roof rhythm + clear-height study','Two parallel gables; continuous ridges and common eaves. Steel structure concealed by wood-look covers.')
    width, depth = design.WIDTH, design.DEPTH
    c1, cy1, c2, cy2 = design.COURT
    wing = c1
    mids = (wing/2, (c2+width)/2)
    p=Plan(d,(110,800),9)
    p.rect((0,0,design.WIDTH,design.DEPTH),'#ecebe3',INK,1.5)
    p.rect(design.COURT,PAPER,GLASS,2)
    for x in (0,c1,c2,width): p.line((x,0),(x,depth),INK,1.6)
    for x in mids:
        p.line((x,0),(x,depth),INK,3)
        p.text(x,depth+2,'RIDGE',11,True)
        for y in (depth*.2,depth*.5,depth*.8):
            for sign in (-1,1):
                a=(x+sign,y); b=(x+sign*7,y)
                p.line(a,b,MUTED,1)
                p.line(b,(b[0]-sign*.9,y+.4),MUTED,1)
                p.line(b,(b[0]-sign*.9,y-.4),MUTED,1)
    p.text(width/2,(cy1+cy2)/2,'OPEN COURTYARD',12,True)
    p.text(width/2,(cy1+cy2)/2-3,f'{c2-c1:g} ft x {cy2-cy1:g} ft',12)
    p.text(width/2,(cy2+depth)/2,'LOW CONNECTOR',11,True)
    p.text(width/2,(cy2+depth)/2-2.3,'Positive fall',10)
    p.text(width/2,cy1/2,'PRIVATE ENTRY',10,True)
    p.dimension((0,-4),(width,-4),ft(width))
    d.text(110,205,'ROOF ORGANIZATION',16,INK,bold=True)
    # Diagram through the rear public band; shared ceiling datums, not a structural detail.
    q=Plan(d,(855,540),9.7)
    q.line((0,0),(width,0),INK,3)
    for a,b in [((0,0),(0,design.EAVE)),((width,0),(width,design.EAVE))]:q.line(a,b,INK,3)
    roof=[(0,design.EAVE),(mids[0],design.RIDGE),(c1,design.EAVE),(c2,design.EAVE),(mids[1],design.RIDGE),(width,design.EAVE)]
    for a,b in zip(roof,roof[1:]):q.line(a,b,INK,4)
    for x in (0,c2):
        q.line((x,design.CEILING_EAVE),(x+wing/2,design.CEILING_RIDGE),WOOD,4)
        q.line((x+wing/2,design.CEILING_RIDGE),(x+wing,design.CEILING_EAVE),WOOD,4)
    if data:
        cover=data['roof']
        for x in (0,c2):
            q.line((x,cover['rafter_cover_lower_chord_at_wall_ft']),(x+wing/2,cover['rafter_peak_lower_chord_ft']),'#967951',4)
            q.line((x+wing/2,cover['rafter_peak_lower_chord_ft']),(x+wing,cover['rafter_cover_lower_chord_at_wall_ft']),'#967951',4)
            q.rect((x+wing/2-.6,cover['ridge_cover_underside_ft'],x+wing/2+.6,cover['ridge_cover_underside_ft']+.6),'#967951')
    q.line((c1,12),(c2,12),WOOD,4)
    q.text(mids[0],5.5,'LIVING',12,True);q.text(width/2,5.5,'DINING',12,True);q.text(mids[1],5.5,'KITCHEN',12,True)
    q.text(mids[0],3.5,'VAULT',11);q.text(width/2,3.5,'12\' CLEAR',11);q.text(mids[1],3.5,'VAULT',11)
    q.dimension((-3,0),(-3,design.CEILING_RIDGE),ft(design.CEILING_RIDGE))
    q.text(-3,design.CEILING_RIDGE+1.5,'LINING',9,True)
    if data:
        lowest_peak=min(data['roof']['ridge_cover_underside_ft'],data['roof']['rafter_peak_lower_chord_ft'])
        q.dimension((width+5,0),(width+5,lowest_peak),ft(lowest_peak))
        q.text(width+5,lowest_peak+1.5,'LOWEST COVER',9,True)
    d.text(850,205,'PUBLIC-ROOM SECTION / DIAGRAM',16,INK,bold=True)
    notes=[
        '10\' finished clear: office, dressing, bathrooms and support rooms.',
        '12\' finished clear: entry and dining. Primary bedrooms also vault.',
        f'Vault lining: {ft(design.CEILING_EAVE)} at eave to {ft(design.CEILING_RIDGE)} near ridge.',
        (f"Cover underside: {ft(data['roof']['rafter_peak_lower_chord_ft'])} at rafter peak; {ft(data['roof']['rafter_cover_lower_chord_at_wall_ft'])} at wall." if data else 'Beam-cover soffits reduce local clear height; see final model receipt.'),
        (f"Ridge cover underside: {ft(data['roof']['ridge_cover_underside_ft'])}; roof lining is higher." if data else 'Member sizes and cover dimensions remain conceptual.'),
        'Gable runoff is toward outer/courtyard eaves; low links have positive fall.',
        'Gutters, overflow paths, weathering and discharge need detailed design.',
        'Shown profiles are architectural allowances; steel sizing is unengineered.',
    ]
    for i,t in enumerate(notes):d.text(850,660+i*34,t,13,MUTED)
    d.text(110,900,'AREA CONVENTION',16,INK,bold=True)
    d.text(110,938,f'{design.WIDTH:g}\' x {design.DEPTH:g}\' envelope minus {c2-c1:g}\' x {cy2-cy1:g}\' open courtyard = {design.AREA:,.0f} sq ft gross enclosed.',16,INK)
    d.text(110,970,'Gross planning-grid area includes wall allowances; excludes court, terraces, parking and roof overhangs. Not a cladding-face measurement.',14,MUTED)
    if data:draw_site_inset(d,data)
    footer(d,'02 / ROOF + SECTION + ARRIVAL')
    d.save()


def draw_site_inset(d,data):
    d.text(110,1015,'ARRIVAL / ILLUSTRATIVE LEVEL SITE',16,INK,bold=True)
    p=Plan(d,(340,1430),5.5)
    p.rect((0,0,design.WIDTH,design.DEPTH),'#d9d7cb',INK,1)
    p.rect(design.COURT,'#d0dcbd',GLASS,1)
    for item in sorted(data['site'],key=lambda x: 0 if x['kind']=='road' else 1):
        color={'parking':'#c5ccc2','road':'#b5bdb4','stall':'#dee4d9','planting':'#a8bd91'}.get(item['kind'],'#e4e0d4')
        p.rect(item['rect'],color,'#a1ad9e',.7)
        r=item['rect']
        title={'parking':'PARKING / DRIVE','road':'ROAD','terrace':'REAR TERRACE','stall':'P','path':'ENTRY PATH'}.get(item['kind'])
        if item['name'].startswith('Parking bay'):title='P'+item['name'][-1]
        if item['name']=='Parking pedestrian link':title='WALK'
        if title:p.text((r[0]+r[2])/2,22 if item['name']=='Two parking spaces' else (r[1]+r[3])/2,title,10,True)
    # These approach details are model-owned records, not an assumed surveyed parcel.
    road=data.get('road_rect')
    if road:p.rect(road,'#c2c9c1')
    for item in data.get('site_labels',[]):p.text(*item['at'],item['text'],11,True)
    d.text(900,1160,'Two equal private suites. One garden-focused public band.',16,INK,bold=True)
    notes=['Front is at the bottom of the plan; no surveyed north is implied.',
           'Parking sits beside the house and is excluded from enclosed area.',
           'The approach uses continuous paving, with a separate pedestrian link.',
           'Opaque street entry opens into the courtyard reveal.',
           'Rear terrace connects living, dining and kitchen to the garden.',
           'Vehicle turning, setbacks, grading and discharge remain unverified.']
    for i,t in enumerate(notes):d.text(900,1200+35*i,t,14,MUTED)


def render_layout_options(folder):
    """Selection-stage proposals. Never read or relabel a native model as evidence."""
    global design
    from io import BytesIO
    from types import SimpleNamespace
    from pypdf import PdfReader, PdfWriter
    original=design;combined=PdfWriter();receipt={'stage':'Proposed 2D layouts for user selection; no native rebuild', 'options':[]}
    folder.mkdir(parents=True,exist_ok=True)
    for key in ('a','b','c'):
        source=folder/f'option-{key}.json'
        if not source.exists():continue
        data=json.loads(source.read_text());data['proposed']=True;data['option_key']=key
        for obj in data.get('furnishings',[]):
            obj['kind']={'appliance':'appliances','fixture':'fixtures','sink':'fixtures','toilet':'fixtures','tub':'fixtures','shower':'fixtures'}.get(obj.get('kind'),obj.get('kind'))
        for obj in data.get('furnishings',[]):
            label=obj.get('plan_label','');name=obj.get('name','').lower()
            if obj.get('kind')=='appliances':
                if 'STACK' in label or 'W+D' in label or 'W/D' in label or ('washer' in name and 'dryer' in name):obj['plan_label']='W/D'
                elif 'fridge' in name or 'refrigerator' in name:obj['plan_label']='FRIDGE'
                elif 'range' in name or 'induction' in name:obj['plan_label']='RANGE'
        data['rooms']=[(r['name'],r['rect'],r.get('ceiling',10)) if isinstance(r,dict) else r for r in data['rooms']]
        if data.get('units')!='feet':raise ValueError('Option units must be feet')
        if len(data.get('wc_rooms',[]))!=2:raise ValueError('Each proposed option needs two explicit clear toilet-room rectangles')
        x1,y1,x2,y2=data['footprint'];c1,cy1,c2,cy2=data['courtyard']
        if x1!=0 or y1!=0:raise ValueError('Option grid starts at 0,0')
        area=(x2-x1)*(y2-y1)-(c2-c1)*(cy2-cy1)
        design=SimpleNamespace(**{k:v for k,v in vars(original).items() if not k.startswith('__')})
        design.WIDTH=x2;design.DEPTH=y2;design.COURT=data['courtyard'];design.AREA=area;design.ROOMS=data['rooms']
        scratch=folder/f'.render-{key}';scratch.mkdir(exist_ok=True)
        draw_floor(scratch,data);draw_details(scratch,data)
        paths=[]
        for kind,filename in [('plan','floor-plan'),('details','interior-details')]:
            pdf=scratch/('floor-plan.pdf' if kind=='plan' else 'interior-details-page.pdf')
            reader=PdfReader(BytesIO(pdf.read_bytes()))
            if len(reader.pages)!=1:raise ValueError('Each comparison sheet must be one page')
            combined.add_page(reader.pages[0])
            stem=folder/f'option-{key}-{kind}'
            import shutil
            shutil.copy2(scratch/f'{filename}.svg',stem.with_suffix('.svg'))
            env=os.environ.copy()
            if Path('/opt/homebrew/etc/fonts/fonts.conf').exists():env.setdefault('FONTCONFIG_FILE','/opt/homebrew/etc/fonts/fonts.conf')
            subprocess.run(['pdftoppm','-png','-r','144','-singlefile',str(pdf),str(stem)],check=True,env=env,capture_output=True)
            paths.extend(str(stem.with_suffix(suffix).relative_to(folder)) for suffix in ('.svg','.png'))
        receipt['options'].append({'id':key,'title':data['title'],'gross_enclosed_sqft':area,'overall_envelope_sqft':x2*y2,'courtyard_sqft':(c2-c1)*(cy2-cy1),'source':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'files':paths})
    design=original
    combined.add_metadata({'/Title':'Twin Gables Courtyard | Three Proposed 2D Layouts','/Subject':'User selection-stage layouts; not native model or construction evidence'})
    if receipt['options']:
        with (folder/'layout-comparison.pdf').open('wb') as handle:combined.write(handle)
    receipt['option_count']=len(receipt['options']);receipt['pdf_pages']=len(combined.pages)
    receipt['artifacts']=[{'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(folder.iterdir()) if p.is_file() and p.suffix in ('.png','.svg','.pdf')]
    receipt['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    receipt['review_status']='Unreviewed candidate; inspect all six sheets before user presentation'
    (folder/'comparison-source.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('LAYOUT_OPTION_CANDIDATES',folder,len(receipt['options']),'options',len(combined.pages),'pages')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--layout-options-dir',type=Path,help='Render selection-stage JSON options only; preserve canonical model and published plans.')
    parser.add_argument('--output-dir',type=Path,default=HOME/'outputs/work/plans')
    parser.add_argument('--data',type=Path,default=HOME/'model/plan-data.json')
    parser.add_argument('--roof-only',action='store_true')
    parser.add_argument('--review-note',default='',help='Only supply after actual review of both rendered PDF pages; stored verbatim.')
    args=parser.parse_args()
    if args.layout_options_dir:
        render_layout_options(args.layout_options_dir)
        return
    args.output_dir.mkdir(parents=True,exist_ok=True)
    if not args.roof_only:
        data=json.loads(args.data.read_text())
        if data['units']!='feet' or data['footprint']!=[0,0,design.WIDTH,design.DEPTH] or data['courtyard']!=list(design.COURT):
            raise ValueError('Model plan receipt and design.py grid disagree; rebuild model first.')
        draw_floor(args.output_dir,data)
    draw_roof(args.output_dir, None if args.roof_only else data)
    for file in args.output_dir.glob('*.pdf'):
        env=os.environ.copy()
        if Path('/opt/homebrew/etc/fonts/fonts.conf').exists(): env.setdefault('FONTCONFIG_FILE','/opt/homebrew/etc/fonts/fonts.conf')
        subprocess.run(['pdftoppm','-png','-r','144','-singlefile',str(file),str(file.with_suffix(''))],check=True,env=env,capture_output=True)
    from pypdf import PdfReader
    import xml.etree.ElementTree as ET
    artifacts=[]
    for p in sorted(args.output_dir.iterdir()):
        if p.suffix not in ('.pdf','.svg','.png'):continue
        if p.suffix=='.pdf' and len(PdfReader(p).pages)!=1:raise ValueError(f'Unexpected PDF page count: {p}')
        if p.suffix=='.svg':ET.parse(p)
        artifacts.append({'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    import reportlab
    poppler=subprocess.run(['pdftoppm','-v'],capture_output=True,text=True,check=True)
    native_path=HOME/'model'/f'{design.SLUG}.blend'
    native_snapshot={'path':str(native_path.relative_to(ROOT)),
                     'sha256':hashlib.sha256(native_path.read_bytes()).hexdigest() if native_path.exists() else None,
                     'scope':'Native snapshot at drawing generation; drawing geometry is tied to plan-data hash. Later camera/light resaves may differ.'}
    receipt={'native_snapshot':native_snapshot,'software':{'python':platform.python_version(),'reportlab':reportlab.Version,'rasterizer':(poppler.stderr or poppler.stdout).splitlines()[0],'raster_dpi':144},
             'design_sha256':hashlib.sha256(Path(design.__file__).read_bytes()).hexdigest(),
             'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'model_plan_data':str(args.data.relative_to(ROOT)),
             'model_plan_data_sha256':hashlib.sha256(args.data.read_bytes()).hexdigest() if args.data.exists() else None,
             'status':'reviewed concept drawings' if args.review_note else 'unreviewed candidate',
             'review_note':args.review_note or None,
             'units':'feet', 'gross_planning_grid_area_sqft':design.AREA,
             'limitations':['Gross planning-grid area includes wall allowances, not exact external cladding measurement.',
                            'Furnishing silhouettes derive from shared-asset manifest bounds and model placement. Plant symbols are indicative.',
                            'Roof/beam-cover section is a concept profile; steel, connections, weathering and services are unengineered.',
                            'No surveyed site, north, code approval or permit documentation is implied.'],
             'files':artifacts}
    (args.output_dir/'plan-source.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('TWIN_GABLES_PLAN_CANDIDATES',args.output_dir)

if __name__=='__main__':main()
