"""Original concept plan SVG/PNG drafts from Lindon's shared meter-based layout.

Run with Python + Pillow. No listing image is incorporated into either output.
Only outputs/work/plans is overwritten; promotion is a separate reviewed action.
"""
from pathlib import Path
from html import escape
import math
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'homes/lindon-brick-house/outputs/work/plans'
INK='#293b3c'; MUTED='#657777'; PAPER='#faf8f3'; SAND='#eae1d4'; WOOD='#ccb18d'; GLASS='#5697a1'

class Sheet:
    """Matched SVG and raster operations, with no PDF intermediate."""
    def __init__(self,w=2200,h=1800):
        self.w,self.h=w,h
        self.image=Image.new('RGB',(w,h),PAPER); self.d=ImageDraw.Draw(self.image)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',f'<rect width="{w}" height="{h}" fill="{PAPER}"/>']
        self.font_path=next((p for p in [Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/Library/Fonts/Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists()),None)
    def polygon(self,pts,fill='none',stroke='none',sw=1):
        self.svg.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        if fill!='none':self.d.polygon(pts,fill=fill)
        if stroke!='none':self.d.line(pts+[pts[0]],fill=stroke,width=max(1,round(sw)),joint='curve')
    def rect(self,x,y,w,h,fill='none',stroke='none',sw=1):self.polygon([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],fill,stroke,sw)
    def line(self,pts,color=INK,sw=2,dashed=False):
        attr=' stroke-dasharray="8 6"' if dashed else ''
        self.svg.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="{sw}"{attr}/>')
        if not dashed:self.d.line(pts,fill=color,width=max(1,round(sw)),joint='curve')
        else:
            for a,b in zip(pts,pts[1:]):
                length=math.dist(a,b)
                for i in range(0,math.ceil(length),14):
                    u=i/max(length,.001);v=min(i+8,length)/max(length,.001)
                    self.d.line([(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u),(a[0]+(b[0]-a[0])*v,a[1]+(b[1]-a[1])*v)],fill=color,width=max(1,round(sw)))
    def ellipse(self,x,y,rx,ry,fill='none',stroke=INK,sw=1):
        self.svg.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        self.d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=None if fill=='none' else fill,outline=None if stroke=='none' else stroke,width=max(1,round(sw)))
    def text(self,x,y,text,size=20,color=INK,anchor='middle',bold=False):
        font=ImageFont.truetype(str(self.font_path),size) if self.font_path else ImageFont.load_default()
        box=self.d.textbbox((0,0),text,font=font); width=box[2]-box[0]
        left=x if anchor=='start' else x-width if anchor=='end' else x-width/2
        self.d.text((left,y-box[3]),text,font=font,fill=color,stroke_width=0)
        self.svg.append(f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}">{escape(text)}</text>')
    def save(self,name):
        OUT.mkdir(parents=True,exist_ok=True)
        (OUT/(name+'.svg')).write_text('\n'.join(self.svg+['</svg>']))
        self.image.save(OUT/(name+'.png'))

def feet(m):
    inches=round(m/.0254)
    return f'{inches//12}′ {inches%12}″'

# Shared layout adapters follow. Geometry is never traced from a raster at render time.

