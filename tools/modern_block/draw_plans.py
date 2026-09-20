"""Modern Block furnished concept plans from shared geometry and furniture records.
Run: MPLCONFIGDIR=/tmp/modern-block-mpl python3 tools/modern_block/draw_plans.py
Review outputs are written to outputs/work/plans. --promote writes reviewed current paths.
"""
from pathlib import Path
import argparse, json, math, os, sys
os.environ.setdefault('MPLCONFIGDIR','/tmp/modern-block-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, Arc, FancyArrowPatch
from matplotlib.transforms import Affine2D
from design import *
import design as design_source
import kitchen_layout as kitchen_source
ROOT=Path(__file__).resolve().parents[2]
HOME=ROOT/'homes/modern-block'
INK='#343a36'; MUTED='#6d746b'; PAPER='#fbfaf6'; STONE='#e5dfd1'; WOOD='#c4a98b'; LINE='#7f776b'

def feet(m):
    inches=round(m/.0254);return f"{inches//12}'-{inches%12}\""
def dim(ax,a,b,label,offset=.8):
    a=list(a);b=list(b)
    if a[1]==b[1]:
        y=a[1]+offset;ax.plot([a[0],a[0]],[a[1],y],color=MUTED,lw=.45);ax.plot([b[0],b[0]],[b[1],y],color=MUTED,lw=.45)
        ax.annotate('',(a[0],y),(b[0],y),arrowprops=dict(arrowstyle='|-|',color=MUTED,lw=.65));ax.text((a[0]+b[0])/2,y+.15,label,ha='center',va='bottom',fontsize=8,color=INK)
    else:
        x=a[0]+offset;ax.plot([a[0],x],[a[1],a[1]],color=MUTED,lw=.45);ax.plot([b[0],x],[b[1],b[1]],color=MUTED,lw=.45)
        ax.annotate('',(x,a[1]),(x,b[1]),arrowprops=dict(arrowstyle='|-|',color=MUTED,lw=.65));ax.text(x+.16,(a[1]+b[1])/2,label,rotation=90,ha='left',va='center',fontsize=8,color=INK)

def segment_wall(ax,a,b,openings=(),width=.15,glazed=False,door_handings=None):
    dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy);ux=dx/length;uy=dy/length
    cursor=0
    normalized=[(o[0],o[1],o[2] if len(o)>2 else ('window' if glazed else 'door')) for o in openings]
    for off,w,kind in sorted(normalized+[(length,0,'')]):
        if off>cursor:ax.plot([a[0]+ux*cursor,a[0]+ux*off],[a[1]+uy*cursor,a[1]+uy*off],color=INK,lw=4 if width>.2 else 2.4,solid_capstyle='butt',zorder=5)
        if w:
            p=(a[0]+ux*off,a[1]+uy*off);q=(p[0]+ux*w,p[1]+uy*w)
            if kind=='window':
                ax.plot([p[0],q[0]],[p[1],q[1]],color='#7faaa9',lw=1.8,zorder=6)
                ax.plot([p[0]-.04*uy,q[0]-.04*uy],[p[1]+.04*ux,q[1]+.04*ux],color='#7faaa9',lw=.7,zorder=6)
            elif kind=='gap':
                pass
            elif kind=='garage':
                ax.plot([p[0],q[0]],[p[1],q[1]],color=WOOD,lw=3,zorder=6)
            elif door_handings and off in door_handings:
                # Coordinated service leaves match the native inset end hinges.
                normal_sign=door_handings[off];leaf=w-.05
                hinge=(p[0]+ux*leaf,p[1]+uy*leaf)
                nx,ny=-uy*normal_sign,ux*normal_sign
                end=(hinge[0]+nx*leaf,hinge[1]+ny*leaf)
                ax.plot([hinge[0],end[0]],[hinge[1],end[1]],color=LINE,lw=.7,zorder=6)
                closed=math.degrees(math.atan2(-uy,-ux))%360
                opened=math.degrees(math.atan2(ny,nx))%360
                swept=closed+(opened-closed+180)%360-180
                ax.add_patch(Arc(hinge,leaf*2,leaf*2,theta1=min(closed,swept),theta2=max(closed,swept),color=LINE,lw=.45,ls='--',zorder=6))
            else:
                # Concept door leaf and swing at measured opening; handing is illustrative.
                end=(p[0]-uy*w,p[1]+ux*w)
                ax.plot([p[0],end[0]],[p[1],end[1]],color=LINE,lw=.7,zorder=6)
                theta=math.degrees(math.atan2(dy,dx));ax.add_patch(Arc(p,w*2,w*2,theta1=theta,theta2=theta+90,color=LINE,lw=.45,ls='--',zorder=6))
        cursor=off+w

