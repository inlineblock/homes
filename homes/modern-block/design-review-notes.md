# Modern Block — independent program and plan review

**Status: source and furnished-plan review complete.** The whole native-model and rendered-image review is recorded separately in `design-review.md`. This review checks concept geometry and documentation; it does not establish manufacturer suitability, engineering, code compliance or a surveyed reconstruction.

User-supplied visual direction guided the courtyard, lanai, guest/office retreat, stone base and warm timber upper volume. The user expressly authorized creative infill for undocumented layouts and views. Reference identities and identifying URLs are excluded from repository records.

## Evidence inspected

- `tools/modern_block/design.py`: two occupied levels, four bedrooms, three full baths plus powder, 527.96 m² / approximately 5,683 sq ft conditioned gross; 64 m² garage, 50 m² lanai and 24 m² upper covered balcony excluded.
- `tools/modern_block/envelope.py` and the model's emitted `opening-schedule.json`: real partition apertures, courtyard/lanai doors, stair/roof geometry and modeled openings.
- `tools/modern_block/interiors.py` and its current 103-record `interiors-layout.json`: linked furniture, kitchen equipment, bedroom clothes storage, bathing fixtures, pantry/laundry/linen shelving and dining arrangement at documented asset size.
- Current ground and upper plans generated from those inputs; actual PNG pixels and independently rendered PDF/SVG previews inspected for furnishings, opening locations, dimension/room-index agreement, readable notes and unclipped content.

## Findings resolved during coordination

| Finding | Final resolution and evidence |
|---|---|
| Initial main block too small for the chosen generous courtyard composition | Coordinated floor plates yield 527.96 m² conditioned gross; the area calculation excludes the 12.04 m² upper stair void and all open exterior areas. |
| Preliminary upper bedroom/stair overlap | Final stair void x19..21.8/y8.2..12.5; east upper bedroom starts at y13, leaving an independent door from the upper gallery. |
| Missing uppermost stair tread | Upper flight now includes the flush top tread spanning y8.2..8.48 at 3.6 m, adjoining the upper floor. Twenty-two equal 163.64 mm rises and 280 mm tread modules remain explicit; full professional stair review is separate. |
| Lanai initially lacked covered doors at its ends | Actual main door x10/y2..3.3 and guest-gallery door x0/y2..3.2 now both meet the covered lanai. The pool-side doors remain additional outdoor access. |
| Balcony chair overlapped the door's potential operation area | Near chair moved to x8.4/y10.6; other chair remains y15, leaving the balcony door zone free. |
| Primary shower too small for selected premium program | Adopted true-size `fixtures/shower-tray-screen-1500x1200/v001`; the 900 mm model is retained only in the secondary/guest baths. |
| Primary basin spacing too tight | Counter now 2.4 m, centered at x18.40, with basin centers x17.875 and x18.925: 1.05 m apart; its east edge x19.60 clears the dressing doorway starting x19.70; separate 72-inch tub and enclosed 1.7 × 1.8 m WC remain in the 5 × 5 m bath. |
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

`tools/modern_block/draw_plans.py` produces `outputs/plans/ground-floor` and `upper-floor` in PNG, editable SVG and one-page PDF formats. Both PDFs reopen through Poppler; both SVGs render through ImageMagick. The drawings have legible furnished layouts, outer dimensions, room-size index, stated area exclusions and concept-document labels. Exterior leaves are shown at the modeled open angle; a drawn aperture or symbol does not certify a complete door/appliance operation test.

Remaining professional limits are intentionally explicit: survey/parcel and tree information, grade and lawful drainage outlet; geotechnical/foundation and structural design; envelope/weather performance; pool barriers/hydraulics; product installation and system sizing; fire/life safety and accessibility review. Mechanical and electrical capacity, waste-bin internals and some controls remain concept reservations. These limits do not claim to be completed construction work.

Final coordination: the primary vanity shifted 0.275 m west to preserve dressing-door access. Both level plans were regenerated from the refreshed furniture schedule and inspected again; the upper plan now shows the revised fixture/counter relationship. Actual shared lighting comprises linear dining pendant, recessed downlights and undercabinet task bars. Custom entry pulls and hardware included in adopted cabinet assets are concept geometry; no unadopted bronze hardware-family dependency is claimed.
