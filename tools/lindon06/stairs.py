"""Meter-based, explicitly proposed stair coordination for the Lindon concept.

The source stair traces are retained in design.SOURCE_STAIR_TRACES. This module
constructs complete flights, risers, stringers, landings and guards rather than
filling bounding boxes with floor blocks. No code/engineering approval implied.
"""
import math
import design


def _distance(a,b):
    return math.hypot(b[0]-a[0],b[1]-a[1])


def _lerp(a,b,t):
    return (a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)


def _rounded_path(points,trim=.65):
    """Short quadratic corner transitions; no zero-radius overlapping tread turn."""
    out=[points[0]]
    for a,b,c in zip(points,points[1:],points[2:]):
        take=min(trim,_distance(a,b)*.45,_distance(b,c)*.45)
        p=_lerp(b,a,take/_distance(a,b));q=_lerp(b,c,take/_distance(b,c))
        out.append(p)
        for j in range(1,9):
            t=j/8
            out.append(((1-t)**2*p[0]+2*(1-t)*t*b[0]+t*t*q[0],
                        (1-t)**2*p[1]+2*(1-t)*t*b[1]+t*t*q[1]))
    out.append(points[-1])
    return out


def _foyer_path():
    pts=[(5.04,4.25),(5.04,5.20)]
    for j in range(1,33):
        theta=math.pi-j/32*math.pi/2
        pts.append((6.13+1.09*math.cos(theta),5.20+1.09*math.sin(theta)))
    pts.append((8.90,6.29))
    return pts


def _path_length(path):
    return sum(_distance(a,b) for a,b in zip(path,path[1:]))


def _at(path,d):
    d=max(0,min(_path_length(path),d))
    for i,(a,b) in enumerate(zip(path,path[1:])):
        length=_distance(a,b)
        if d<=length or i==len(path)-2:
            u=((b[0]-a[0])/length,(b[1]-a[1])/length)
            return _lerp(a,b,min(1,d/length)),u
        d-=length


def _ribbon(path,a,b,width):
    left=[];right=[]
    for j in range(5):
        p,u=_at(path,a+(b-a)*j/4);n=(-u[1],u[0])
        left.append((p[0]+n[0]*width/2,p[1]+n[1]*width/2))
        right.append((p[0]-n[0]*width/2,p[1]-n[1]*width/2))
    return left+list(reversed(right))


def _platform_polygon(p,u,start,end,width):
    n=(-u[1],u[0])
    return [(p[0]+u[0]*t+n[0]*side*width/2,
             p[1]+u[1]*t+n[1]*side*width/2)
            for t,side in [(start,-1),(end,-1),(end,1),(start,1)]]


