"""Twin Gables dimensioned concept; feet at UI boundary, meters in Blender."""
SLUG='eichler-twin-gables'
WIDTH,DEPTH=68.,60.
COURT=(24.,6.,44.,42.)
AREA=WIDTH*DEPTH-(COURT[2]-COURT[0])*(COURT[3]-COURT[1])
EAVE,RIDGE=12.9,18.5
CEILING_EAVE,CEILING_RIDGE=12.2,17.8
FLAT_HEIGHT=10.
ROOMS=[
 ('Primary suite west',(0,0,20,15),'vault'),('West dressing',(0,15,8,28),10),('West ensuite',(8,15,20,28),10),
 ('Primary suite east',(48,0,68,15),'vault'),('East dressing',(48,15,56,28),10),('East ensuite',(56,15,68,28),10),
 ('Office / guest',(0,28,20,42),10),('Guest bath',(13,28,20,36),10),
 ('Laundry',(48,28,58,42),10),('Pantry',(58,32,68,42),10),('Mechanical',(58,28,68,32),10),
 ('West gallery',(20,0,24,42),10),('East gallery',(44,0,48,42),10),
 ('Entry',(24,0,44,6),12),('Living',(0,42,24,60),'vault'),('Dining',(24,42,44,60),12),('Kitchen',(44,42,68,60),'vault')]
WALLS=[
 ('West gallery partition',(19.75,.25),(19.75,42),[(7.75,3),(29.75,3),(37.75,3)]),
 ('East gallery partition',(48.25,.25),(48.25,42),[(7.75,3),(33.75,3)]),
 ('West bedroom services',(0,15),(19.75,15),[(2.5,3),(10.5,3)]),
 ('East bedroom services',(48.25,15),(68,15),[(2.6,3),(10.25,3)]),
 ('West dressing bath',(8,15),(8,28),[]),('East dressing bath',(56,15),(56,28),[]),
 ('West suite office',(0,28),(19.75,28),[]),('East suite utility',(48.25,28),(68,28),[]),
 ('Office guestbath west',(13,28),(13,36),[]),('Office guestbath north',(13,36),(19.75,36),[]),
 ('Office living',(0,42),(19.75,42),[]),('Laundry pantry',(58,28),(58,42),[(.5,3)]),
 ('Pantry mechanical access',(58,32),(68,32),[(1,8)]),('Pantry kitchen',(48.25,42),(68,42),[(14.35,3)]),
]
# Room labels are gross planning bounds; Office/guest excludes the56sqft hallbath.
VIEWS={
 '01-front':((34,-99,14),(34,18,7),45),
 '02-rear':((34,153,20),(34,40,7),45),
 '03-side':((-72,22,8),(14,29,7),40),
 '04-living':((3.5,44.5,5.5),(31,55,6.7),21),
 '05-kitchen':((53,56.8,6),(64,48,4.7),18),
 '06-courtyard':((40.7,9,5.5),(29,35,6),24),
 '07-primary':((17,12.5,5.5),(7,5,6),24),
 '08-primary-bath':((16.5,21.8,5.5),(10,18,4.4),18),
 '09-rear-terrace':((77,81,10),(30,53,7),36),
 '11-east-primary':((50.5,12.5,5.5),(62,5,6),24),
 '12-east-bath':((64.5,21.8,5.5),(58,18,4.4),18),
 '14-bath-detail':((13,17.2,5.5),(16,25,4),21),
 '13-dressing':((4.1,15.8,5.5),(4.1,25.6,4.6),22),
 '10-roof-site':((-25,-30,76),(34,27,0),45),
}
def roof_z(x):
 c=12 if x<=24 else 56
 return RIDGE-abs(x-c)*(RIDGE-EAVE)/12