def footprint(ax,r,fill=STONE,lw=.8):
    x0,y0,x1,y1=r;ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,facecolor=fill,edgecolor=LINE,lw=lw,zorder=1))

def outline(ax,r,color=LINE,dashed=False,lw=.8,zorder=6):
    x0,y0,x1,y1=r
    ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,edgecolor=color,lw=lw,ls='--' if dashed else '-',zorder=zorder))

def exterior_projections(ax,level):
    """Distinguish occupied cantilever, ground enclosure and exterior shading geometry."""
    pier=design_source.EAST_FLUE_PIER
    footprint(ax,pier,'#cfc7b7')
    outline(ax,pier,INK,lw=1)
    ax.annotate('STONE FLUE PIER',xy=((pier[0]+pier[2])/2,(pier[1]+pier[3])/2),xytext=(24.1,5.6),
                ha='center',fontsize=6.5,color=MUTED,rotation=90,
                arrowprops=dict(arrowstyle='-',color=MUTED,lw=.55),zorder=8)
    if level=='ground':
        footprint(ax,design_source.ENTRY_LANDING,'#ded5c5')
        x0,y0,x1,y1=design_source.ENTRY_STEPS
        for i in range(3):
            yy=y0+i*(y1-y0)/3
            footprint(ax,(x0,yy,x1,yy+(y1-y0)/3),'#ebe5d9')
        outline(ax,design_source.ENTRY_PORTAL,WOOD,dashed=True,lw=1.1)
        outline(ax,(UPPER_RECT[0],UPPER_RECT[1],UPPER_RECT[2],MAIN[1]),WOOD,dashed=True,lw=1.1)
        ax.text(13.2,UPPER_RECT[1]-.4,'UPPER FLOOR ABOVE\n'+feet(MAIN[1]-UPPER_RECT[1])+' PROJECTION',ha='center',va='top',fontsize=6.4,color=MUTED)
        ax.annotate('SHELTERED PORCH\n3 EQUAL RISERS',xy=(20.4,-.7),xytext=(17.8,-2.75),
                    ha='center',fontsize=6.5,color=MUTED,
                    arrowprops=dict(arrowstyle='-',color=MUTED,lw=.55),zorder=8)
    else:
        depth=design_source.FRONT_REVEAL_DEPTH
        outline(ax,(10.4,UPPER_RECT[1]-depth,16.7,UPPER_RECT[1]),WOOD,dashed=True)
        ax.plot([UPPER_RECT[0],UPPER_RECT[2]],[MAIN[1],MAIN[1]],color=MUTED,ls='--',lw=.65,zorder=4)
        ax.annotate('GROUND WALL BELOW',xy=(10.7,MAIN[1]),xytext=(8.8,-1.65),ha='center',fontsize=6.3,color=MUTED,arrowprops=dict(arrowstyle='-',color=MUTED,lw=.45),zorder=8)
        screen=design_source.PRIMARY_BATH_SCREEN
        footprint(ax,screen,'#d9c3a7')
        x0,y0,x1,y1=screen
        for i in range(24):
            xx=x0+(i+.5)*(x1-x0)/24
            ax.plot([xx-.035,xx+.035],[y0,y1],color=WOOD,lw=.65,zorder=7)
        ax.text((x0+x1)/2,y0-.10,'RAISED-SILL BATH GLAZING\nEXTERNAL PRIVACY SCREEN',
                ha='center',va='top',fontsize=6.4,color=MUTED)

