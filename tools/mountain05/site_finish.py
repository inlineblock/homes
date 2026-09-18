"""Arrival continuity and distant woodland beyond the illustrative road."""
import bpy,math,random
from common import geometry as g
from common.geometry import box
from common.library import instance
from design import grade
from assets import conifer

def finish_site(root,M):
    for o in list(bpy.context.scene.objects):
        if o.name.startswith(('Arrival road cut paver','Distant shared forest')):bpy.data.objects.remove(o,do_unlink=True)
    g.collection('06 Landscape | wooded slope road and walkout bench')
    # A site-cut strip closes the last module to road edge without a soil gap.
    box('Arrival road cut paver',(36,-27.05,-.16),(4,1.94,.10),M['stone'],.006)
    tree=conifer(root,M);rng=random.Random(5531)
    for y in [-62,-82]:
        for x in range(-130,21,14):
            xx=x+rng.uniform(-3,3);yy=y+rng.uniform(-2,2)
            instance('Distant shared forest',tree,(xx,yy,grade(xx,yy)),rng.uniform(0,math.tau),rng.uniform(1.05,1.40))
