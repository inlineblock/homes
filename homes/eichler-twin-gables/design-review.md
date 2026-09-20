# Twin Gables Courtyard — design review

Status: reviewed architectural concept. All 14 native views, both plan sheets and eight photographic studies were inspected on 2026-09-20. This is concept review, not construction or permit approval.

## Accepted design

Two broad, parallel Eichler-inspired gables sit over full-height walls. The opaque center entry and screened front bedrooms protect street privacy; the internal courtyard and glazed rear public rooms provide the open garden character. The side uses straight continuous ridges, common eaves and repeated structural bays instead of the rejected irregular side concept.

The 68 × 60 ft planning floorplate excludes a 20 × 36 ft open-air courtyard, yielding **3,360 sq ft gross planning area**, including wall allowances. It is not a net usable-area schedule or a survey of exterior cladding faces. Parking, terraces, courtyard and overhangs are excluded.

## Household completeness

Both primary suites have actual king beds, fitted walk-in clothes storage, double vanity basins, a separate tub and shower, an enclosed toilet room with pocket entry, and a closed linen cabinet inside the bathroom. The office/guest room has a desk, guest bed and storage but is not counted as a third dedicated bedroom. A third full bathroom serves guests.

The kitchen includes a 36-inch induction cooktop, separate built-in oven, hood, 48-inch panel-ready refrigerator, dishwasher, sink, waste pullout, drawer storage and fitted walk-in pantry. Laundry and mechanical/service reservations are modeled. Two marked parking spaces connect to the entry walk on an illustrative level site.

## Review evidence and corrections

Independent program and visual reviewers inspected the furnished plan and first native views. The plan clearly distinguishes both complete suites, public rooms, pantry, laundry, guest accommodation and courtyard circulation. Native review identified oversized rugs, door/cabinet conflicts, obstructing context trees, cropped facade views, exposed hollow beam-cover ends, roof-cover intersections, a poorly visible cooktop and a driveway-to-road gap. These findings were corrected in the native source before photographic finishing. Bathroom render states also move both levers and the latch spindle with the closed leaf; the dressing view uses a recorded camera position inside the aisle.

`model/functional-validation.json` measures evaluated geometry and sampled operating envelopes, including galleries, clothes-storage aisles, WC compartments, linen/shower bounds, kitchen aisles, interior door sweeps, appliance openings and finished headroom. All 21 measured checks pass against frozen native SHA `de8b42f5d457c2332b92658a116c562ca89da1e44168826c2c78be50ccd2fe89`. These are finite generic-geometry checks, not manufacturer or code compliance. Separate fresh reopening and repository checks pass. IFC4 schema validation reports zero errors, and fresh Bonsai import contains 2,000 mesh objects.

## Reviewed visual tour

Native views: private front, rear garden elevation, useful side elevation, vaulted living, complete kitchen, courtyard, both primary bedrooms and bathrooms, rear terrace, roof/site relationship, dressing storage and bathroom linen detail. Plans: furnished ground floor and coordinated roof/section/site sheet.

Eight photographic studies were derived from the reviewed native front, rear, side, living, kitchen, courtyard, primary bedroom and bathroom views. Each selected image and native source has a verified hash and actual prompt in [photo provenance](outputs/photo-provenance.json). The side study was corrected to remove an invented paved strip. Other studies preserve the modeled architecture, camera and equipment while enriching surface detail, lighting, landscape and incidental decoration. Native images and plans govern dimensions and modeled scope.

## Measured concept clearances

- Both toilet rooms: about 4.15 × 6.25 ft inside clear, with modeled pocket recesses.
- Both bathroom linen cabinets: closed 24 × 24 × 96 in units with shelves; approximately 1.35 in nominal separation from the shower envelope.
- Walk-in closed-handle aisles: west 40.34 in, east 38.54 in; one open wardrobe leaf leaves about 28.94/27.14 in respectively. Opposing leaves are operated separately. These are not accessible-dressing-room approvals.
- Enclosed courtyard galleries: approximately 48.72 in clear at measured frames. Kitchen counter working aisle: approximately 53.38 in, with appliance checks recorded separately.
- Flat support/office ceilings: 10 ft. Entry and dining: about 12 ft. Vault lining: 12.2–17.8 ft; lower rafter-cover datums about 10.73–16.33 ft and ridge-cover underside 16.45 ft. Named native headroom rays are in the functional receipt.

## Shared assets and evidence

The saved model has 55 pinned relative library dependencies and 465 actual instances across 44 component families. The hollow wood-look beam cover and closed linen cabinet are new reusable library contributions. Column solids are explicitly identified as appearance proxies; they are not detailed hollow post assemblies. The asset schedule discloses generic planting variations.

- [Native reopening](model/native-validation.json) and [functional measurements](model/functional-validation.json)
- [Repository checks](model/repository-validation.json) and [actual asset adoption](model/asset-adoption-review.json)
- [IFC validation](model/ifc-validation.json) and [Bonsai reopening](model/bonsai-validation.json)
- [Plan source and output hashes](outputs/plans/plan-source.json), [render states](outputs/render-receipt.json), and [output review](model/output-validation.json)

## Concept limits

The steel framing and wood-look covers are architectural assumptions, not engineered sizes or connections. Site, climate, survey, local approvals, thermal/fire assemblies, glazing/roof products, weathering, drainage discharge and service sizing are unverified. Product selection must resolve installation gaps, operating requirements and tolerances. Clerestory perimeter/jamb closures and weather seals remain schematic; bright edge reveals in native views are not a verified weather-tight assembly. Bedroom escape-opening selection remains unverified. Parking is a level-site planning allowance, not a surveyed turning or setback study. Classified IFC geometry and dimensioned concept drawings are not permit or construction documentation.
