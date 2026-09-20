# Landscape plant library and expansion plan

The current library has six plant families, not enough for varied home settings. This plan adds **35 proposed families**: five mountain, five desert, five water-wise/xeriscape, five coastal, five suburban and ten fruit-tree families. Each row is a modeling proposal, **not an available Blender asset or a verified planting specification**. Do not add a proposed ID to a home's dependency manifest until the asset is built, reviewed and actually linked.

The three requested forms per family are a first production brief: at least **105 form/state concepts**, not 105 finished models. Reuse structure and materials where botanically appropriate while making meaningful silhouettes, leaf forms and growth habits. Additional useful variations are encouraged.

## Available now

| Existing family | Current catalog version | What it supplies |
| --- | --- | --- |
| [Mountain conifer](mountain-conifer/v002/asset.json) | v002 | Tall evergreen forest silhouette |
| [Broad-canopy oak](broad-canopy-oak/v001/asset.json) | v001 | Large spreading broadleaf canopy |
| [Olive tree](olive-tree/v001/asset.json) | v001 | Small ornamental tree |
| [Sage shrub](sage-shrub/v002/asset.json) | v002 | Generic rounded shrub |
| [Ornamental grass](ornamental-grass-clump/v002/asset.json) | v002 | Generic grass clump |
| [Flowering perennial](flowering-perennial-clump/v001/asset.json) | v001 | Generic flowering accent |

Earlier versions remain available to existing pins. These meshes must not be relabeled as the species below without reviewing leaf, branching and growth-habit differences. Six names here describe available asset families, not an assertion of botanical accuracy.

## Choosing among the new families

The groups are browse tags, not mutually exclusive ecosystems or ready-made planting prescriptions. Match the actual region, elevation, winter cold, summer heat, sun, soil, water and coastal exposure before adoption. Use regional native choices where appropriate and check local invasive restrictions. A coastal setting may be cool Pacific, humid subtropical or sheltered inland; a desert may be hot or cold. Xeriscaping is water-wise landscape design and need not look like a cactus garden.

Botanical source links support the selection notes. The shape/state variants are original asset-production proposals; they do not promise a cultivar's performance or a universal mature size. Record actual cultivar/rootstock and modeled dimensions when building, and keep modeled size separate from expected mature spread. Establishment irrigation and a plant's permanent water needs must be considered separately.

All entries below have status **planned / not modeled**. IDs are proposed family slugs under `library/landscape/`; no version or availability is implied.

## Mountain — five new families

