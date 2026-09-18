"""Coastal House: all authoring dimensions in feet, conceptual site only."""
SLUG='coastal-house'
WIDTH,DEPTH=68,40
AREA=WIDTH*DEPTH
HEIGHT=10.5
DOOR={'start':10.,'end':40.,'panels':6,'pocket_center':7.30,'head':9.5,'sill':.08,'track_y':40.0,'pitch':.15}
WINDOW={'start':48.,'end':60.,'panels':4,'pocket_center':61.60,'head':8.5,'sill':3.18,'track_y':40.0,'pitch':.13}
# Wall centerlines and door apertures measured from each segment's start.
WALLS=[
 ('Primary east',(18,0),(18,24),[(11.5,3.3)]),
 ('Primary bath front',(0,16),(18,16),[(4,3),(12,3)]),
 ('Bath closet partition',(10,16),(10,24),[]),
 ('Primary service rear',(0,24),(18,24),[]),
 ('Entry east',(22,0),(22,16),[]),
 ('Bedroom divider',(39,0),(39,16),[]),
 ('Guest bedrooms hall',(22,16),(56,16),[(3,3.3),(21,3.3)]),
 ('Guest bedroom east',(56,0),(56,16),[]),
 ('Guest service west',(60,0),(60,16),[(.6,3.3),(10,3.3)]),
 ('Guest service divider',(60,8),(68,8),[]),
]
ROOMS=[('PRIMARY BEDROOM',0,0,18,16),('PRIMARY BATH',0,16,10,24),('DRESSING',10,16,18,24),('BEDROOM 02',22,0,39,16),('BEDROOM 03',39,0,56,16),('BATH 02',60,0,68,8),('LAUNDRY',60,8,68,16),('LIVING',0,24,28,40),('DINING',28,21,44,40),('KITCHEN',44,21,68,40)]
VIEWS=[('01 Terrace open','01-terrace-open',120),('02 Great room','02-great-room',120),('03 Serving counter','03-serving-counter-open',120),('04 Serving closed','04-serving-counter-closed',1),('05 Terrace closed','05-terrace-closed',1)]
