# Coastal House authoring

- `design.py` owns dimensions, room boundaries, opening systems and deliverable view names. Keep measurements synchronized with the model, drawings and checks.
- `materials.py` imports the shared finish palette; `furniture.py` owns detailed furnishings/joinery; `openings.py` owns moving panel geometry; `build.py` assembles architecture and environment.
- `render.py` writes drafts, never saves transient camera or closed-envelope states over the native model. `COASTAL_SAMPLES` and `COASTAL_PERCENT` are draft-only overrides.
- Verify the reopened file, relative assets, measured area, walking routes and panel clearance across the motion range. Report geometric checks separately from engineering or product approval.
- Rebuilds overwrite the generated native file. Inspect Git status and preserve any manual user model edits first. Published library versions are immutable.
- `envelope.py` owns low roof pitches, drainage concept, carport, road/arrival and front garden. Preserve the revised entry/bedroom dimensions from `design.py`; `BEDS` is shared by model and plan. Never alter furniture placement only in a drawing.
- Use `common.shared_assets.load_catalog` with explicit selected keys and `dependencies` for pinned per-home metadata. Coastal adopts olive, paver and wardrobe v001 plus grass/shrub v002. Keep the original garage coupe generator available for the illustrated parking models.
- All eleven image states must represent the current design, including the living retreat. Re-render every affected view after geometry changes; a reviewed view can remain when the change lies outside its visible content. Record that decision in output QA. Final images are 3200 x 2000 at 256 maximum Cycles samples for front/roof/side and closed-terrace views, 512 for interiors/counters and the open-terrace hero; drafts can use render environment overrides only in ignored work output.
- Verify a 36-inch parking/road route, separate 30-inch driver approaches, guest wardrobe access, measured entry clear width and panel motion. These are concept geometry checks, not accessible-route, turning-radius, weather or safety approvals.

- `suite.py`, `bath_finishes.py`, `service.py`, `appliances.py` and `lighting_hardware.py` own complete household provisions. Keep toilet-room wall names distinct from fixture cleanup; assert actual WC walls exist. Guest storage, primary dressing and appliances must be checked as linked instance geometry.

- The primary wing is 18 x 26 ft: preserve the expanded 54-inch shower approach, 18 x 12 ft king bedroom and enclosed WC door parked outside its compartment. Both toilets use the pinned shared fixture. Check guest shower, toilet and basin access separately; an entry-only bathroom route is insufficient.

- `verandah.py` owns the supported slatted pergola, low screen and shared drawing dimensions for the entry canopy. Slatted shade is not a rainproof roof. `gardens.py` owns grouped linked planting, actual terrain contact and route exclusions. `comfort.py` owns shared living/dining placement, selective finishes and original room artwork; `design.py` owns outdoor conversation placements.
- Build with `--factory-startup` to keep the native model free of unrelated add-on workspace links. Reopen with the geometry verifier and adoption audit. If Bonsai dependencies need repair, use the supported extension startup/install workflow and separately verify a real IFC import; do not infer success from a loaded menu alone.
- Include actual evaluated collection instances in walking checks. For curves, use tessellated visible geometry rather than control-handle bounds. Preserve clearance diameters and route destinations; investigate any failure instead of excluding linked furniture or hardware.
