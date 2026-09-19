"""Proposed openings shared by the model, drawing and schedule; meters."""
import math
from design import LEVELS

def garage_openings(a,b):
    length=math.dist(a,b)
    if (a[1]+b[1])/2<1 and length>4 and (b[0]-a[0])*(b[1]-a[1])<0:
        return [dict(offset=.325,width=length-.65,sill=.04,height=2.51,kind='garage_door')]
    return proposed_openings('main',a,b)

def proposed_openings(key,a,b):
    L=math.dist(a,b);ops=[]
    if L<.05:return ops
    mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
    horizontal=abs(a[1]-b[1])<.2;vertical=abs(a[0]-b[0])<.2
    if key=='basement':
        if my>14 and L>2.5:ops=[dict(offset=.45,width=L-.9,sill=.12,height=2.48)]
        elif mx<.1 and vertical and L>6:
            for low,high in [(.8,2.9),(5.3,7.4)]:
                off=(a[1]-high) if b[1]<a[1] else low-a[1]
                if 0<off and off+high-low<L:ops.append(dict(offset=off,width=high-low,sill=1.05,height=1.4))
    elif key=='main':
        if my>15 and horizontal and L>3:
            if L>8:
                w=(L-1.15)/2;ops=[dict(offset=.35,width=w,sill=.08,height=2.68),dict(offset=.80+w,width=w,sill=.08,height=2.68)]
            else:ops=[dict(offset=.35,width=L-.7,sill=.18,height=2.58)]
        elif horizontal and my<.5 and L>2.4:ops=[dict(offset=.4,width=L-.8,sill=.45,height=2.3)]
        elif horizontal and 11<my<13 and L>3:
            # Sink-side daylight; keep a solid pier behind cooktop and hood.
            x0,x1=4.60,6.35
            off=(a[0]-x1) if b[0]<a[0] else x0-a[0]
            if 0<off and off+x1-x0<L:ops=[dict(offset=off,width=x1-x0,sill=1.1,height=1.67)]
        elif horizontal and 2.2<my<3.3 and 4<mx<8 and L>2.5:
            ops=[dict(offset=.26,width=L-.52,sill=.02,height=2.72,kind='entry')]
        elif vertical and L>4 and (mx<.5 or mx>18):
            w=min(3.6,L-1.3);ops=[dict(offset=(L-w)/2,width=w,sill=.5,height=2.25)]
        elif vertical and 4.1<mx<4.5 and 9<my<12 and L>2:
            ops=[dict(offset=(L-1.6)/2,width=1.6,sill=1.1,height=1.67)]
    elif L>3.0:
        w=min(3.55,L-1.05);ops=[dict(offset=(L-w)/2,width=w,sill=.6,height=2.2)]
        if my>14 and mx>10:ops=[dict(offset=(L-w)/2,width=w,sill=.08,height=2.68)]

    # The front brick tower has one aligned, two-storey charcoal window inset.
    # These are deliberate facade proposals, independent of the source glazing.
    if horizontal and key=='main' and my<-.2 and 8<mx<11.5:
        ops=[dict(offset=8.51-a[0],width=2.37,sill=.45,height=2.3)]
    if horizontal and key=='upper' and abs(my)<.1 and 8<mx<11.5:
        ops=[dict(offset=8.51-a[0],width=2.37,sill=.6,height=2.2)]

    # Retain actual exterior passage locations. The new front opening is a
    # combined door/sidelight; rear wall modules containing source doors are
    # explicitly door assemblies instead of fixed window panes.
    ux,uy=(b[0]-a[0])/L,(b[1]-a[1])/L
    for source in LEVELS[key]['exterior_openings']:
        if source['type']!='door':continue
        t=[];normal=[]
        for p in [source['a'],source['b']]:
            dx,dy=p[0]-a[0],p[1]-a[1];t.append(dx*ux+dy*uy);normal.append(abs(dx*uy-dy*ux))
        lo,hi=min(t),max(t)
        if max(normal)>.16 or lo<-.15 or hi>L+.15:continue
        lo=max(.04,lo);hi=min(L-.04,hi)
        hit=False
        for op in ops:
            if lo<op['offset']+op['width'] and hi>op['offset']:
                op['kind']='entry' if 'Front entry'==source['name'] else 'glazed_door'
                op['sill']=.02;op['height']=max(op['height'],2.45);hit=True
        if not hit and hi-lo>.5:ops.append(dict(offset=lo,width=hi-lo,sill=.02,height=2.4,kind='passage'))
    return sorted(ops,key=lambda op:op['offset'])

def schedule():
    records=[]
    for key,data in LEVELS.items():
        p=data['footprint']
        for i,(a,b) in enumerate(zip(p,p[1:]+p[:1])):
            L=math.dist(a,b)
            for op in proposed_openings(key,a,b):
                def at(t):return [a[j]+(b[j]-a[j])*t/L for j in range(2)]
                records.append(dict(level=key,wall=i,a=at(op['offset']),b=at(op['offset']+op['width']),**op))
    return records
