"""Original shared luminaires. Authoring/placement dimensions are feet; native units are meters.

Collection geometry is immutable and linked. Actual lights belong to the host so
each instance can be dimmed without editing a library. No rated photometry implied.
"""
from pathlib import Path
import bpy
import math
from . import geometry as g
from .library import linked_collection, instance

CATALOG = {
    'downlight': ('lighting-recessed-downlight-3in', 8, .20, -.022, .20),
    'taskbar': ('lighting-undercabinet-bar-4ft', 12, 3.9, -.058, .065),
    'linear': ('lighting-linear-pendant-4ft', 35, 3.9, -2.655, .080),
}

def ring(name, outer, inner, low, high, material, segments=96):
    """Hollow ring with real aperture, dimensions in feet."""
    vertices = []
    for z, r in [(low, outer), (low, inner), (high, outer), (high, inner)]:
        vertices.extend((r*math.cos(i*math.tau/segments)*g.F,
                         r*math.sin(i*math.tau/segments)*g.F,z*g.F) for i in range(segments))
    faces=[]
    for i in range(segments):
        j=(i+1)%segments
        faces.extend([(i,j,2*segments+j,2*segments+i),
                      (segments+j,segments+i,3*segments+i,3*segments+j),
                      (j,i,segments+i,segments+j),
                      (2*segments+i,2*segments+j,3*segments+j,3*segments+i)])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);g.ACTIVE.objects.link(obj);obj.data.materials.append(material)
    return obj

def build(key):
    """Build only library-owned local geometry; called by the immutable publisher."""
    names={'downlight':'Recessed 3 inch dark baffle downlight',
           'taskbar':'Four foot undercabinet task light',
           'linear':'Four foot slim linear suspended pendant'}
    coll=g.collection(names[key])
    dark=g.material('Lighting | satin graphite',(.024,.028,.030),.3,.72)
    white=g.material('Lighting | warm white trim',(.8,.8,.77),.32,.18)
    diffuser=g.material('Lighting | opal diffuser',(.87,.84,.76),.35)
    p=diffuser.node_tree.nodes.get('Principled BSDF')
    p.inputs['Emission Color'].default_value=(1,.84,.62,1)
    p.inputs['Emission Strength'].default_value=.25
    if key=='downlight':
        # 3.6 inch outside trim, 3 inch clear opening, 3.6 inch service depth.
        ring('Downlight | small white trim',.15,.125,-.013,0,white)
        ring('Downlight | dark recessed baffle',.125,.110,0,.075,dark)
        ring('Downlight | recessed housing',.139,.126,.03,.30,dark)
        g.cyl('Downlight | opal lens', (0,0,.074),.11,.008,diffuser,64)
        g.cyl('Downlight | closed housing top',(0,0,.296),.139,.008,dark,64)
        for z in [.014,.026,.038,.05]:
            ring('Downlight | concentric baffle groove',.113,.110,z,z+.003,dark)
    elif key=='taskbar':
        g.box('Task bar | aluminum body',(0,0,-.025),(4,1/12,.05),dark,.008)
        g.box('Task bar | downward opal lens',(0,0,-.052),(3.94,.064,.006),diffuser,.002)
        for x in [-1.87,1.87]:
            g.box('Task bar | mounting clip',(x,0,-.008),(.09,.092,.016),dark,.003)
    else:
        g.box('Linear pendant | ceiling canopy',(0,0,-.035),(1.25,.30,.07),dark,.018)
        for x in [-1.45,1.45]:
            g.cyl('Linear pendant | ceiling suspension anchor',(x,0,-.0125),.035,.025,dark,32)
            g.rod('Linear pendant | suspension wire',(x,0,0),(x,0,-2.5),.003,dark)
        g.rod('Linear pendant | flexible power cable',(0,0,-.07),(0,0,-2.5),.007,dark)
        g.box('Linear pendant | aluminum extrusion',(0,0,-2.575),(4,.125,.15),dark,.018)
        g.box('Linear pendant | opal diffuser',(0,0,-2.651),(3.94,.083,.006),diffuser,.002)
    coll['units']='meters'
    coll['source_units']='feet (converted by common.geometry.F)'
    coll['origin']='Mounting plane center at Z=0; light emits along -Z'
    return coll

def load(root, keys=None):
    return {key: linked_collection(root,'fixtures',CATALOG[key][0]) for key in (keys or CATALOG)}

def place(name, collection, key, loc, rotation=0, power=None, color=(1,.84,.66)):
    """Place linked geometry + host-owned dimmable light, location in feet.

    All origins are mounting plane center. Rotation is around Z in radians.
    Recessed fixture housing extends 3.6 inches ABOVE the ceiling: the host must
    cut a 3.4 inch housing opening and reserve housing space. Do not hide it inside a solid
    roof/ceiling slab. Under-cabinet bar top is Z=0; pendant canopy top is Z=0.
    power is illustrative Blender watts, not lumens or a product specification.
    Pass power=0 for geometry-only instances; never stretch these fixtures.
    """
    obj=instance(name,collection,loc,rotation=rotation)
    slug,default,size,z,size_y=CATALOG[key]
    obj['shared_asset']=f'fixtures/{slug}/v001'
    obj['mounting_plane']='Z=0; local -Z emission'
    energy=default if power is None else power
    if energy>0:
        source=g.area(name+' | host dimmable source',(0,0,z),(0,0,z-1),energy,size,color,
                      shape='DISK' if key=='downlight' else 'RECTANGLE',
                      size_y=None if key=='downlight' else size_y)
        source.parent=obj
        source['photometry']='Illustrative artistic illumination; no IES/product rating'
    return obj

def dependencies(root=None, keys=None):
    return [f'../../library/fixtures/{CATALOG[key][0]}/v001' for key in (keys or CATALOG)]
