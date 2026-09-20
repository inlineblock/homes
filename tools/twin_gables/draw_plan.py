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


class Plan:
    def __init__(self, drawing, origin, scale):
        self.d, self.ox, self.oy, self.s = drawing, *origin, scale

    def xy(self, x, y):
        return self.ox + x * self.s, self.oy - y * self.s

    def rect(self, rect, fill, stroke='none', sw=1):
        x1, y1, x2, y2 = rect
        self.d.rect(*self.xy(x1, y2), (x2-x1)*self.s, (y2-y1)*self.s, fill, stroke, sw)

    def line(self, a, b, color=INK, sw=1):
        self.d.line(*self.xy(*a), *self.xy(*b), color, sw)

    def text(self, x, y, value, size=13, bold=False, color=INK):
        self.d.text(*self.xy(x,y), value, size, color, anchor='middle', bold=bold)

    def circle(self, x, y, r, fill, stroke='none', sw=1):
        self.d.circle(*self.xy(x,y), r*self.s, fill, stroke, sw)

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
        if 'Primary suite' in name: x=x1+14 if x1==0 else x1+6;y=y1+3.2;title='PRIMARY WEST' if x1==0 else 'PRIMARY EAST'
        elif 'dressing' in name:title='WALK-IN';y=y1+6.2
        elif 'ensuite' in name:title='ENSUITE';y=y1+6.2
        elif 'Office' in name:title='OFFICE / GUEST';x=x1+6.5;y=y2-4.7
        elif 'Guest bath' in name:title='BATH 3';x=x1+4.2;y=y1+4.6
        elif 'gallery' in name:title='GALLERY';y=y2-1;
        elif name=='Kitchen':y=y1+1.5; x=x1+7
        elif name=='Living':y=y1+1.5
        elif name=='Dining':y=y1+1.5
        elif name=='Pantry':y=y1+4.8
        elif name=='Laundry':y=y1+5.2
        labels.append({'at':[x,y],'text':title,'size':11 if 'gallery' in name or name=='Guest bath' else 13})
    return labels

