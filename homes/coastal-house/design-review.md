# Coastal House design review

## Current design and evidence status

The current design is a **raised driftwood coastal pavilion**. A genuine living/dining vault and high glazing lift above the lower bedroom/entry and kitchen wings. The exposed interior frames, attached pergola, eaves and island share the driftwood finish; pale perimeter oak, mushroom exterior plaster, warm interior plaster, large-format limestone and oatmeal/olive textiles provide complementary tones. Darker timber remains within the shared outdoor furniture.

**Native model and current outputs reviewed:** the raised coastal pavilion [native model receipt](model/model-validation.json) confirms a successful reopen. The geometry verifier confirms four roof planes, 13 real upper glazing panels, six sloped rafters, six side supports including one stone-encased wet-zone post, matching pergola timber and genuine sloping ceilings. The pergola retains exactly two outer supports, no house-side posts, ledger/header contact and 30 ft opening coverage; minimum roof-soffit separation is now 3.10 ft. Nineteen interior routes, four terrace routes, two arrival routes, two driver approaches and 420 moving-panel component checks pass. All 37 exact shared asset pins agree with actual adoption.

The [saved-lighting receipt](model/lighting-validation.json) measures all 25 real recessed openings, eight in the vault and seventeen in flat ceilings. Each opening has a clear center ray and four collar contacts with its actual ceiling plane. All twelve contact vertices across the three sloped pendant mounts meet the ceiling; the unscaled fixture retains a level diffuser at approximately 8.55 ft and vertical emission. These checks establish modeled mounting, not rated photometry or electrical/structural approval.

**Current IFC and Bonsai import verified:** the [IFC4 schema receipt](model/ifc-validation.json) reports zero errors. The [actual Bonsai 0.8.5 import](model/bonsai-validation.json), using Blender 4.5.14 LTS, reopens **789 mesh objects**. Imported geometry confirms all four roof planes, thirteen upper glazing panels, six sloping rafters and six frame columns, including one stone-encased wet-zone post. Timber appearance agrees with the pergola. The attached pergola retains two outer posts, no house-side posts and 45 open slats; the entry canopy has two supports. The import review directly checks 117 product meshes, with a maximum IFC-to-Bonsai bounds difference below 0.000003 ft.

The import receipt's source Blender hash `e7481133030133dd630bd6a49a875062a520ed7276fa4f4c839941b002818b0b` and IFC hash `685200f5e1f3747dc7a0845fb26d30992fda53c3df750b0de9fbc47a15fdd5c2` match the current files. Export/import success establishes classified concept geometry, material appearance and tessellation, not construction readiness.

Thirteen final native images, an exterior and two interior Imagegen studies, floor/site drawings, the measured roof section and all ten booklet pages have been visually reviewed and promoted. Native, export and output evidence are recorded separately.

## Program and spatial assumptions

- One story, three bedrooms and two bathrooms; 2,720 gross enclosed sq ft from the 68 x 40 ft exterior floor plate. Walls are included; carport, terrace, pergola, entry canopy, eaves and illustrative site are excluded.
- Front road and coast are artistic site assumptions. A 26 x 24 ft detached carport provides two nominal 12 ft parking bays and a 26 ft driveway. Preserve the 6 ft separate front walk and 4 ft crosswalk behind the vehicles.
- The daylit entry is 8 ft wide by 12 ft in planning dimensions, with approximately 7.65 ft wall-to-wall clearance, a full-height sidelight, coat wardrobe, drop shelf and wall mirror.
- Bedroom 02 is nominally 15 x 12 ft; Bedroom 03 is 15 x 16 ft. Each retains 6 ft of 24-inch-deep wardrobe. Room dimensions include storage zones rather than reporting net clear floor area.
- The 18 x 26 ft primary wing contains an 18 x 12 ft king bedroom, 6 x 6 ft dressing room entered from the bathroom, separate 72-inch tub and 5.2 x 7.4 ft shower, double vanity with 36-inch basin centers, enclosed 4 x 6 ft toilet room and towel storage.
- Laundry linen storage, pantry, island waste/recycling and a 5 x 4.8 ft mechanical reservation remain part of the household program. Equipment size, ventilation, service access and final cabinetry operation remain unresolved.

## Outdoor rooms and arrival

The **32 ft wide house-attached pergola** extends from X=9 to 41 ft and projects **15.15 ft**, from Y=40.85 to 56 ft. It spans the full 30 ft glass opening. A ledger above the opening header supports the house edge; exactly two outer posts stand at (9,56) and (41,56) ft, with **no house-side legs**. The conceptual outer beam is **18 inches deep**, with a steel core clad in timber. Open timber slats cast patterned shade and are **not rainproof**. The low west screen defines a side without enclosing the central shore outlook. Structural attachment, beam/post sizing, footings, connections and wind restraint remain unengineered.

A linked outdoor sofa centered at (4.5,51.5) ft faces +X across the coffee table at (10,51.5) ft. Two chairs at (15.5,47.75) and (15.5,55.25) ft face -X. The inward-facing grouping is intended to preserve a route between the furniture and pergola post. Dining stays beneath the pergola, and the separate exterior serving counter retains its stools. The refreshed receipt confirms the static terrace routes, geometric support contact and moving opening clearances. Occupied seating and moving-chair envelopes remain unverified; keep tracks, pockets and the threshold drain clear.