class Plan:
    def __init__(self,title,boundary,index):
        self.s=Sheet(); self.boundary=boundary; self.furniture_bounds=[]
        xs=[p[0] for p in boundary];ys=[p[1] for p in boundary]
        self.xmin,self.xmax,self.ymin,self.ymax=min(xs),max(xs),min(ys),max(ys)
        self.scale=min(1850/max(self.xmax-self.xmin,1),1200/max(self.ymax-self.ymin,1))
        self.ox=(2200-(self.xmax-self.xmin)*self.scale)/2-self.xmin*self.scale
        self.oy=350+(self.ymax-self.ymin)*self.scale+self.ymin*self.scale
        self.s.text(100,85,'L I N D O N   B R I C K   H O U S E',24,MUTED,'start')
        self.s.text(100,155,title,50,INK,'start',True)
        self.s.text(100,203,'Concept remodel / dimensions approximate / verify on site',25,MUTED,'start')
        self.s.text(2100,85,f'0{index} / FLOOR PLAN',21,MUTED,'end')
        self.s.text(100,1730,'Original reconstructed concept diagram • Not a measured survey or construction drawing',21,MUTED,'start')
        self.s.text(100,1770,'Reference room relationships retained; stair routing is proposed. Dimensions and conditions require field verification.',19,MUTED,'start')
    def xy(self,p):return (self.ox+p[0]*self.scale,self.oy-p[1]*self.scale)
    def poly(self,pts,fill='none',stroke=INK,sw=2):self.s.polygon([self.xy(p) for p in pts],fill,stroke,sw)
    def rect(self,x,y,w,h,fill='none',stroke=INK,sw=1):self.poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],fill,stroke,sw)
    def line(self,a,b,color=INK,sw=2,dashed=False):self.s.line([self.xy(a),self.xy(b)],color,sw,dashed)
    def text(self,x,y,t,size=19,color=INK):self.s.text(*self.xy((x,y)),t,size,color)
    def ellipse(self,x,y,rx,ry,fill='none',stroke=INK,sw=1):self.s.ellipse(*self.xy((x,y)),rx*self.scale,ry*self.scale,fill,stroke,sw)
    def overall(self):
        x1,y1=self.xy((self.xmin,self.ymax));x2,_=self.xy((self.xmax,self.ymax)); y=y1-48
        self.s.line([(x1,y),(x2,y)],MUTED,1)
        for x in [x1,x2]:self.s.line([(x,y-9),(x,y+9)],MUTED,1)
        self.s.text((x1+x2)/2,y-13,feet(self.xmax-self.xmin)+'  overall estimate',21,MUTED)
        x=x2+47;y1=self.xy((0,self.ymax))[1];y2=self.xy((0,self.ymin))[1]
        self.s.line([(x,y1),(x,y2)],MUTED,1)
        for y in [y1,y2]:self.s.line([(x-9,y),(x+9,y)],MUTED,1)
        # Horizontal dimension text avoids tiny rotated raster glyphs.
        self.s.text(x-2,y2+33,feet(self.ymax-self.ymin),20,MUTED,'end')
    def legend(self):
        y=1620
        for x,c,t in [(110,INK,'Walls'),(340,GLASS,'Glazing'),(600,WOOD,'Storage / cabinetry'),(1030,'#a99677','Furniture / fixtures')]:
            self.s.line([(x,y),(x+55,y)],c,7);self.s.text(x+74,y+7,t,20,MUTED,'start')
        self.s.text(2090,y+7,'Orientation: front / rear, not geographic north',19,MUTED,'end')
        self.s.text(110,y+43,'CL = clothes / coat closet     WIC = walk-in closet     Arrows: main / basement UP, upper DOWN; stair geometry is proposed',18,MUTED,'start')
    def bed(self,x,y,w=1.6,d=2.1,angle=0):
        c=math.cos(angle);s=math.sin(angle)
        def p(a,b):return(x+a*c-b*s,y+a*s+b*c)
        self.poly([p(-w/2,-d/2),p(w/2,-d/2),p(w/2,d/2),p(-w/2,d/2)],SAND,'#a99677',2)
        for a in [-w/4,w/4]:
            self.poly([p(a-w*.2,-d*.43),p(a+w*.2,-d*.43),p(a+w*.2,-d*.23),p(a-w*.2,-d*.23)],'#fffdfa','#b6a38a',1)
        self.line(p(-w/2,d*.12),p(w/2,d*.12),'#b6a38a',1)
    def stair(self,rect,treads=15,label='UP',axis='y'):
        x,y,w,h=rect;self.rect(x,y,w,h,'#f5f2ea',MUTED,1)
        if axis=='y':
            for i in range(1,treads):self.line((x,y+h*i/treads),(x+w,y+h*i/treads),'#a6afab',1)
            self.line((x+w*.5,y+.18),(x+w*.5,y+h-.2),MUTED,2)
        else:
            for i in range(1,treads):self.line((x+w*i/treads,y),(x+w*i/treads,y+h),'#a6afab',1)
            self.line((x+.18,y+h*.5),(x+w-.2,y+h*.5),MUTED,2)
        self.text(x+w/2,y+h/2,label,15,MUTED)


def point_inside(p,poly):
    x,y=p;inside=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
    return inside


def centroid(poly):
    # Polygon centroid is useful for non-rectangular rooms; fall back if degenerate.
    cross=[a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])]
    A=sum(cross)
    if abs(A)<1e-7:return tuple(sum(p[i] for p in poly)/len(poly) for i in range(2))
    return tuple(sum((a[i]+b[i])*c for a,b,c in zip(poly,poly[1:]+poly[:1],cross))/(3*A) for i in range(2))


