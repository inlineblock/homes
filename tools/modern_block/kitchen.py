"""Install the shared concealed-kitchen kit within the existing room envelope."""
import math
from pathlib import Path
import bpy
from common import geometry as g
import design as d
import kitchen_layout as k


def build_kitchen(root, asset, box, area, plan):
    root = Path(root)
    def material(slug):
        path = root/'library/materials'/slug/'v001'/f'{slug}.blend'
        with bpy.data.libraries.load(str(path), link=True) as (source, target):
            target.materials = [source.materials[0]]
        return target.materials[0]
    cream = material('cream-cabinet-enamel')
    hood_finish = material('warm-limestone-plaster')
    stone = material('cream-veined-stone')
    oak = material('coastal-white-oak')
    dark = material('charcoal-facade-panel')
    def put(category, slug, name, xyz, rotation=0):
        return asset(category, slug, name, xyz, rotation)
    def cabinet(slug, name, x, y, z=d.GROUND, rotation=0):
        return put('cabinetry', slug, name, (x,y,z), rotation)
    def top(name, rectangle, hole=None):
        x0,y0,x1,y1=rectangle
        if hole:
            a,b,c,e=hole
            regions=[(x0,y0,a,y1),(c,y0,x1,y1),(a,y0,c,b),(a,e,c,y1)]
        else:
            regions=[rectangle]
        for i,(a,b,c,e) in enumerate(regions):
            if c>a and e>b:
                box(f'{name} stone {i+1}', ((a+c)/2,(b+e)/2,d.GROUND+k.COUNTER_TOP-k.COUNTER_THICKNESS/2),
                    (c-a,e-b,k.COUNTER_THICKNESS),stone,.003)

    g.collection('Interior | concealed kitchen')
    # The cleaning zone sits beneath the existing north window. Each dishwasher
    # is a real independent opening cavity, not a bank of solid drawer meshes.
    cabinet('cream-inset-sink-base-36in','Kitchen cream sink base',k.SINK[0],k.WALL_RUN_Y)
    put('fixtures','kitchen-sink-bridge-faucet-brass-650','Kitchen bridge sink',
        (k.SINK[0],k.SINK[1],d.GROUND+k.COUNTER_TOP))
    for i,x in enumerate(k.DISHWASHERS,1):
        put('appliances','cream-inset-dishwasher-24in',f'Kitchen concealed dishwasher {i}',(x,k.WALL_RUN_Y,d.GROUND))
    top('Kitchen cleanup counter',(10.23,19.075,12.558,19.82),
        (k.SINK[0]-.332,k.SINK[1]-.232,k.SINK[0]+.332,k.SINK[1]+.232))
    cabinet('cream-inset-drawer-base-24in','Kitchen refrigeration landing drawers',k.LANDING_DRAWER_X,k.WALL_RUN_Y)
    top('Kitchen refrigeration landing',(13.802,19.075,14.437,19.82))
    # A thin noncombustible finish reservation leaves the range's rear service
    # allowance intact. Final lining material and heat/glazing details await
    # the actual appliance specification.
    box('Kitchen cleanup stone-look lining',(11.394,19.867,d.GROUND+1.14),(2.328,.006,.4438),stone,.001)
    box('Kitchen range stone-look lining',(k.RANGE_X,19.867,d.GROUND+1.35),(1.2192,.006,.86),stone,.001)
    box('Kitchen landing stone-look lining',(14.127,19.867,d.GROUND+1.14),(.650,.006,.4438),stone,.001)
    put('appliances','cream-brass-dual-fuel-range-48in','Kitchen cream brass range',(k.RANGE_X,k.WALL_RUN_Y,d.GROUND))
    put('appliances','cream-plaster-wall-hood-48in','Kitchen cream capture hood',(k.RANGE_X,k.WALL_RUN_Y,d.GROUND+k.HOOD_BOTTOM))
    duct_bottom=d.GROUND+k.HOOD_BOTTOM+.90
    duct_top=d.GROUND_ROOF_Z+.35
    box('Kitchen hood exhaust to roof',(k.RANGE_X,k.WALL_RUN_Y+.16,(duct_bottom+duct_top)/2),(.254,.254,duct_top-duct_bottom),dark)
    chase_bottom=d.GROUND+k.HOOD_BOTTOM+.94
    chase_top=d.GROUND+d.GROUND_CLEAR
    for dx,dy,w,depth in [(-.21,0,.02,.40),(.21,0,.02,.40),(0,-.19,.40,.02),(0,.19,.40,.02)]:
        box('Kitchen cream hood service chase',(k.RANGE_X+dx,k.WALL_RUN_Y+.16+dy,(chase_bottom+chase_top)/2),
            (w,depth,chase_top-chase_bottom),hood_finish,.003)
    # Narrow fitted end strips close dimensional gaps; all full modules remain
    # rigid linked assets. Fillers do not extend across any appliance opening.
    for i,(a,b) in enumerate([(10.15,10.249),(10.871,10.877),(11.803,11.829),(12.451,12.558),(13.802,13.814),(14.436,14.449)]):
        box(f'Kitchen fitted perimeter filler {i}',((a+b)/2,19.155,d.GROUND+.49),(b-a,.03,.78),cream,.001)
    put('appliances','cream-inset-fridge-freezer-48in','Kitchen concealed refrigeration',(k.FRIDGE[0],k.FRIDGE[1],d.GROUND))
    # Hinge relief stays open in front of the hinge. The shallow upper display
    # is above the appliance; it cannot seal its separate condenser intake.
    cabinet('cream-inset-glazed-upper-36in','Kitchen refrigerator glazed display',k.FRIDGE[0],19.58,d.GROUND+2.24)
    for xx in [14.405,15.735]:
        box('Kitchen refrigerator rear niche cheek',(xx,19.68,d.GROUND+1.12),(.035,.30,2.24),cream,.002)
    box('Kitchen refrigerator display shelf',(k.FRIDGE[0],19.58,d.GROUND+2.22),(1.365,.3556,.04),cream,.004)
    box('Kitchen refrigerator display apron',(k.FRIDGE[0],19.413,d.GROUND+2.17),(1.365,.02,.06),cream,.002)
    for xx in [14.49-.015,15.67-.015]:
        box('Kitchen upper display fitted side',(xx,19.58,d.GROUND+2.62),(.235,.3556,.76),cream,.003)

    # Freestanding island: three drawer stacks, microwave and waste module.
    top('Kitchen island',k.ISLAND)
    cursor=14.22
    modules=[('oak-inset-drawer-base-24in',.6096,'south drawers'),
             ('oak-inset-microwave-base-24in',.6604,'microwave housing'),
             ('oak-inset-drawer-base-24in',.6096,'prep drawers'),
             ('oak-inset-waste-pullout-18in',.4572,'waste and recycling'),
             ('oak-inset-drawer-base-24in',.6096,'north drawers')]
    for slug,width,label in modules:
        yy=cursor+width/2
        cabinet(slug,'Kitchen island '+label,k.ISLAND_CORE_X,yy,rotation=math.pi/2)
        if 'microwave-base' in slug:
            put('appliances','microwave-drawer-24in','Kitchen island microwave',(k.ISLAND_CORE_X,yy,d.GROUND+.447),math.pi/2)
        cursor+=width
    for yy,depth in [(14.11,.22),((cursor+17.4)/2,17.4-cursor)]:
        box('Kitchen island fitted end closure',(13.475,yy,d.GROUND+.44),(.61,depth,.88),oak,.003)
    for yy in [14.025,17.375]:
        box('Kitchen island fitted return',(13.315,yy,d.GROUND+.44),(1.035,.05,.88),oak,.003)
    for i in range(5):
        cabinet('oak-inset-island-back-panel-24in','Kitchen island seating panel',12.80,14.176+i*.6096,rotation=-math.pi/2)
    for yy,depth in [(14.022,.044),(17.246,.308)]:
        box('Kitchen island fitted seating end',(12.80,yy,d.GROUND+.44),(.035,depth,.88),oak,.002)
    for yy in k.STOOL_Y:
        put('furniture','coastal-oak-counter-stool','Kitchen oak stool',(12.0,yy,d.GROUND+.02),math.pi/2)
    for yy in [14.86,16.52]:
        put('fixtures','lighting-brass-double-shade-pendant','Kitchen shaded island pendant',(13.10,yy,d.GROUND+d.GROUND_CLEAR),math.pi/2)
        area('Kitchen pendant warm pool',(13.10,yy,d.GROUND+d.GROUND_CLEAR-1.36),(13.1,yy,d.GROUND+.90),65,.8)
    put('fixtures','lighting-brass-picture-light-24in','Kitchen window picture light',(11.5,19.858,d.GROUND+3.23))
    # Mount on solid wall, clear of the existing window and range hood.
    put('fixtures','lighting-brass-shaded-sconce','Kitchen cleanup sconce',(10.32,19.858,d.GROUND+2.18))
    area('Kitchen cleanup task light',(11.3,19.25,d.GROUND+2.5),(11.3,19.42,d.GROUND+.91),75,1.4)
    # Pantry pieces retain a separate storage role and a usable counter. The
    # garage door state is demonstrated in its dedicated view.
    cabinet('cream-inset-drawer-base-24in','Pantry appliance garage base west',16.59,15.50)
    cabinet('cream-inset-drawer-base-24in','Pantry appliance garage base east',17.1996,15.50)
    top('Pantry appliance garage counter',(16.2652,15.14,17.5244,15.84))
    cabinet('cream-inset-appliance-garage-48in','Pantry appliance garage',16.8948,15.49,d.GROUND+k.COUNTER_TOP)
    cabinet('cream-inset-pantry-36in','Pantry enclosed food storage',18.21,15.50)
    put('fixtures','lighting-undercabinet-bar-4ft','Pantry task bar',(16.8948,15.20,d.GROUND+1.87))
    area('Pantry garage task illumination',(16.8948,15.12,d.GROUND+1.88),(16.8948,15.52,d.GROUND+1.1),45,.85)
    area('Pantry ceiling illumination',(17.35,14.20,d.GROUND+3.1),(17.35,15.5,d.GROUND+1.25),190,1.5)
    # Counter outline is recorded as actual modeled host geometry for drawings.
    x0,y0,x1,y1=k.ISLAND
    plan.append({'name':'Kitchen island countertop','level':'ground','kind':'counter',
                 'polygon':[[x0,y0],[x1,y0],[x1,y1],[x0,y1]],'color':'#eee7dc'})
