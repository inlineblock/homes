# Coastal House design review

## Current design and evidence status

The current design is a **warm coastal verandah house**. A supported timber pergola, a west conversation terrace and a planted entry court give the long glazed house comfortable places to arrive, gather and linger. Warm mineral plaster, pale perimeter oak, a smoked-oak island and tactile oatmeal/olive textiles establish a coordinated palette.

**Current native geometry verified:** the [refreshed receipt](model/model-validation.json) confirms a successful reopen of the house-attached pergola and relocated seating. There are exactly two outer posts at (9,56) and (41,56) ft, zero house-side columns, ledger contact with the header face, full 30 ft sliding-wall coverage and a 0.08 ft slat-to-soffit gap. Forty-five open slats are modeled. Nineteen interior routes, four terrace routes, two arrival routes and two driver approaches passed. Seven animation frames produced 420 panel-component checks without panel/wall collisions, and both open apertures remain clear. The [adoption receipt](model/asset-adoption.json) confirms 33 asset versions matching the manifest. These are geometry and static-route checks, not engineering or occupied-seating approval.

**Current outputs reviewed:** all eleven native renders were regenerated from the verified attached-pergola model and inspected before promotion. The replacement Imagegen hero, furnished floor/site plans and all eight booklet pages were also visually reviewed. The [output receipt](model/output-validation.json) records current hashes and scope. The Imagegen study remains a surface/site interpretation rather than exact geometry evidence.

**House IFC verified:** the current closed-envelope IFC4 export has [zero schema errors](model/ifc-validation.json). A fresh [Bonsai 0.8.5 import](model/bonsai-validation.json) in Blender 4.5.14 LTS reopened 1,012 mesh objects and checked the actual imported members: two outer pergola posts, zero house-side posts, 45 open slats and two entry-canopy supports. Source Blender and IFC hashes are recorded in the receipt. This establishes schema/import/tessellation, not engineered construction documentation.

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

Warm-limestone plaster replaces the uniformly pale wall palette. The smoked-oak island remains distinct from the lighter perimeter cabinetry and serving counter. Linked indoor furniture, a woven oatmeal rug and olive cushions give the living retreat texture; original coastal relief art and a linear dining pendant add deliberate focal points. The existing fitted chaise extension remains local to the room.

The complete kitchen retains a 36-inch induction cooktop, 30-inch oven, 36-inch hood, 24-inch dishwasher, 48-inch panel-ready refrigerator, sink, pantry and waste/recycling. Appliance bodies occupy genuine cabinet bays. A vertical hood duct allowance is modeled; final exterior termination, fan sizing, makeup air, fire stopping, services and product clearances remain unresolved.

The lighting concept retains 25 shared downlights with ceiling cutouts, concealed kitchen task lighting, an entry opal pendant and the dining focal pendant. Shared satin-bronze pulls and door levers provide coordinated hardware. These are original visual assets, not rated products or verified photometry.

The [asset schedule](assets/README.md) records the exact pinned families. The new furniture/textile families are shared library assets rather than private duplicates. Native reopening confirms the relative asset links resolve, and the refreshed adoption audit matches all 33 asset versions to the manifest.

## Envelope and moving openings

- House roof: low 2:12 standing-seam gable above level ceilings. Carport: 1:12 mono-pitch. House gutters have modeled fall toward end downpipes; lawful outfall, system sizing and below-ground routing are unresolved.
- The 30 ft great-room opening and separate 12 ft serving opening use actual moving panels and independent pockets. Frame 1 is closed; frame 120 is open. The attached-pergola revision passes 420 component checks across seven sampled frames, including both endpoints, without panel/wall collisions.
- The continuous counter top is at 3.10 ft, below the 3.18 ft window bottom; the exterior knee overhang is approximately 15.1 inches.
- The new pergola and entry canopy do not establish envelope performance. Low-slope roof product eligibility, wind/impact resistance, coastal corrosion, seals, screens, thermal bridging, flashings and structural headers remain unverified.

## Operating-space assumptions

The source retains approximately 5.6 ft between the island work edge and rear serving cabinetry. A conceptual 24-inch dishwasher-door projection leaves roughly 49 inches; an assumed 24-inch oven door leaves about 40 inches within its 5.3 ft aisle. These are planning envelopes rather than selected-product kinematics. Refrigerator hinges, pulls, drawers, ventilation and removal space require manufacturer review.

The primary shower approach has an approximately 54-inch local gap between the dressing-room corner and tub; the principal tub-to-vanity aisle is approximately 3.3 ft. Both bathrooms use linked elongated toilets. The primary compartment door parks outside its west wall, and the guest toilet faces west. The current rebuilt interior routes pass 30-inch swept checks; they do not certify wheelchair transfer, full door/lid operation or local accessibility.

## Completed output review

All **eleven native gallery views** were regenerated and reviewed: rear open/closed, great room, serving counter open/closed, front arrival, roof/parking, west garden, entry hall, primary bath and living retreat. The attached ledger, two outer posts and open slats agree across exterior and interior angles. No older view was retained. Reviewed the single-level furnished plan, arrival/roof site plan and all **eight booklet pages**, including captions, dimensions, image framing and page margins.

The first-image Imagegen study derives from the final open-terrace native render. The exact prompt and current source/image hashes are saved. Review confirmed full opening coverage, two outer posts and no house-side columns; material, foliage and illustrative shore details remain interpreted. The native blue foreground backdrop artifact becomes continuous sand in the study, not a pool. Native model/IFC receipts and the photographic study remain distinct evidence.

The repository gallery check passes all six homes, including eleven Coastal views, one occupied-level plan and three signature features. Relative links in the changed home, catalog and software/library documents resolve.

## Open site and regulatory work

No actual parcel, survey, jurisdiction, flood elevation, orientation or geotechnical data is supplied. Access grades, setbacks, emergency egress, energy performance, wind loads, drainage, corrosion, utility connections and construction details require project-specific professional work. A fireplace is optional and is not included. See [kitchen/bath tiers](../../docs/research/kitchen-bath-tiers.md) and [roof/climate notes](../../docs/research/roof-climate-materials.md) for sourced starting points, not approvals.
