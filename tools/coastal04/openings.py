"""Paired opening systems: editable panels animate into concealed side pockets."""
import bpy
from common.geometry import box,rod,F
from design import DOOR,WINDOW

def sliding(name,spec,M):
    width=(spec['end']-spec['start'])/spec['panels'];h=spec['head']-spec['sill'];z=(spec['head']+spec['sill'])/2
    for i in range(spec['panels']):
        closed=spec['start']+(i+.5)*width;y=spec['track_y']+(i-(spec['panels']-1)/2)*spec['pitch']
        parts=[]
        parts.append(box(name+' panel %02d glazing'%(i+1),(closed,y,z),(width-.14,.024,h-.17),M['glass']))
        for dx in [-width/2+.045,width/2-.045]:parts.append(box(name+' vertical stile',(closed+dx,y,z),(.09,.095,h),M['bronze'],.012))
        for zz in [spec['sill']+.045,spec['head']-.045]:parts.append(box(name+' horizontal rail',(closed,y,zz),(width,.12,.09),M['bronze'],.012))
        parts.append(rod(name+' recessed pull',(closed+width/2-.14,y-.09,z-.45),(closed+width/2-.14,y-.09,z+.45),.022,M['dark']))
        for o in parts:
            o['opening_system']=name;o['panel_index']=i;o['closed_x_ft']=o.location.x/F;o['open_x_ft']=o.location.x/F+spec['pocket_center']-closed
            o['ifc_class']='IfcDoor' if name=='Great room' else 'IfcWindow'
            o.keyframe_insert(data_path='location',frame=1);o.location.x=o['open_x_ft']*F;o.keyframe_insert(data_path='location',frame=120)
            if o.animation_data:
                for fc in o.animation_data.action.fcurves:
                    for k in fc.keyframe_points:k.interpolation='LINEAR'
    # Tracks continue into pocket; pockets are an actual cavity, not solid intersecting walls.
    a=min(spec['start'],spec['pocket_center']-width/2-.1);b=max(spec['end'],spec['pocket_center']+width/2+.1)
    for i in range(spec['panels']):
        y=spec['track_y']+(i-(spec['panels']-1)/2)*spec['pitch']
        for zz in [spec['sill']-.03,spec['head']+.025]:box(name+' continuous track',((a+b)/2,y,zz),(b-a,.028,.035),M['bronze'],.004)
    fixed_end=spec['end'] if spec['pocket_center']<spec['start'] else spec['start']
    box(name+' end jamb',(fixed_end,40,z),(.12,.94,h+.15),M['bronze'],.015)
    box(name+' header',((a+b)/2,40,spec['head']+.10),(b-a,.98,.17),M['bronze'],.015)
