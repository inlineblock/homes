"""Approximate Lindon listing-plan transcription, in meters.

NOT measured/as-built data. Source plans are explicitly nondimensioned. Main
enclosed outline is area-calibrated to the MLS 2,448 sf; upper/basement are
registered to common core landmarks, NOT independently forced to MLS areas.
Floor elevations and wall heights are modeling assumptions. Preserve the pixel
traces/transforms so measured information can replace this first-pass baseline.
"""
from math import hypot, sqrt, pi, sin, cos

SLUG = "lindon-brick-house"
FT = 0.3048
SOURCE_TOUR = "https://tours.benaccinelli.com/1044eastcenterstreet"
SOURCE_MLS = "https://www.utahrealestate.com/2185212"
AREA_BASIS = "Main exterior-outline area calibrated to listing estimate; not measured"
SOURCE_IMAGES = {
    "main": "2nd_floor_1044_east_center_street_lindon_without_dim_378.jpg",
    "upper": "3rd_floor_1044_east_center_street_lindon_without_dim_491.jpg",
    "basement": "1st_floor_1044_east_center_street_lindon_without_dim_812.jpg",
}


def area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1]
                   for a, b in zip(poly, poly[1:]+poly[:1]))) / 2


# Main source pixel origin is left/front corner. Positive physical Y goes rearward.
MAIN_FOOTPRINT_PX = [
    (169,753),(363,753),(363,632),(498,632),(498,753),(535,753),
    (535,768),(657,768),(657,753),(685,753),(685,658),(792,658),
    (812,678),(983,496),(965,477),(965,448),(1020,448),(1020,40),
    (562,40),(562,222),(359,222),(359,366),(169,366),
]
MAIN_SQFT = 2448
S = sqrt(MAIN_SQFT * FT**2 / area(MAIN_FOOTPRINT_PX))
MAIN_METERS_PER_PIXEL = S
# Registration is slightly anisotropic because the separate supplied drawings
# do not align perfectly under a uniform scale. This is an explicit approximation.
TRANSFORMS = {
    "main": dict(x_scale=1., x_offset=0., y_scale=1., y_offset=0.),
    "upper": dict(x_scale=661/686, x_offset=359-244*661/686,
                  y_scale=255/280, y_offset=498-514*255/280),
    "basement": dict(x_scale=851/1164, x_offset=169-208*851/1164,
                     y_scale=713/974, y_offset=40-41*713/974),
}


def point(level, xy):
    t = TRANSFORMS[level]
    x = xy[0]*t["x_scale"] + t["x_offset"]
    y = xy[1]*t["y_scale"] + t["y_offset"]
    return ((x-169)*S, (753-y)*S)


def polygon(level, vertices):
    return [point(level, p) for p in vertices]


def rect(x0, y0, x1, y1):
    return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]


def room(level, name, kind, vertices, **extra):
    return dict(name=name, type=kind, polygon=polygon(level, vertices),
                source_pixels=vertices, **extra)


def wall(level, name, a, b, gaps=()):
    """Door/open-passage gaps are fractional intervals along this source segment.

    Returns intervals (start_m, width_m), measured along a -> b. The renderer
    must leave the opening empty below door head, rather than add a solid wall.
    """
    pa, pb = point(level,a), point(level,b)
    length = hypot(pb[0]-pa[0],pb[1]-pa[1])
    return dict(name=name, a=pa, b=pb,
                openings=[(lo*length,(hi-lo)*length) for lo,hi in gaps],
                source_pixels=[a,b], evidence="approximate source trace")


def opening(level, name, a, b, kind="door", **extra):
    return dict(name=name, a=point(level,a), b=point(level,b),
                type=kind, **extra)


GARAGE_FOOTPRINT_PX = [(812,678),(1059,430),(1430,781),
                       (1194,1016),(1044,865),(1020,888)]
GARAGE_FOOTPRINT = polygon("main",GARAGE_FOOTPRINT_PX)
GARAGE = dict(name="Three-car angled garage", polygon=GARAGE_FOOTPRINT,
              z=-0.15, height=2.95, status="approximate; floor drop assumed")

