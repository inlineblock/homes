# Modern Block — independent program and plan review

**Status: taller-volume and occupied-cantilever source and furnished-plan review complete.** The whole native-model and rendered-image review is recorded separately in `design-review.md`. This review checks concept geometry and documentation; it does not establish manufacturer suitability, engineering, code compliance or a surveyed reconstruction.

User-supplied visual direction guided the courtyard, lanai, guest/office retreat, stone base and warm timber upper volume. The user expressly authorized creative infill for undocumented layouts and views. Reference identities and identifying URLs are excluded from repository records.

## Evidence inspected

- `tools/modern_block/design.py`: two occupied levels, four bedrooms, three full baths plus powder, 542.36 m² / approximately 5,838 sq ft conditioned gross; 64 m² garage, 50 m² lanai and 24 m² upper covered balcony excluded.
- `tools/modern_block/envelope.py` and the model's emitted `opening-schedule.json`: real partition apertures, courtyard/lanai doors, stair/roof geometry and modeled openings.
- `tools/modern_block/interiors.py` and its current 103-record `interiors-layout.json`: linked furniture, kitchen equipment, bedroom clothes storage, bathing fixtures, pantry/laundry/linen shelving and dining arrangement at documented asset size.
- Current ground and upper plans generated from those inputs; actual PNG pixels and independently rendered PDF/vector previews inspected for furnishings, opening locations, dimension/room-index agreement, readable notes and unclipped content.

## Findings resolved during coordination

| Finding | Final resolution and evidence |
|---|---|
| Initial main block too small for the chosen generous courtyard composition | Coordinated floor plates yield 542.36 m² conditioned gross; the area calculation excludes the 12.04 m² upper stair void and all open exterior areas. |
| Preliminary upper bedroom/stair overlap | Final stair void x19..21.8/y8.2..12.5; east upper bedroom starts at y13, leaving an independent door from the upper gallery. |
| Stair must reach the new upper datum without expanding into rooms | Two 12-riser flights use 11 goings each and the two landing transitions: 24 rises at 171.45 mm reach 4.1148 m. The highest separate tread is one rise below the upper floor; the 2.8 × 4.3 m void remains unchanged. Revised native verification is separate. |
| Lanai initially lacked covered doors at its ends | Actual main door x10/y2..3.3 and guest-gallery door x0/y2..3.2 now both meet the covered lanai. The pool-side doors remain additional outdoor access. |
| Balcony chair overlapped the door's potential operation area | Near chair moved to x8.4/y10.6; other chair remains y15, leaving the balcony door zone free. |
| Primary shower too small for selected premium program | Adopted true-size `fixtures/shower-tray-screen-1500x1200/v001`; the 900 mm model is retained only in the secondary/guest baths. |
| Primary basin spacing too tight | Counter now 2.4 m, centered at x18.40, with basin centers x17.875 and x18.925: 1.05 m apart; its east edge x19.60 clears the dressing doorway starting x19.70; separate 72-inch tub and enclosed 1.7 × 1.8 m WC remain in the expanded 5 × 6.2 m bath. |
| Hanging storage incorrectly standing in for shelving | Pantry, laundry and upper landing use `cabinetry/oak-shelving-2ft/v001`; bedroom wardrobes keep clothes-hanging internals. |
| Dining furniture omitted the intended end seats | Eight chairs now surround the shared 8-foot dining table; furnished plan shows the service/outdoor route around them. |
| Stair room index ambiguous | Stair opening explicitly labeled 06 upstairs and 05 downstairs; 09 upstairs identifies the actual linen/landing zone. |
| Drawing/model dimensions could drift | Plans read the frozen geometry source, exact emitted furniture footprints and native opening schedule; both levels use feet/inches presentation with metric source dimensions. |

## Coordinated program checks

All four bedrooms have actual bed and wardrobe footprints, with independent routes to bathrooms. The primary dressing room has a single bank of 0.638 m-deep wardrobes in its 2 m depth; opposing cabinets would have compromised its aisle. The guest suite and office have separate doors from the guest gallery, with the guest bath accessible at its north end.

