# Garage Loft authoring

- `design.py` contains dimensions shared by models, drawings, and checks. Equipment proxies live in a separate module and become reusable library assets.
- Render lift positions separately without overwriting the native stored state. Vehicles and platforms move together; fixed guide columns do not move.
- Keep manufacturer planning references distinct from original geometry, structural sizing, and code verification. Record circulation and clearance assumptions.
- Generate draft views in the home's ignored `outputs/work/`; promote only after visual inspection. Keep named output files and indexes stable.
