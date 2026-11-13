import sys
from functools import lru_cache
from math import sqrt

import cadquery as cq

from .geometry import ROOT, V, Item, box, cylinder, cut_holes, m3_nut, orient, read_step, standard_screw, translate, xy_panel
from .structure import AQUA, BLACK, METAL, axis_cylinder, laser, mounted_hardware, printed, stock

COM = ROOT / "commercial"
OLED_STEP = "auxiliary/oled/2_42inch_oled_module-sku25742_asm.stp"
sys.path.insert(0,str(COM / "weighing"))

@lru_cache(maxsize=20)
def asset(relative):
    return read_step(COM / relative)


def weighing(p):
    from bmh12m205 import build_weighing_components

    group = "Pesaje"
    parts = build_weighing_components(height_mm=p.scale_height)
    items = [
        stock(f"BMH_{i}",name,group,translate(shape,y=p.center_y,z=p.panel),AQUA,
              state="interfaz verificada en plano, superficie sin volumen")
        for i,(name,shape) in enumerate(parts.items(),1)
    ]
    native = cylinder(p.carrier_diameter/2,p.carrier_thickness,(0,0,0))
    placed = translate(native,y=p.center_y,z=p.carrier_z)
    items.append(Item("P10","Plato portante lavable Ø240",group,placed,METAL,"Acero inoxidable 304 1,5 mm",
                      "laser",native,"P10","prototipo"))
    # Four low locators and two prototype clamp designs act on the fixed base only.
    # The toe height is confirmed against the actual instrument before use.
    for sx in (-1,1):
        for sy in (-1,1):
            bx, by = sx*65.0,p.center_y+sy*57.0
            toe = box(-3.5,-9,0,8,9,5)
            toe = cut_holes(toe,[(0,0)],p.printed_hole,5)
            placed = orient(toe,(bx,by,p.panel),(sx,0,0),(0,0,1))
            key=f"B{sx+1}{sy+1}"
            items.append(printed(key,"Localizador de base fija","Pesaje",toe,placed,part="P34",
                                 state="prototipo: verificar pies OEM"))
            items.extend(mounted_hardware(key,(bx,by,0),(0,0,1),p.panel+8,20))
    # A low hold-down tongue reaches the bottom perimeter. Slot and shim are adjustable.
    shoe=box(-7,-6,0,12,6,3)
    slot=box(-1.5,-1.8,-0.1,4.5,1.8,3.1)
    for x in (-1.5,4.5):
        slot=slot.fuse(cylinder(1.8,3.2,(x,0,-0.1)))
    shoe=shoe.cut(slot).clean()
    for sx in (-1,1):
        for sy in (-1,1):
            bx,by=sx*65.0,p.center_y+sy*57.0
            placed=orient(shoe,(bx,by,p.panel+5),(sx,0,0),(0,0,1))
            items.append(printed(f"C{sx+1}{sy+1}","Mordaza baja para base fija","Pesaje",shoe,placed,
                                 part="P35",state="verificar altura de borde OEM antes de usar"))
    # Physical dish geometry varies. This surface is a visibility/reference profile only.
    return items


