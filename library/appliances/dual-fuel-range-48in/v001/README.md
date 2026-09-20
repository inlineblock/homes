# 48-inch dual-fuel range — six burners, griddle, two ovens

Original generic concept, not a purchasable or certified appliance. Floor-centered, front **−Y**, meters; do not scale.

![Closed native preview](preview.png)

![Hinged open native preview](open-preview.png)

Link collection `dual-fuel-range-48in | v001` from `dual-fuel-range-48in.blend`. The preview studio is separate and should not be instanced. Actual cavities, racks, support grates and independently hinged oven doors are modeled. Door pivot empties carry the opening angle. The closed model is the saved default; the open preview is generated from the same geometry.

See [asset.json](asset.json) for measured closed/open bounds, the suggested concept recess, exact material dependency, unresolved services and ventilation. Host open-door passage, adjacent combustible surfaces, extraction and anti-tip installation still require review.

Generate only while unpublished with `Blender --background --python tools/library/build_pro_ranges.py -- build --slug dual-fuel-range-48in`; fresh reopen with `... -- verify --slug dual-fuel-range-48in`. Published versions are immutable.
