"""Room-side electric fireplace; preserves the independently serviced glass pocket.

All dimensions below are feet. Electrical/thermal installation is unselected.
"""
ASSET='fixtures/slim-electric-fireplace-48in'
X1,X2=4.525,9.98
FRONT,BACK=38.35,39.35
HEARTH_FRONT=38.30
INSERT_FRONT=38.335
INSERT_BOTTOM=1.15
INSERT_WIDTH,INSERT_HEIGHT,INSERT_DEPTH=4.,1.5,.65
TOP=3.15

def build(root,M):
    from common.geometry import box, collection
    from common.library import linked_collection, instance
    collection('01 Architecture | living fireplace')
    center=(X1+X2)/2;w=X2-X1
    def stone(name,loc,size):
        o=box('Living fireplace '+name,loc,size,M['stone'],.012);o['ifc_class']='IfcBuildingElementProxy';o['fireplace_surround']=True
        return o
    stone('low hearth',(center,(HEARTH_FRONT+BACK)/2,.075),(w,BACK-HEARTH_FRONT,.15))
    stone('plinth',(center,(FRONT+BACK)/2,(.15+INSERT_BOTTOM)/2),(w,BACK-FRONT,INSERT_BOTTOM-.15))
    jamb=(w-INSERT_WIDTH-.04)/2
    for x in [X1+jamb/2,X2-jamb/2]:
        stone('side jamb',(x,(FRONT+BACK)/2,(INSERT_BOTTOM+INSERT_BOTTOM+INSERT_HEIGHT)/2),(jamb,BACK-FRONT,INSERT_HEIGHT))
    stone('mantel',(center,(FRONT+BACK)/2,(INSERT_BOTTOM+INSERT_HEIGHT+TOP)/2),(w,BACK-FRONT,TOP-INSERT_BOTTOM-INSERT_HEIGHT))
    asset=linked_collection(root,'fixtures','slim-electric-fireplace-48in','v001')
    o=instance('Living shared electric fireplace',asset,(center,INSERT_FRONT,INSERT_BOTTOM))
    o['ifc_class']='IfcBuildingElementProxy'
    o['export_linked_geometry']=True
    o['concept_type']='Electric; front-service; no combustion flue'
    o['installation_limits']='Original concept, final product/electrical/thermal clearances unselected'
    # Space behind the case remains empty. Front-access electrical reservation
    # stays wholly on the room side of the moving-panel pocket.
    o['rear_service_gap_ft']=BACK-(INSERT_FRONT+INSERT_DEPTH)
    o['front_service_depth_ft']=3.
    return o

def dependency():return {'id':ASSET,'version':'v001','path':'../../library/'+ASSET+'/v001/'}
