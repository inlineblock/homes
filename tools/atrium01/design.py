"""Single measured source for the Atrium 01 architectural concept (feet)."""
FT = 0.3048
WIDTH, DEPTH, HEIGHT = 60, 44, 9
ATRIUM = (22, 10, 38, 25)
GROSS_AREA = WIDTH * DEPTH - (ATRIUM[2]-ATRIUM[0])*(ATRIUM[3]-ATRIUM[1])
# name, rectangle, display label. Rectangles describe design zones, not net area surveys.
ROOMS = [
 ('bedroom-2',(0,0,18,12),'BEDROOM 02'),
 ('bath-2',(8,12,18,20),'BATH 02'),
 ('wardrobe',(0,12,8,20),'STORAGE'),
 ('bedroom-3',(0,20,18,30),'BEDROOM 03'),
 ('primary',(0,30,18,44),'PRIMARY BEDROOM'),
 ('primary-bath',(18,34,28,44),'PRIMARY BATH'),
 ('closet',(22,28,28,34),'DRESSING'),
 ('hall',(18,0,22,34),'GALLERY'),
 ('bath-3',(22,0,30,8),'BATH 03'),
 ('entry',(30,0,38,10),'ENTRY'),
 ('pantry',(38,0,44,8),'PANTRY / LAUNDRY'),
 ('kitchen',(44,0,60,21),'KITCHEN'),
 ('dining',(38,21,60,31),'DINING'),
 ('living',(28,31,60,44),'LIVING'),
]
# Wall: name, endpoints, thickness, openings along wall: offset, width, sill, head, type.
WALLS = [
 ('south',(0,0),(60,0),.5,[(3,12,2.8,8.5,'window'),(31,5,0,8.5,'entry'),(45,13,6.8,8.7,'window')]),
 ('west',(0,0),(0,44),.5,[(3,7,2.8,8.5,'window'),(22,6,2.8,8.5,'window'),(33,9,.5,8.5,'window')]),
 ('north',(0,44),(60,44),.5,[(2,14,.5,8.5,'window'),(20,6,6,8.5,'window'),(29,29,.1,8.7,'glass')]),
 ('east',(60,0),(60,44),.5,[(11,31,.1,8.7,'glass')]),
 ('bedroom-gallery',(18,0),(18,44),.35,[(3.5,3,0,7.5,'door'),(14,3,0,7.5,'door'),(24,3,0,7.5,'door'),(30.5,3,0,7.5,'door'),(37,3,0,7.5,'door')]),
 ('bedroom-2-north',(0,12),(18,12),.35,[(2,4,0,7.5,'door')]),
 ('bedroom-3-south',(0,20),(18,20),.35,[]),
 ('bedroom-3-north',(0,30),(18,30),.35,[]),
 ('bath-2-west',(8,12),(8,20),.35,[]),
 ('ensuite-south',(18,34),(28,34),.35,[]),
 ('ensuite-east',(28,34),(28,44),.35,[]),
 ('closet-east',(28,28),(28,34),.35,[]),
 ('closet-south',(22,28),(28,28),.35,[]),
 ('closet-west',(22,28),(22,34),.35,[(1.3,3.2,0,7.5,'door')]),
 ('entry-bath-west',(22,0),(22,10),.35,[]),
 ('entry-bath-east',(30,0),(30,8),.35,[(3.5,3,0,7.5,'door')]),
 ('entry-bath-north',(22,8),(30,8),.35,[]),
 ('pantry-west',(38,0),(38,10),.35,[]),
 ('pantry-east',(44,0),(44,8),.35,[(3,3,0,7.5,'door')]),
 ('pantry-north',(38,8),(44,8),.35,[]),
]
COURTYARD_GLAZING = [
 ('atrium-west',(22,10),(22,25)), ('atrium-east',(38,10),(38,25)),
 ('atrium-south',(22,10),(38,10)), ('atrium-north',(22,25),(38,25)),
]
SLABS = [(0,0,60,10),(0,10,22,25),(38,10,60,25),(0,25,60,44)]
CAMERAS = {
 '01 Kitchen hero': ((39.6,21.2,5.6),(52.5,7.8,4.0),27),
 '02 Kitchen courtyard': ((57.2,18.5,5.5),(40,9.8,4.0),25),
 '03 Atrium exterior': ((84,-37,26),(29,20,2.5),39),
 '04 Whole-home cutaway': ((87,-61,92),(30,22,0),45),
}