The kitchen includes cooktop, separate oven, hood/exhaust concept, 48-inch panel-ready refrigeration, sink, dishwasher, pantry and working/serving surfaces. The principal east work aisle is approximately 2.06 m; the 0.96 m north island-end passage is an explicitly narrower end route. The west stool circulation route is approximately 1.65 m and knee overhang approximately 0.38 m. Actual appliance/product installation and full operating envelopes remain unselected.

Two 4.8 × 1.9 m parking reservations align with the west garage doors. Front arrival, coat storage, service hall, pantry, laundry and separate mechanical room have identifiable routes. The main family bedrooms depend on stairs; a ground guest sleeping option exists across the sheltered lanai, without an accessibility claim.

The plans show the 4 × 8 m pool, shared outdoor seats and chaises, open pivot-screen state, upper covered balcony and a concise low-roof 1:80 drainage note. The native/gallery review supplies the closed screen state and actual exterior/interior appearance.

## Output receipt

`tools/modern_block/draw_plans.py` produces `outputs/plans/ground-floor` and `upper-floor` in PNG, editable SVG and one-page PDF formats. Both PDFs reopen through Poppler; both SVGs reopen in macOS Quick Look. The drawings have legible furnished layouts, outer dimensions, room-size index, stated area exclusions and concept-document labels. Exterior leaves are shown at the modeled open angle; a drawn aperture or symbol does not certify a complete door/appliance operation test.

Remaining professional limits are intentionally explicit: survey/parcel and tree information, grade and lawful drainage outlet; geotechnical/foundation and structural design; envelope/weather performance; pool barriers/hydraulics; product installation and system sizing; fire/life safety and accessibility review. Mechanical and electrical capacity, waste-bin internals and some controls remain concept reservations. These limits do not claim to be completed construction work.

Final coordination: the primary vanity shifted 0.275 m west to preserve dressing-door access. Both level plans were regenerated from the refreshed furniture schedule and inspected again; the upper plan now shows the revised fixture/counter relationship. Actual shared lighting comprises linear dining pendant, recessed downlights and undercabinet task bars. Custom entry pulls and hardware included in adopted cabinet assets are concept geometry; no unadopted bronze hardware-family dependency is claimed.

## Facade revision coordination

The facade-only revision retained occupied floor boundaries and room functions. The subsequent 1.2 m occupied upper-front extension adds 14.4 m² without reducing the remaining rooms; its drawing refresh is recorded below. The plan author independently inspected the pre-revision native front view, both furnished plans, exterior-opening definitions and interior placements before recommending the selected changes.

| Finding | Resolution verified in revised source and furnished plans |
|---|---|
| Three near-equal upper street windows flatten the elevation and the middle one crosses the bath partition at x17 | Two unequal openings, x10.6–16.5 for the bedroom and x17.5–21.5 for the bathroom, leave a 1.0 m solid bay centered on that partition. |
| Tall clear street glazing directly exposes primary bathing fixtures | Raised 1.10 m bathroom sill with a 1.75 m opening height, plus external timber screening; small east bath opening limited to y0.6–2.2. Nighttime and oblique privacy remain a selected-system review. |
| The entry lacks a distinct sheltered threshold | Outward portal x19.2–22 / y−1.2–0 and level porch x18.9–22 / y−1.4–0 retain the existing door and living furniture. Three equal risers reconcile the illustrative −0.53 m grade with finished floor. |
| Existing conceptual flue crosses the upper WC | Route the flue outside occupied space in the new east pier x22.12–22.72 / y2.65–4.45, to above the revised roof datum. Product routing, fire separation and listed installation requirements remain unresolved. |
| East elevation windows lack a coordinated vertical composition | Align stair openings at y8.4–12.2, keeping all facade deepening outside x22 so the stair's internal opening remains intact. |