| Proposed family / ID | Three starting forms | Selection notes and botanical source |
| --- | --- | --- |
| Quaking aspen (*Populus tremuloides*) · `quaking-aspen` | Slender young tree; mature pale-trunk grove; golden autumn grove | Cool mountain settings; not a default for hot dry valleys. [USU Extension](https://extension.usu.edu/forestry/tree-identification/poplar-aspen/quaking-aspen) |
| Rocky Mountain maple (*Acer glabrum*) · `rocky-mountain-maple` | Small branching tree; broad multi-stem shrub; yellow autumn canopy | Foothill/montane understory. [CSU native shrubs](https://extension.colostate.edu/resource/native-shrubs-for-colorado-landscapes/) |
| Saskatoon serviceberry (*Amelanchier alnifolia*) · `saskatoon-serviceberry` | Upright flowering shrub; berry-bearing thicket; autumn foliage | Foothill to subalpine candidate; preserve its open branching habit. [CSU native shrubs](https://extension.colostate.edu/resource/native-shrubs-for-colorado-landscapes/) |
| Red-osier dogwood (*Cornus sericea*) · `red-osier-dogwood` | Leafy arching shrub; white-flowering mass; bare red winter stems | Moist understory/streamside placement, not a generic shrub for dry slopes. [CSU native shrubs](https://extension.colostate.edu/resource/native-shrubs-for-colorado-landscapes/) |
| Kinnikinnick (*Arctostaphylos uva-ursi*) · `kinnikinnick` | Small evergreen mat; broad irregular groundcover; berry-bearing rock-edge patch | Well-drained gravelly ground and suitable light exposure. [CSU native shrubs](https://extension.colostate.edu/resource/native-shrubs-for-colorado-landscapes/) |

## Desert — five new families

| Proposed family / ID | Three starting forms | Selection notes and botanical source |
| --- | --- | --- |
| Blue palo verde (*Parkinsonia florida*) · `blue-palo-verde` | Young open canopy; mature green-barked spreading tree; yellow bloom | Sonoran desert character; consider thorns and flower/pod litter near paths. [University of Arizona Extension](https://extension.arizona.edu/publication/mesquite-and-palo-verde-trees-urban-landscape) |
| Desert willow (*Chilopsis linearis*) · `desert-willow` | Single-trunk flowering tree; multi-stem canopy; dormant branching with seed capsules | Dry-wash/foothill character; a flowering tree distinct from true willows. [UA Extension](https://yavapaiplants.extension.arizona.edu/chilopsis-linearis) |
| Ocotillo (*Fouquieria splendens*) · `ocotillo` | Sparse leafless canes; rain-leafed canes; red flower tips | Moisture-dependent foliage; avoid permanently lush specimens in every scene. [UA Extension](https://extension.arizona.edu/publication/cactus-agave-yucca-and-ocotillo) |
| Parry’s agave (*Agave parryi*) · `parry-agave` | Compact blue-gray rosette; offset colony; mature flowering stalk | Upland Southwest option; check site suitability separately from low-desert plants and keep spines out of routes. [UA Arboretum](https://arboretum.arizona.edu/agave-parryi-parrys-agave) |
| Fishhook barrel cactus (*Ferocactus wislizeni*) · `fishhook-barrel-cactus` | Small rounded barrel; mature leaning column; flower-ring specimen | Sonoran/Southwest accent with distinct ribs and hooked spines; keep clear of circulation. [National Park Service](https://www.nps.gov/tont/learn/nature/cacti.htm) |

## Xeriscape / water-wise — five new families

These choices give water-wise landscapes grasses, flowers and shrubs rather than another all-cactus palette.

| Proposed family / ID | Three starting forms | Selection notes and botanical source |
| --- | --- | --- |
| Blue grama (*Bouteloua gracilis*) · `blue-grama` | Young green bunch; arching eyelash seedheads; dormant straw-colored bunch | Sunny prairie/steppe character; model its distinctive asymmetric seedheads. [CSU native grasses](https://extension.colostate.edu/resource/native-grasses-for-use-in-colorado-landscapes/) |
| Little bluestem (*Schizachyrium scoparium*) · `little-bluestem` | Upright blue-green summer clump; copper autumn clump; winter seed-bearing clump | Sun and drainage; distinguish establishment water from later drought tolerance. [NC State Extension](https://plants.ces.ncsu.edu/plants/schizachyrium-scoparium/) |
| Pineleaf penstemon (*Penstemon pinifolius*) · `pineleaf-penstemon` | Needle-leaf cushion; orange-red tubular flowers; named yellow-flowered selection | Low flowering accent; a yellow-flowered selection needs cultivar metadata, not an unexplained recolor. [CSU perennials](https://extension.colostate.edu/resource/herbaceous-perennials/) |
| Fernbush (*Chamaebatiaria millefolium*) · `fernbush` | Young lacy shrub; mature white-flowering shrub; sparse winter structure | Intermountain West candidate; allow its spreading mature shrub form rather than scaling it into a tiny border. [CSU Extension](https://arapahoe.extension.colostate.edu/2025/09/03/from-the-hort-desk-23/) |
| Prairie coneflower (*Ratibida columnifera*) · `prairie-coneflower` | Yellow-ray bloom; red/yellow ray bloom; dry elongated cones | Sunny low-water accent; model the tall central cone and drooping rays. [CSU perennials](https://extension.colostate.edu/resource/herbaceous-perennials/) |

## Beach / coastal — five new families

Do not combine these into a single universal beach palette: the first three serve cool/mild Pacific settings, while the last two serve warm Atlantic/Gulf or southeastern settings.

| Proposed family / ID | Three starting forms | Selection notes and botanical source |
| --- | --- | --- |
| Shore pine (*Pinus contorta* var. *contorta*) · `shore-pine` | Young open tree; irregular mature crown; wind-shaped specimen | Cool Pacific coast; distinguish its paired needles and irregular crown from the existing mountain conifer. [Oregon State](https://landscapeplants.oregonstate.edu/plants/pinus-contorta-var-contorta) |
| Coast silktassel (*Garrya elliptica*) · `coast-silktassel` | Leafy screen; winter male catkins; open small-tree form | Mild Pacific garden; use sheltered placement unless exposure is verified. Its name alone does not establish direct salt-spray suitability. [Oregon State](https://landscapeplants.oregonstate.edu/plants/garrya-elliptica) |
| Beach strawberry (*Fragaria chiloensis*) · `beach-strawberry` | Glossy low mat; white-flowering mat; runner-edge colony | Cool Pacific groundcover; model runners and three-part leaves, without promising a productive fruit crop. [University of Washington](https://depts.washington.edu/propplnt/Plants/fragariachiloensis.htm) |
| Sea oats (*Uniola paniculata*) · `sea-oats` | Young dune clump; green seed panicles; tan flattened seedheads | Warm Atlantic/Gulf dune character. Use nursery-grown material if planting; local protection/restoration rules apply. [NC State Extension](https://plants.ces.ncsu.edu/plants/uniola-paniculata/common-name/sea-oats/) |
| Yaupon holly (*Ilex vomitoria*) · `yaupon-holly` | Natural multi-stem tree; named dwarf shrub; fruiting female specimen | Warm southeastern/coastal setting; dwarf form and fruiting state require the appropriate cultivar and pollination assumptions. [NC State Extension](https://plants.ces.ncsu.edu/plants/ilex-vomitoria/) |

## Suburban gardens — five new families

“Suburban” describes use and composition, not a shared climate. Choose among these for the actual locality rather than mixing all five by default.

| Proposed family / ID | Three starting forms | Selection notes and botanical source |
| --- | --- | --- |
| Eastern redbud (*Cercis canadensis*) · `eastern-redbud` | Airy multi-stem summer tree; single-trunk spring flowering tree; exposed winter branching | A distinct small-tree silhouette and heart-shaped foliage. Select an appropriate regional form. [NC State Extension](https://plants.ces.ncsu.edu/plants/cercis-canadensis/) |
| Panicle hydrangea (*Hydrangea paniculata*) · `panicle-hydrangea` | Rounded white-flowering shrub; loose late-season pinking hedge; trained tree form | Cultivar and pruning determine size/form; use real cone-shaped flower panicles. [NC State Extension](https://plants.ces.ncsu.edu/plants/hydrangea-paniculata/) |
| Ninebark (*Physocarpus opulifolius*) · `ninebark` | Arching green shrub; named compact burgundy selection; peeling-bark winter structure | Cultivar-specific foliage/size; account for heat and sun exposure. [NC State Extension](https://plants.ces.ncsu.edu/plants/physocarpus-opulifolius/) |
| American hornbeam (*Carpinus caroliniana*) · `american-hornbeam` | Slender young tree; mature sculpted-trunk crown; autumn multi-stem specimen | Useful understory character; not a default dry-site tree. [NC State Extension](https://plants.ces.ncsu.edu/plants/carpinus-caroliniana/) |
| Japanese laceleaf maple (*Acer palmatum*, dissected-leaf selections) · `japanese-laceleaf-maple` | Cascading green form; burgundy weeping form; upright dissected-leaf selection | These require different branching, not just colors; record the actual cultivar and site limitations. [NC State Extension](https://plants.ces.ncsu.edu/plants/acer-palmatum-subsp-matsumurae/) |

## Citrus and other fruit trees — ten new families

Fruit size, leaf shape, crown habit, trunk structure and seasonal states must distinguish these families. Do not make one tree and swap yellow, green and orange spheres into its canopy. A patio plant is not automatically a dwarf-rootstock tree; distinguish age, container, pruning and rootstock.

| Proposed family / ID | Three starting forms | Selection notes and botanical source |
| --- | --- | --- |
| Lemon — Improved Meyer hybrid and Eureka selections · `lemon-tree` | Patio-trained Meyer; broader Eureka garden crown; labeled fruiting/blossom close-up form | Separate selections within the family, with their own fruit traits and climate notes. [UCR Meyer](https://citrusvariety.ucr.edu/crc3737), [UCR collection](https://citrusvariety.ucr.edu/citrus-varieties/alphabetical-order) |
| Lime — Bearss (*Citrus × latifolia*) · `lime-tree` | Compact trained tree; bushier natural form; fruiting canopy with labeled ripening state | Resolve frost exposure, rootstock and training; do not treat all lime types as interchangeable. [UCR Bearss](https://citrusvariety.ucr.edu/crc3772) |
| Sweet orange — Washington navel (*Citrus sinensis*) · `sweet-orange-tree` | Young open canopy; mature rounded crown; fruiting/blossoming detail form | Rootstock and training control small-tree claims. [UCR Washington navel](https://citrusvariety.ucr.edu/crc1241A) |
| Mandarin / satsuma — Owari (*Citrus unshiu*) · `satsuma-mandarin-tree` | Low spreading tree; fruit-loaded drooping branches; patio-trained specimen | A comparatively cold-hardy citrus selection, not a default outdoor mountain tree. [UCR Owari](https://citrusvariety.ucr.edu/crc3178) |
| Grapefruit — Marsh (*Citrus × paradisi*) · `grapefruit-tree` | Young upright tree; large spreading crown; hanging fruit clusters | Preserve its larger fruit/canopy character; allow appropriate garden space. [UCR Marsh](https://citrusvariety.ucr.edu/crc3184) |
| Kumquat — Nagami (source: *Fortunella margarita*, also grouped under *Citrus japonica*) · `kumquat-tree` | Dense small-leaf shrub; patio standard; oval-fruited specimen | Fine foliage and small oval fruit distinguish it from other citrus. [UCR Nagami](https://citrusvariety.ucr.edu/crc3877) |
| Avocado (*Persea americana*) · `avocado-tree` | Young orchard tree; maintained garden crown; large mature fruiting crown | Needs drainage and room; cultivar/climate govern pollination. Do not claim two trees are always required. [UF/IFAS](https://ask.ifas.ufl.edu/publication/MG213) |
| Fig (*Ficus carica*) · `fig-tree` | Low branching tree; multi-stem fruiting bush; bare dormant form | Large lobed leaves; cultivar and sheltered-site choice govern cold-site use. [UGA Home Garden Figs](https://extension.uga.edu/content/dam/extension-county-offices/madison-county/4h/fruit-tree-sale/Home%20Garden%20Figs.PDF) |
| Pomegranate (*Punica granatum*) · `pomegranate-tree` | Natural multi-stem shrub; trained flowering tree; fruit-loaded crown | Heat-oriented choice; cold exposure still requires a site check. [UGA Extension](https://site.extension.uga.edu/fultonag/2020/12/pomegranates/) |
| Apple (*Malus domestica*) · `apple-tree` | Named dwarf/rootstock trained tree; freestanding orchard form; espalier | Match cultivar, rootstock, climate and pollenizer; include blossom, fruit and dormant states as follow-on variants. [Iowa State Extension](https://yardandgarden.extension.iastate.edu/how-to/growing-apples-home-garden) |

## How to build useful variations

Use each family's three starting forms above as a minimum production brief, not a reason to stop. Separate three axes instead of cloning every combination into a new asset:

- **Architecture:** young/mature, single/multi-stem, upright/spreading/weeping or genuinely wind-shaped. A different growth habit needs different branch geometry, not nonuniform stretching.
- **State:** leaf-on, dormant, flower, fruit or seed where botanically applicable. Keep one coherent season and phenological state across a home's scene. Do not combine peak autumn, spring blossom and summer growth indiscriminately.
- **Composition:** author several deterministic branch/clump arrangements so repeated instances do not look copied. Make clustered groves and groundcover patches expose their per-plant spacing and individual base origins.

For close views, provide attached branches, coherent leaf clusters, readable bark, appropriately curved leaves, petals and fruit, physically scaled textures and believable light transmission. Avoid floating foliage, identical spherical crowns, giant leaves and repeated flat flower cards. Fruit should have stems and plausible branch attachment; visible scale and shape matter. Background variants may simplify detail but must preserve species silhouette and seasonal color. Store named geometry/state collections within a reviewed version when appropriate; distinguish coexisting named selections from revisions to an adopted asset.

Each published family needs:

1. Botanical identity, selected cultivar/rootstock if relevant, visual-accuracy limitations, reference sources and redistribution rights. Botanical reference photographs are not automatically licensed textures.
2. Modeled meter dimensions, age/training intent, season/fruit state, deterministic seed, ground-contact origin and allowed variation. Distinguish modeled crown extent from researched mature spread and required spacing.
3. Site-selection metadata: region/climate basis, sun, soil/drainage, establishment and ongoing water needs. For coastal candidates, distinguish salt spray, saline inundation and sheltered-coastal placement; use **unknown** when not sourced. Do not label any asset universally climate-approved or fire-safe.
4. Portable native collections/materials, relative dependencies, original procedural or redistribution-compatible textures, and explicit version/derivation records under the [asset workflow](../../docs/assets.md).
5. An actual native preview showing whole silhouette, a human-scale context and a close detail; reopen verification and measured bounds. Review a host planting composition for terrain contact, spacing, sightlines, paths and visual repetition. Image Gen can illustrate a completed home, but cannot stand in for the plant's native asset preview or invent missing model detail.
6. A status that distinguishes **planned**, **modeled**, **reviewed library asset** and **adopted in a home**. Publishing a file does not establish actual reuse. Update the main catalog and home dependency schedule only when those steps actually occur.

## Suggested build sequence

1. **First 12, for immediate range:** quaking aspen, Rocky Mountain maple, blue palo verde, Parry’s agave, blue grama, pineleaf penstemon, shore pine, beach strawberry, eastern redbud, lemon, lime and avocado. These introduce canopy, groundcover, rosette, fine-grass and edible-tree forms across the requested settings.
2. **Complete each five-plant setting palette:** build the remaining mountain, desert, xeriscape, coastal and suburban families, maintaining regional distinctions and distinct silhouettes.
3. **Complete the fruit collection:** sweet orange, satsuma, grapefruit, kumquat, fig, pomegranate and apple, with clear named-selection/training metadata.
4. **Expand variants and adopt deliberately:** finish all planned forms, add useful details and seasonal states, then migrate suitable home plantings with fresh visual review. Do not scatter every available plant into every house; layer canopy, understory, accents and groundcover around the architecture.

This list authorizes no claim that new native plants have already been built. Preserve the six existing families and their adopted versions while the expansion is produced.