def opening_mark(plan,a,b,kind='door',inside=None):
    plan.line(a,b,'#ffffff',max(12,plan.scale*.25))
    if kind=='passage':return
    if kind in {'window','glazing'}:
        plan.line(a,b,GLASS,4);return
    length=math.dist(a,b)
    if length<.05:return
    ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length
    if length>1.45:
        plan.line(a,b,WOOD,1,True);return
    sign=1
    if inside:
        mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        if not point_inside((mx-uy*.3,my+ux*.3),inside):sign=-1
    end=(a[0]-sign*uy*length,a[1]+sign*ux*length)
    plan.line(a,end,WOOD,2)
    arc=[]
    for i in range(19):
        t=sign*i*math.pi/36
        arc.append((a[0]+length*(ux*math.cos(t)-uy*math.sin(t)),a[1]+length*(uy*math.cos(t)+ux*math.sin(t))))
    plan.s.line([plan.xy(p) for p in arc],WOOD,1)


def plan_wall(plan,w):
    a,b=w['a'],w['b'];length=math.dist(a,b)
    if length<1e-6:return
    def pt(d):return(a[0]+(b[0]-a[0])*d/length,a[1]+(b[1]-a[1])*d/length)
    start=0
    for off,width in sorted(w.get('openings',[])):
        plan.line(pt(start),pt(off),INK,max(4,plan.scale*.13))
        opening_mark(plan,pt(off),pt(off+width));start=off+width
    plan.line(pt(start),b,INK,max(4,plan.scale*.13))


def draw_path_stair(plan,stair):
    if 'footprint' in stair:plan.poly(stair['footprint'],'#ede9df',MUTED,1)
    path=stair['path']
    for a,b in zip(path,path[1:]):
        dist=math.dist(a,b)
        if dist<.01:continue
        nx,ny=-(b[1]-a[1])/dist*.40,(b[0]-a[0])/dist*.40
        for i in range(max(2,round(dist/.25))):
            t=i/max(2,round(dist/.25));x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t
            plan.line((x-nx,y-ny),(x+nx,y+ny),'#a9b1ac',1)
    plan.s.line([plan.xy(p) for p in path],MUTED,2)
    a,b=path[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0])
    for d in [-.6,.6]:plan.line(b,(b[0]-.30*math.cos(ang+d),b[1]-.30*math.sin(ang+d)),MUTED,2)


def room_label(plan,room):
    if room['type']=='hall' and room['name']!='Upper central landing':return
    names={'Garage entry':'MUDROOM','Formal living room':'FORMAL LIVING','Family living room':'FAMILY LIVING','Formal dining':'DINING','Breakfast nook':'BREAKFAST','Primary bedroom':'PRIMARY BEDROOM','Primary bathroom':'PRIMARY BATH','Primary toilet compartment':'WC','Primary walk-in closet':'DRESSING','Shared upper bathroom':'SHARED BATH','Garage-wing bathroom':'BATH','Upper laundry':'LAUNDRY','Upper central landing':'UPPER LANDING','Upper front hall':'HALL','Garage-wing hall':'HALL','Northwest bedroom hall':'HALL','Central hall':'HALL','Basement bedroom hall':'HALL','Basement rear stair hall':'HALL','Basement shower/WC compartment':'SHOWER / WC','Bathroom vanity area':'BATH','Eat-in second kitchen':'SECOND KITCHEN','Basement general storage':'GENERAL STORAGE','Utility / laundry':'UTILITY / LAUNDRY'}
    name=names.get(room['name'],room['name'].upper())
    if room['type']=='bedroom' and room.get('bedroom_id',1)!=1:name='BEDROOM '+str(room['bedroom_id'])
    if room['type']=='closet':name='WIC' if 'walk-in' in room['name'].lower() else 'CL'
    if room['type']=='storage' and room['name']!='Basement general storage':name='STORAGE'
    x,y=centroid(room['polygon']);size=17 if room['type'] in {'closet','hall','wc_compartment','storage'} else 20
    # Prefer a clear patch inside this room; labels must not erase the furniture.
    label_width=(len(name)*size*.54+12)/plan.scale;label_height=(size+10)/plan.scale
    rx=[p[0] for p in room['polygon']];ry=[p[1] for p in room['polygon']]
    candidates=[]
    for ix in range(19):
        for iy in range(19):
            cx=min(rx)+(max(rx)-min(rx))*(ix+.5)/19;cy=min(ry)+(max(ry)-min(ry))*(iy+.5)/19
            bounds=(cx-label_width/2,cy-.1,cx+label_width/2,cy+label_height)
            corners=[(bounds[0],bounds[1]),(bounds[2],bounds[1]),(bounds[2],bounds[3]),(bounds[0],bounds[3])]
            if not all(point_inside(p,room['polygon']) for p in corners):continue
            if any(bounds[0]<o[2]+.05 and bounds[2]>o[0]-.05 and bounds[1]<o[3]+.05 and bounds[3]>o[1]-.05 for o in plan.furniture_bounds):continue
            candidates.append((math.dist((cx,cy),(x,y)),cx,cy))
    if candidates:_,x,y=min(candidates)
    sx,sy=plan.xy((x,y));w=len(name)*size*.54
    plan.s.rect(sx-w/2-5,sy-size-2,w+10,size+8,'#faf8f3')
    plan.s.text(sx,sy,name,size,INK)


