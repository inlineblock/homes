"""Refined original finishes, construction detail and scene dressing for Garage Loft."""
import bpy,math,random,json
from pathlib import Path
from common import geometry as g
from common.geometry import box,rod,cyl,sphere,F,material,area
from common.materials import noise_material
from common.landscape import grasses,rock

def wood(name,dark,light):
    m=material(name,dark,.38);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(32,32,.65)
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=2;noise.inputs['Roughness'].default_value=.7
    l.new(coord.outputs['Object'],mapping.inputs[0]);l.new(mapping.outputs[0],noise.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*dark,1);ramp.color_ramp.elements[1].color=(*light,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.13;bump.inputs['Distance'].default_value=.00025;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    p.inputs['Coat Weight'].default_value=.12;p.inputs['Coat Roughness'].default_value=.35
    return m

def prepare(root,M):
    M['walnut']=wood('Fine straight-grain oiled walnut',(.065,.03,.013),(.15,.079,.036))
    M['plaster']=noise_material('Fine warm mineral render',(.55,.53,.48),(.64,.62,.57),170,.77,.0003)
    M['concrete']=noise_material('Polished grey aggregate concrete',(.28,.29,.28),(.37,.38,.36),135,.34,.0003)
    M['fabric']=noise_material('Woven warm greige',(.26,.24,.21),(.4,.37,.32),250,.88,.0002)
    M['soil']=noise_material('Low meadow ground',(.045,.055,.025),(.095,.11,.045),130,.95,.001)
    M['fir']=noise_material('Rough muted tree bark',(.045,.028,.016),(.1,.068,.04),65,.92,.0015)
    M['green']=noise_material('Canopy color variation',(.025,.055,.017),(.075,.12,.035),9,.65,.0002)
    M['leaves']=noise_material('Fine olive foliage',(.045,.08,.024),(.12,.16,.055),12,.72,.0001)
    M['car-glass']=material('Automotive smoked glazing',(.009,.014,.018),.12,.28)
    M['stone']=noise_material('Pale limestone fine grain',(.53,.5,.43),(.64,.6,.53),180,.43,.0004)
    folder=root/'library/materials/warm-vertical-cedar/v002';path=folder/'warm-vertical-cedar.blend'
    if not path.exists():
        folder.mkdir(parents=True,exist_ok=True);m=wood('Cedar fine longitudinal grain',(.14,.06,.026),(.29,.145,.065));bpy.data.libraries.write(str(path),{m},fake_user=True)
        meta={'schema_version':1,'id':'materials/warm-vertical-cedar','version':'v002','name':'Warm cedar with physically scaled fine grain','units':'meters','license':'CC-BY-4.0','rights':'Original asset; attribution Homes project contributors','source':{'kind':'original','generator':'tools/garage03/finishes.py'},'files':{'blender':path.name},'dependencies':[],'change_from_v001':'Subtle physical-scale grain and restrained color/roughness; no coarse generated-coordinate mottling.'}
        (folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')

def details(M):
    g.collection('18 Finish detail | joinery and lighting')
    # Façade construction edges, reveals and ground-level warm lighting.
    for x in [2.92,25.08]:box('Garage opening metal jamb',(x,.08,4.5),(.14,.35,9),M['black'],.018)
    box('Garage opening head trim',(14,.08,9.04),(22.3,.35,.14),M['black'],.018)
    for x in [31.95,35.55]:box('Entry door frame',(x,.02,4),(.1,.35,8.1),M['black'],.012)
    box('Entry door header',(33.75,.02,8.03),(3.7,.35,.1),M['black'],.012)
    for x in [31.25,35.9]:
        box('Entry sconce backing',(x,-.29,6.2),(.34,.16,1.4),M['black'],.035)
        box('Entry sconce opal',(x,-.41,6.2),(.2,.1,1.1),M['glow'],.04)
        area('Entry sconce pool',(x,-.65,6),(x,-.8,0),16,1,color=(1,.68,.4))
    # Lettering helps both scale and composition without fictitious site/address.
    font=bpy.data.curves.new('Garage number lettering','FONT');font.body='03';font.size=.46*F;font.extrude=.015*F
    o=bpy.data.objects.new('Garage number',font);g.ACTIVE.objects.link(o);o.location=(29.1*F,-.08*F,5.7*F);o.rotation_euler=(math.pi/2,0,0);font.materials.append(M['black'])
    for x in [1.25,34.75]:
        rod('Concealed-tone rainwater downpipe',(x,33.75,.3),(x,33.75,22.5),.08,M['black'])
    ceiling=material('Smooth warm white ceiling',(.69,.68,.64),.88)
    box('Game room finished ceiling',(18,17,22.48),(35,33,.04),ceiling)
    # Original abstract wall art, layered relief rather than downloaded artwork.
    box('Art slim walnut frame',(13.8,33.29,18.8),(3.6,.12,4.2),M['walnut'],.025)
    box('Art canvas',(13.8,33.2,18.8),(3.35,.035,3.95),M['stone'])
    art=cyl('Art circular field',(13.45,33.17,19.3),.93,.025,M['sage'],64);art.rotation_euler.x=math.pi/2
    box('Art ochre field',(14.35,33.14,18),(1.25,.026,1.6),M['terracotta'])
    # Upper room skirting and discreet perimeter ceiling shadow joint.
    for z,th in [(13.67,.34),(22.33,.05)]:
        box('Rear room trim',(18,33.38,z),(35,.12,th),M['black'],.008)
        box('West room trim',(.61,17,z),(.12,33,th),M['black'],.008)
    # Furniture detailing: individual door reveals and toe kick, refined dark countertop.
    for x in [3.5,5.9,8.35,10.85]:box('Bar door reveal',(x,31.08,15),(.035,.035,2.85),M['black'])
    box('Bar recessed toe kick',(7.2,31.16,13.7),(7.35,.12,.24),M['black'])
    for x in [4.7,7.2,9.7]:box('Bar slim handle',(x,31.07,16.12),(.95,.035,.035),M['black'],.01)
    # Upholstery seams, sofa feet and softer throw cushions.
    for y in [9.4,15.6]:
        for x in [25,26.8]:rod('Sofa slim foot',(x,y,13.5),(x,y,14.4),.055,M['black'])
    for y in [10.25,14.9]:
        o=box('Sofa loose cushion',(26.45,y,15.75),(.5,1.75,1.7),M['fabric'],.28);o.rotation_euler.y=-.18
    for y in [9.5,15.6]:box('Sofa tailored arm',(25.95,y,15.2),(2.6,.28,1.35),M['fabric'],.14)
    # Coffee-table books and a ceramic vessel add a readable human scale.
    for i in range(2):
        o=box('Coffee table art book',(22.5,12.25,14.83+i*.09),(1.0,1.32,.08),M['white'] if i else M['black'],.012);o.rotation_euler.z=i*.13
    cyl('Table ceramic bowl',(21.4,13.5,14.95),.28,.18,M['sage'],48)
    # Refined cue rack and cue tips.
    for z in [15.35,19.25]:box('Cue rack crosspiece',(1.65,33.06,z),(1.4,.19,.12),M['walnut'],.03)
    # Interior architectural light, warm against blue sky.
    for x in [7,19,30]:
        for y in [6,25]:
            cyl('Recessed ceiling downlight',(x,y,22.46),.12,.04,M['black'],32)
            cyl('Downlight luminous aperture',(x,y,22.43),.08,.025,M['glow'],32)
            area('Ceiling downlight',(x,y,22.36),(x,y,13.5),45,.32,color=(1,.79,.57))
    for o in g.ACTIVE.objects:
        if o.type=='MESH':o['ifc_storey']='Game room' if o.location.z>12*F else 'Ground floor'
    # Strip fixtures light the garage without turning it into a white softbox.
    for x in [6.5,21.5]:
        box('Garage linear ceiling fitting',(x,16,11.88),(.3,14,.12),M['black'],.025)
        box('Garage linear diffuser',(x,16,11.81),(.19,13.6,.025),M['glow'],.01)
        area('Garage fixture',(x,16,11.7),(x,16,0),330,11,color=(.89,.93,1),shape='RECTANGLE',size_y=.3)
    g.collection('19 Landscape | designed forecourt')
    gravel=noise_material('Fine basalt gravel',(.06,.065,.058),(.14,.145,.125),95,.91,.007)
    for x in [-3,39.5]:
        box('Garden gravel bed',(x,15,-.03),(4.3,38,.14),gravel,.03)
        for xx in [x-2.2,x+2.2]:box('Garden steel edging',(xx,15,.07),(.035,38,.16),M['black'])
    # Joints across the forecourt are scored, not obstacles in the walking route.
    for y in [-7,-14,-21,-28]:box('Driveway control joint',(14,y,-.015),(26,.045,.02),M['black'])
    box('Driveway trench drain',(14,-1,-.008),(23,.22,.025),M['black'])
    for i in range(120):box('Trench drain grille',(2.55+i*.192,-1,.005),(.035,.2,.016),M['steel'])
    # Native ornamental planting, coarse rocks, and original low bollard lights.
    for i in range(18):
        x=-3.6 if i<9 else 40.5;y=-4+(i%9)*4.2
        grasses('Fine ornamental grass',x,y,1.9,M['leaves'],400+i)
        if i%3==0:rock('Garden basalt',x+.5,y+1.5,.8,M['concrete'],200+i)
    for x in [-1,37.8]:
        for y in [-3,10,24]:
            box('Garden bollard',(x,y,1.4),(.25,.25,2.8),M['black'],.035)
            box('Bollard light aperture',(x,y-.14,2.4),(.19,.025,.35),M['glow'],.012)
            area('Bollard pool',(x,y-.3,2.4),(x,y-1.4,0),7,.3,color=(1,.68,.39))

def smooth_upholstery():
    """Soften close-view upholstery without changing its circulation envelope."""
    for o in bpy.data.objects:
        if o.type=='MESH' and any(k in o.name for k in ['Lounge sofa','Sofa loose cushion','Sofa tailored arm']):
            for mod in o.modifiers:
                if mod.type=='BEVEL':mod.segments=8;mod.harden_normals=True
            for poly in o.data.polygons:poly.use_smooth=True
