# Stainless microwave drawer, 24 inch

Original concept asset. Bottom/floor center at Z=0, front −Y, meters. Preserve scale; this is not a manufacturer product or installation approval.

Link the closed collection `microwave-drawer-24in | v001` from `microwave-drawer-24in.blend`. The explicit open/service collection is `microwave-drawer-24in | open v001`; link only one operating state at a time.

![Closed native preview](preview.png)

![Open or service native preview](preview-open.png)

See [asset.json](asset.json) for actual measured bounds, installation assumptions, fixed dependencies and the moving mechanisms. Native hinge/slide empties record `motion_kind`, `motion_axis`, `open_value` and `closed_location`; rotation values are degrees, translation values meters. The saved canonical collection is closed. Open-state geometry is a separate collection, not a scaled appliance.

[Fresh-reopen validation](validation.json) distinguishes isolated asset operation from host installation. Allow additional operating-person space and check adjacent doors, circulation, services and selected-product clearances in the home.

Source: `tools/library/build_concealed_kitchen_appliances.py`. Derivation: `appliances/built-in-oven-30in` / `v001`. CC BY 4.0, attribution Homes project contributors; source code is MIT. Preserve immutable published versions.
