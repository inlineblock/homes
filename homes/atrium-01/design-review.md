# Atrium 01 — coordinated concept review

The courtyard-ring revision follows the recorded [design intent](design-intent.md), [program](program.md) and create-home workflow. Independent architecture, layout, interiors, site/assets and visual reviews were synthesized before final output promotion. The original low post-and-beam character, open courtyard, three bedrooms/three bathrooms and walnut/sage kitchen remain; the internal plan is rebuilt around a sheltered arrival and continuous enclosed circulation.

## Resolved in the model

- Entry now reaches both wings indoors. A separate two-car carport leads to a covered walk; the open-air courtyard is a destination, not a required route.
- Every bedroom has real clothing storage. Pantry, laundry, linen, cleaning and utility storage are distinct. The living cabinet moved north to keep the turn toward dining clear.
- Kitchen worktops have real sink/cooktop apertures and usable equipment cavities. Wide paneled refrigeration, dishwasher, single separate oven, induction cooking, extraction and waste storage are modeled. A continuous hollow exhaust route passes through an actual roof opening to an open-sided cowl; detailed product/MEP design is unselected.
- Primary suite includes two basins, separate tub and shower, enclosed WC and private vestibule. Door hinges and pocket directions were coordinated with actual fixtures and standing zones. Lower vanity bases give appropriate basin rim height.
- Glazing is fitted to use: kitchen windows rise above counters; bedroom glass has paired raised/lowered opaque roller shades; courtyard and rear sliders have sampled operating states. Shade edges are not a certified light seal.
- Ceiling plane is 10 ft 6 in, principal beam clearance 9 ft 6 in and local service ceiling 9 ft. Recessed lights occupy real apertures. Timber framing, eaves and covered edges are expressed. One welded low-slope membrane fixes the mismatched roof joints; gutters/downpipes and courtyard drains provide a concept water route.

## Verification evidence

| Evidence | Result and scope |
| --- | --- |
| [Native checks](model/model-validation.json) | Fresh Blender 4.5.14 LTS reopen; zero failures. Measured 2,400 sq ft, three actual beds/three baths, 53 relative library links. Evaluated linked meshes, fixture/storage access, door/slider operations, parking and all 19 indoor program destinations checked. |
| [Actual adoption](model/asset-adoption.json) | Shared repository checker confirms native pins match all 53 manifest versions; actual placement/material use and schedule present. |
| Kitchen operation | Conservative published equipment envelopes plus operator space: fridge 900 mm, dishwasher 845 mm, oven 848 mm remaining. These are conceptual reservations, not selected-manufacturer installation approval. |
| Doors and shades | Twelve architectural doors and three sliders sampled; ten paired shade bays checked against actual glass and nearby geometry. Minimum cassette gap 12 mm, beam clearance 31.2 mm, jamb overlap 17 mm. |
| [IFC4 export](model/ifc-validation.json) | 738 classified products, zero schema errors; source/native hashes recorded. Classified concept geometry, not complete semantic BIM or an engineered building. |
| [Fresh Bonsai import](model/bonsai-validation.json) | 738 mesh objects imported; independent IFC tessellation matches selected slab/wall/roof bounds exactly. Native file and saved user preferences unchanged. |
| [Visual output record](model/output-validation.json) | All final native/photo image dimensions and hashes; review scope and rendering settings recorded. |
| [Camera reopen](model/gallery-validation.json) | All 14 saved named cameras match source definitions. Cutaway and lowered-shade states exist only during rendering. |
| [Plan review](outputs/plans/plan-validation.json) | Furnished floor and illustrative site drawings promoted as SVG, PNG and PDF. Actual PNGs and rasterized PDFs inspected; both PDFs reopen, with source/output hashes recorded. |

Final native source SHA-256: `ea9fb6d7b49622bcdfead03564806f0c6c3c813f5a6c44bb317ba8e9d2fb3eda`.

## Visual closure and photographic tour

All 14 final native views were inspected by the author and an independent reviewer. The review resolved obscuring site trees, kitchen tile composition, missing living-room storage/reading light, bedroom privacy, incomplete bath coverage, the blank foreground in the gallery camera and roof seam gaps. Final views cover three overall exterior angles, human-scale arrival, indoor gallery, kitchen in both directions, living room, open courtyard, primary bedroom and bath, alternate lowered privacy shades and furnished roof-off layout. No blocking visual defect remained at native promotion.

The completed photographic tour contains ten corresponding built-in Imagegen edits: front, rear and elevated roof/site, both kitchen directions, courtyard, living, primary bedroom, double vanity and tub/shower. [Prompts and source/output provenance](outputs/photo-study.md) distinguish the generated illustrations from native evidence. Each selected result was compared with its source for architecture and operating state; richer surrounding planting is illustrative context. Two focused corrections restored the courtyard slab paving and removed an invented raised garden wall outside the bedroom. The home landing page retains every native view and plan beside these studies. The repository gallery checker passes all eight current home records, including Atrium's 14 native views, ten photographic studies, occupied-level plan and three signature features.

## Professional development still required

No surveyed parcel, actual climate, orientation, soils, grade or approved road connection is asserted. Structural member/foundation sizing, lateral resistance, waterproofing details, roof/court drainage capacity and discharge, envelope performance, mechanical loads/flows, product selection, accessibility/code review and approvals require project-specific professional work. The nominal area includes wall thickness and excludes the open court, carport, canopies and terraces; it is neither net usable nor appraised area. These conceptual limits are separate from the checked functional geometry.

Reproduction commands and draft/final handling are in the [authoring guidance](../../tools/atrium01/AGENTS.md). Drawing tools require CairoSVG/PyMuPDF; optional IFC/Bonsai runtime paths remain process-local.
