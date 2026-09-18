"""Original smooth hollow bathroom fixtures, feet in authoring coordinates."""
import bpy
import math
from . import geometry as g
from .geometry import F, cyl, box, rod
from mathutils import Matrix, Vector

DESCRIPTIONS = {
    'bathtub': ('Original 72-inch freestanding bathtub', 'Floor-center origin; length along X, width along Y. Nominal 72L x 36W x 24H inches. Smooth hollow shell with actual basin, rolled rim and drain. Host supplies freestanding or wall-mounted filler, access and plumbing. Original visualization envelope, not a manufacturer product or installation specification.'),
    'toilet': ('Original elongated floor-mounted toilet', 'Floor-center origin, front -Y. Nominal 16W x30D inches maximum plan envelope, 30-inch tank height. Raised lid modeled at90degrees, increasing overall height to approximately39inches. Continuous ceramic pedestal and hollow bowl, separate open seat, raised lid, tank cover and flush button. Original visualization concept; plumbing and installation requirements are not manufacturer-approved.'),
}

METADATA = {
    'toilet': {
        'nominal_dimensions_inches': {'width':16,'depth':30,'tank_height':30},
        'placement': {'origin':'Floor center of nominal 16 x30 inch plan envelope','front':'-Y','up':'Z','allowed_scaling':'Scale1 only; rigid placement/rotation. Publish another dimensional asset instead of stretching.'},
        'installation': {
            'mounting_requirements':['Floor mounted on continuous level support. Waste outlet, rear wall connection and water supply are conceptual allowances, not a selected rough-in.'],
            'operating_envelope': {'basis':'Measured original lid geometry rotated about its hinge; no manufacturer data','modeled_state':'Horizontal open seat with lid raised90degrees','lid_angle_degrees':90,'lid_travel_degrees':[0,90],'plan_envelope_inches':[16,30],'host_open_state_checked':False,'notes':'Closed-to-raised lid swept geometry stays inside this plan envelope; host must verify vertical space and surrounding installation/standing space.'},
            'service_requirements':['Access to tank lid and water shutoff; exact service/rear clearances unresolved until product selection.','Provide a deliberately dimensioned clear standing area in front; no jurisdiction-specific compliance claim.']},
        'derived_from':None,
    }
}


