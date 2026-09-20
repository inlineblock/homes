"""Solid west living wall and room-facing electric fireplace. Dimensions in feet."""
ASSET='fixtures/slim-electric-fireplace-48in'
WALL_Y1,WALL_Y2=26.2,39.375
WALL_DEPTH=.8
CENTER_Y=32.2
from roof_design import ceiling_height
WALL_HEIGHT=ceiling_height(WALL_DEPTH,CENTER_Y)+.02
WIDTH=6.
Y1,Y2=CENTER_Y-WIDTH/2,CENTER_Y+WIDTH/2
BACK,FRONT=.83,1.83
HEARTH_FRONT=1.88
INSERT_FRONT=1.845
INSERT_BOTTOM=1.15
INSERT_WIDTH,INSERT_HEIGHT,INSERT_DEPTH=4.,1.5,.65
TOP=3.15

def fit_wall_top(obj):
    """Continue the solid wall to the actual sloping ceiling without a ledge."""
    from common.geometry import F
    for v in obj.data.vertices:
        if v.co.z>0:
            x=(obj.location.x+v.co.x)/F
            v.co.z=(ceiling_height(x,CENTER_Y)+.02)*F-obj.location.z
    obj.data.update()

def build(root,M):
    import math
    from common.geometry import box, collection
    from common.library import linked_collection, instance
    collection('01 Architecture | living fireplace')
    def stone(name,loc,size):
        o=box('Living fireplace '+name,loc,size,M['stone'],.012)
        o['ifc_class']='IfcBuildingElementProxy';o['fireplace_surround']=True
        return o
    stone('low hearth',((HEARTH_FRONT+BACK)/2,CENTER_Y,.075),(HEARTH_FRONT-BACK,WIDTH,.15))
    stone('plinth',((FRONT+BACK)/2,CENTER_Y,(.15+INSERT_BOTTOM)/2),(FRONT-BACK,WIDTH,INSERT_BOTTOM-.15))
    jamb=(WIDTH-INSERT_WIDTH-.04)/2
    for y in [Y1+jamb/2,Y2-jamb/2]:
        stone('side jamb',((FRONT+BACK)/2,y,INSERT_BOTTOM+INSERT_HEIGHT/2),(FRONT-BACK,jamb,INSERT_HEIGHT))
    stone('mantel',((FRONT+BACK)/2,CENTER_Y,(INSERT_BOTTOM+INSERT_HEIGHT+TOP)/2),(FRONT-BACK,WIDTH,TOP-INSERT_BOTTOM-INSERT_HEIGHT))
    asset=linked_collection(root,'fixtures','slim-electric-fireplace-48in','v001')
    o=instance('Living shared electric fireplace',asset,(INSERT_FRONT,CENTER_Y,INSERT_BOTTOM),math.pi/2)
    o['ifc_class']='IfcBuildingElementProxy';o['export_linked_geometry']=True
    o['concept_type']='Electric; front-service; no combustion flue'
    o['installation_limits']='Original concept, final product/electrical/thermal clearances unselected'
    o['rear_service_gap_ft']=INSERT_FRONT-INSERT_DEPTH-BACK
    o['front_service_depth_ft']=3.
    return o

def dependency():return {'id':ASSET,'version':'v001','path':'../../library/'+ASSET+'/v001/'}