UPPER_FOOTPRINT_PX = [
    (244,655),(388,655),(388,794),(582,794),(582,753),(664,753),
    (731,684),(948,900),(991,857),(1146,1016),(1355,807),
    (974,427),(930,470),(930,208),(650,208),(650,40),(455,40),
    (455,208),(244,208),
]
BASEMENT_FOOTPRINT_PX = [
    (208,1015),(445,1015),(445,945),(639,945),(639,1015),
    (879,1015),(879,874),(1088,874),(1390,557),(1357,520),
    (1357,413),(1315,413),(1315,261),(1372,261),(1372,41),
    (746,41),(746,190),(758,190),(758,215),(723,215),
    (723,270),(758,270),(758,290),(465,290),(465,499),(208,499),
]

LEVELS = {
    "main": dict(name="Main floor", z=0., height=3.0,
        listing_area_sqft=2448, footprint=polygon("main",MAIN_FOOTPRINT_PX),
        rooms=[], interior_wall_segments=[], exterior_openings=[], voids=[], stairs=[]),
    "upper": dict(name="Upper floor", z=3.25, height=2.7,
        listing_area_sqft=2180, footprint=polygon("upper",UPPER_FOOTPRINT_PX),
        rooms=[], interior_wall_segments=[], exterior_openings=[], voids=[], stairs=[]),
    "basement": dict(name="Walkout basement", z=-3.15, height=2.8,
        listing_area_sqft=2179, footprint=polygon("basement",BASEMENT_FOOTPRINT_PX),
        rooms=[], interior_wall_segments=[], exterior_openings=[], voids=[], stairs=[]),
}

L="main"
LEVELS[L]["rooms"] = [
    room(L,"Formal living room","living",rect(174,530,359,748)),
    room(L,"Office","office",[(174,370),(357,370),(384,381),(421,414),(360,478),(360,526),(174,526)]),
    room(L,"Foyer","entry",[(362,550),(423,550),(423,498),(562,498),(562,554),(498,620),(498,630),(362,630)]),
    room(L,"Formal dining","dining",[(498,620),(562,554),(681,554),(681,748),(498,748)]),
    room(L,"Kitchen","kitchen",[(363,226),(649,226),(649,411),(425,411),(382,372),(363,366)]),
    room(L,"Breakfast nook","dining",rect(566,44,1016,235)),
    room(L,"Family living room","living",[(651,237),(1016,237),(1016,444),(893,444),(875,495),(742,495),(742,414),(651,414)]),
    room(L,"Powder room","half_bath",rect(670,422,737,494)),
    room(L,"Coat closet","closet",rect(455,446,580,494)),
    room(L,"Central hall","hall",rect(423,498,754,550)),
    room(L,"Garage entry","mudroom",[(688,555),(812,555),(861,622),(811,673),(791,654),(688,654)]),
    room(L,"Garage entry closet","closet",rect(688,555,713,654)),
]
LEVELS[L]["interior_wall_segments"] = [
    wall(L,"Office / formal living",(169,526),(361,526)),
    wall(L,"Formal living / foyer",(361,526),(361,753),[(.10,.46)]),
    wall(L,"Office diagonal entry",(361,478),(422,414),[(.08,.84)]),
    wall(L,"Coat closet rear",(451,443),(584,443)),
    wall(L,"Coat closet front",(451,498),(584,498)),
    wall(L,"Coat closet west",(451,443),(451,498)),
    wall(L,"Coat closet door",(584,443),(584,498),[(.15,.92)]),
    wall(L,"Powder west",(667,418),(667,498)),
    wall(L,"Powder rear",(667,418),(741,418)),
    wall(L,"Powder east",(741,418),(741,498)),
    wall(L,"Powder entry",(667,498),(741,498),[(.37,.94)]),
    wall(L,"Hall / family room",(741,498),(877,498)),
    wall(L,"Dining / garage entry",(685,554),(685,658)),
    wall(L,"Garage entry closet",(713,554),(713,658),[(.13,.88)]),
    wall(L,"Garage entry stair partition",(754,554),(820,554),[(.13,.73)]),
]
LEVELS[L]["exterior_openings"] = [
    opening(L,"Front entry",(412,633),(462,633)),
    opening(L,"Rear breakfast door",(675,40),(724,40)),
    opening(L,"Rear family corner door",(1020,48),(1020,97)),
    opening(L,"Garage-house entry",(812,673),(861,622)),
    opening(L,"Secondary garage-house door",(944,538),(982,500)),
]
LEVELS[L]["stairs"] = [
    dict(name="Curved foyer stair", target="upper", path=polygon(L,[(391,547),(391,520),(418,493),(451,478)]),
         footprint=polygon(L,[(362,550),(421,550),(421,531),(451,500),(451,461),(423,443),(362,501)]),
         note="Source curved stair; full rise, winders and headroom must be resolved by parent."),
    dict(name="Back hall stair", target="upper", path=polygon(L,[(754,526),(869,526),(923,477),(962,470)]),
         footprint=polygon(L,[(753,498),(874,498),(925,445),(965,445),(965,482),(893,551),(753,551)]),
         note="Source separate back stair; approximate path only."),
    dict(name="Basement stair", target="basement", path=polygon(L,[(831,571),(861,601),(888,574)]),
         footprint=polygon(L,[(814,553),(863,553),(895,579),(863,617),(828,579)]),
         note="Down stair adjacent to back stair and garage entry; inferred vertical connection."),
]

