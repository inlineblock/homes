"""Mountain House concept. Author-facing dimensions in feet; internal model meters."""
SLUG='mountain-house'
WIDTH,DEPTH=60,40
MAIN=0.0
LOWER=-11.0
MAIN_SLABS=[(0,0,60,12),(0,12,24,27),(32,12,60,27),(0,27,60,40)]
LOWER_SLABS=[(24,0,60,40),(0,24,24,40)]
STAIR_VOID=(24,12,32,27)
GARAGE=(0,0,24,24)
MAIN_AREA=sum((c-a)*(d-b) for a,b,c,d in MAIN_SLABS)
LOWER_AREA=sum((c-a)*(d-b) for a,b,c,d in LOWER_SLABS)
GROSS=MAIN_AREA+LOWER_AREA
CONDITIONED=GROSS-24*24
DECKS=[(0,40,60,54),(60,18,68,54)]
DECK_AREA=sum((c-a)*(d-b) for a,b,c,d in DECKS)
PATIO=(24,40,60,53)
RISERS=20
RISE=11/RISERS
TREAD=11/12
STAIR_START=12.0
STAIR_LANDING=STAIR_START+9*TREAD
MAIN_WALLS=[
 ('Garage east',(24,0),(24,24),[(6,3.5)]),
 ('Garage rear',(0,24),(24,24),[]),
 ('Mudroom east',(32,0),(32,12),[(1.8,3),(7,3.5)]),
 ('Powder rear',(24,6),(32,6),[]),
 ('Stair west',(24,12),(24,27),[]),
 ('Primary bath west',(40,0),(40,12),[]),
 ('Primary bath rear',(40,12),(60,12),[(2,3)]),
 ('Primary WC east',(45,0),(45,6),[]),
 ('Primary WC rear',(40,6),(45,6),[(1,3)]),
 ('Primary west',(46,12),(46,26),[(6,3),(10.3,3.5)]),
 ('Closet west',(40,12),(40,22),[]),
 ('Closet rear',(40,22),(46,22),[]),
 ('Primary rear',(46,26),(60,26),[]),
]
LOWER_WALLS=[
 ('Lower bedroom 02 east',(18,24),(18,40),[(3,3.5)]),
 ('Lower bedroom 03 front',(42,26),(60,26),[(12,3.5)]),
 ('Lower bedroom 03 west',(42,26),(42,40),[]),
 ('Lower bath west',(42,18),(42,26),[(.6,3.3)]),
 ('Lower bath east',(52,18),(52,26),[]),
 ('Lower bath front',(42,18),(52,18),[]),
 ('Lower utility rear',(32,14),(60,14),[(2,3.5),(17,3.5)]),
 ('Lower utility divider',(46,0),(46,14),[(5,3.5)]),
]
VIEWS=[('01 Forest rear','01-forest-rear'),('02 Road arrival','02-road-arrival'),('03 Deck living','03-deck-living'),('04 Walkout patio','04-walkout-patio'),('05 Hillside section','05-hillside-section'),('06 Kitchen','06-kitchen'),('07 Primary bath','07-primary-bath'),('08 Kitchen appliances','08-kitchen-appliances')]
def roof_z(y):return 10.5+y*.055

def grade(x,y):
    import math
    if y<0:return -.30
    base=-.4-.265*min(y,40)-.20*max(0,y-40)
    if 22<x<63 and 40<y<68:
        shoulder=min(1,(x-22)/2,(63-x)/2)
        bench=-11.4 if y<=56 else -11.4-(y-56)*5.0/12
        base=base*(1-shoulder)+bench*shoulder
    # Smooth forest-floor variation away from the building and patio grading bench.
    away=max(0,min(1,(max(-x,x-68,y-70)-3)/10))
    return base+away*(.55*math.sin(x*.06+y*.045)+.25*math.sin(x*.18-y*.08))
