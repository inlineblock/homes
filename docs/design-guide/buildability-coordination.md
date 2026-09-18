# Buildability and coordination

Checked 2026-09-17. Use this chapter when turning a home brief into coordinated geometry, and again before presenting it as ready for a later stage. It provides decisions and evidence gates, not engineering calculations, a construction specification, or local code approval. Unknown site conditions remain unknown; draw an illustrative site only when it is explicitly labeled as such.

Start with [the home design standard](../home-design-standard.md), the home's brief, and the [shared asset workflow](../assets.md). The checklists below are repository working methods informed by the linked primary sources. Actual professional scope and deliverables depend on the project agreement and jurisdiction.

## 1. State what the evidence supports

Track status **per system or claim**, rather than assigning an impressive label to the entire house. A native model, an IFC export and a beautiful image provide different evidence. AIA distinguishes schematic spatial studies from design development's coordinated systems and the more detailed information needed for construction documents. [AIA: architect's basic services](https://www.aia.org/resource-center/defining-the-architects-basic-services)

| Evidence level | Required record | What it does not establish |
| --- | --- | --- |
| Concept modeled | Named geometry exists in the native file; plan, section and render agree. | Capacity, assembly performance or product suitability. |
| Dimensioned / coordinated | Actual clearances, datums and interfaces recorded; conflicts checked in relevant operating states. | Structural or regulatory approval. |
| Product selected | Exact model, current manufacturer documents, relevant configuration, installation limits and service envelope recorded. | Suitability without checking the project conditions. |
| Engineered | Responsible qualified professional's project-specific design, assumptions, calculations/details and revision identified. | Permit issuance or correct field installation. |
| Permitted | Issued authority document, scope, date, conditions and corresponding drawing revision retained. | Completion, final inspection or permission to occupy. |
| Constructed / commissioned | As-built evidence, inspections, measured tests, deficiencies and handover documents retained. | Performance of untested systems or future maintenance. |

Use a short ledger: **item; decision; status; evidence path; unresolved issue; next responsible party**. For example, “rear glass header: conceptual member modeled; span and bearing locations shown; size and deflection unresolved; structural engineer required.” Never change that entry to “engineered” because an exporter recognizes an `IfcBeam`.

## 2. Establish the site before choosing the foundation

Choose either **illustrative terrain** or **verified parcel basis**. For a real site, request or identify boundary/topographic survey, datum, easements, utilities, access limits, setbacks and relevant hazard information. Confirm where water and wastewater can legally go; a downhill pipe does not establish an acceptable discharge point. FEMA's coastal siting checklist includes topography, soils, groundwater, erosion history, infrastructure and development restrictions. Its coastal examples do not replace a mountain-site investigation. [FEMA P-55, volume I, chapter 4](https://www.fema.gov/sites/default/files/2020-08/fema55_voli_combined.pdf)

For slopes, record existing and proposed grade separately. Reserve zones for cut/fill, retaining, temporary excavation support, drainage, foundation access and protected trees. Seek geotechnical advice appropriate to soil, slope, rock, groundwater and neighboring structures before selecting bearing assumptions or retaining details. A picturesque walkout requires an actual landing and a continuing route; do not hide a cliff immediately beyond the door.

**Concept evidence:** longitudinal site section from road through house to downhill boundary; floor datums; approximate excavation envelope; driveway and pedestrian approach; water-flow arrows; list of assumptions awaiting survey/geotechnical confirmation.

## 3. Draw gravity and lateral load paths

Choose an initial framing strategy—bearing walls, posts/beams, or a coordinated combination—before removing walls for views. Trace roof and floor loads to supports and foundations. Independently trace the resistance to lateral forces and uplift. PNNL describes continuous positive connections through roof, walls and foundations; isolated attractive beams are not a complete structural strategy. [PNNL: continuous load path](https://basc.pnnl.gov/resource-guides/continuous-load-path-provided-connections-roof-through-wall-foundation)

For a wide sliding-glass wall, reserve header depth, end bearings, columns or wall piers, lateral-system locations and foundations. Coordinate head tracks, pocket depth and service access with those reserves. Consider whether deflection could affect door operation, without inventing an allowable deflection or beam size. If an architectural goal depends on an unobstructed corner or extreme span, mark it as an engineering driver early.

Carry site-specific snow, drifting, sliding snow, wind, seismic and relevant imposed loads into the engineering brief. Do not infer capacity from member appearance, material name or a library preview. Heavy tubs, masonry, planters, hot tubs, vehicle lifts and concentrated equipment loads need explicit flags.

**Concept evidence:** support grid over each floor, two structural sections, marked transfer locations, conceptual member-depth allowances, and an unresolved-load list.

## 4. Resolve decks, carports and retaining interfaces

Choose attached or freestanding deck support deliberately. Show post-to-footing logic, beam/joist direction, lateral restraint, guards, stairs and the interface with the house. Check that supports do not occupy walkout exits or parking maneuvering space. PNNL calls for connected load paths and support appropriate to wind and cumulative snow loads for attached porches, carports and decks. [PNNL: exterior attachments](https://basc.pnnl.gov/resource-guides/porches-carports-and-deck-attachments)

Distinguish an open deck from a waterproof terrace over occupied or intentionally dry space. Open board gaps do not create a weatherproof ceiling below. If the lower patio must stay dry, reserve a selected drainage/waterproofing system and its outlet, inspection and cleaning access. Keep wood clear of soil and persistent wetting according to the eventual assembly specification.

For retaining, show retained height, surcharge sources, approximate footing/excavation reserve, groundwater/drainage intent and guard conditions. Do not assume a basement wall and a landscape retaining wall have interchangeable duties. Below-grade moisture details must coordinate the wall, slab and drainage system; hydrostatic conditions require specific consideration. [DOE/PNNL: residential moisture control, foundation chapters](https://basc.pnnl.gov/sites/default/files/resource/Lstiburek%20Moisture%20Control%20for%20Residential%20Buildings%20Final%2010-23-20.pdf)

## 5. Separate garage operation from living-space performance

Model parked vehicles, opening doors, circulation, storage, garage-door tracks and motors together. Preserve a pedestrian route to the house and any stair in ordinary parked conditions. For lifts, use the selected manufacturer's motion envelope, operating position, pit, controls, access and maintenance requirements; a raised-car render proves none of these.

Draw the complete garage-to-house boundary through walls, ceiling, floor edges and penetrations. Identify the locally required separation assemblies and doors for professional/code review; do not describe generic drywall as a certified fire-resistance assembly. Air sealing, fire protection and thermal insulation are separate coordination tasks. PNNL documents contaminant paths through shared framing and the need for a continuous garage air barrier. [PNNL: attached garage air sealing](https://basc.pnnl.gov/resource-guides/air-sealing-attached-garage)

An upstairs game room needs its own resolved heating/cooling distribution, outdoor air strategy, acoustic separation and service access. Avoid using garage air as the home's return-air source. NIST's garage transport research reinforces that contaminant movement depends on actual leakage and pressure relationships, not just the presence of a separating wall. [NIST: garage-to-house pollutant transport](https://www.nist.gov/publications/air-and-pollutant-transport-attached-garages-residential-living-spaces)

## 6. Verify stairs and guards in section

Choose the stair location with the floor opening, structure and ceiling zones visible. Record floor-to-floor height, finished floor build-ups, consistent riser count, tread geometry, usable width, landings, handrail/guard zones and actual headroom along the walking line. Include door swings and furniture movement at both ends. Review local requirements before citing any minimum as applicable.

Check stair access in all intended states: cars parked, lift moving or parked, adjacent doors open, and dining chairs pulled back. A plan-only stair symbol is insufficient. Show guards at every exposed floor edge and stair opening; leave intended entry points open. Guard geometry and fixing strength remain distinct checks. Recheck finished dimensions after flooring, waterproofing or ceiling changes.

## 7. Trace water, air and thermal control continuously

Choose an enclosure assembly suitable to exposure and climate, then trace each control layer at roof/wall, window/wall, wall/foundation, balcony/door and service penetrations. Roof pitch alone does not resolve runoff: show collection, overflow strategy, discharge and maintenance access. DOE distinguishes rain, ground moisture, capillary action, air transport and vapor diffusion; one decorative surface does not control every mechanism. [DOE: moisture flow](https://bsesc.energy.gov/energy-basics/building-enclosure-building-science-intro-moisture-flow)

For the long indoor/outdoor glass wall, coordinate flush-looking thresholds with drainage, flashing, track cleaning, wind-driven rain and accessibility intent. A countertop passing through an opening needs a weather-seal and thermal-interface concept; do not model solid material through a closed sash.

For baths, distinguish finish tile from the waterproof system. Coordinate shower slope/drain, membrane continuity, corners, penetrations, thresholds, tub access and any floor recess with framing. PNNL notes that ordinary cement board is water-resistant rather than inherently waterproof. [PNNL: tub and shower backing](https://basc.pnnl.gov/resource-guides/cement-board-installed-behind-tile-and-panel-tub-and-shower-enclosures)

**Concept evidence:** one representative wall section and enlarged sketches of the highest-risk junctions. Use explicit “assembly unresolved” notes where details have not been chosen.

## 8. Reserve services before polishing ceilings

Choose plausible equipment locations and reserve routes for supply/return air, outdoor air, exhaust, plumbing, electrical distribution and controls. Then check conflicts against beams, stairs, glazing pockets and cabinets. PNNL recommends early coordination of equipment and compact duct routing before construction drawings are finalized. Its guidance relies on room loads and proper duct design rather than sizing by rendered room appearance. [PNNL: compact air distribution](https://basc.pnnl.gov/resource-guides/compact-air-distribution)

Show filter changes, valve access, electrical working areas and a removal route for the largest replaceable equipment. Include condensate and leak-management intent, kitchen exhaust/makeup-air coordination, dryer exhaust or selected ventless-dryer provisions, and outdoor-unit sound/airflow zones. Conceal equipment only when it remains operable and maintainable. Count chase and ceiling depth in the section; never route ducts through solid beams by omission.

Coordinate sequencing too: some air-barrier surfaces must be installed before a chase becomes inaccessible. PNNL's dropped-ceiling duct guide explicitly coordinates framing, drywall, HVAC and other trades. [PNNL: ducts in dropped ceilings](https://basc.pnnl.gov/resource-guides/ducts-dropped-ceilings)

## 9. Use gates for cost, construction and handover

| Gate | Decision and record |
| --- | --- |
| Brief / feasibility | Program priorities; site unknowns; budget basis; consultant needs; preliminary access and infrastructure constraints. |
| Coordinated concept | Plans/sections agree; baseline home functions work; structural/service reserves exist; exceptional spans, retaining and custom glazing identified for pricing. |
| Design development | Selected assemblies and major products coordinated; specialist input; updated estimate with scope, exclusions, location/date and contingencies. |
| Construction documentation / procurement | Detailed interfaces, schedules and specifications; professional review; approvals where required; lead times, substitutions and responsibilities tracked. |
| Construction | Contractor-led sequencing and temporary works; inspections before concealment; approved changes carried back into drawings; unresolved defects recorded. |
| Handover | As-built documents, product manuals, commissioning results, access instructions, maintenance plan and outstanding-item closeout. |

Treat these as planning gates, not authorization to start site work. Include excavation access, lifting large glazing, temporary weather protection, dry-in, rough services, enclosure inspections, finishes and testing in the construction discussion. Site safety and temporary works require the responsible construction team.

Estimate whole assemblies, not visible finishes alone. Compare initial cost with cleaning, recoating, access, energy, replacement and repair implications over an explicit period. NIST's life-cycle-cost framework supports considering future costs; federal assumptions and discount rates are not automatically appropriate to a private home. [NIST Handbook 135](https://www.nist.gov/publications/life-cycle-costing-manual-federal-energy-management-program-0)

Testing is distinct from modeling. DOE's residential commissioning research includes measured leakage, ventilation, airflow and room-pressure checks. Record only the tests actually performed and their scope; modeled systems are not commissioned systems. [DOE: whole-house design and commissioning](https://www1.eere.energy.gov/buildings/publications/pdfs/building_america/project_home_again_whdesign.pdf)

## 10. Keep reusable components and project decisions aligned

Follow [the immutable asset version/fork workflow](../assets.md): link the pinned suitable version; publish a new version or distinct asset for changed reusable geometry; explicitly adopt it per home. Preserve original rights and dependencies. A shared asset's physical dimensions do not certify its capacity, code compliance or suitability for a new exposure.

Keep project-specific orientation, clearances, foundations, drainage and services in the home's decision records. When a component changes, recheck its interfaces, rebuild affected plans/renders, reopen native links and update the dependency schedule. The completion review must name remaining professional/site checks without concealing actual concept failures. A missing stair route is a design defect to fix now; an uncalculated beam is an explicit engineering task for the next appropriate stage.