def furniture(ax,record):
    if 'corners_m' in record:
        corners=record['corners_m'];record=dict(record)
        record['x']=sum(p[0] for p in corners)/4;record['y']=sum(p[1] for p in corners)/4
        record['width']=math.dist(corners[0],corners[1]);record['depth']=math.dist(corners[1],corners[2])
        record['rotation']=record.get('rotation_rad',0)
        record['kind']=record.get('asset_id',record.get('name','furniture'))
    if 'polygon' in record:
        zorder=1.5 if record.get('kind')=='counter' else 3
        ax.add_patch(Polygon(record['polygon'],closed=True,fc=record.get('color',WOOD),ec=LINE,lw=.55,zorder=zorder));return
    x=record.get('x',0);y=record.get('y',0);w=record.get('width',record.get('w',1));d=record.get('depth',record.get('d',1));angle=record.get('rotation_deg',math.degrees(record.get('rotation',0)))
    kind=record.get('kind','furniture').lower();trans=Affine2D().rotate_deg_around(x,y,angle)+ax.transData
    color='#f3f0e8' if any(k in kind for k in ['bed','sofa','chair','bath','toilet','sink','shower','tub','basin']) else WOOD
    if 'rug' in kind:
        ax.add_patch(Rectangle((x-w/2,y-d/2),w,d,facecolor='#ede7d8',edgecolor='#c5bda8',lw=.4,transform=trans,zorder=2));return
    ax.add_patch(Rectangle((x-w/2,y-d/2),w,d,facecolor=color,edgecolor=LINE,lw=.65,transform=trans,zorder=3))
    if 'bed' in kind:
        for px in [-w*.23,w*.23]:ax.add_patch(Rectangle((x+px-w*.19,y-d*.43),w*.38,d*.22,facecolor='white',edgecolor=LINE,lw=.35,transform=trans,zorder=4))
        ax.plot([x-w/2,x+w/2],[y-d*.12,y-d*.12],color=LINE,lw=.4,transform=trans,zorder=4)
    if any(k in kind for k in ['sink','basin','toilet','tub']):
        ax.add_patch(Rectangle((x-w*.36,y-d*.32),w*.72,d*.64,facecolor='#fff',edgecolor=LINE,lw=.4,transform=trans,zorder=4))
    if 'shower' in kind:
        ax.plot([x-w*.4,x+w*.4],[y-d*.4,y+d*.4],color=LINE,lw=.5,transform=trans,zorder=4)
    if 'cook' in kind or 'range' in kind:
        for px in [-w*.25,w*.25]:
            for py in [-d*.23,d*.23]:ax.add_patch(Circle((x+px,y+py),min(w,d)*.14,fc='none',ec=LINE,lw=.5,transform=trans,zorder=4))
    tag=record.get('tag')
    if tag:ax.text(x,y,tag,fontsize=5.5,ha='center',va='center',color=INK,zorder=5)

def read_layout(path):
    if not path.exists():return []
    raw=json.loads(path.read_text())
    return raw.get('items',raw.get('placements',[])) if isinstance(raw,dict) else raw

