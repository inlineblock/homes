"""Large-format stone wet-wall concept and mirror finish for the primary bath."""
import bpy
from common.geometry import collection,box,material

def finishes(M):
    collection('07 Finishes | primary bathing stone')
    # Real thin slab panels; waterproofing and backing are not specified here.
    for x0,x1 in [(0.4,5.65),(5.67,11.8),(11.82,17.8)]:
        box('Primary bath rear limestone slab',((x0+x1)/2,25.79,5.2),(x1-x0,.06,10.35),M['stone'],.006)
    box('Primary shower west stone lining',(.43,20.65,5.2),(.06,4.9,10.35),M['stone'],.006)
    box('Primary shower privacy sill lining',(.43,24.45,2.8),(.06,2.7,5.55),M['stone'],.006)
    box('Primary shower south stone lining',(3.05,18.21,5.2),(5.5,.06,10.35),M['stone'],.006)
    mirror=material('Primary silvered mirror',(.90,.91,.92),.06,1)
    for o in bpy.context.scene.objects:
        if o.name.startswith('Primary vanity mirror'):
            o.data.materials.clear();o.data.materials.append(mirror)
