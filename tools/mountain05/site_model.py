"""Illustrative forest slope, road, driveway and walkout grading bench."""
import bpy,math,random
from common import geometry as g
from common.geometry import box,rod,F
from common.architecture import mesh
from common.library import instance
from common.shared_assets import place
from assets import conifer
from design import grade

def site(root,M,CAT):
    g.collection('06 Landscape | wooded slope road and walkout bench')
    verts=[];faces=[];nx=191;ny=146
    for j in range(ny):
        y=-100+j*2
        for i in range(nx):x=-180+i*2;verts.append((x,y,grade(x,y)))
    for j in range(ny-1):
        for i in range(nx-1):
            x=-180+i*2+1;y=-100+j*2+1
            if 0<x<60 and 0<y<40:continue
            k=j*nx+i;faces.append((k,k+1,k+nx+1,k+nx))
    # Site-specific continuous duff/moss blend in world meters; original shader.
    # The reusable living planting above it comes from linked library assets.
    ground=M['soil'].copy();ground.name='Mountain site duff with irregular moss patches'
    n=ground.node_tree.nodes;l=ground.node_tree.links;bs=n.get('Principled BSDF')
    tex=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.33;noise.inputs['Detail'].default_value=4;noise.inputs['Roughness'].default_value=.72
    l.new(tex.outputs['Object'],noise.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.23;ramp.color_ramp.elements[0].color=(.025,.019,.011,1)
    ramp.color_ramp.elements[1].position=.76;ramp.color_ramp.elements[1].color=(.070,.090,.025,1)
    e=ramp.color_ramp.elements.new(.47);e.color=(.045,.038,.017,1)
    e=ramp.color_ramp.elements.new(.60);e.color=(.039,.057,.018,1)
    l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],bs.inputs['Base Color'])
    detail=n.new('ShaderNodeTexNoise');detail.inputs['Scale'].default_value=25;detail.inputs['Detail'].default_value=3
    l.new(tex.outputs['Object'],detail.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.48;bump.inputs['Distance'].default_value=.065
    l.new(detail.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal'])
    o=mesh('Continuous sloping forest ground',verts,faces,ground)
    for f in o.data.polygons:f.use_smooth=True
    # Road and drive lie at the upper datum; no reversing over pedestrian entrance.
    box('Front illustrative asphalt road',(25,-38,-.38),(360,20,.22),M['dark'],.02)
    box('Garage drive court',(13,-14,-.20),(27,28,.22),M['stone'],.02)
    for x in range(0,27,3):box('Driveway quiet paving joint',(x,-14,-.078),(.018,28,.005),M['dark'])
    for y in range(-28,0,4):box('Driveway transverse paving joint',(13,y,-.078),(27,.018,.005),M['dark'])
    box('Front entry landing',(36,-3,-.09),(7,6,.18),M['stone'],.02)
    for i in range(5):place('Shared arrival paving module',CAT['paver'],(36,-8-i*4.02,-.11))
    box('Drive to entry pedestrian link',(30,-8,-.16),(10,4,.14),M['stone'],.02)
    # Patio at walkout datum with a dedicated grade bench below; regular shared pavers.
    box('Walkout patio foundation',(42,46.5,-11.37),(36,13,.44),M['dark'],.02)
    for i in range(9):
        for j in range(3):place('Shared walkout limestone module',CAT['paver'],(25.9+i*4.02,42.1+j*4.02,-11.14))
    box('Walkout perimeter cut paver',(42,52.64,-11.19),(36,.67,.10),M['stone'],.01)
    # Modest retaining edge at rear of patio bench, beyond the usable paving.
    box('Patio low retaining edge',(42,55.8,-12.2),(38,.6,1.7),M['rock'],.03)
    # Continuous grade beneath plants. Large trees are true collection instances.
    tree=conifer(root,M);rng=random.Random(5505)
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    def hull(points):
        pts=sorted(set(points));lo=[];hi=[]
        for p in pts:
            while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
            lo.append(p)
        for p in reversed(pts):
            while len(hi)>1 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
            hi.append(p)
        return lo[:-1]+hi[:-1]
    corners=[(-12,-12),(80,-12),(80,66),(-12,66)]
    corridors=[hull(corners+[camera]) for camera in [(109,114),(118,72),(89,-94),(67,76)]]
    def on_view_corridor(x,y):
        # A crown-radius buffer is included in the building corners.
        return any(all(cross(p,poly[(i+1)%len(poly)],(x,y))>=0 for i,p in enumerate(poly)) for poly in corridors)
    positions=[]
    for i in range(210):
        x=rng.uniform(-115,150);y=rng.uniform(-15,152)
        if on_view_corridor(x,y):continue
        if -50<x<102 and -20<y<12:continue
        if any((x-a)**2+(y-b)**2<12**2 for a,b in positions):continue
        positions.append((x,y))
        instance('Shared mountain conifer v002',tree,(x,y,grade(x,y)),rng.uniform(0,math.tau),rng.uniform(.80,1.30))
    for x,y,s in [(-19,29,.87),(-22,67,1.06),(-34,-13,1.0),(20,118,1.15),(144,12,1.08)]:
        if not on_view_corridor(x,y):instance('Framing shared fir v002',tree,(x,y,grade(x,y)),rng.uniform(0,math.tau),s)
    def planting_allowed(x,y):
        if -1<x<69 and -1<y<55:return False
        if -2<x<28 and -29<y<0:return False
        if 26<x<41 and -29<y<-1:return False
        if y<-27:return False
        return True
    # Small plants form irregular drifts instead of isolated objects on bare soil.
    # Instances stay rooted exactly on the continuous evaluated grade.
    for i in range(1250):
        x=rng.uniform(-48,114);y=rng.uniform(-25,118)
        if not planting_allowed(x,y):continue
        density=.50+.28*math.sin(x*.22+y*.13)+.16*math.sin(x*.49-y*.31)
        if rng.random()>density:continue
        place('Shared understory meadow grass v002',CAT['grass'],(x,y,grade(x,y)),rng.uniform(0,math.tau),rng.uniform(.45,.95))
        if rng.random()<.38:
            xx=x+rng.uniform(-1.6,1.6);yy=y+rng.uniform(-1.6,1.6)
            if planting_allowed(xx,yy):place('Shared forest shrub v002',CAT['shrub'],(xx,yy,grade(xx,yy)),rng.uniform(0,math.tau),rng.uniform(.45,.95))
    # Denser grounded planting beds frame the approach and soften the house base.
    for i in range(120):
        x=rng.uniform(42,70);y=rng.uniform(-19,-2)
        if rng.random()<.62:place('Shared entry grass drift',CAT['grass'],(x,y,grade(x,y)),rng.uniform(0,math.tau),rng.uniform(.42,.72))
        else:place('Shared entry shrub drift',CAT['shrub'],(x,y,grade(x,y)),rng.uniform(0,math.tau),rng.uniform(.45,.72))