def build_stairs(M):
    from common import geometry as g
    from utils import prism,rod,beam,tag
    g.collection('10 Stairs | proposed coordinated flights and guards')
    receipts=[]
    rear=_rounded_path(design.REAR_STAIR_PATH)
    specs=[('Curved foyer stair',_foyer_path(),0.,3.25,19,'Ground floor'),
           ('Rear main to upper stair',rear,0.,3.25,19,'Ground floor'),
           ('Rear basement to main stair',rear,-3.15,0.,18,'Walkout basement')]

    def rail(name,a,b,z,level):
        length=_distance(a,b)
        if length<.05:return
        tag(rod(name+' oak handrail',(*a,z+1.03),(*b,z+1.03),.028,M['oak']),'IfcRailing',level)
        # Thin closely spaced vertical balusters leave visual continuity through
        # the foyer without treating glass as an engineered guard specification.
        n=max(1,math.ceil(length/.11))
        for j in range(n+1):
            p=_lerp(a,b,j/n)
            tag(rod(name+' baluster',(*p,z+.03),(*p,z+1.01),.009,M['dark']),'IfcRailing',level)

    for name,path,bottom,top,risers,level in specs:
        width=1.04;run=_path_length(path);rise=(top-bottom)/risers
        going=run/(risers-1)
        for j in range(risers-1):
            a=j*going;b=(j+1)*going;z=bottom+(j+1)*rise
            tread=tag(prism(name+f' oak tread {j+1:02}',_ribbon(path,a,b,width),z-.055,z,M['oak']),
                      'IfcStairFlight',level)
            tread['rise_m']=rise;tread['centerline_going_m']=going
            p,u=_at(path,a)
            tag(prism(name+f' closed riser {j+1:02}',_platform_polygon(p,u,-.012,.012,width),
                      bottom+j*rise,z,M['oak']),'IfcStairFlight',level)
        # Last riser meets a real top landing, bridging to the floor beyond the
        # opening. End landings are not stair-run length or additional risers.
        p,u=_at(path,run)
        tag(prism(name+' final riser',_platform_polygon(p,u,-.012,.012,width),top-rise,top,M['oak']),
            'IfcStairFlight',level)
        tag(prism(name+' upper landing',_platform_polygon(p,u,0,.72,1.08),top-.18,top,M['oak']),
            'IfcSlab','Upper floor' if top>1 else 'Ground floor')
        if bottom==0 and 'Rear' in name:
            p,u=_at(path,0)
            tag(prism(name+' lower landing bridge',_platform_polygon(p,u,-.72,0,1.08),-.18,0,M['oak']),
                'IfcSlab','Ground floor')

        # Sloped stringers and handrails follow both sides of every tread, with
        # intermediate posts. Curved/winder geometry has an explicit centerline
        # going; inner-edge compliance remains a measured-design check.
        count=max(12,math.ceil(run/.22))
        for side in [-1,1]:
            last=None;last_top=None
            for j in range(count+1):
                d=run*j/count;p,u=_at(path,d);n=(-u[1],u[0])
                xy=(p[0]+n[0]*side*(width/2-.025),p[1]+n[1]*side*(width/2-.025))
                z=bottom+rise+(top-bottom-rise)*j/count
                current=(*xy,z-.12);r_top=(*xy,z+.96)
                if last:
                    tag(beam(name+' side stringer',last,current,.08,.19,M['oak']),'IfcMember',level)
                    tag(rod(name+' continuous handrail',last_top,r_top,.026,M['oak']),'IfcRailing',level)
                last=current;last_top=r_top
            # Balusters are mounted to their actual tread elevation.
            for j in range(risers-1):
                for t in [.2,.65]:
                    d=(j+t)*going;p,u=_at(path,d);n=(-u[1],u[0])
                    xy=(p[0]+n[0]*side*(width/2-.025),p[1]+n[1]*side*(width/2-.025))
                    z=bottom+(j+1)*rise
                    rail_z=bottom+rise+(top-bottom-rise)*d/run+.96
                    tag(rod(name+' tread baluster',(*xy,z),(*xy,rail_z),.009,M['dark']),'IfcRailing',level)
        receipts.append(dict(name=name,risers=risers,rise_m=rise,width_m=width,
            centerline_run_m=run,centerline_going_m=going,
            lower_z_m=bottom,upper_z_m=top,
            evidence='Proposed stair geometry; not measured, engineered or code approved'))

    # Opening perimeter guards leave the designated floor-to-stair entry ends
    # open. The sloped flight rails above protect those intentional transitions.
    for key in ['main','upper']:
        level='Ground floor' if key=='main' else 'Upper floor'
        z=design.LEVELS[key]['z']
        for hole in design.LEVELS[key]['voids']:
            p=hole['polygon'];name=hole['name']
            for i,(a,b) in enumerate(zip(p,p[1:]+p[:1])):
                mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
                if 'rear' in name.lower():
                    # West top arrival is clear. The main-floor lower
                    # landing approaches from north; upper north edge is guarded.
                    if mid[0]<13.1 or (key=='main' and mid[1]>7.14):continue
                elif 'curved' in name.lower():
                    if mid[0]>8.8:continue
                elif 'Open foyer' in name:
                    # Its north edge adjoins the stair opening, not a floor edge.
                    if mid[1]>4.6:continue
                rail(name+f' edge {i+1}',a,b,z,level)

    return dict(stairs=receipts,
        stacked_rear_vertical_separation_m=[3.15,3.25],
        unresolved=['Structural attachment and stringer sizing',
                    'Code-specific winder walking line, guard and handrail requirements',
                    'As-built stair survey and underside storage coordination',
                    'North-facing rear lower landings are a proposed circulation change'])


if __name__=='__main__':
    # Pure geometric receipt works in ordinary Python without importing Blender.
    for name,path,n,h in [('foyer',_foyer_path(),19,3.25),
                          ('rear upper',_rounded_path(design.REAR_STAIR_PATH),19,3.25),
                          ('rear basement',_rounded_path(design.REAR_STAIR_PATH),18,3.15)]:
        print(name,'rise',round(h/n,4),'center-going',round(_path_length(path)/(n-1),4),
              'run',round(_path_length(path),3))
