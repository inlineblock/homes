"""Coastal House: all authoring dimensions in feet, conceptual site only."""
SLUG='coastal-house'
WIDTH,DEPTH=68,40
AREA=WIDTH*DEPTH
HEIGHT=10.5
DOOR={'start':10.,'end':40.,'panels':6,'pocket_center':7.30,'head':9.5,'sill':.08,'track_y':40.0,'pitch':.15}
WINDOW={'start':48.,'end':60.,'panels':4,'pocket_center':61.60,'head':8.5,'sill':3.18,'track_y':40.0,'pitch':.13}
# Wall centerlines and door apertures measured from each segment's start.
WALLS=[
 ('Primary east',(18,0),(18,26),[(8.5,3.3)]),
 ('Primary bath front',(0,12),(18,12),[(8,3.3)]),
 ('Bath closet partition',(6,12),(6,18),[(.5,3)]),
 ('Dressing rear',(0,18),(6,18),[]),
 ('Primary WC west',(14,12),(14,18),[(.35,3)]),
 ('Primary WC rear',(14,18),(18,18),[]),
 ('Primary service rear',(0,26),(18,26),[]),
 ('Entry east',(26,0),(26,12),[(5.4,3.3)]),
 ('Bedroom divider',(41,0),(41,16),[]),
 ('Bedroom 02 rear',(26,12),(41,12),[]),
 ('Guest bedrooms hall',(41,16),(56,16),[(2,3.3)]),
 ('Guest bedroom east',(56,0),(56,16),[]),
 ('Guest service west',(60,0),(60,16),[(.6,3.3),(10,3.3)]),
 ('Guest service divider',(60,8),(68,8),[]),
]
ROOMS=[('PRIMARY BEDROOM',0,0,18,12),('PRIMARY BATH',6,12,18,26),('DRESSING',0,12,6,18),('BEDROOM 02',26,0,41,12),('BEDROOM 03',41,0,56,16),('BATH 02',60,0,68,8),('LAUNDRY',60,8,68,16),('LIVING',0,26,28,40),('DINING',28,21,44,40),('KITCHEN',44,21,68,40)]
VIEWS=[('01 Terrace open','01-terrace-open',120),('02 Great room','02-great-room',120),('03 Serving counter','03-serving-counter-open',120),('04 Serving closed','04-serving-counter-closed',1),('05 Terrace closed','05-terrace-closed',1),('06 Front arrival','06-front-arrival',120),('07 Roof and parking','07-roof-and-parking',120),('08 West garden','08-west-garden',120),('09 Entry hall','09-entry-hall',120),('10 Primary bath','10-primary-bath',120),('11 Living retreat','11-living-retreat',120),('12 Vaulted living','12-vaulted-living',120),('13 Kitchen to vault','13-kitchen-to-vault',120)]

BEDS=[("Primary",6,5.5,6.5),("Guest 02",33.1,4.75,5),("Guest 03",47.5,6.7,5)]

# Conversation area: feet, floor origin; furnishings face +Y before rotation.
OUTDOOR_LOUNGE=[
 ('Shared west terrace sofa','coastal-outdoor-sofa',(4.5,51.5,0),-90),
 ('Shared west terrace lounge chair left','coastal-outdoor-lounge-chair',(15.5,47.75,0),65),
 ('Shared west terrace lounge chair right','coastal-outdoor-lounge-chair',(15.5,55.25,0),115),
 ('Shared west terrace coffee table','oak-rounded-coffee-table',(10,51.5,0),0),
]
