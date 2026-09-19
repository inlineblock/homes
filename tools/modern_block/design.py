"""Modern Block dimensional design source; meters. All dimensions are concept choices."""
F=0.3048
SLUG='modern-block'
GROUND=0.0
UPPER=3.6
GROUND_HEIGHT=3.3
UPPER_HEIGHT=3.0
MAIN=(10,0,22,20)
GUEST=(-8,0,0,12)
GARAGE=(-8,12,0,20)
UPPER_RECT=(10,0,22,17)
STAIR_VOID=(19,8.2,21.8,12.5)
COURT=(0,5,10,20)
LANAI=(0,0,10,5)
POOL=(3,9,7,17)
ENTRY_PORTAL=(19.2,-1.35,22,0)
ENTRY_LANDING=(18.9,-1.4,22,0)
ENTRY_STEPS=(18.9,-2.6,22,-1.4)
EAST_FLUE_PIER=(22.12,2.65,22.72,4.45)
FRONT_REVEAL_DEPTH=.45
PRIMARY_BATH_SCREEN=(17.5,-.75,21.5,-.45)
ROOMS={
 'ground':[
 ('Living / arrival',10,0,22,7),('Dining',10,7,16,13),('Kitchen',10,13,16,20),
 ('Foyer / gallery',16,7,19,13),('Stair',19,8.2,21.8,12.5),
 ('Pantry',16,13,19,16),('Laundry',19,13,22,16),('Service hall',16,16,22,17.2),
 ('Powder',16,17.2,19,20),('Mechanical',19,17.2,22,20),
 ('Office',-8,0,-2,5),('Guest bedroom',-8,5,-2,10),('Guest bath',-8,10,-2,12),('Guest gallery',-2,0,0,12),
 ('Two-car garage',-8,12,0,20)],
 'upper':[
 ('Primary bedroom',10,0,17,7),('Primary bath',17,0,22,5),('Dressing',17,5,22,7),
 ('Shared bath',10,7,15,11),('Upper gallery',15,7,19,13),('Stair void',19,8.2,21.8,12.5),
 ('Bedroom 2',10,11,15,17),('Bedroom 3',17,13,22,17),('Linen / landing',17,11,19,13)]}
# Partition openings are measured offsets from point a in meters.
PARTITIONS={
 'ground':[
 ('Guest office',(-8,5),(-2,5),[]),('Guest bedroom',(-8,10),(-2,10),[]),
 ('Guest corridor',(-2,0),(-2,12),[(2,1.0),(6.5,1.0),(10.3,1.0)]),
 ('Service west',(16,13),(16,20),[(.8,1.0),(3.15,1.0)]),
 ('Service south',(16,13),(22,13),[(4,1.0)]),
 ('Service division',(19,13),(19,20),[(3.1,1.0)]),
 ('Service hall south',(16,16),(22,16),[(.8,1.0),(3.8,1.0)]),
 ('Service hall north',(16,17.2),(22,17.2),[(.8,1.0),(3.8,1.0)]),
 ],
 'upper':[
 ('Primary suite north',(10,7),(22,7),[(5.4,1.1),(7.7,1.0)]),
 ('Primary bath west',(17,0),(17,7),[(2.8,1.0),(5.5,1.0)]),
 ('Bath dressing divide',(17,5),(22,5),[(2.7,1.0)]),
 ('Primary WC west',(20.3,3.2),(20.3,5),[]),('Primary WC south',(20.3,3.2),(22,3.2),[(.4,.85)]),
 ('Shared bath east',(15,7),(15,11),[(1.3,.95)]),
 ('West bedroom south',(10,11),(15,11),[]),('West bedroom east',(15,11),(15,17),[(.65,1.0)]),
 ('East bedroom south',(17,13),(22,13),[]),('East bedroom west',(17,13),(17,17),[(.55,1.0)])
 ]}
def rect_poly(r):
 x0,y0,x1,y1=r;return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
def area(r):return (r[2]-r[0])*(r[3]-r[1])
CONDITIONED_M2=area(MAIN)+area(GUEST)+area(UPPER_RECT)-area(STAIR_VOID)
GARAGE_M2=area(GARAGE)
