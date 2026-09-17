# Garage Loft authoring

- `design.py` contains dimensions shared by models, drawings, and checks. Equipment proxies live in a separate module and become reusable library assets.
- Render lift positions separately without overwriting the native stored state. Vehicles and platforms move together; fixed guide columns do not move.
- Keep manufacturer planning references distinct from original geometry, structural sizing, and code verification. Record circulation and clearance assumptions.
- Generate draft views in the home's ignored `outputs/work/`; promote only after visual inspection. Keep named output files and indexes stable.

- Verify walking envelopes against the reopened model's actual walls and open door leaf, in both lift positions. Include the separate exterior entrance, first riser, operator bay and deck-to-apron transition. Do not substitute parameter equality assertions for obstruction checks.
- Keep geometry, illustrated routes, door swings, area figures, and operator/access-protection notes aligned across drawings and the model. Review the human-access sheet before promoting attractive exterior images.

- `cars.py` owns the original detailed vehicle geometry; `finishes.py` owns refined finishes, joinery details and forecourt dressing. Keep these concerns out of the circulation/layout parameters.
- `GARAGE_SAMPLES` and `GARAGE_RENDER_PERCENT` are preview overrides. Final outputs use the native 192-sample, 2560 x 1850 defaults; don't accidentally promote undersized previews.