L="upper"
LEVELS[L]["rooms"] = [
    room(L,"Primary bedroom","bedroom",[(670,213),(926,213),(926,474),(891,510),(670,510)], bedroom_id=1),
    room(L,"Primary walk-in closet","closet",[(459,274),(662,274),(662,400),(627,400),(627,454),(500,454),(500,318),(459,318)]),
    room(L,"Primary bathroom","full_bath",[(459,44),(646,44),(646,133),(596,133),(596,209),(662,209),(662,266),(459,266)]),
    room(L,"Primary toilet compartment","wc_compartment",rect(599,138,646,205)),
    room(L,"Bedroom 2 northwest","bedroom",[(249,213),(420,213),(420,303),(445,333),(407,374),(249,374)],bedroom_id=2),
    room(L,"Bedroom 2 reach-in closet","closet",rect(423,213,451,321)),
    room(L,"Shared upper bathroom","full_bath",rect(249,382,406,454)),
    room(L,"Northwest bedroom hall","hall",[(410,379),(455,336),(495,386),(495,454),(410,454)]),
    room(L,"Upper central landing","hall",[(340,461),(656,461),(656,571),(526,571),(455,571),(455,514),(340,514)]),
    room(L,"Bedroom 3 front","bedroom",[(392,650),(430,614),(514,614),(547,590),(578,626),(578,789),(392,789)],bedroom_id=3),
    room(L,"Bedroom 3 reach-in closet","closet",[(426,609),(457,577),(522,577),(540,592),(516,610)]),
    room(L,"Upper laundry","laundry",[(585,633),(716,633),(734,652),(661,748),(585,748)]),
    room(L,"Garage-wing bathroom","three_quarter_bath",[(844,569),(973,434),(1045,502),(908,638)]),
    room(L,"Bedroom 4 over garage","bedroom",[(948,614),(1060,514),(1199,657),(1100,754),(1028,754),(944,674)],bedroom_id=4),
    room(L,"Bedroom 4 reach-in closet","closet",[(952,608),(1045,512),(1067,531),(975,625)]),
    room(L,"Bedroom 5 over garage","bedroom",[(1070,759),(1100,759),(1203,659),(1348,807),(1228,930),(1170,884),(1096,958),(997,858),(1070,804)],bedroom_id=5),
    room(L,"Bedroom 5 walk-in closet","closet",[(1101,961),(1171,891),(1222,936),(1146,1008)]),
    room(L,"Garage-wing hall","hall",[(737,682),(795,619),(840,573),(906,643),(940,678),(1026,757),(1065,757),(1065,802),(947,893)]),
    room(L,"Upper front hall","hall",[(455,574),(525,574),(580,626),(720,626),(739,648),(795,613),(832,574)]),
]
LEVELS[L]["interior_wall_segments"] = [
    wall(L,"Northwest bedroom closet front",(422,208),(422,309),[(.12,.9)]),
    wall(L,"Northwest bedroom diagonal",(422,309),(459,345),[(.09,.9)]),
    wall(L,"Northwest bedroom south",(244,377),(410,377)),
    wall(L,"Northwest bathroom hall",(409,377),(409,458),[(.12,.57)]),
    wall(L,"Northwest bath south",(244,458),(449,458)),
    wall(L,"Primary bath west",(455,208),(455,341)),
    wall(L,"Primary bath / closet",(455,271),(665,271),[(.25,.51)]),
    wall(L,"Primary WC west",(596,135),(596,209)),
    wall(L,"Primary WC south",(596,209),(650,209),[(.15,.92)]),
    wall(L,"Primary closet hall wall",(498,318),(498,458)),
    wall(L,"Primary closet hall diagonal",(455,341),(498,386),[(.06,.96)]),
    wall(L,"Primary closet south",(498,458),(665,458),[(.79,.99)]),
    wall(L,"Primary closet bedroom",(665,271),(665,514),[(.76,.96)]),
    wall(L,"Primary bath bedroom",(665,208),(665,271),[(.08,.85)]),
    wall(L,"Primary bedroom stair side",(665,514),(891,514)),
    wall(L,"Primary closet return",(627,404),(665,404)),
    wall(L,"Primary closet cabinet return",(627,404),(627,458)),
    wall(L,"Front bedroom diagonal",(387,644),(455,572)),
    wall(L,"Front closet back",(455,572),(525,572)),
    wall(L,"Front closet front",(427,615),(517,615),[(.12,.91)]),
    wall(L,"Front bedroom door",(525,572),(581,628),[(.23,.94)]),
    wall(L,"Front bedroom east",(581,628),(581,794)),
    wall(L,"Laundry north",(581,628),(722,628),[(.44,.8)]),
    wall(L,"Laundry diagonal",(665,752),(739,677)),
    wall(L,"Wing bath southwest",(838,574),(908,644),[(.4,.96)]),
    wall(L,"Wing bath bedroom",(908,644),(1046,506)),
    wall(L,"Near wing bedroom hall",(908,644),(1027,759),[(.1,.39)]),
    wall(L,"Near wing bedroom south",(1027,759),(1100,759)),
    wall(L,"Wing bedroom divider",(1100,759),(1202,656)),
    wall(L,"Far wing bedroom hall",(1069,759),(1069,805),[(.05,.91)]),
    wall(L,"Far wing bedroom diagonal hall",(1069,805),(994,859)),
    wall(L,"Far WIC northwest",(1095,959),(1171,884)),
    wall(L,"Far WIC northeast",(1171,884),(1228,932),[(.24,.94)]),
]
LEVELS[L]["voids"] = [
    dict(name="Open foyer below",polygon=polygon(L,[(249,567),(304,567),(304,542),(337,515),(454,515),(454,571),(388,644),(388,650),(249,650)])),
    dict(name="Curved foyer stair opening",polygon=polygon(L,[(249,460),(449,460),(449,514),(337,514),(308,543),(308,563),(249,563)])),
    dict(name="Rear stair opening",polygon=polygon(L,[(655,519),(886,519),(832,573),(655,573)])),
]
LEVELS[L]["exterior_openings"] = [opening(L,"Primary rear balcony door",(811,208),(863,208))]
LEVELS[L]["stairs"] = [
    dict(name="Curved foyer stair arrival",target="main",path=polygon(L,[(278,562),(278,526),(316,488),(445,488)])),
    dict(name="Rear stair arrival",target="main",path=polygon(L,[(655,545),(768,545),(812,581)])),
]

