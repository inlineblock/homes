# Twin Gables authoring

- `design.py` owns feet-based footprint, room coordinates, roof datums and cameras; model coordinates use meters. The source design is an Eichler-inspired twin gable courtyard, not a literal A-frame.
- Keep two continuous parallel roof ridges and common eaves/window heads. Front entry is opaque; courtyard is revealed after entry. Never substitute the old Timber model or import its home-specific generators.
- `build.py` overwrites only this home's model and machine receipts; generated candidates go to ignored outputs/work. Root documents and galleries are separately maintained.
- Shared objects/materials must be real pinned library links. Site-specific walls, roof planes, fitted counters and structural layout stay here. The framing visualization uses steel assumptions concealed by wood-look covers, not engineered member sizes.
- `render.py` renders requested cameras only into outputs/work and does not save transient render state. Coordinate GPU use before rendering.
- Reopen through `verify.py`; inspect actual front/rear/side and interior pixels before promotion. Flat ceilings are finished clear10ft in office/support rooms and12ft in connectors; both primary bedrooms and public rooms are vaulted. The beam cover lower chords, not just the roof lining, govern clear heights.
