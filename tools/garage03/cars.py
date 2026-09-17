"""Original sculpted coupe geometry; illustrative envelope, not a branded vehicle."""
import bpy,math
from common import geometry as g
from common.geometry import box,cyl,sphere,rod,F
from common.architecture import mesh

def car(name,x,y,z,paint,M):
    def at(a,b,c):return(x+a,y+b,z+c)
    def finish(o):
        for p in o.data.polygons:p.use_smooth=True
        return o
    # Loft the body through varying width and crown sections; wheel wells are real cuts.
    sections=[(-7.6,1.65,.65,1.18),(-7.25,2.5,.5,1.45),(-6.5,2.84,.46,1.7),(-4.7,2.97,.45,2.15),(-2.8,2.86,.47,2.14),(0,2.86,.48,2.03),(2.8,2.99,.49,2.23),(4.65,3,.5,2.33),(6.5,2.83,.55,2.06),(7.3,2.5,.65,1.88),(7.6,2,.8,1.63)]
    verts=[]
    for yy,w,lo,hi in sections:
        for xx,zz in [(-.83*w,lo),(-w,lo+.22),(-w,hi-.22),(-.9*w,hi),(-.58*w,hi+.035),(0,hi+.08),(.58*w,hi+.035),(.9*w,hi),(w,hi-.22),(w,lo+.22),(.83*w,lo)]:verts.append(at(xx,yy,zz))
    k=11;faces=[]
    for i in range(len(sections)-1):
        for j in range(k):faces.append((i*k+j,i*k+(j+1)%k,(i+1)*k+(j+1)%k,(i+1)*k+j))
    faces += [tuple(reversed(range(k))),tuple((len(sections)-1)*k+j for j in range(k))]
    body=finish(mesh(name+' body',verts,faces,paint));sub=body.modifiers.new('Sculpted body curvature','SUBSURF');sub.levels=2;sub.render_levels=2
    bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=sub.name)
    for side in [-1,1]:
        for yy in [-4.65,4.65]:
            cutter=cyl('Temporary wheel opening',at(side*2.9,yy,1),1.105,2.0,M['black'],48);cutter.rotation_euler.y=math.pi/2
            mod=body.modifiers.new('Wheel arch','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    bev=body.modifiers.new('Body edge radius','BEVEL');bev.width=.018*F;bev.segments=3
    # Curved cabin cross sections. Smoked glass under painted pillars and roof.
    rows=[(-3.65,2.39,2.08,2.12),(-1.9,1.98,3.64,3.96),(-.9,1.94,3.76,4.08),(1.4,1.98,3.73,4.03),(3.85,2.44,2.31,2.37)]
    vv=[]
    for yy,w,edge,top in rows:
        for xx,zz in [(-2.46,2.03),(-w,edge),(-w*.55,top-.06),(0,top),(w*.55,top-.06),(w,edge),(2.46,2.03)]:vv.append(at(xx,yy,zz))
    ff=[]
    for i in range(len(rows)-1):
        for j in range(6):ff.append((i*7+j,i*7+j+1,(i+1)*7+j+1,(i+1)*7+j))
    cabin=finish(mesh(name+' smoked glazing',vv,ff,M['car-glass']));m=cabin.modifiers.new('Compound glazing curves','SUBSURF');m.levels=2
    # Broad, gently crowned roof panel; pillar tubes follow the greenhouse.
    roofverts=[]
    for yy in [-1.85,1.42]:
        for xx in [-1.97,-1.05,0,1.05,1.97]:roofverts.append(at(xx,yy,4.115-.11*(abs(xx)/1.97)**2))
    roof=finish(mesh(name+' roof',roofverts,[(i,i+1,i+6,i+5) for i in range(4)],paint));solid=roof.modifiers.new('Roof skin','SOLIDIFY');solid.thickness=.045*F
    for side in [-1,1]:
        rod(name+' A pillar',at(side*2.4,-3.58,2.16),at(side*1.97,-1.85,4.02),.062,paint)
        rod(name+' rear pillar',at(side*1.97,1.42,4.02),at(side*2.4,3.76,2.36),.09,paint)
        rod(name+' window sill',at(side*2.47,-3.58,2.14),at(side*2.47,3.75,2.18),.038,M['black'])
        rod(name+' B pillar',at(side*2.46,.75,2.11),at(side*1.98,.75,3.97),.045,M['black'])
        # Flush handle, sill blade, mirrors and aerodynamic intakes.
        box(name+' flush handle',at(side*2.92,.9,1.88),(.03,.58,.08),M['black'],.025)
        box(name+' side skirt',at(side*2.84,0,.58),(.14,6.8,.18),M['black'],.04)
        sphere(name+' mirror',at(side*3.035,-2.2,2.43),(.105,.38,.16),paint)
        box(name+' lower intake',at(side*1.76,-7.25,.89),(1.1,.16,.25),M['black'],.12)
        lamp=box(name+' headlamp',at(side*2.0,-6.91,1.5),(1.25,.32,.16),M['glass'],.07);lamp.rotation_euler.z=side*.1
        rod(name+' LED signature',at(side*1.44,-7.02,1.55),at(side*2.53,-6.97,1.6),.024,M['glow'])
        rod(name+' rear light strip',at(side*.4,7.64,1.55),at(side*1.8,7.59,1.55),.046,M['red'])
        cyl_o=cyl(name+' exhaust outlet',at(side*1.8,7.3,.68),.15,.35,M['steel']);cyl_o.rotation_euler.x=math.pi/2
        for yy in [-4.65,4.65]:
            tire=finish(cyl(name+' tire',at(side*2.76,yy,1),.99,.64,M['rubber'],64));tire.rotation_euler.y=math.pi/2
            bevel=tire.modifiers.new('Rounded tire shoulders','BEVEL');bevel.width=.085*F;bevel.segments=4
            rotor=cyl(name+' brake disc',at(side*3.02,yy,1),.67,.025,M['steel'],64);rotor.rotation_euler.y=math.pi/2
            face=side*3.09
            # Annular alloy rim and tire sidewall rings.
            for radius,minor,xx,mat in [(.76,.055,face,M['steel']),(.66,.018,face,M['black']),(.89,.011,side*3.085,M['rubber'])]:
                bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=10,location=[v*F for v in at(xx,yy,1)],major_radius=radius*F,minor_radius=minor*F,rotation=(0,math.pi/2,0));o=g.move(bpy.context.object);o.name=name+' wheel rim';o.data.materials.append(mat);finish(o)
            for j in range(5):
                a=j*math.tau/5
                for off in [-.08,.08]:rod(name+' split alloy spoke',at(face,yy+math.sin(a)*.16,1+math.cos(a)*.16),at(face,yy+math.sin(a+off)*.72,1+math.cos(a+off)*.72),.028,M['steel'])
                bolt=cyl(name+' wheel bolt',at(face+side*.02,yy+math.sin(a)*.15,1+math.cos(a)*.15),.028,.03,M['black'],12);bolt.rotation_euler.y=math.pi/2
            hub=cyl(name+' center cap',at(face+side*.015,yy,1),.115,.04,M['steel']);hub.rotation_euler.y=math.pi/2
            box(name+' brake caliper',at(side*3.015,yy+.49,1),(.08,.18,.55),M['red'],.055)
    box(name+' front splitter',at(0,-7.17,.54),(4.9,.58,.13),M['black'],.09)
    box(name+' rear diffuser',at(0,7.2,.67),(4.9,.42,.32),M['black'],.08)
    for xx in [-1.2,-.6,0,.6,1.2]:box(name+' diffuser fin',at(xx,7.2,.61),(.055,.58,.28),M['black'],.012)
    box(name+' plate recess',at(0,7.635,1.12),(1.6,.025,.42),M['black'],.055)
    for xx in [-1.25,1.25]:
        box(name+' leather seat',at(xx,.1,1.46),(1.7,2.1,.35),M['black'],.2)
        o=box(name+' seat back',at(xx,1,2.34),(1.7,.42,1.65),M['black'],.22);o.rotation_euler.x=-.12
        sphere(name+' head restraint',at(xx,1.1,3.2),(.5,.22,.35),M['black'])
    return [o for o in g.ACTIVE.objects if o.name.startswith(name)]