def draw(level,out,layout,openings):
    fig=plt.figure(figsize=(18,12),facecolor=PAPER)
    ax=fig.add_axes([.04,.13,.70,.77]);ax.set_aspect('equal');ax.axis('off');ax.set_facecolor(PAPER)
    side=fig.add_axes([.78,.13,.20,.76]);side.axis('off')
    if level=='ground':
        for r in [MAIN,GUEST,GARAGE]:footprint(ax,r,'#f6f2e9')
        footprint(ax,LANAI,'#ddd6c8');footprint(ax,COURT,'#e9eddf');footprint(ax,POOL,'#9bc3c4')
        ax.text(5,6.8,'COURTYARD',fontsize=11,ha='center',color=MUTED)
        ax.text(5,13,'POOL\n13\'-1" × 26\'-3"',ha='center',va='center',fontsize=9,color='#365f64')
        ax.text(5,1.5,'COVERED LANAI',ha='center',fontsize=10,color=INK)
        for x in [.2,9.8]:ax.plot([x,x],[.1,4.9],color=WOOD,lw=5)
        for cy in [14.05,17.85]:
            footprint(ax,(-6.0,cy-.95,-1.2,cy+.95),'#d9dddc');ax.add_patch(Rectangle((-5.1,cy-.8),2.9,1.6,fill=False,ec=LINE,lw=.6,zorder=2))
        ext=[('main-south',(10,0),(22,0)),('main-west',(10,0),(10,20)),('main-east',(22,0),(22,20)),('main-north',(10,20),(22,20)),('guest-south',(-8,0),(0,0)),('guest-west',(-8,0),(-8,20)),('guest-east',(0,0),(0,20)),('garage-north',(-8,20),(0,20)),('garage-divide',(-8,12),(0,12))]
        dim(ax,(-8,20),(22,20),feet(30),1.2);dim(ax,(22,0),(22,20),feet(20),3.3)
        dim(ax,(-8,0),(0,0),feet(8),-3.45);dim(ax,(0,0),(10,0),feet(10),-3.45);dim(ax,(10,0),(22,0),feet(12),-3.45)
        ax.set_xlim(-9.5,27);ax.set_ylim(-4.1,22.5)
    else:
        footprint(ax,(7,9,10,17),'#ddd6c8');ax.text(8.5,13.8,'COVERED\nBALCONY',ha='center',va='center',fontsize=8,color=MUTED)
        footprint(ax,UPPER_RECT,'#f6f2e9')
        ux0,uy0,ux1,uy1=UPPER_RECT
        ext=[('upper-south',(ux0,uy0),(ux1,uy0)),('upper-west',(ux0,uy0),(ux0,uy1)),('upper-east',(ux1,uy0),(ux1,uy1)),('upper-north',(ux0,uy1),(ux1,uy1))]
        dim(ax,(ux0,uy1),(ux1,uy1),feet(ux1-ux0),1.1);dim(ax,(ux1,uy0),(ux1,uy1),feet(uy1-uy0),3.3)
        dim(ax,(ux1,uy0),(ux1,MAIN[1]),feet(MAIN[1]-uy0),1.45)
        ax.set_xlim(5.8,27);ax.set_ylim(UPPER_RECT[1]-2.0,19)
    exterior_projections(ax,level)
    for name,a,b in ext:
        if isinstance(openings,list):
            ops=[];dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy);u=(dx/length,dy/length)
            for opening in openings:
                if ('upper' if 'Upper' in opening.get('level','') else 'ground')!=level:continue
                p,q=opening['a'],opening['b']
                if abs((p[0]-a[0])*u[1]-(p[1]-a[1])*u[0])>.01 or abs((q[0]-a[0])*u[1]-(q[1]-a[1])*u[0])>.01:continue
                t=[(r[0]-a[0])*u[0]+(r[1]-a[1])*u[1] for r in [p,q]]
                if min(t)>=-.01 and max(t)<=length+.01:ops.append((min(t),abs(t[1]-t[0]),'gap' if opening.get('kind')=='door' else opening.get('kind','window')))
        else:ops=openings.get(name,[])
        segment_wall(ax,a,b,ops,.28,True)
    if isinstance(openings,list):
        for op in openings:
            if op.get('kind')!='door' or ('upper' if 'Upper' in op.get('level','') else 'ground')!=level:continue
            a,b=op['a'],op['b'];length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length
            hinge=(a[0]+ux*.05,a[1]+uy*.05);dv=(ux*math.cos(.22)-uy*math.sin(.22),uy*math.cos(.22)+ux*math.sin(.22))
            end=(hinge[0]+dv[0]*(length-.1),hinge[1]+dv[1]*(length-.1))
            ax.plot([hinge[0],end[0]],[hinge[1],end[1]],color=WOOD,lw=1.3,zorder=6)
    for name,a,b,ops in PARTITIONS[level]:
        handings=({3.15:-1} if name=='Service west' else {.8:1} if name=='Service hall south' else None) if level=='ground' else None
        segment_wall(ax,a,b,ops,door_handings=handings)
    if level=='ground':
        sx,sy=kitchen_source.SINK
        # Same four stone regions around the actual sink aperture as the host.
        for r in [(10.23,19.075,sx-.332,19.82),(sx+.332,19.075,12.558,19.82),
                  (sx-.332,19.075,sx+.332,sy-.232),(sx-.332,sy+.232,sx+.332,19.82),
                  (13.802,19.075,14.437,19.82),kitchen_source.ISLAND,
                  (16.2652,15.14,17.5244,15.84)]:
            footprint(ax,r,'#e8e3d8')
    for record in layout:
        if record.get('level')==level:furniture(ax,record)
    if level=='upper':
        r=design_source.SHOWER_SERVICE_WALL
        footprint(ax,r,'#cfc7b7');outline(ax,r,INK,lw=1.1)
        ax.annotate('SHOWER PLUMBING WALL\n'+feet(design_source.SHOWER_SERVICE_HEIGHT)+' HIGH',
                    xy=((r[0]+r[2])/2,(r[1]+r[3])/2),xytext=(19.2,-.64),
                    ha='center',va='center',fontsize=6.4,color=MUTED,
                    arrowprops=dict(arrowstyle='-',color=MUTED,lw=.55),zorder=8)
    for slug,x,y,angle in ([('coastal-outdoor-sofa',4.9,3.9,math.pi),('coastal-outdoor-lounge-chair',1.8,3.6,-.5),('slatted-outdoor-chaise',1.35,10.3,0),('slatted-outdoor-chaise',1.35,14.2,0)] if level=='ground' else [('coastal-outdoor-lounge-chair',8.4,10.6,math.pi/2),('coastal-outdoor-lounge-chair',8.4,15,math.pi/2)]):
        meta=json.loads((ROOT/'library/furniture'/slug/'v001/asset.json').read_text());w,dep,_=meta['dimensions_m'];furniture(ax,{'x':x,'y':y,'width':w,'depth':dep,'rotation':angle,'kind':slug})
    if level=='ground':
        for x in [1,3,5,7,9]:
            ux=math.cos(math.radians(75))*.9;uy=math.sin(math.radians(75))*.9
            ax.plot([x-ux,x+ux],[-uy,uy],color=WOOD,lw=2.8,zorder=6)
        ax.text(5,.6,'PIVOT SCREENS / OPEN',ha='center',fontsize=6,color=MUTED)
    # U stair is an actual reserved opening; identical run logic in both levels.
    x0,y0,x1,y1=STAIR_VOID
    if level=='upper':footprint(ax,STAIR_VOID,'#eee9e0');ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,ec=INK,lw=.9,ls='--',zorder=5))
    for i in range(12):
        y=y0+.28*i
        ax.plot([19.1,20.3],[y,y],color=LINE,lw=.55,zorder=6)
    for i in range(11):
        y=11.28-.28*i
        ax.plot([20.5,21.7],[y,y],color=LINE,lw=.55,zorder=6)
    points=[(19.7,8.35),(19.7,11.89),(21.1,11.89),(21.1,8.35)]
    if level=='upper':points=list(reversed(points))
    ax.plot([v[0] for v in points[:-1]],[v[1] for v in points[:-1]],color=INK,lw=.65,zorder=7)
    ax.annotate('',xy=points[-1],xytext=points[-2],arrowprops=dict(arrowstyle='->',color=INK,lw=.65),zorder=7)
    ax.text(points[0][0],points[0][1]-.2,'UP' if level=='ground' else 'DOWN',ha='center',fontsize=6,color=INK,zorder=7)
    rooms=ROOMS[level]
    for i,(name,x0,y0,x1,y1) in enumerate(rooms,1):
        lx,ly=(x1-.3,y1-.35) if 'Stair' in name else (x0+.30,y1-.34)
        ax.text(lx,ly,str(i).zfill(2),fontsize=7.5,color=INK,ha='center',va='center',bbox=dict(boxstyle='circle,pad=.18',fc=PAPER,ec=MUTED,lw=.5),zorder=9)
    side.text(0,1,'ROOM INDEX',fontsize=12,fontweight='bold',color=INK,va='top')
    step=.047 if level=='ground' else .065
    for i,(name,x0,y0,x1,y1) in enumerate(rooms,1):
        yy=.94-(i-1)*step;side.text(0,yy,f'{i:02d}  {name}',fontsize=9,color=INK,va='top');side.text(.085,yy-.020,f'{feet(x1-x0)} × {feet(y1-y0)}',fontsize=7.5,color=MUTED,va='top')
    side.text(0,.235,'ROOF + DRAINAGE INTENT',fontsize=9,fontweight='bold',color=INK)
    side.text(0,.217,'Low roofs fall 1:80 toward +Y.\nRear collection to planted-strip concept.\nOverflow, capacity and lawful discharge\nremain unresolved.',fontsize=7.6,color=MUTED,linespacing=1.45,va='top')
    side.text(0,.055,'Outer room zones shown.\nNet room sizes depend on wall thickness.\nExterior doors shown at modeled angle.\nDashed outline: overhead projection.\nOrientation is not surveyed.',fontsize=7.6,color=MUTED,linespacing=1.5,va='bottom')
    fig.text(.04,.953,'MODERN BLOCK',fontsize=25,fontweight='bold',color=INK)
    fig.text(.04,.921,(f'Ground floor + courtyard  ·  {feet(design_source.GROUND_CLEAR)} minimum clear ceiling' if level=='ground' else f'Upper floor + private rooms  ·  {feet(design_source.UPPER_CLEAR)} clear ceiling'),fontsize=15,color=MUTED)
    fig.text(.975,.945,'CONCEPT PLAN  /  '+('01' if level=='ground' else '02'),ha='right',fontsize=10,color=MUTED)
    if level=='ground':fig.text(.04,.111,"Rear service ceiling: 3.7776 m / approx. 12′5″ clear  •  Garage: 3.7576 m / approx. 12′4″ clear  •  Lanai: 12 ft clear with glazed transoms above 3 m leaves",fontsize=8.3,color=MUTED)
    fig.text(.04,.089,f'Upper finished floor +{feet(design_source.UPPER)}  •  {design_source.FLOOR_ASSEMBLY/.0254:.0f} in floor/services reserve  •  24 equal stair rises at 6¾ in; 11 treads per flight',fontsize=8.8,color=MUTED)
    fig.text(.04,.065,'4 bedrooms  •  3 full baths + powder  •  2-car garage',fontsize=10,color=INK)
    fig.text(.04,.04,f'Conditioned gross: {CONDITIONED_M2:,.2f} m² / {CONDITIONED_M2/0.09290304:,.0f} sq ft. Excludes garage, lanai, pool, balcony, porch, screens/reveals, terraces and upper stair void; occupied cantilever included.',fontsize=8.6,color=MUTED)
    fig.text(.04,.021,'Creative architectural study. Dimensions are concept choices; not an as-built record, permit drawing or code approval.',fontsize=8,color=MUTED)
    fig.text(.975,.043,'METERS IN MODEL  /  FEET + INCHES SHOWN',ha='right',fontsize=8,color=MUTED)
    out.mkdir(parents=True,exist_ok=True)
    for suffix in ['png','svg','pdf']:fig.savefig(out/f'{level}-floor.{suffix}',dpi=180,facecolor=PAPER,metadata={'Title':f'Modern Block {level} concept plan'} if suffix=='pdf' else None)
    svg=out/f'{level}-floor.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--promote',action='store_true');p.add_argument('--layout',type=Path,default=ROOT/'tools/modern_block/interiors-layout.json');p.add_argument('--openings',type=Path,default=HOME/'model/opening-schedule.json');args=p.parse_args()
    out=HOME/('outputs/plans' if args.promote else 'outputs/work/plans')
    layout=read_layout(args.layout);ops=json.loads(args.openings.read_text()) if args.openings.exists() else {}
    for level in ['ground','upper']:draw(level,out,layout,ops)
    print(json.dumps({'output':str(out),'furniture_records':len(layout),'openings_file':args.openings.exists()}))