The front door receives a **12 x 9 ft timber-lined entry canopy**, with a modeled sloping metal cap and drainage concept. Planting groups frame the approach and terrace ends. The six-foot walk, parking crosswalk, vehicle area, front porch and entire furnished terrace are excluded from plant footprints in the placement source. The refreshed native adoption receipt confirms **170 grasses, 51 shrubs and six olive trees**. Terrain placement samples the actual dune mesh and accounts for the flat foundation beneath it. Plant forms are illustrative rather than a coastal botanical specification.

## Interior, kitchen and shared assets

Warm-limestone plaster replaces the uniformly pale wall palette. The driftwood island remains distinct from the lighter perimeter cabinetry and serving counter. Linked indoor furniture, a woven oatmeal rug and olive cushions give the living retreat texture; original coastal relief art and a linear dining pendant add deliberate focal points. The existing fitted chaise extension remains local to the room.

The complete kitchen retains a 36-inch induction cooktop, 30-inch oven, 36-inch hood, 24-inch dishwasher, 48-inch panel-ready refrigerator, sink, pantry and waste/recycling. Appliance bodies occupy genuine cabinet bays. A vertical hood duct allowance is modeled; final exterior termination, fan sizing, makeup air, fire stopping, services and product clearances remain unresolved.

The lighting concept retains 25 shared downlights with ceiling cutouts, concealed kitchen task lighting, an entry opal pendant and the dining focal pendant. Shared satin-bronze pulls and door levers provide coordinated hardware. These are original visual assets, not rated products or verified photometry.

The [asset schedule](assets/README.md) records the pinned families. Furniture, textiles, driftwood, bronze-gray metal, mineral plaster and wall panels come from the shared library. Native reopening confirms relative links resolve, and the [adoption audit](model/asset-adoption.json) matches all **37 asset versions** to the manifest. The facade uses five full linked 4 x 2 ft limestone panels and 31 explicitly modeled perimeter cuts; the current IFC/Bonsai receipt confirms those quantities and module dimensions. Field cuts retain the stone material and physical scale. Anchor/cavity design, substrate capacity, waterproofing and movement remain unresolved.

## Envelope and moving openings

- House roof: raised 3:12 living/dining gable above real sloping ceilings and exposed driftwood frames; lower front and kitchen roofs fall at 1:12. Carport: 1:12 mono-pitch. Stepped junctions, gutters and five house downpipes are modeled; lawful outfall, system sizing, flashed assemblies and below-ground routing remain unresolved.
- The 30 ft great-room opening and separate 12 ft serving opening use actual moving panels and independent pockets. Frame 1 is closed; frame 120 is open. The attached-pergola revision passes 420 component checks across seven sampled frames, including both endpoints, without panel/wall collisions.
- The continuous counter top is at 3.10 ft, below the 3.18 ft window bottom; the exterior knee overhang is approximately 15.1 inches.
- The new pergola and entry canopy do not establish envelope performance. Low-slope roof product eligibility, wind/impact resistance, coastal corrosion, seals, screens, thermal bridging, flashings and structural headers remain unverified.

## Operating-space assumptions

The source retains approximately 5.6 ft between the island work edge and rear serving cabinetry. A conceptual 24-inch dishwasher-door projection leaves roughly 49 inches; an assumed 24-inch oven door leaves about 40 inches within its 5.3 ft aisle. These are planning envelopes rather than selected-product kinematics. Refrigerator hinges, pulls, drawers, ventilation and removal space require manufacturer review.

The primary shower approach has an approximately 54-inch local gap between the dressing-room corner and tub; the principal tub-to-vanity aisle is approximately 3.3 ft. Both bathrooms use linked elongated toilets. The primary compartment door parks outside its west wall, and the guest toilet faces west. The current rebuilt interior routes pass 30-inch swept checks; they do not certify wheelchair transfer, full door/lid operation or local accessibility.

## Output review

All thirteen native images were freshly rendered from the current model at 3200 x 2000 and inspected. Independent review approved the terrace, kitchen-to-vault, front arrival, roof/site and west-side views; the old exterior lighting stripe is absent. The open/closed comparisons retain identical cameras and real panel movement. All ten booklet pages and the three vector/PNG drawings were reviewed; floor-plan and porch label collisions were corrected. The floor plan includes the six actual frame post footprints.

The exterior hero and both interior studies use built-in Imagegen from current native sources. Invented upper-floor cues in the exterior and an altered outdoor coffee table in the vault study were corrected. These remain photographic interpretations: fine textures, daylight, backdrop, foliage and small details vary. Native renders remain beside them, with prompts and source/selected-image hashes in the gallery and provenance files.

The [current output receipt](model/output-validation.json) records model, image, plan and booklet hashes. Gallery coverage passes all six homes; checked local document links resolve. No draft or output-history folder is published.

## Open site and regulatory work

No actual parcel, survey, jurisdiction, flood elevation, orientation or geotechnical data is supplied. Access grades, setbacks, emergency egress, energy performance, wind loads, drainage, corrosion, utility connections and construction details require project-specific professional work. A fireplace is optional and is not included. See [kitchen/bath tiers](../../docs/research/kitchen-bath-tiers.md) and [roof/climate notes](../../docs/research/roof-climate-materials.md) for sourced starting points, not approvals.
