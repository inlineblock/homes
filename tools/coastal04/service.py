"""Everyday household storage and explicitly unengineered service allowance."""
import bpy,math
from common.geometry import box,collection,F
from common.architecture import interior_wall
from common.shared_assets import place

def household(M,shared):
    collection('04 Furnishings | entry and linen storage')
    place('Entry coat storage',shared['wardrobe'],(24.8,10.9,0),rotation=-math.pi/2)
    # A shallow drop shelf does not narrow the checked walking centerline.
    box('Entry keys drop shelf',(18.48,6.0,3.2),(.55,2.6,.14),M['oak'],.025)
    box('Entry drop tray',(18.48,6.0,3.31),(.36,.8,.06),M['stone'],.012)
    # Laundry has a clear central access zone; linen occupies its east wall.
    place('Laundry linen storage',shared['wardrobe'],(66.65,12.0,0),rotation=-math.pi/2)
    for z in [2.0,3.5,5.0,6.5]:box('Linen cabinet shelf insert',(66.65,12.0,z),(1.8,1.8,.055),M['oak'],.005)
    # Dedicated refuse/recycling pullout on the island work side, away from seating.
    collection('03 Kitchen | waste storage')
    for x in [49.8,50.65]:
        box('Kitchen waste recycling bin',(x,30.1,1.1),(.72,1.4,1.75),M['dark'],.065)
    box('Kitchen waste pullout cabinet front',(50.22,30.83,1.52),(1.85,.06,2.62),M['oak'],.018)
    collection('01 Architecture | mechanical service allowance')
    interior_wall('Service closet west',(63,16),(63,21),[(1.0,3.0)],M['plaster'],10.4)
    interior_wall('Service closet rear',(63,21),(68,21),[],M['plaster'],10.4)
    o=box('Service allowance door open',(64.45,17.10,3.75),(2.8,.12,7.5),M['oak'],.02);o['ifc_class']='IfcDoor'
    o=box('Reserved MEP equipment and maintenance allowance',(65.4,19.0,4.0),(4,3.3,8.0),M['dark']);o.display_type='WIRE';o.hide_render=True;o['ifc_class']='IfcBuildingElementProxy';o['scope']='Unengineered equipment and maintenance reservation; exact plant, ventilation and clearances unresolved.'