L="basement"
LEVELS[L]["rooms"] = [
    room(L,"Bedroom 6 northwest","bedroom",[(214,505),(454,505),(454,678),(420,678),(345,752),(214,752)],bedroom_id=6),
    room(L,"Bedroom 6 reach-in closet","closet",[(214,758),(336,758),(296,803),(214,803)]),
    room(L,"Bedroom 7 southwest","bedroom",[(214,809),(297,809),(347,760),(442,853),(442,1010),(214,1010)],bedroom_id=7),
    room(L,"Bedroom 7 walk-in closet","closet",[(402,805),(457,756),(636,756),(636,849),(443,849)]),
    room(L,"Bedroom 7 storage","storage",rect(448,856,635,939)),
    room(L,"Utility / laundry","utility",[(461,508),(534,572),(568,572),(568,653),(548,677),(461,677)]),
    room(L,"Basement bedroom hall","hall",[(350,755),(424,684),(548,684),(578,653),(578,577),(646,577),(646,746),(457,746),(398,803)]),
    room(L,"Eat-in second kitchen","kitchen",[(473,296),(752,296),(752,565),(535,565),(473,500)]),
    room(L,"Sitting room","living",[(752,45),(929,45),(929,104),(971,104),(971,559),(875,559),(875,565),(756,565),(756,291),(758,274),(723,274),(723,216),(758,216),(758,188),(752,188)]),
    room(L,"Basement coat storage","closet",rect(934,45,971,99)),
    room(L,"Bathroom vanity area","three_quarter_bath",rect(653,575,875,675)),
    room(L,"Basement shower/WC compartment","bath_compartment",rect(653,681,875,747)),
    room(L,"Billiards room","recreation",[(982,45),(1366,45),(1366,255),(1315,255),(1315,290),(982,290)]),
    room(L,"Recreation room","recreation",[(982,294),(1310,294),(1310,415),(1353,415),(1353,521),(1383,557),(1245,701),(1182,663),(982,663)]),
    room(L,"Basement rear stair hall","hall",rect(883,571,971,746)),
    room(L,"Basement stair storage","storage",rect(982,672,1146,742)),
    room(L,"Basement general storage","storage",[(645,756),(1180,756),(1180,779),(1085,869),(873,869),(873,1009),(645,1009)]),
]
LEVELS[L]["interior_wall_segments"] = [
    wall(L,"Northwest bedroom east",(457,499),(457,681)),
    wall(L,"Northwest bedroom hall diagonal",(348,754),(420,681),[(.08,.92)]),
    wall(L,"Bedroom closet north",(208,755),(348,755),[(.08,.8)]),
    wall(L,"Bedroom closet south",(208,806),(298,806)),
    wall(L,"Bedroom7 hall diagonal",(348,759),(445,852),[(.02,.62)]),
    wall(L,"Bedroom7 WIC north",(457,752),(639,752)),
    wall(L,"Bedroom7 WIC diagonal",(399,807),(457,752),[(.1,.86)]),
    wall(L,"Bedroom7 WIC south",(445,852),(639,852)),
    wall(L,"Bedroom7 storage access",(445,852),(445,945),[(.12,.88)]),
    wall(L,"Bedroom7 storage south",(445,945),(639,945)),
    wall(L,"Bedroom7 storage east",(639,752),(639,1015)),
    wall(L,"Utility kitchen diagonal",(465,499),(535,571)),
    wall(L,"Utility north return",(535,571),(574,571)),
    wall(L,"Utility east",(574,571),(574,655),[(.05,.9)]),
    wall(L,"Utility hall diagonal",(574,655),(550,681)),
    wall(L,"Utility south",(420,681),(550,681)),
    wall(L,"Kitchen bathroom partition",(574,571),(879,571),[(0.,.25)]),
    wall(L,"Bath hall west",(649,571),(649,753),[(.08,.35)]),
    wall(L,"Bathroom compartment divider",(649,678),(879,678),[(.39,.73)]),
    wall(L,"Shower divider",(742,678),(742,750)),
    wall(L,"Bathroom south",(649,751),(879,751)),
    wall(L,"Bathroom hall east",(879,563),(879,751),[(.27,.52)]),
    wall(L,"Sitting recreation divider",(976,41),(976,566),[(.84,.99)]),
    wall(L,"Coat closet south",(930,103),(976,103),[(.11,.91)]),
    wall(L,"Coat closet west",(930,41),(930,103)),
    wall(L,"Stair storage north",(976,667),(1151,667)),
    wall(L,"Stair storage west",(976,667),(976,748),[(.18,.9)]),
    wall(L,"Stair storage east",(1151,667),(1151,748)),
    wall(L,"General storage / hall",(879,751),(1179,751),[(.065,.255)]),
]
LEVELS[L]["exterior_openings"] = [
    opening(L,"Sitting-room walkout",(854,41),(926,41)),
    opening(L,"Billiards walkout",(1096,41),(1167,41)),
]
LEVELS[L]["stairs"] = [
    dict(name="Basement rear stair",target="main",path=polygon(L,[(1178,739),(1178,688),(1210,653),(1250,692)]),
         footprint=polygon(L,[(1155,667),(1178,667),(1210,627),(1275,691),(1208,744),(1155,744)]),
         note="Source stair in angled rear corner; alignment with main must be reviewed in section."),
]

