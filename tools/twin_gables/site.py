"""Illustrative level woodland site, plantedcourt and two-car sideforecourt."""
import random,math
from common import geometry as g
from common.geometry import box,rod
from assets import put

def build(M):
 g.collection('06 Landscape | planted courtyard and native asset garden')
 box('Illustrative level ground',(34,28,-.65),(240,220,1),M['meadow'])
 for loc,size in [((11,-13,-.14),(35,27,.12)),((57,-13,-.14),(35,27,.12)),((-5,30,-.14),(9,63,.12)),((73,38,-.14),(7,46,.12)),((34,78,-.14),(76,10,.12))]:box('Defined planted loam bed',loc,size,M['soil'],.3)
 # Broadsite-specific patio slab, regular sharedfourfootpavingmodules where fullfit.
 box('Rear terrace foundation',(34,66.2,-.25),(70,12.4,.4),M['stone'],.04)
 for i in range(17):
  for j in range(3):put('Shared rear terrace limestone paver','surfaces','honed-limestone-paver-4ft',(1.3+i*4.04,62+j*4.04,0))
 # Accessiblecontinuousentrypath; no deep soilgap route disguised bysteppingstones.
 box('Entry path continuous substrate',(34,-18,-.12),(8.1,36,.20),M['stone'],.01)
 for x in [31.98,36.02]:
  for j in range(9):put('Shared entry limestone paver','surfaces','honed-limestone-paver-4ft',(x,-2-j*4.04,0))
 # Court floor iscontinuousunderplantedislands, houseentries have dry hardscape.
 box('Courtyard drained paving substrate',(34,24,-.13),(19.9,35.9,.20),M['stone'],.01)
 for x in [26.0,30.02,34.04,38.06,42.08]:
  for y in [8,12.02,16.04,20.06,24.08,28.1,32.12,36.14,40.16]:
   if x in [30.02,38.06] and 14<y<33:continue
   put('Shared courtyard limestone paver','surfaces','honed-limestone-paver-4ft',(x,y,-.025))
 for x in [30,38]:box('Courtyard planted soil island',(x,23,-.01),(3.85,19,.18),M['soil'],.15)
 put('Signature courtyard red maple','landscape','japanese-laceleaf-maple',(34,24,.08),scale=.9)
 box('Central maple root planting island',(34,24,.02),(3.5,3.5,.14),M['soil'],.15)
 rng=random.Random(188)
 for i in range(174):
  if i<112:
   x=rng.uniform(-4,72);y=rng.uniform(-26,-3)
   if 29<x<39:continue
  elif i<144:x=rng.choice([rng.uniform(-9,-3),rng.uniform(71,77)]);y=rng.uniform(0,59)
  else:x=rng.uniform(-6,74);y=rng.uniform(75,83)
  kind=['sage-shrub','ornamental-grass-clump','flowering-perennial-clump'][i%3]
  ver='v002' if kind in ['sage-shrub','ornamental-grass-clump'] else 'v001'
  put('Layered woodland garden planting','landscape',kind,(x,y,-.12),rng.uniform(0,6.28),ver,scale=rng.uniform(.8,1.25))
 for x in [30,38]:
  for y in [15,18,21,27,31]:
   put('Courtyard understorey grass','landscape','ornamental-grass-clump',(x+rng.uniform(-1,1),y,.08),version='v002',scale=.75)
 for i,(x,y) in enumerate([(-45,-28),(-45,88),(-20,83),(-12,112),(81,115),(90,89),(98,62),(96,25),(85,-23),(-24,-30)]):
  put('Woodland canopy context','landscape','broad-canopy-oak',(x,y,-.14),i*.77,scale=.9+(i%3)*.1)
 # Outdoorrear furniture stayswellclearofmovingglazing.
 put('Rear garden outdoor sofa','furniture','coastal-outdoor-sofa',(53,69,0),math.pi)
 put('Rear garden lounge chair','furniture','coastal-outdoor-lounge-chair',(63,67,0),math.pi/2)
 put('Rear outdoor coffee table','furniture','oak-rounded-coffee-table',(55.5,66,0))
 put('Terrace dining oak table','furniture','oak-dining-table-8ft',(31,67,0))
 for x in [28,31,34]:
  for y,rot in [(64,math.pi),(70,0)]:put('Terrace dining chair','furniture','oak-upholstered-dining-chair',(x,y,0),rot)
 g.collection('07 Arrival | two-car forecourt and service route')
 box('Side driveway and parking',(83,-1,-.22),(24,58,.3),M['paving'],.04)
 box('Road illustrative front',(34,-40,-.3),(150,20,.3),M['paving'])
 box('Parking pedestrian link',(57,-20,-.10),(44,5,.18),M['stone'])
 # Dimensionedparkingzones markeddiscreetly, no toyvehicleproxy.
 for x in [77.5,88.5]:
  for xx in [x-4.5,x+4.5]:box('Parking bay edge inlay',(xx,1,-.04),(.06,20,.015),M['stone'])
  box('Parking wheelstop',(x,10,.15),(6,.45,.35),M['stone'],.04)
  box('EV service post reservation',(x,12,1.9),(.35,.4,3.8),M['dark'],.03)