def _surface(name,profile,material,center_y=0,segments=96,caps=True):
    verts=[];faces=[]
    for item in profile:
        rx,ry,z=item[:3];cy=item[3] if len(item)>3 else center_y
        for i in range(segments):
            a=i*math.tau/segments
            verts.append((rx*math.cos(a)*F,(cy+ry*math.sin(a))*F,z*F))
    for j in range(len(profile)-1):
        for i in range(segments):faces.append((j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i))
    if caps:faces.extend([tuple(reversed(range(segments))),tuple((len(profile)-1)*segments+i for i in range(segments))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.materials.append(material)
    obj=bpy.data.objects.new(name,mesh);g.ACTIVE.objects.link(obj)
    for face in mesh.polygons:face.use_smooth=True
    return obj


def _toilet():
    ceramic=g.material('Original toilet satin white ceramic',(.75,.77,.76),.19)
    seatmat=g.material('Original toilet white seat',(.80,.81,.79),.26)
    metal=g.material('Original toilet satin flush hardware',(.47,.5,.51),.22,.85)
    # Continuous closed vessel: foot, pedestal, outer bowl, rim and concave basin.
    profile=[(.01,.01,0,.07),(.31,.45,0,.07),(.35,.50,.04,.07),(.36,.51,.13,.07),
             (.29,.41,.36,.10),(.30,.42,.70,.10),(.43,.64,.90,-.05),
             (.56,.82,1.08,-.24),(.625,.925,1.27,-.29),(.645,.945,1.36,-.29),
             (.635,.935,1.395,-.29),(.56,.845,1.395,-.29),(.535,.805,1.34,-.29),
             (.48,.71,1.13,-.24),(.32,.48,.86,-.12),(.19,.29,.72,.02),
             (.13,.19,.69,.08),(.01,.01,.69,.08)]
    _surface('Toilet continuous pedestal and hollow bowl',profile,ceramic)
    # Elliptical annular seat, never a solid white oval filling the bowl.
    seat_profile=[(.641,.904,1.405),(.655,.918,1.425),(.655,.918,1.465),
                  (.641,.904,1.485),(.465,.685,1.485),(.450,.670,1.46),
                  (.450,.670,1.43),(.465,.685,1.405),(.641,.904,1.405)]
    seat=_surface('Toilet open oval seat',seat_profile,seatmat,center_y=-.29,caps=False)
    # Raised lid is rotated about a real hinge at the back of the seat.
    lid=_surface('Toilet raised lid',[(.01,.01,1.51),(.62,.835,1.51),(.643,.858,1.53),(.643,.858,1.56),(.62,.835,1.58),(.01,.01,1.58)],seatmat,center_y=-.35)
    hinge=Vector((0,.52*F,1.52*F))
    lid.matrix_world=Matrix.Translation(hinge)@Matrix.Rotation(math.radians(-90),4,'X')@Matrix.Translation(-hinge)
    lid['hinge_y_ft']=.52;lid['hinge_z_ft']=1.52;lid['open_angle_degrees']=90
    for x in [-.28,.28]:
        rod('Toilet seat hinge pin',(x-.09,.52,1.49),(x+.09,.52,1.49),.032,metal)
    # Tank joins the pedestal at the rear, with separate removable lid.
    box('Toilet cistern body',(0,.946,1.87),(1.255,.578,1.16),ceramic,.11)
    box('Toilet removable tank lid',(0,.946,2.465),(1.30,.608,.070),ceramic,.028)
    cyl('Toilet dual flush button surround',(.34,.946,2.507),.061,.012,metal,48)
    box('Toilet flush button division',(.34,.946,2.514),(.006,.091,.005),ceramic,.002)
    # Rear connector and floor mounting caps are generic visual allowances.
    box('Toilet rear ceramic connection',(0,.63,.73),(.52,.63,1.10),ceramic,.12)
    for x in [-.31,.31]:cyl('Toilet concealed floor fixing cap',(x,.15,.12),.048,.04,ceramic,32)


def build_bath_fixture(key):
    if key == 'toilet':
        return _toilet()
    if key != 'bathtub':
        raise ValueError(key)
    porcelain=g.material('Original bath satin white porcelain',(.73,.75,.74),.22)
    steel=g.material('Original bath polished drain',(.5,.53,.53),.18,.85)
    # Continuous closed surface goes from underside through outer wall, over
    # the rim and down the concave inner bowl. No opaque block fills the basin.
    profile=[(.01,.01,.0),(2.15,.76,.0),(2.37,.91,.05),(2.49,1.04,.20),
             (2.66,1.20,.66),(2.88,1.41,1.55),(2.975,1.475,1.93),
             (3.0,1.5,1.985),(2.985,1.485,2.0),(2.90,1.40,2.0),
             (2.84,1.34,1.95),(2.79,1.29,1.57),(2.59,1.10,.70),
             (2.40,.91,.35),(2.23,.80,.27),(.01,.01,.27)]
    verts=[];faces=[];N=128
    for rx,ry,z in profile:
        for i in range(N):
            a=i*math.tau/N
            verts.append((rx*math.cos(a)*F,ry*math.sin(a)*F,z*F))
    for j in range(len(profile)-1):
        for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
    faces.extend([tuple(reversed(range(N))),tuple((len(profile)-1)*N+i for i in range(N))])
    mesh=bpy.data.meshes.new('Original hollow oval bathtub shell')
    mesh.from_pydata(verts,[],faces);mesh.materials.append(porcelain)
    obj=bpy.data.objects.new('Original hollow oval bathtub shell',mesh);g.ACTIVE.objects.link(obj)
    for face in mesh.polygons:face.use_smooth=True
    cyl('Bathtub drain',(0,0,.278),.09,.012,steel,64)