# Source-linked feature locations allow the parent to place real library assets.
# These are placement centers, not equipment size or clearance verification.
FIXTURE_CENTERS = {
    "main": {"kitchen_sink":point("main",(390,257)),
             "cooktop":point("main",(501,241)),
             "island":point("main",(507,337)),
             "powder_basin":point("main",(684,434)),
             "powder_toilet":point("main",(720,438))},
    "upper": {"primary_tub":point("upper",(493,86)),
              "primary_shower":point("upper",(621,88)),
              "primary_wc":point("upper",(621,159)),
              "primary_basin_1":point("upper",(473,159)),
              "primary_basin_2":point("upper",(472,244)),
              "laundry_washer":point("upper",(599,650)),
              "laundry_dryer":point("upper",(599,685))},
    "basement": {"second_sink":point("basement",(651,317)),
                 "second_range":point("basement",(493,436)),
                 "utility_laundry_1":point("basement",(482,553)),
                 "utility_laundry_2":point("basement",(481,594)),
                 "bath_vanity":point("basement",(797,593)),
                 "shower":point("basement",(694,714)),
                 "wc":point("basement",(850,712))},
}

BEDROOM_CENTERS = {
    1: point("upper",(800,361)), 2:point("upper",(332,297)),
    3: point("upper",(482,700)), 4:point("upper",(1067,660)),
    5: point("upper",(1180,819)), 6:point("basement",(326,623)),
    7: point("basement",(327,912)),
}

