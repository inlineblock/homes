"""Measured planning geometry in feet. Exterior-led interpretation of the reference."""
WIDTH,DEPTH=62,48
ATRIUM=(19,8,43,32)
AREA=WIDTH*DEPTH-24*24
SLABS=[(0,0,62,8),(0,8,19,32),(43,8,62,32),(0,32,62,48)]
ROOMS=[
 ('bedroom-3',(0,0,15,14),'BEDROOM 03'),
 ('bath-2',(0,14,9,22),'BATH 02'),
 ('bath-3',(9,14,15,22),'BATH 03'),
 ('bedroom-2',(0,22,15,36),'BEDROOM 02'),
 ('utility',(0,36,15,48),'LAUNDRY / FLEX'),
 ('west-gallery',(15,0,19,36),'GALLERY'),
 ('primary',(47,0,62,24),'PRIMARY SUITE'),
 ('primary-bath',(47,24,55,32),'PRIMARY BATH'),
 ('dressing',(55,24,62,32),'DRESSING'),
 ('east-gallery',(43,0,47,32),'GALLERY'),
 ('entry',(19,0,43,8),'GLAZED ENTRY'),
 ('living',(15,32,29,48),'LIVING'),
 ('dining',(29,32,39,48),'DINING'),
 ('kitchen',(39,32,54,48),'KITCHEN'),
 ('pantry',(54,32,62,48),'PANTRY / STORAGE'),
]
# Interior walls with doorway offsets along each segment.
WALLS=[
 ('west-gallery',(15,0),(15,36),[(4,3),(17,3),(27,3)]),
 ('bed3-bath',(0,14),(15,14),[(3,3)]),
 ('bath-divide',(9,14),(9,22),[]),
 ('bed2-bath',(0,22),(15,22),[]),
 ('bed2-utility',(0,36),(15,36),[]),
 ('utility-east',(15,36),(15,48),[(3,3)]),
 ('east-gallery',(47,0),(47,32),[(12,3)]),
 ('suite-services',(47,24),(62,24),[(2,3),(10,3)]),
 ('ensuite-closet',(55,24),(55,32),[]),
 ('suite-north',(47,32),(62,32),[]),
 ('pantry-west',(54,32),(54,48),[(1.5,3)]),
]
# Keep plaster partitions within the exterior timber skin.
WALLS=[(name,(min(61.6,max(.4,a[0])),min(47.6,max(.4,a[1]))),(min(61.6,max(.4,b[0])),min(47.6,max(.4,b[1]))),opens) for name,a,b,opens in WALLS]
def roof_height(x):
    if x<=19:return 9.7+3.3*x/19
    if x>=43:return 13-3.3*(x-43)/19
    return 16-abs(x-31)/4