def camera_mount(p):
    group="Camara"
    local = asset("electronics/Adafruit-5838-referencia-parcial.step")
    pcb_x, pcb_y = -0.20,p.center_y+30.65
    pcb_z=p.lens_z+5.1
    camera=orient(local,(pcb_x,pcb_y,pcb_z),(1,0,0),(0,0,-1))
    items=[stock("E01","Adafruit 5838 · geometria parcial documentada",group,camera,(0.09,0.30,0.27),
                 state="reconstruccion parcial del fabricante; eje XY provisional")]
    base_z=p.shelf+p.panel
    bridge_z=pcb_z+1.57+p.lens_adjust
    height=bridge_z-base_z
    for sx in (-1,1):
        ax=sx*94
        side=box(-11,-25,0,11,25,4)
        side=side.fuse(box(-8,-12,4,8,12,height))
        side=cut_holes(side,[(0,-19),(0,19)],p.printed_hole,4)
        side=cut_holes(side,[(0,0)],p.printed_hole,height)
        side=side.cut(box(-3.1,-12.1,height-6,3.1,3.45,height-3.4)).clean()
        items.append(printed(f"K{sx+1}","Pedestal de camara","Camara",side,
                             translate(side,ax,p.center_y,base_z),part="P31"))
        for oy in (-19,19):
            items.extend(mounted_hardware(f"K{sx+1}_{oy}",(ax,p.center_y+oy,p.shelf),(0,0,1),p.panel+4,16))
    bridge=box(-107,-12,0,107,12,4)
    bridge=cut_holes(bridge,[(-94,0),(94,0)],p.printed_hole,4)
    for cx in (pcb_x-8.89,pcb_x+8.89):
        cy=30.65-33.02
        slot=box(cx-1.65,cy-3.0,-0.1,cx+1.65,cy+3.0,4.1)
        for end in (cy-3.0,cy+3.0):
            slot=slot.fuse(cylinder(1.65,4.2,(cx,end,-0.1)))
        bridge=bridge.cut(slot)
        shim=cylinder(2.8,p.lens_adjust,(0,0,0)).cut(cylinder(1.55,p.lens_adjust+0.2,(0,0,-0.1)))
        cx_world,cy_world=cx,p.center_y+cy
        items.append(printed(f"P32_{cx}","Separador intercambiable de camara","Camara",shim,
                             translate(shim,cx_world,cy_world,bridge_z-p.lens_adjust),part="P32",
                             state="prototipo: comprobar componentes alrededor del agujero"))
        screw=orient(standard_screw(12,2.5),(cx_world,cy_world,pcb_z),(1,0,0),(0,0,1))
        items.append(stock(f"EC{cx}","Tornillo M2.5×12 de camara",group,screw,material="Acero A2"))
        # The same nominal nut envelope is used in the screen tray and camera crossbar.
        n=cq_hex_nut(5.0,2.0,1.25)
        items.append(stock(f"ECN{cx}","Tuerca M2.5 de camara",group,
                           translate(n,cx_world,cy_world,bridge_z+4),material="Acero A2"))
    bridge=bridge.clean()
    items.append(printed("P30","Travesaño de camara con ranuras","Camara",bridge,
                         translate(bridge,y=p.center_y,z=bridge_z)))
    for sx in (-1,1):
        # This pin registers the crossbar in its pedestal. Access through the lid.
        screw=orient(standard_screw(12),(sx*94,p.center_y,bridge_z+4),(1,0,0),(0,0,-1))
        items.append(stock(f"KTop{sx}","Tornillo M3×12 del travesaño",group,screw,material="Acero A2",
                           state="usar tuerca cautiva antes de fijar travesaño"))
        nut=m3_nut().rotate(V(),V(0,0,1),90)
        items.append(stock(f"KTopN{sx}","Tuerca M3 cautiva del travesaño",group,
                           translate(nut,sx*94,p.center_y,bridge_z-5.8),material="Acero A2"))
    return items


def cq_hex_nut(af, height, bore):
    blank=cq.Workplane("XY").polygon(6,af/0.866025403784).extrude(height).val()
    return blank.cut(cylinder(bore,height+0.2,(0,0,-0.1))).clean()