NOTES = [
    "Pixel-derived first pass; supplied floor plans have no dimensions and state approximate measurements.",
    "Two above-ground levels plus walkout basement; five upper bedrooms and two basement bedrooms.",
    "Main scale is area-derived; upper/basement alignment is approximate and deliberately not area-forced.",
    "All z/height values are assumptions, not listing measurements. Stair rise/headroom unresolved.",
    "Upper footprint includes rooms above angled garage, while left main office/formal wing is single story.",
    "Room polygons are zoning outlines, not a complete non-overlapping finished-area accounting.",
    "Main exterior bay, angled garage connector and upper balcony need photo/section reconciliation.",
    "New red-brick exterior and window redesign are proposed work, separate from source-plan topology.",
]

# Proposed stair coordination, replacing ambiguous source-scale runs while
# retaining every original trace above. These are design changes, not as-built
# measurements. Two rear flights are stacked on one aligned footprint.
SOURCE_STAIR_TRACES = {k:list(v['stairs']) for k,v in LEVELS.items()}
SOURCE_STAIR_VOIDS = {k:list(v['voids']) for k,v in LEVELS.items()}
REAR_STAIR_PATH = [(17.05,7.15),(17.05,6.35),(15.894,5.154),(13.283,5.154)]
REAR_STAIR_VOID = [(12.98,4.54),(16.15,4.54),(17.65,6.12),
                   (17.65,7.15),(16.45,7.15),(16.45,6.68),
                   (15.64,5.79),(12.98,5.79)]
# Arc boundary follows both sides of the curved flight with a 70 mm edge
# allowance. A coarse diagonal chord would clip the outside curved treads.
FOYER_STAIR_VOID = ([(5.63,4.20),(5.63,5.20)] +
    [(6.13 + .50*cos(pi-j*pi/32), 5.20 + .50*sin(pi-j*pi/32)) for j in range(1,17)] +
    [(8.90,5.70),(8.90,6.88),(6.13,6.88)] +
    [(6.13 + 1.68*cos(pi/2+j*pi/32), 5.20 + 1.68*sin(pi/2+j*pi/32)) for j in range(1,17)] +
    [(4.45,4.20)])
