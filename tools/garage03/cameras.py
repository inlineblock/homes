"""Garage gallery cameras; authoring positions and targets are in feet."""
from design import UPPER_FLOOR

VIEWS = [
    ('01 Exterior','01-exterior',(57,-65,24),(18,10,10),45),
    ('02 Game room','02-game-room',(26.2,2.6,UPPER_FLOOR+5.8),(14,18,UPPER_FLOOR+2.5),22),
    ('03 Garage stored','03-garage-stored',(14,-19,5),(14,14,-1.2),25),
    ('04 Pit section','04-pit-section',(56,-53,24),(17,11,5),43),
    ('05 Raised retrieval','05-raised-retrieval',(14,-22,9),(14,12,3),25),
    ('06 Circulation','06-circulation',(39,-19,28),(19,10,0),38),
    ('07 Rear garden','07-rear-garden',(-18,89,32),(17,20,10.5),44),
    ('08 Elevated approach','08-elevated-approach',(-60,-55,68),(18,13,10),46),
]


def add_cameras(only_missing=False):
    import bpy
    from common.geometry import camera
    for name, filename, loc, target, lens in VIEWS:
        if name in bpy.data.objects:
            if only_missing:
                continue
            raise ValueError('Camera already exists: '+name)
        obj=camera(name,loc,target,lens)
        if filename=='08-elevated-approach':
            obj.data.type='ORTHO';obj.data.ortho_scale=76*.3048
