"""Write the grouped asset-use schedule and reject missing or stale adoption pins.

Plain Python: python3 tools/modern_block/schedule.py
Blender build: write_schedule(ROOT, deps) after project.json is written.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
# ID, exact version, adoption status, actual host use. Preserve family-level intent
# when adding a dependency; an unclassified new pin must not silently disappear.
GROUPS=[
 ('Courtyard, planting and screens',[
  ('landscape/broad-canopy-oak','v001','New original','Nine instanced trees; trunk/grade placement and modest uniform size variation.'),
  ('landscape/ornamental-grass-clump','v002','Reused','Forecourt and courtyard underplanting; documented uniform landscape variation.'),
  ('landscape/sage-shrub','v002','Reused','Forecourt shrub groups, kept outside routes and driveway.'),
  ('fixtures/courtyard-pool-4x8m','v001','New variation','One 4 × 8 m pool; derives from 6 × 12 m v001, with actual site/deck cavity.'),
  ('openings/timber-pivot-louver-1800x3000','v001','New original','Five lanai leaves at 2 m centers; open 75° and closed view states.'),
 ]),
 ('Envelope, paving and linked hardware',[
  ('openings/angled-cedar-privacy-screen-2000x2800','v001','New original','Two rigid fixed bathroom screens; 350 mm rear-frame-to-glazing service gap.'),
  ('surfaces/honed-limestone-wall-panel-4x2','v001','Reused','Full rigid limestone facade panels; local perimeter cuts use the same linked material.'),
  ('surfaces/honed-limestone-paver-4ft','v001','Reused','Full terrace modules and stepping path; site-specific cut strips at boundaries.'),
  ('openings/slim-dark-window','v002','Reused; approximate resize','Facade glazing; host resize changes frame sightlines and requires resolved dimensional variants later.'),
  ('hardware/bar-pull-matte-black','v001','Reused nested dependency','Concept grip included in the linked window assembly; not a specified window lock.'),
 ]),
 ('Cabinetry and useful storage',[
  ('cabinetry/oak-wardrobe-2ft','v001','Reused','18 bays across bedroom/dressing storage, foyer coats and pavilion office storage; hanging rails retained.'),
  ('cabinetry/oak-drawer-base-2ft','v001','Reused','14 kitchen and vanity drawer modules beneath bespoke continuous counters.'),
  ('cabinetry/oak-shelving-2ft','v001','New variation','Eight open pantry/laundry/landing linen bays; wardrobe-derived carcass with shelf decks and no cabinet doors.'),
 ]),
 ('Kitchen and laundry equipment',[
  ('appliances/panel-ready-fridge-48in','v001','Reused','Wide kitchen refrigeration, rigid full-size placement.'),
  ('appliances/built-in-oven-30in','v001','Reused','Kitchen oven bay, rigid full-size placement.'),
  ('appliances/induction-cooktop-36in','v001','Reused','Kitchen cooktop in the host counter.'),
  ('appliances/wall-hood-36in','v001','Reused','Kitchen extraction hood with a modeled conceptual duct to roof.'),
  ('appliances/dishwasher-24in','v001','Reused','Kitchen island appliance bay beside sink.'),
  ('fixtures/kitchen-sink-mixer-650','v001','Reused','Island sink and mixer with a real host counter aperture.'),
  ('appliances/front-loading-laundry-600','v001','Reused','Two original appliance proxies labeled washer and dryer; commercial products/services unresolved.'),
 ]),
 ('Bathing and sanitation',[
  ('fixtures/vanity-basin-mixer-mirror','v001','Reused','Seven basin/mixer/mirror assemblies across powder and three full bathrooms, including primary double vanity.'),
  ('fixtures/toilet-elongated','v001','Reused','Four toilets, including enclosed primary toilet compartment.'),
  ('fixtures/freestanding-tub-72in','v001','Reused','Primary separate freestanding bath.'),
  ('fixtures/shower-tray-screen-1500x1200','v001','New variation','Primary separate shower; dedicated 1.5 × 1.2 m sibling of 900 mm v001, without stretching.'),
  ('fixtures/shower-tray-screen-900','v001','Reused','Upper shared and guest bathroom showers.'),
 ]),
 ('Living, dining and work furniture',[
  ('furniture/linen-three-seat-sofa','v001','Reused','Living-room sofa.'),
  ('furniture/oak-rounded-coffee-table','v001','Reused','Living-room low table.'),
  ('furniture/oak-dining-table-8ft','v001','Reused','Main dining table.'),
  ('furniture/oak-upholstered-dining-chair','v001','Reused','Dining, desk and pavilion reading seating.'),
  ('furniture/coastal-oak-counter-stool','v001','Reused','Four kitchen island stools.'),
  ('furniture/oak-writing-desk','v001','Reused','Primary window desk and pavilion office desk.'),
  ('furniture/oak-round-dining-table-1000','v001','Reused','Pavilion reading table.'),
  ('fixtures/closed-glass-fireplace-48in','v001','Reused','Living firebox in a bespoke open masonry surround; conceptual flue route.'),
 ]),
 ('Bedrooms, textiles and outdoor furniture',[
  ('furniture/oak-linen-king-bed','v001','Reused','Primary king bed.'),
  ('furniture/oak-linen-queen-bed','v001','Reused','Three queen beds in guest and upper secondary bedrooms.'),
  ('furniture/oak-open-nightstand','v001','Reused','Eight bedside tables.'),
  ('furniture/woven-oatmeal-rug','v001','Reused','Living and primary bedroom rugs.'),
  ('furniture/olive-linen-cushion','v001','Reused','Two living sofa cushions.'),
  ('furniture/coastal-outdoor-sofa','v001','Reused','Covered lanai seating.'),
  ('furniture/coastal-outdoor-lounge-chair','v001','Reused','Lanai, balcony and living lounge seating.'),
  ('furniture/slatted-outdoor-chaise','v001','Reused','Two poolside chaises.'),
 ]),
 ('Lighting',[
  ('fixtures/lighting-recessed-downlight-3in','v001','Reused','Ambient fittings with actual recesses cut into host ceilings.'),
  ('fixtures/lighting-undercabinet-bar-4ft','v001','Reused','Kitchen task lighting.'),
  ('fixtures/lighting-linear-pendant-4ft','v001','Reused','Dining focal pendant.'),
 ]),
 ('Pinned material dependencies',[
  ('materials/bronze-gray-standing-seam','v001','Reused nested dependency','Fixed privacy-screen frame finish.'),
  ('materials/warm-vertical-cedar','v003','Reused','Upper facade boards, doors and linked screen timber; physical aligned grain.'),
  ('materials/charcoal-facade-panel','v001','Reused','Low-roof/dark exterior finish and selected host surfaces.'),
  ('materials/coastal-honed-limestone','v001','Reused','Facade/paver/coping dependencies and site-specific host stone cuts/counters.'),
  ('materials/coastal-white-oak','v001','Reused','Cabinetry, furniture dependencies and host millwork.'),
  ('materials/smoked-oak','v001','Reused nested dependency','Outdoor timber furniture finish.'),
  ('materials/olive-linen','v001','Reused nested dependency','Cushion and upholstered furniture textile.'),
  ('materials/woven-oatmeal','v001','Reused nested dependency','Rug and upholstered furniture textile.'),
 ]),
]

def write_schedule(root=ROOT,deps=None):
 root=Path(root);home=root/'homes/modern-block'
 if deps is None:deps=json.loads((home/'project.json').read_text())['asset_dependencies']
 pins={(a['id'],a['version']) for a in deps};records=[e for _,es in GROUPS for e in es];expected={(e[0],e[1]) for e in records}
 assert len(records)==len(expected),'Duplicate schedule records'
 assert pins==expected,f'Update schedule families: new pins {sorted(pins-expected)}; stale records {sorted(expected-pins)}'
 for id,version in expected:
  m=json.loads((root/'library'/id/version/'asset.json').read_text());assert (m['id'],m['version'])==(id,version)
 text='# Adopted asset families\n\n'
 text+='Audited against the current `project.json` pins, native reopening receipt and interior placement records: **52 exact dependencies**, including **six newly contributed assets**. New means published for this concept; reused includes nested material/hardware dependencies. All are original shared library assets with recorded rights. Each link opens its placement and installation contract.\n\n'
 text+='Furniture, cabinetry, equipment and the new screen/pool assemblies use rigid native scale. Plants use recorded uniform variation. Facade windows are explicitly resized appearance studies; their frame sightlines and operating envelopes remain approximate. A dependency check or closed asset preview does not establish installation approval.\n\n'
 for title,entries in GROUPS:
  text+='## '+title+'\n\n| Exact adopted ID / version | Status | Host use |\n| --- | --- | --- |\n'
  for id,version,status,use in entries:text+=f'| [`{id}` / `{version}`](../../../library/{id}/{version}/asset.json) | {status} | {use} |\n'
  text+='\n'
 text+='## Host geometry and review limits\n\n'
 text+='Bespoke geometry is limited to the pavilion layout, slabs/foundations, walls and actual openings, roof falls/gutters/rooflights, terrace and facade boundary cuts, fitted continuous kitchen/vanity counters and their apertures, service-route allowances, stairs/guards, projecting entrance/reveals, external flue pier, supported driveway alignment and parking reservations. These depend on the specific home dimensions. Full stone modules, plants, furniture and standard fixtures remain linked collections.\n\n'
 text+='Native verification records four bed instances, 18 wardrobe bays, eight shelf modules, linked pool geometry, five louver instances and 2 m louver spacing. The pool shell and water require the modeled opening in terrain/deck; louver rotation requires its 0.903 m swept radius. Larger shower and open pantry variants preserve true product-concept dimensions. Inspect the host model and plans for circulation, shelving access, door movement, counter cutouts and service fit. Actual engineering, weatherproofing, mechanical capacity, pool barriers, code approval and selected commercial products remain unresolved.\n\n'
 text+='This schedule is reproducible with `python3 tools/modern_block/schedule.py`. Its writer checks exact equality with the project dependency pins; update the grouped records whenever adoption changes. Generated placements are in `tools/modern_block/interiors-layout.json`, and native verification is in `model/native-validation.json`.\n'
 (home/'assets/README.md').write_text(text)
 return len(expected)
if __name__=='__main__':print('ASSET_SCHEDULE_WRITTEN',write_schedule())