def electronics(p):
    group="Electronica"
    x,y,z=-92.5,258.5,p.shelf+p.panel
    # PCB mounted with USB edge toward the back and antenna toward the service bay interior.
    loc=(x+12.7,y+31.4325,z+9)
    dev=orient(asset("electronics/ESP32-S3-DevKitC-1-v1.1-referencia-parcial.step"),loc,(-1,0,0),(0,0,1))
    items=[stock("E02","Espressif ESP32-S3-DevKitC-1 v1.1 · referencia parcial",group,dev,(0.12,0.13,0.16),
                 state="PCB DXF oficial; WROOM-1 STEP oficial; conectores no modelados")]
    mount=xy_panel((-27,-33,27,36),3,[(-20.5,-24.5),(20.5,-24.5),(-20.5,26.5),(20.5,26.5)])
    mount=mount.cut(box(-10,-31,-0.1,10,31,3.1))
    for sx in (-1,1):
        # Support the edges of the PCB away from the 22.86 mm header row pitch.
        rail=box(12,-27,3,16,19,9).fuse(box(13, -27,9,16,19,12.0))
        if sx == -1:
            rail=box(-16,-27,3,-12,19,9).fuse(box(-16,-27,9,-13,19,12.0))
        mount=mount.fuse(rail)
    mount=mount.clean()
    items.append(printed("P36","Cuna desmontable por bordes · ESP32-S3","Electronica",mount,
                         translate(mount,x,y,z),state="prototipo: comprobar revision y pines bajos"))
    for ox in (-20.5,20.5):
        for oy in (-24.5,26.5):
            items.extend(mounted_hardware(f"CPU{ox}_{oy}",(x+ox,y+oy,p.shelf),(0,0,1),p.panel+3,16))

    # Separate removable carrier panel for the future control PCB.
    service_holes=[(x,z) for x in (-32.5,32.5) for z in (-15.5,15.5)]
    blank=xy_panel((-37,-18,37,18),3,service_holes)
    service_center=(106.5,p.depth+3,350.5)
    items.append(laser("P09","Placa ciega reemplazable para entrada de alimentacion",blank,
                       orient(blank,service_center,(1,0,0),(0,-1,0)),
                       material="Contrachapado abedul 3 mm sellado"))
    for dx,dz in service_holes:
        items.extend(mounted_hardware(f"SV{dx}_{dz}",(service_center[0]+dx,p.depth+3,service_center[2]+dz),
                                      (0,-1,0),p.panel+3,16))
    return items


def oled_origin(p):
    return (-30.75, p.panel + 0.5 + 3.58852, p.screen_z - 22.425)


def oled_placement(shape, p):
    return orient(shape, oled_origin(p), (1, 0, 0), (0, -1, 0))


def display(p):
    group="Frontal"
    top=p.shelf+p.panel
    origin=oled_origin(p)
    display_3d=oled_placement(asset(OLED_STEP), p)
    items=[stock("E03","Waveshare OLED 2.42 SKU 25742 · STEP OEM",group,display_3d,(0.11,0.15,0.17),
                 state="seleccion electrica propuesta")]
    boss_y=origin[1]+3.41148
    for sx in (-1,1):
        xmin,xmax=sorted((sx*34,sx*44))
        foot=box(xmin,8,top,xmax,34,top+4)
        foot=foot.cut(cylinder(p.printed_hole/2,4.2,(sx*38,27,top-0.1)))
        bracket=foot.fuse(box(xmin,boss_y,top+4,xmax,boss_y+4,p.screen_z+18))
        for raw_z in (3.5,36):
            z=origin[2]+raw_z
            a,b=sorted((sx*24,sx*37))
            bracket=bracket.fuse(box(a,boss_y,z-2.8,b,boss_y+4,z+3))
            bracket=bracket.cut(axis_cylinder(3.0,4.2,(sx*27.75,boss_y-0.1,z),(0,1,0)))
            # Screw enters from the rear into the OEM bosses. Threaded part is nominal only.
            screw=orient(standard_screw(5,2.5),(sx*27.75,boss_y+4,z),(1,0,0),(0,-1,0))
            items.append(stock(f"LCD{sx}_{raw_z}","Tornillo M2.5 de pantalla",group,screw,material="Acero A2",
                               state="confirmar profundidad del separador OEM"))
        native=translate(bracket.clean(),-sx*38,-27,-top)
        items.append(printed(f"P37_{sx}","Soporte OLED izquierdo" if sx<0 else "Soporte OLED derecho",group,native,
                             bracket.clean(),part="P37L" if sx<0 else "P37R"))
        items.extend(mounted_hardware(f"LFoot{sx}",(sx*38,27,p.shelf),(0,0,1),p.panel+4,16))
    for x,label in [(-54,"Tara"),(54,"Captura")]:
        rim=axis_cylinder(18.06,4,(x,-4,p.screen_z),(0,1,0))
        actuator=axis_cylinder(13.0,5,(x,-8,p.screen_z),(0,1,0))
        body=axis_cylinder(15.56,18.7,(x,0,p.screen_z),(0,1,0))
        items.append(stock(f"SW{x}",f"Adafruit 1505 {label} · interfaz parcial",group,
                           rim.fuse(actuator,body).clean(),BLACK,
                           state="contorno de ficha; terminales y agarre de tuerca por verificar"))
    return items