LEVELS['main']['voids'] = [dict(name='Aligned rear basement stair opening',
    polygon=REAR_STAIR_VOID, proposed=True)]
LEVELS['upper']['voids'] = [SOURCE_STAIR_VOIDS['upper'][0],
    dict(name='Reconciled curved foyer stair opening',polygon=FOYER_STAIR_VOID,proposed=True),
    dict(name='Aligned rear upper stair opening',polygon=REAR_STAIR_VOID,proposed=True)]
LEVELS['main']['ceiling_voids'] = LEVELS['upper']['voids']
LEVELS['basement']['ceiling_voids'] = LEVELS['main']['voids']
LEVELS['upper']['ceiling_voids'] = []
LEVELS['main']['stairs'] = [
    dict(name='Proposed curved foyer stair',target='upper',
         path=[(5.04,4.25),(5.04,5.20),(6.13,6.29),(8.90,6.29)],
         footprint=FOYER_STAIR_VOID,risers=19,rise=3.25/19,width=1.04,proposed=True),
    dict(name='Proposed aligned rear stair',target='upper',path=REAR_STAIR_PATH,
         footprint=REAR_STAIR_VOID,risers=19,rise=3.25/19,width=1.04,proposed=True),
]
LEVELS['basement']['stairs'] = [dict(name='Proposed aligned basement stair',
    target='main',path=REAR_STAIR_PATH,footprint=REAR_STAIR_VOID,
    risers=18,rise=3.15/18,width=1.04,proposed=True)]
LEVELS['upper']['stairs'] = []
# Keep replaced zones/walls as source evidence, but do not display or build
# full-height source storage inside the proposed stair reservation.
SOURCE_STAIR_STORAGE_ROOMS = {}
SOURCE_STAIR_STORAGE_WALLS = {}
for _key, _room_name, _wall_prefix in [
    ('main', 'Coat closet', 'Coat closet'),
    ('basement', 'Basement stair storage', 'Stair storage'),
]:
    SOURCE_STAIR_STORAGE_ROOMS[_key] = [r for r in LEVELS[_key]['rooms'] if r['name'] == _room_name]
    SOURCE_STAIR_STORAGE_WALLS[_key] = [w for w in LEVELS[_key]['interior_wall_segments'] if w['name'].startswith(_wall_prefix)]
    LEVELS[_key]['rooms'] = [r for r in LEVELS[_key]['rooms'] if r['name'] != _room_name]
    LEVELS[_key]['interior_wall_segments'] = [w for w in LEVELS[_key]['interior_wall_segments'] if not w['name'].startswith(_wall_prefix)]
# The north-turning lower flight needs clearance past the family-room
# partition end. Retain its original trace and shorten only that local return.
SOURCE_STAIR_ADJUSTED_WALLS = []
for _wall in LEVELS['main']['interior_wall_segments']:
    if _wall['name'] == 'Hall / family room':
        SOURCE_STAIR_ADJUSTED_WALLS.append(dict(_wall))
        _wall['b'] = (15.35, _wall['b'][1])
        _wall['evidence'] = 'proposed shortened return for rear-stair clearance'
NOTES.extend([
    'Stair flights/voids were concept-adjusted for realistic rise/run; original traces preserved in SOURCE_STAIR_TRACES and SOURCE_STAIR_VOIDS.',
    'Rear basement stair is relocated into a stacked reservation below the upper flight; old stair-storage room label and full-height walls are omitted from proposed data.',
    'Original foyer coat storage and tall partitions are omitted from the proposed reservation; any replacement under-stair storage awaits underside coordination.',
    'Rear lower arrival turns north into the family/recreation rooms; it does not penetrate the short exterior return or invent a garage passage. The family-room partition return is shortened 0.73 m to clear the flight; original retained separately.',
    'Stair dimensions are coordinated concept geometry only; local rules, structure, handrail details and professional review remain unverified.',
])

for _level in LEVELS.values():
    _level["modeled_outline_area_sqft"] = area(_level["footprint"])/FT**2
    _level["modeled_void_area_sqft"] = sum(area(v["polygon"]) for v in _level["voids"])/FT**2
    _level["evidence"] = "approximate nondimensioned listing-plan transcription"