The reviewed plan revision shows the open porch and stair footprint, dashed portal/canopy projection, upper front reveal and privacy screen, and east masonry projection. Open projected exterior features are excluded from conditioned floor area; the later enclosed occupied upper cantilever is included. These additions do not certify structural capacity, privacy, weather resistance or accessible entry.

The refreshed opening schedule and 103 linked-furniture footprints generated both current level plans. Inspection confirmed the new room-aligned front openings, external screened bathroom bay, unchanged stair/room footprint, external masonry pier and forward porch/treads. The first drawing pass exposed overlapping drainage/legend notes; their positions were corrected before promotion. PNGs and independently rasterized one-page PDFs show legible full sheets without overlaps or clipping. The SVG geometry was reopened with macOS Quick Look; that previewer's thumbnail sizing needed a temporary pixel-sized viewport for review. Repository SVGs retain their authored physical dimensions and full viewBox. The current six drawing files are promoted under `outputs/plans/`.

## Taller-volume and occupied-cantilever review

The selected revision moves the upper front enclosure to y−1.2, sets upper finished floor at +4.1148 m, and provides 12 ft clear ground ceilings / 10 ft clear upper ceilings. The intervening 18 in floor/service zone is a reservation, not an engineered framing specification. The primary suite gains the 14.4 m² strip; the unchanged 12.04 m² stair opening leaves 542.36 m² conditioned gross. The 64 m² garage raises enclosed gross to 606.36 m². No room is reduced.

The reviewer established that the existing 4.3 m-long stair space fits 24 rises without a larger opening: each 12-riser flight needs 11 goings at 280 mm plus its landing transition. The half landing remains 1.22 m deep and rises to +2.0574 m. The higher stair, guards, lighting and ceiling geometry require fresh native verification; a plan symbol alone does not verify headroom.

The updated plan source follows the upper footprint for wall edges and dimensions, shows the occupied projection dashed above the ground plan, marks the ground wall below in the upper plan, and moves reveal/screen linework to the new facade datum. Ceiling heights, floor datum, floor/service reserve, riser count and area convention are explicit drawing notes. Both plans were regenerated from the refreshed native opening schedule and 103-record furniture schedule, then visually inspected in PNG, independently rasterized PDF and reopened SVG form. The current six drawing files have been promoted.

Keep the bath's heavy fixtures behind y0 over the ground envelope; retain all internal door locations and balcony access. The new occupied cantilever requires structural design, thermal/water-control continuity, movement limits and flashing coordination. These professional design tasks are not verified by the selected footprint or available 18 in zone.

The final drawing receipt confirms the 1.2 m occupied upper projection, 542.36 m² area, unchanged stair footprint, correct bathroom divider/door locations and retained balcony access. Clear-height notes distinguish the 12 ft minimum ground datum from the 3.7776 m rear service backing and 3.7576 m garage clearances. The lanai keeps 3 m operable leaves with fixed glazing above, while its ceiling meets the 12 ft datum. No new program/plan conflicts or annotation overlaps were found in the inspected sheets. Native height measurements and structural/assembly limits remain in the separate model verification receipt.

## Primary shower service-wall closure

The occupied front extension exposed the shower's previous wall-mounted fittings. The architectural source now builds a stone plumbing wall at x20.20–21.86 / y0.02–0.18, 2.30 m (approximately 7 ft 7 in) above the upper finished floor. Its footprint and partial height are explicitly shown and labeled on the revised upper plan. The fin adjoins the east enclosure, avoiding a narrow unserviceable strip there; the front dry strip remains accessible around its west end. It does not cross the shower tray, tub, bathroom door, dressing route or WC access, and it does not change gross conditioned area. Waterproofing, plumbing installation and assembly detailing remain professional/product decisions.

The upper PNG, PDF and editable SVG were regenerated and visually inspected, including independent PDF rasterization and native vector preview, then promoted to their existing current paths. The ground drawing files are unchanged. This closes the source/plan coordination item; final rendered service-wall appearance belongs to the native output review.