def leds(p):
    group="Iluminacion"
    profile=asset("auxiliary/led/klus_A08504_cut_220_faceted.step")
    positions=[
        (-p.inside_x+16.5,44,180),(p.inside_x-16.5,44,-90),
        (-p.inside_x+16.5,p.inside_rear-46,90),(p.inside_x-16.5,p.inside_rear-46,0),
    ]
    # Manufacturer-published 8 mm width. Locate its adhesive face on the
    # 11.2 mm LED bed measured from the OEM section. Thickness remains open.
    depth = 8.5421
    led_edge = [(5+(s+depth)/sqrt(2),5+(depth-s)/sqrt(2),z)
                for s,z in ((-4,10),(4,10),(4,210),(-4,210))]
    led_face = cq.Face.makeFromWires(cq.Wire.makePolygon([V(*point) for point in led_edge], close=True))
    items=[]
    for index,(x,y,angle) in enumerate(positions,1):
        def pose(shape):
            return translate(shape.rotate(V(),V(0,0,1),angle),x,y,89)
        items.append(stock(f"L{index}","KLUŚ 45-16 A08504A_1 · tramo 220 mm",group,
                           pose(profile),METAL,"Aluminio anodizado",state="seccion OEM OBJ"))
        tape=box(16.0001,1.3,17.5,16.5,8.1,202.5) if index in (1,4) else box(1.3,16.0001,17.5,8.1,16.5,202.5)
        items.append(stock(f"LT{index}","Junta adhesiva de fijacion 0,5 × 6,8 × 185",group,
                           pose(tape),BLACK,"Cinta acrilica de transferencia",
                           state="espesor y adhesion en vapor por validar; alternativa clip OEM"))
        items.append(stock(f"COB{index}","Ephycob 300D 5 V · superficie de tira 8 × 200",group,
                           pose(led_face),(0.96,0.82,0.39),"Tira COB 4000 K",
                           state="solo superficie de apoyo; espesor y terminales pendientes"))
    return items


def detector(p):
    group="Frontal"
    # Locate the OEM part in the dry bay. Only the physical verification can release
    # the spring/plunger interface, so the mount is a replaceable, slotted subassembly.
    shape=asset("auxiliary/door/asq10228.step")
    top=p.shelf+p.panel
    x,y=120.0,30.0
    # +Y of the lever points towards the fascia and +X of the leads towards the side.
    switch=orient(shape,(x,y,top+12.2),(-1,0,0),(0,0,1))
    foot=box(-17,-10,0,17,4,4)
    upright=box(-8,-5,4,8,7,8)
    mount=foot.fuse(upright)
    mount=cut_holes(mount,[(-12,0),(12,0)],3.6,8)
    mount=mount.cut(cylinder(1.8,8.2,(-4.45,0,-0.1)))
    mount=mount.cut(cylinder(2.0,4.2,(3.95,0,3.9))).clean()
    arm_x = 128.0
    arm = box(-5,0,0,5,4,80)
    arm = arm.fuse(box(-4,0,74,4,16.35-(p.door_outer_y-4),80))
    for z in (268,279):
        arm = arm.cut(axis_cylinder(p.printed_hole,4.2,(0,-0.1,z-263),(0,1,0)))
    arm=arm.clean()
    parts=[
        printed("P39","Accionador frontal de prueba","Puerta",arm,
                translate(arm,arm_x,p.door_outer_y-4,263),
                door=True,state="punta de referencia; ajustar carrera con detector real"),
    ]
    for z in (268,279):
        parts.extend(mounted_hardware(f"Striker{z}",(arm_x,p.door_outer_y-4,z),(0,1,0),p.panel+4,16,door=True))
    return [
        stock("E04","Panasonic ASQ10228 · STEP OEM",group,switch,(0.19,0.22,0.23),
              state="seleccion electrica propuesta; comprobar logica y accionamiento"),
        printed("P38","Soporte ajustable del detector",group,mount.clean(),
                translate(mount.clean(),x,y,top),state="solo prototipo; comprobar accionador con muestra"),
        *mounted_hardware("SWfeetL",(x-12,y,p.shelf),(0,0,1),p.panel+4,16),
        *mounted_hardware("SWfeetR",(x+12,y,p.shelf),(0,0,1),p.panel+4,16),
        *parts,
    ]