def main():
    import design as D
    from openings import schedule,garage_openings
    proposed=schedule()
    for index,key in enumerate(['main','upper','basement'],1):
        lev=D.LEVELS[key]
        extents=lev['footprint']+(D.GARAGE_FOOTPRINT if key=='main' else [])
        plan=Plan(lev['name'],extents,index)
        datum=('−' if lev['z']<0 else '+')+feet(abs(lev['z']))
        plan.s.text(2100,203,'Assumed floor datum '+datum,21,MUTED,'end')
        plan.poly(lev['footprint'],'#ffffff',INK,max(8,plan.scale*.24))
        for room in lev['rooms']:
            tint='#f4efe7' if room['type'] in {'closet','storage','utility','laundry'} else '#edf2f1' if 'bath' in room['type'] or room['type']=='wc_compartment' else '#ffffff'
            plan.poly(room['polygon'],tint,'none')
        # Restore continuous perimeter over zoning fills, then cut real openings.
        plan.poly(lev['footprint'],'none',INK,max(8,plan.scale*.24))
        if key=='main':
            plan.poly(D.GARAGE_FOOTPRINT,'#eeeae3',INK,max(8,plan.scale*.24))
            for a,b in zip(D.GARAGE_FOOTPRINT,D.GARAGE_FOOTPRINT[1:]+D.GARAGE_FOOTPRINT[:1]):
                length=math.dist(a,b)
                for op in garage_openings(a,b):
                    start=tuple(a[i]+(b[i]-a[i])*op['offset']/length for i in range(2))
                    end=tuple(a[i]+(b[i]-a[i])*(op['offset']+op['width'])/length for i in range(2))
                    if op.get('kind')=='garage_door':
                        plan.line(start,end,'#ffffff',max(12,plan.scale*.25));plan.line(start,end,WOOD,4)
                    else:opening_mark(plan,start,end,'passage' if op.get('kind')=='passage' else 'window',D.GARAGE_FOOTPRINT)
            x,y=centroid(D.GARAGE_FOOTPRINT);plan.text(x,y,'THREE-CAR GARAGE',23)
            plan.text(x,y-.5,'Angled wing / approximate outline',17,MUTED)
        for v in lev['voids']:
            plan.poly(v['polygon'],PAPER,'#9aada9',2)
            x,y=centroid(v['polygon']);plan.text(x,y,'OPEN BELOW' if 'foyer below' in v['name'].lower() else 'STAIR OPENING',15,MUTED)
        for w in lev['interior_wall_segments']:plan_wall(plan,w)
        for op in proposed:
            if op['level']==key:opening_mark(plan,op['a'],op['b'],'window' if op.get('kind')!='passage' else 'passage',lev['footprint'])
        for op in lev['exterior_openings']:opening_mark(plan,op['a'],op['b'],op['type'],lev['footprint'])
        for stair in lev['stairs']:draw_path_stair(plan,stair)
        if key=='upper':
            for stair in D.LEVELS['main']['stairs']:
                if stair['target']=='upper':draw_path_stair(plan,{**stair,'path':list(reversed(stair['path']))})
        draw_furnishings(plan,key,D)
        for room in lev['rooms']:room_label(plan,room)
        plan.overall();plan.legend()
        plan.s.text(110,264,'REAR / GARDEN AT TOP',18,MUTED,'start')
        plan.s.text(2100,264,'FRONT / STREET AT BOTTOM',18,MUTED,'end')
        plan.s.save(key+'-floor-plan')
        print('PLAN_DRAFT_WRITTEN',key)


