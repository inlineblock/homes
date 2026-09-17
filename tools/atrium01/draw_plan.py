"""Dimensioned concept plan in SVG and PDF, from the shared measured layout."""
from pathlib import Path
from html import escape
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from design import *
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'homes/atrium-01/drawings';OUT.mkdir(parents=True,exist_ok=True)
W,H=1600,1200;S=16.3;OX,OY=125,974
pdf=canvas.Canvas(str(OUT/'floor-plan.pdf'),pagesize=(1152,864));pdf.scale(.72,.72);pdf.setTitle('Atrium 01 | Dimensioned concept plan')
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
def rect(x,y,w,h,fill='none',stroke='none',sw=1):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    if fill!='none':pdf.setFillColor(HexColor(fill))
    if stroke!='none':pdf.setStrokeColor(HexColor(stroke))
    pdf.setLineWidth(sw);pdf.rect(x,H-y-h,w,h,fill=int(fill!='none'),stroke=int(stroke!='none'))
def line(x1,y1,x2,y2,color='#333f37',sw=1):
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>');pdf.setStrokeColor(HexColor(color));pdf.setLineWidth(sw);pdf.line(x1,H-y1,x2,H-y2)
def text(x,y,t,size=14,color='#28372e',anchor='start',bold=False):
    svg.append(f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{700 if bold else 400}">{escape(t)}</text>')
    pdf.setFillColor(HexColor(color));pdf.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
    {'start':pdf.drawString,'middle':pdf.drawCentredString,'end':pdf.drawRightString}[anchor](x,H-y,t)
def circle(x,y,r,fill='none',stroke='#607263',sw=1):
    svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    if fill!='none':pdf.setFillColor(HexColor(fill))
    if stroke!='none':pdf.setStrokeColor(HexColor(stroke))
    pdf.setLineWidth(sw);pdf.circle(x,H-y,r,fill=int(fill!='none'),stroke=int(stroke!='none'))
def xy(x,y):return OX+x*S,OY-y*S
def r(x1,y1,x2,y2,fill,stroke='none',sw=1):
    x,y=xy(x1,y2);rect(x,y,(x2-x1)*S,(y2-y1)*S,fill,stroke,sw)
def ln(a,b,color='#333f37',sw=1):line(*xy(*a),*xy(*b),color,sw)
def label(x,y,t,size=12,bold=False):text(*xy(x,y),t,size,anchor='middle',bold=bold)
def dimh(x1,x2,y,t):
    ln((x1,y),(x2,y),'#637267',.8)
    for x in [x1,x2]:ln((x-.22,y-.22),(x+.22,y+.22),'#637267',1)
    label((x1+x2)/2,y+.45,t,13)
def dimv(y1,y2,x,t):
    ln((x,y1),(x,y2),'#637267',.8)
    for y in [y1,y2]:ln((x-.22,y-.22),(x+.22,y+.22),'#637267',1)
    xx,yy=xy(x,(y1+y2)/2);rect(xx-20,yy-13,40,25,'#f7f5ef');text(xx,yy+5,t,13,anchor='middle')

rect(0,0,W,H,'#f7f5ef')
text(78,79,'H O M E S   /   A T R I U M   0 1',17,bold=True)
text(78,139,'A modern Eichler-inspired home',39,bold=True)
text(78,177,'3 bedrooms   /   3 baths   /   2,400 sq ft gross enclosed   /   Kitchen-led concept',17,'#647366')
line(78,204,1520,204,'#a5b19f',1)
r(0,0,60,44,'#eeeae0')
for slug,coords,name in ROOMS:
    if 'bath' in slug:r(*coords,'#e1e9e2')
    elif slug in ['bedroom-2','bedroom-3','primary']:r(*coords,'#ece5d7')
r(*ATRIUM,'#ced9bd')
r(23.2,13.5,29.8,22.5,'#9fac86')
for y in [11.7,14.7,17.7,20.7,23.7]:r(31.6,y-1.25,36.4,y+1.25,'#e9e6db','#a3ad93',.7)
cx,cy=xy(26.5,18);circle(cx,cy,2.3*S,'#abbf91','#738665')
for name,a,b,t,opens in WALLS:
    L=math.dist(a,b);ux=(b[0]-a[0])/L;uy=(b[1]-a[1])/L;point=lambda q:(a[0]+ux*q,a[1]+uy*q)
    cursor=0
    for off,w,sill,head,kind in sorted(opens):
        if off>cursor:ln(point(cursor),point(off),'#2e3c33',max(4,t*S))
        if kind in ['window','glass','entry']:
            ln(point(off),point(off+w),'#76a5a4',2)
            for j in range(max(1,round(w/4))+1):
                p=point(off+w*j/max(1,round(w/4)));ln((p[0]-.10,p[1]-.10),(p[0]+.10,p[1]+.10),'#2e3c33',2)
        elif kind=='door':
            inward=-1 if name in ['bedroom-gallery','entry-bath-east','pantry-east'] else 1
            p=point(off);q=(p[0]+(inward*w if uy else 0),p[1]+(w if ux else 0));ln(p,q,'#8e7c62',1.6)
            # A quarter-circle swing composed of line segments, matching the open door leaf.
            prev=point(off+w)
            for j in range(1,13):
                a0=math.pi/2*j/12;q=(p[0]+w*(inward*math.sin(a0) if uy else math.cos(a0)),p[1]+w*(math.cos(a0) if uy else math.sin(a0)));ln(prev,q,'#b5ad99',.65);prev=q
        cursor=off+w
    if cursor<L:ln(point(cursor),b,'#2e3c33',max(4,t*S))
for name,a,b in COURTYARD_GLAZING:
    ln(a,b,'#76a5a4',2.5)
    L=math.dist(a,b);n=max(1,round(L/4))
    for i in range(n+1):
        x=a[0]+(b[0]-a[0])*i/n;y=a[1]+(b[1]-a[1])*i/n;r(x-.07,y-.07,x+.07,y+.07,'#2e3c33')
# Model-aligned furniture symbols.
for x,y,w in [(8,5.7,5),(8,25,5),(8,37,6.4)]:
    r(x-w/2,y-3.3,x+w/2,y+3.3,'#f9f7f0','#a99e87',1)
    for dx in [-w*.24,w*.24]:r(x+dx-w*.2,y+1.45,x+dx+w*.2,y+2.9,'#e0dbcd','#b7ab95',.6)
    ln((x-w/2,y-1),(x+w/2,y-1),'#b7ab95',.8)
for x,y,w,d in [(8,12,10,8),(22,0,8,8),(18,34,10,10)]:
    r(x+.25,y+.25,x+3.75,y+3.75,'#f1f2e9','#94a493',.8)
    ln((x+.25,y+.25),(x+3.75,y+3.75),'#94a493',.7)
    r(x+w*.65-1.75,y+d-2.1,x+w*.65+1.75,y+d-.1,'#c9b79b','#94846c',.7)
    xx,yy=xy(x+w*.65,y+d-1.1);circle(xx,yy,.65*S,'#faf8f1','#94a493',.7)
    xx,yy=xy(x+1,y+d-2);circle(xx,yy,.6*S,'#faf8f1','#94a493',.7)
r(44.5,.3,58.1,2.7,'#b89d78','#7f715b',1)
r(57.35,1,60,20.2,'#b89d78','#7f715b',1)
r(47.85,5.95,52.15,16.05,'#f2ecda','#857d68',1.5)
for y in [7.3,9.75,12.2,14.65]:
    xx,yy=xy(46.8,y);circle(xx,yy,.69*S,'#ac906d','#756953',.8)
r(44.5,24.5,52.5,28.1,'#b89d78','#7f715b',1)
for x in [45.7,48.5,51.3]:
    for y in [23.7,28.9]:r(x-.65,y-.6,x+.65,y+.6,'#d5cebd','#8d8270',.7)
r(36,32,52,42,'#e4dcc7')
r(38,39.3,49,42.7,'#ccc3ad','#978b76',1)
r(41,35.35,47,38.25,'#b99b70','#86775b',1)
r(28.3,34.4,29.9,42.4,'#d3cbbb','#978b76',.8)
# Labels placed away from furniture and circulation.
for x,y,t,d in [(9,10.4,'BEDROOM 02',"18' x 12' zone"),(13.5,16.1,'BATH 02',"10' x 8'"),(4,16,'STORAGE',"8' x 8'"),(9,28.7,'BEDROOM 03',"18' x 10' zone"),(9,42.7,'PRIMARY',"18' x 14' zone"),(23,40.3,'PRIMARY BATH',"10' x 10'"),(25,31.5,'DRESSING',"6' x 6'"),(26.4,5.65,'BATH 03',"8' x 8'"),(34,6,'ENTRY',''),(41,7,'PANTRY /','LAUNDRY'),(50,19.4,'KITCHEN',''),(48.5,30.1,'DINING',''),(44,33.2,'LIVING',''),(30,23.2,'OPEN ATRIUM',"16' x 15'")]:
    label(x,y,t,11.8,True)
    if d:label(x,y-1.0,d,10.5)
label(20,19,'G',11);label(20,18,'A',11);label(20,17,'L',11);label(20,16,'L',11);label(20,15,'E',11);label(20,14,'R',11);label(20,13,'Y',11)
dimh(0,60,-3.3,"60'-0\"");dimv(0,44,-3.2,"44'-0\"")
dimh(22,38,46.1,"16'-0\" atrium width")
dimh(0,18,46.1,"18'-0\"");dimh(38,60,46.1,"22'-0\"")
dimv(10,25,40,"15'-0\"")
dimv(5.95,16.05,54.7,"10'-1\"")
dimh(47.85,52.15,4.4,"4'-4\"")
# Sidebar is a short design brief, not an invented building specification.
text(1165,274,'01 / DESIGN INTENT',15,bold=True)
for i,t in enumerate(['A low, horizontal home wrapped','around an open-air garden.','Warm walnut, pale limestone,','sage ceramic, and exposed fir.']):text(1165,309+i*25,t,15,'#637267')
text(1165,447,'02 / THE KITCHEN',15,bold=True)
for i,t in enumerate(['10 ft island with four seats','South cooking wall + display shelf','East sink and appliance run','Courtyard-facing breakfast edge','Pantry / laundry beside the entry']):text(1165,482+i*25,t,15,'#637267')
text(1165,647,'03 / AREA BASIS',15,bold=True)
for i,t in enumerate(['60 x 44 ft footprint = 2,640 sq ft','16 x 15 ft atrium = 240 sq ft','Gross enclosed = 2,400 sq ft','Includes wall thickness.','Excludes courtyard and terraces.','No garage in this concept.']):text(1165,682+i*25,t,15,'#637267')
text(1165,887,'CONCEPT / REVISION 01',15,bold=True)
for i,t in enumerate(['Planning zones are indicative.','Dimensions govern; do not scale.','Site orientation is not assigned.','Not for permitting or construction.']):text(1165,922+i*24,t,13,'#637267')
line(78,1085,1520,1085,'#a5b19f',1)
text(78,1122,'A-01     FLOOR PLAN',16,bold=True)
text(78,1151,'Original design study  /  September 17, 2026',13,'#637267')
for i in range(2):rect(660+i*5*S,1122,5*S,7,'#344a3c' if i==0 else '#c2cbb9')
for i in [0,5,10]:text(660+i*S,1150,str(i)+(' ft' if i==10 else ''),12,anchor='middle')
text(1520,1151,'HOMES  /  ATRIUM 01',13,'#637267',anchor='end')
svg.append('</svg>');(OUT/'floor-plan.svg').write_text('\n'.join(svg));pdf.save()
print('PLAN_SAVED',OUT)
