"""Reviewed envelope and bathroom finish details shared by build and safe native updates."""
import bpy,math
from common import geometry as g
from common.geometry import box,cyl,curve,area,F
from common.architecture import mesh
from common.furnishings import bowl
from design import roof_z

def polish(ROOT,M,clad,glazing):
    s=bpy.context.scene
    # The primary bedroom moved: its side glass must not cross the bath partition.
    for o in list(s.objects):
        if o.name.startswith(('East timber wall','Primary side sill','Primary side head','Primary forest window','Refined ')):bpy.data.objects.remove(o,do_unlink=True)
    g.ACTIVE=next(c for c in bpy.data.collections if c.name.startswith('01 Architecture'))
    for a,b in [(0,13),(23,29),(33.5,40)]:clad('East timber wall',(59.8,a),(59.8,b),0,roof_z((a+b)/2))
    clad('Primary side sill',(59.8,13),(59.8,23),0,2.4);clad('Primary side head',(59.8,13),(59.8,23),9,roof_z(18))
    glazing('Primary forest window',(59.8,13),(59.8,23),0,9,2.4,3)
    g.collection('07 Finishes | bath stone surfaces')
    # Dry-finish geometry; waterproofing assembly remains a specified-design task.
    for a,b in [(40,47),(57,60)]:box('Refined bath front stone lining',((a+b)/2,.56,5.05),(b-a,.12,10.1),M['stone'],.008)
    box('Refined bath clerestory sill lining',(52,.56,3.5),(10,.12,7),M['stone'],.008)
    box('Refined bath clerestory head lining',(52,.56,9.65),(10,.12,.9),M['stone'],.008)
    box('Refined bath east stone lining',(59.44,6,5.05),(.12,12,10.1),M['stone'],.008)
    box('Refined bath limestone floor',(50,6,.035),(19.6,11.6,.035),M['stone'],.003)
    # The vanity bowls become actual recessed basins rather than tall vessels.
    top=bpy.data.objects['Primary double vanity stone']
    for o in list(s.objects):
        if o.name.startswith(('Primary double vanity basin','Primary vanity faucet')):bpy.data.objects.remove(o,do_unlink=True)
    for x in [53,57]:
        cut=cyl('Temporary primary sink cutout',(x,10.8,3.0),.67,.65,M['steel'],64)
        bpy.context.view_layer.objects.active=top;mod=top.modifiers.new('Recessed basin opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
        bowl('Primary double vanity basin',x,10.8,2.70,.74,M['porcelain'])
        curve('Primary vanity faucet',[(x,11.5,3.1),(x,11.5,3.7),(x,11.0,3.83),(x,10.8,3.6)],.028,M['steel'])
    for obj in s.objects:
        if obj.name.startswith('Primary vanity mirror'):
            mat=g.material('Refined clear silver mirror',(.8,.8,.8),.04,1);obj.data.materials.clear();obj.data.materials.append(mat)
    area('Refined primary bath soft daylight',(51,6.7,9.7),(53,5,2.5),280,8,(1,.93,.83))
    area('Refined primary vanity soft fill',(54,8.6,8.6),(55,10.8,3.0),100,6,(1,.95,.87))
    # Shared base cabinets intentionally omit tops, so host vanities need them.
    for prefix,x,y,z in [('Lower shared bath',48.2,23.5,-11),('Powder',26,1.4,0)]:
        for obj in list(s.objects):
            if obj.name.startswith(prefix+' basin') or obj.name.startswith(prefix+' vanity basin'):bpy.data.objects.remove(obj,do_unlink=True)
        t=box('Refined '+prefix+' vanity stone',(x,y,z+2.95),(2.25,2.5,.16),M['counter'],.02)
        cut=cyl('Temporary vanity bowl opening',(x,y,z+2.95),.56,.55,M['steel'],48)
        bpy.context.view_layer.objects.active=t;mod=t.modifiers.new('Actual basin cutout','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
        bowl('Refined '+prefix+' inset basin',x,y,z+2.74,.60,M['porcelain'])
        curve('Refined '+prefix+' faucet',[(x,y+.85,z+3.04),(x,y+.85,z+3.62),(x,y+.4,z+3.7),(x,y,z+3.4)],.027,M['steel'])