def draw_floor(out, data):
    """Plan linework is source geometry; furnishing silhouettes are exported bounds."""
    d=Drawing(1900,1960,out/'floor-plan.pdf',out/'floor-plan.svg','Twin Gables | Furnished concept floor plan')
    header(d,'One level / furnished concept plan',
           f"Two primary suites + office / three baths / {design.AREA:,.0f} sq ft gross enclosed / front privacy + garden connection")
    p=Plan(d,(245,1540),20.5)
    p.rect((0,0,design.WIDTH,design.DEPTH),'#eae8de')
    for name,rect,height in design.ROOMS:
        color=WET if any(x in name.lower() for x in ('bath','ensuite','laundry')) else '#eae8de'
        if 'dressing' in name.lower():color='#e3d9c8'
        if 'Primary suite' in name:color='#eee6d7'
        p.rect(rect,color)
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
        name=obj.get('name','').lower();rect=obj.get('rect')
        footprint=obj.get('footprint')
        if rect is None and footprint:
            rect=[min(q[0] for q in footprint),min(q[1] for q in footprint),max(q[0] for q in footprint),max(q[1] for q in footprint)]
        if rect is None:continue
        if rect[1]>=design.DEPTH or rect[3]<=0:continue
        if any(t in name for t in ('light','hood','tap','faucet','pull','lever')) or ('mirror' in name and 'basin' not in name):continue
        fill=WOOD
        if any(t in name for t in ('bed','sofa','chair','stool')):fill='#f9f5e9'
        if any(t in name for t in ('basin','sink','toilet','tub','shower')):fill='#f8fbf8'
        if any(t in name for t in ('cooktop','oven','fridge','washer','dryer','dishwasher')):fill='#8f9990'
        if 'rug' in name:fill='#ded7c7'
        if footprint:p.polygon(footprint,fill,'#9b9c8d',.85)
        else:p.rect(rect,fill,'#9b9c8d',.85)
        x1,y1,x2,y2=rect
        if 'bed' in name:
            rotation=obj.get('rotation',0)
            if abs(math.sin(rotation))>.9:
                bx=x1+.25 if rotation<0 else x2-1.3
                p.rect((bx,y1+.3,bx+1.05,y2-.3),'#dcd4c2','#b8b2a1',.6)
            else:p.rect((x1+.3,y2-1.3,x2-.3,y2-.25),'#dcd4c2','#b8b2a1',.6)
        if 'toilet' in name:
            p.circle((x1+x2)/2,(y1+y2)/2,min(x2-x1,y2-y1)*.3,'#ffffff','#b0b9b0',.7)
            if 'enclosed' in name:p.text((x1+x2)/2,y1-1,'WC',12,True)
        if obj.get('kind')=='appliances':
            if 'induction' in name or 'cooktop' in name:
                p.rect(rect,'#3d4842','#26372d',.7)
                for dx in (.3,.7):
                    for dy in (.25,.75):p.circle(x1+(x2-x1)*dx,y1+(y2-y1)*dy,.21,'#707b73','#c0c9c0',.6)
            label=None
            if 'refrigerator' in name:
                label='FRIDGE'
                p.text((x1+x2)/2,(y1+y2)/2+.7,'48 in',10,True)
            elif 'dishwasher' in name:label='DW'
            elif 'oven' in name:label='OVEN'
            elif 'washer' in name:label='W'
            elif 'dryer' in name:label='D'
            if 'induction' in name:p.text(x1-1.2,(y1+y2)/2,'HOB',9,True)
            if 'induction' in name:p.text(x1-1.2,(y1+y2)/2-.7,'OVEN',8,True)
            if 'induction' in name:p.text(x1-1.2,(y1+y2)/2+.7,'HOOD',8,True)
            if label:p.text((x1+x2)/2,(y1+y2)/2,label,10,True,'#24382f')
        if 'basin' in name:p.circle((x1+x2)/2,(y1+y2)/2,min(x2-x1,y2-y1)*.35,'#e2eae5','#82958a',.8)
        if 'sink and mixer' in name:
            p.rect((x1+.12,y1+.2,x2-.2,y2-.2),'#e2eae5','#82958a',.8)
        if 'shower' in name:
            p.line((x1,y1),(x2,y2),'#bac9c0',.7)
            p.line((x1,y2),(x2,y1),'#bac9c0',.7)

        if 'linen closet' in name:p.text((x1+x2)/2,(y1+y2)/2,'LINEN',10,True)

    for wall in data['walls']:
        a,b=wall['a'],wall['b'];length=math.dist(a,b)
        ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length
        point=lambda t:(a[0]+ux*t,a[1]+uy*t)
        cursor=0;sw=5.8 if wall.get('exterior') else 4
        for opening in sorted(wall.get('openings',[]),key=lambda item:item['offset']):
            off,w=opening['offset'],opening['width']
            p.line(point(cursor),point(off),INK,sw)
            if opening.get('type')=='window':
                p.line(point(off),point(off+w),GLASS,2.3)
            elif opening.get('type') in ('slider','glazing','sliding glazing','pocket','fixed glazing'):
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
    # Label anchors are supplied alongside source room records; avoid furniture overlaps.
    for item in data.get('labels',[]) or room_labels(data):
        x,y=item['at'];p.text(x,y,item['text'],item.get('size',12),item.get('bold',True))
    for name,(x1,y1,x2,y2),height in design.ROOMS:
        if 'dressing' in name:p.text((x1+x2)/2,(y1+y2)/2-1,'HANG / SHELF',8,color=MUTED)
        if 'Primary suite' in name:
            p.text(x1+14 if x1==0 else x1+6,y1+1.9,f'{x2-x1:g} x {y2-y1:g} ft gross',10,color=MUTED)
        if name in ('Living','Dining','Kitchen'):
            p.text((x1+x2)/2,y1+.35,f'{x2-x1:g} x {y2-y1:g} ft gross',10,color=MUTED)
    p.dimension((0,design.DEPTH+4),(design.WIDTH,design.DEPTH+4),ft(design.WIDTH))
    p.dimension((design.WIDTH+4,0),(design.WIDTH+4,design.DEPTH),ft(design.DEPTH),'y')
    c1,cy1,c2,cy2=design.COURT
    p.text((c1+c2)/2,cy2-5,'OPEN COURTYARD',16,True)
    p.text((c1+c2)/2,cy2-6.5,f"{c2-c1:g}' x {cy2-cy1:g}'",13)
    p.text(design.WIDTH/2,-2,'4 ft SOLID ENTRY DOOR',11,True)
    p.text(design.WIDTH/2,-4,'OPAQUE ENTRY / FRONT',13,True)
    p.text(design.WIDTH/2,-6,'ROAD + PARKING: SEE ARRIVAL DIAGRAM',10,color=MUTED)
    d.text(100,1750,'EVERYDAY COMFORT',17,INK,bold=True)
    notes=[
       'Both primary suites: king bedroom, walk-in dressing, double vanity, separate tub + shower, enclosed WC and bath linen.',
       'Full kitchen: 36-in induction cooking, built-in oven + hood, 48-in panel-ready fridge, dishwasher, sink, drawers and walk-in pantry.',
       'Office / guest is a separate flexible room; it is not counted as a third dedicated bedroom. Hall bath, laundry and service allowances shown.',
       'Area is gross planning-grid area including wall allowances, not a measured exterior-cladding footprint. Product/engineering review remains.',
    ]
    for i,t in enumerate(notes):d.text(100,1785+i*25,t,14,MUTED)
    footer(d,'01 / MAIN FLOOR')
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


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=HOME/'outputs/work/plans')
    parser.add_argument('--data',type=Path,default=HOME/'model/plan-data.json')
    parser.add_argument('--roof-only',action='store_true')
    parser.add_argument('--review-note',default='',help='Only supply after actual review of both rendered PDF pages; stored verbatim.')
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
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