def draw_furnishings(plan,key,D):
    import json
    from interiors import FURNITURE,FIXTURES,FITTED_GEOMETRY
    for row in FITTED_GEOMETRY:
        if row['level']!=key:continue
        x,y,z=row['location'];w,d,h=row['dimensions'];a=row.get('rotation',0)
        pts=[(x+u*math.cos(a)-v*math.sin(a),y+u*math.sin(a)+v*math.cos(a)) for u,v in [(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)]]
        plan.poly(pts,'#e6e1d7','#918e80',1)
        plan.furniture_bounds.append((min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)))
    for row in FURNITURE+FIXTURES:
        if row['level']!=key or row['kind']=='hood':continue
        path=ROOT/'library'/row['asset']/row['version']/'asset.json'
        metadata=json.loads(path.read_text())
        w,d,h=row['dimensions'];bb=metadata.get('bounds_m',{'min':[-w/2,-d/2,0],'max':[w/2,d/2,h]})
        x0,y0=bb['min'][:2];x1,y1=bb['max'][:2]
        x,y,z=row['location'];ang=row.get('rotation',0);c=math.cos(ang);sn=math.sin(ang);kind=row['kind']
        def point(a,b):return(x+a*c-b*sn,y+a*sn+b*c)
        def box(a,b,ww,dd,fill=SAND,stroke='#a99677',sw=1):plan.poly([point(a,b),point(a+ww,b),point(a+ww,b+dd),point(a,b+dd)],fill,stroke,sw)
        def line(a,b,col=MUTED,sw=1):plan.line(point(*a),point(*b),col,sw)
        def oval(cx,cy,rx,ry,fill='#ffffff',stroke=MUTED):
            plan.poly([point(cx+rx*math.cos(i*math.tau/32),cy+ry*math.sin(i*math.tau/32)) for i in range(32)],fill,stroke,1)
        footprint=[point(x0,y0),point(x1,y0),point(x1,y1),point(x0,y1)]
        plan.furniture_bounds.append((min(p[0] for p in footprint),min(p[1] for p in footprint),max(p[0] for p in footprint),max(p[1] for p in footprint)))
        if kind=='bed':plan.bed(x,y,w,d,ang);continue
        if kind in {'cabinet','wardrobe','vanity'}:
            box(x0,y0,w,d,WOOD)
            line((x0,y0+.08),(x1,y0+.08),'#8d785d')
            if kind=='wardrobe':line((0,y0),(0,y1),'#8d785d')
        elif kind=='sofa':
            box(x0,y0,w,d)
            box(x0,y0,w,.20,'#d6c6b3')
            for ratio in [1/3,2/3]:line((x0+w*ratio,y0+.2),(x0+w*ratio,y1-.1),'#b5a38e')
        elif kind=='chair':
            box(x0,y0,w,d,'#f8f4ec');box(x0,y0,w,.13,'#cbb695')
        elif kind=='pool':
            box(x0,y0,w,d,'#8d6950');box(x0+.14,y0+.14,w-.28,d-.28,'#496768')
            for xx in [x0+.16,x1-.16]:
                for yy in [y0+.16,(y0+y1)/2,y1-.16]:oval(xx,yy,.07,.07,'#273c3c','#273c3c')
        elif kind=='table' and 'round' in row['asset']:oval((x0+x1)/2,(y0+y1)/2,w/2,d/2,WOOD,'#a99677')
        elif kind in {'table','nightstand','desk'}:box(x0,y0,w,d,WOOD)
        elif kind=='toilet':
            box(x0,y1-.18,w,.18,'#ffffff',MUTED);oval(0,y0+d*.37,w*.47,d*.32)
        elif kind=='tub':
            oval((x0+x1)/2,(y0+y1)/2,w*.5,d*.5);oval((x0+x1)/2,(y0+y1)/2,w*.42,d*.38,'#edf2f1')
        elif kind in {'sink','basin'}:oval(0,0,w*.4,d*.4)
        elif kind=='shower':
            box(x0,y0,w,d,'#e2eeee',GLASS);line((x0,y0),(x1,y1),'#aac6c9');line((x1,y0),(x0,y1),'#aac6c9')
        elif kind in {'washer','dryer','laundry'}:
            box(x0,y0,w,d,'#ffffff',MUTED);oval(0,0,w*.28,min(w,d)*.28,'#edf2f1')
        elif kind=='cooktop':
            box(x0,y0,w,d,'#d4dddc',MUTED)
            for xx in [-w*.23,w*.23]:
                for yy in [-d*.23,d*.23]:oval(xx,yy,min(w,d)*.12,min(w,d)*.12,'none')
        elif kind=='fireplace':
            box(x0,y0,w,d,'#dbc7b2');box(x0,y0,w,.1,'#484c48')
        else:
            box(x0,y0,w,d,'#f0eee9',MUTED)
            label={'fridge':'48″ FR','dishwasher':'DW','oven':'OVEN'}.get(kind,kind.upper())
            plan.text(x,y,label,12,MUTED)


if __name__=='__main__':main()
