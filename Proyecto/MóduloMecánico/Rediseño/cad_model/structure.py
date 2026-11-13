import cadquery as cq

from .geometry import Item, V, box, cylinder, cut_holes, orient, standard_screw, m3_nut, translate, xy_panel

WOOD = (0.64, 0.51, 0.34)
WHITE = (0.87, 0.88, 0.84)
BLACK = (0.14, 0.17, 0.19)
METAL = (0.65, 0.68, 0.72)
AQUA = (0.34, 0.66, 0.63)


def printed(key, label, group, native, world=None, *, part=None, door=False, state="prototipo"):
    return Item(key, label, group, native if world is None else world, BLACK, "PETG", "FDM",
                native, part or key, state, door)


def stock(key, label, system, shape, color=METAL, material="", state="nominal", door=False):
    return Item(key, label, system, shape, color, material, state=state, door=door)


def laser(key, label, native, shape, door=False, *, material="Contrachapado abedul 6 mm sellado", color=WOOD):
    return Item(key, label, "Carcasa" if not door else "Puerta", shape, color, material,
                "laser", native, key, "prototipo", door)


def axis_cylinder(diameter, length, point, direction):
    return cylinder(diameter / 2, length, point, direction)


def mounted_hardware(key, head, axis, stack, length, group="Fijaciones", door=False):
    direction = V(*axis)
    point = V(*head)
    x_direction = (1, 0, 0) if axis[0] == 0 else (0, 1, 0)
    screw = orient(standard_screw(length), point, x_direction, axis)
    nut = orient(m3_nut(), point + direction.multiply(stack), x_direction, axis)
    return [
        stock(f"{key}_screw", f"ISO 4762 M3×{length} · {key}", group, screw, material="Acero A2", door=door),
        stock(f"{key}_nut", f"ISO 4032 M3 · {key}", group, nut, material="Acero A2", door=door),
    ]


def side_holes(p):
    deck = [(y-8, z) for y in (48, 260) for z in (p.panel + 8, p.shelf + p.panel + 8, p.lid_z - 8)]
    ends = [(p.panel + 8, z+4) for z in (14, 304)] + [(p.inside_rear - 8, z+4) for z in (14, 310)]
    return deck + ends


def deck_holes(p):
    return [(side * (p.inside_x - 8), y) for side in (-1, 1) for y in (48, 260)]


def fascia_holes(p):
    return [(sign*(p.inside_x-8), z-4) for sign in (-1,1) for z in (14,304)]


def hinge_specs(p):
    return [(i, z) for i, z in enumerate((86.0, 222.0), 1)]


def wood_panels(p):
    w, d, h, t = p.width, p.depth, p.height, p.panel
    ext = w / 2
    ix = p.inside_x
    deck = deck_holes(p)
    hinge_front = [(p.hinge_x + 6.6, z + dz) for _, z in hinge_specs(p) for dz in (-11, 11)]
    hinge_door = [(p.hinge_x + 22.5, z + dz) for _, z in hinge_specs(p) for dz in (-11, 11)]
    door_hand = [(p.aperture / 2 - 34, z) for z in (132, 170)]
    door_striker = [(128,z) for z in (268,279)]
    latch_pivot = [(p.latch_x, 151)]
    vent_zs = (290, 299, 308)
    vent_slots = [(-p.vent_width / 2, z - p.vent_slot / 2, p.vent_width / 2, z + p.vent_slot / 2)
                  for z in vent_zs]
    front_mounts = fascia_holes(p)
    rear_mounts = [(sign*(ix-8), z-4) for sign in (-1,1) for z in (14,310)]
    def front_frame():
        frame = xy_panel((-ext, t, ext, p.lid_z), t, front_mounts + hinge_front + latch_pivot,
                         [(-p.aperture / 2, p.sill, p.aperture / 2, p.lintel),
                          (-p.screen_width / 2, p.screen_z - p.screen_height / 2,
                           p.screen_width / 2, p.screen_z + p.screen_height / 2),
                          (122,336,134,344)], p.laser_hole)
        return cut_holes(frame, [(x, p.screen_z) for x in (-54, 54)], 16.0, t)
    vent_mounts = [(x, z) for x in (-49, 49) for z in (278, 314)]
    service_mounts = [(x, z) for x in (74, 139) for z in (335, 366)]
    service = [(78, 337, 135, 364)]
    door_width = p.aperture + 2 * p.door_overlay
    door_bounds = (-door_width / 2, p.sill - p.door_overlay, door_width / 2, p.lintel + p.door_overlay)
    saddle_mounts = [(x, p.center_y + y) for x, y in ((-65, -57), (65, -57), (-65, 57), (65, 57))]
    display_mounts = [(x, 27) for x in (-38, 38)]
    carrier_mounts = [(x, p.center_y + y) for x in (-94,94) for y in (-19,19)]
    ring_mounts = [(x, p.center_y+y) for x,y in ((-72,0),(72,0),(0,-72),(0,72))]
    control_mounts = [(x, y) for x in (-113, -72) for y in (234, 285)]
    switch_mounts = [(x,30) for x in (108,132)]
    led_risers = [(x, y) for x in (-134, 134) for y in (45, 258)]
    shelf = xy_panel((-ix, t, ix, d-t), t, deck + display_mounts + carrier_mounts + control_mounts + ring_mounts + switch_mounts,
                     [(x-7, y-4, x+7, y+4) for x, y in led_risers] +
                     [(-72, 285, -52, 295)], p.laser_hole)
    shelf = shelf.cut(cylinder(p.optical_hole/2, t+0.2, (0,p.center_y,-0.1))).clean()
    base = xy_panel((-ext, 0, ext, d), t, deck + saddle_mounts, diameter=p.laser_hole)
    roof = xy_panel((-ext, 0, ext, d), t, deck, diameter=p.laser_hole)
    front = front_frame()
    rear = xy_panel((-ext, t, ext, p.lid_z), t, rear_mounts + vent_mounts + service_mounts,
                    vent_slots + service, p.laser_hole)
    sides = xy_panel((t, t, d-t, p.lid_z), t, side_holes(p), diameter=p.laser_hole)
    hinge_reliefs = [(door_bounds[0]-0.1, z-3.1, p.hinge_x+9.7, z+3.1) for _, z in hinge_front]
    latch_relief = [(p.latch_x-3.3, 147.7, door_bounds[2]+0.1, 154.3)]
    door = xy_panel(door_bounds, t, hinge_door + door_hand + door_striker, hinge_reliefs+latch_relief,
                    diameter=p.laser_hole)
    return [
        laser("P01", "Piso", base, base),
        laser("P02", "Tapa superior desmontable", roof, translate(roof,z=p.lid_z)),
        laser("P03", "Frente con vano y fascia", front, orient(front,(0,t,0),(1,0,0),(0,-1,0))),
        laser("P04", "Panel posterior", rear, orient(rear,(0,d,0),(1,0,0),(0,-1,0))),
        laser("P05", "Panel lateral izquierdo", sides, orient(sides,(-ext,0,0),(0,1,0),(1,0,0))),
        laser("P06", "Panel lateral derecho", sides, orient(sides,(ix,0,0),(0,1,0),(1,0,0))),
        laser("P07", "Divisor de camara humeda", shelf, translate(shelf,z=p.shelf)),
        laser("P08", "Puerta opaca desmontable", door, orient(door,(0,-p.door_gap,0),(1,0,0),(0,-1,0)), True),
    ]


def angle_cleats(p):
    # Each joint aligns a circular bore through a 6 mm panel and a 4 mm cleat leg.
    items = []
    for side in (-1, 1):
        for i, y in enumerate((48,260), 1):
            for j, surface in enumerate(("floor","shelf","roof"), 1):
                # local +X points inwards from the side wall, local +Z from the joined deck into the cleat.
                sign_z = -1 if surface == "roof" else 1
                deck_z = {"floor": p.panel, "shelf": p.shelf+p.panel, "roof": p.lid_z}[surface]
                corner = (side*p.inside_x,y,deck_z)
                offset = 8*side*sign_z
                cleat = box(0,min(-5,offset-5),0,18,max(5,offset+5),4).fuse(
                    box(0,min(-5,offset-5),0,4,max(5,offset+5),18)
                )
                cleat = cleat.cut(axis_cylinder(p.printed_hole,20,(8,0,-1),(0,0,1)))
                cleat = cleat.cut(axis_cylinder(p.printed_hole,20,(-1,offset,8),(1,0,0))).clean()
                placed = orient(cleat,corner,(-side,0,0),(0,0,sign_z))
                key = f"A{side+1}{i}{j}"
                items.append(printed(key,"Escuadra de panel","Carcasa",cleat,placed,part="P20A" if offset>0 else "P20B"))
                screw_z = deck_z - sign_z*p.panel
                foot_stack = 4 if surface == "floor" else 0
                items.extend(mounted_hardware(f"{key}D",(side*(p.inside_x-8),y,screw_z-foot_stack),
                                              (0,0,sign_z),p.panel+4+foot_stack,20 if foot_stack else 16))
                items.extend(mounted_hardware(f"{key}L",(side*p.width/2,y-8,deck_z+8*sign_z),(-side,0,0),p.panel+4,16))
    return items


def front_rear_blocks(p):
    items = []
    for rear in (False, True):
        for side in (-1,1):
            for j, z in enumerate((14.0,310.0) if rear else (14.0,304.0), 1):
                y = p.inside_rear if rear else p.panel
                axis = (0,-1,0) if rear else (0,1,0)
                offset = 4*side*axis[1]
                cleat = box(0,-8,0,18,8,4).fuse(box(0,-8,0,4,8,18))
                cleat = cleat.cut(axis_cylinder(p.printed_hole,20,(8,-offset,-1),(0,0,1)))
                cleat = cleat.cut(axis_cylinder(p.printed_hole,20,(-1,offset,8),(1,0,0))).clean()
                origin = (side*p.inside_x,y,z)
                key = f"R{int(rear)}{side+1}{j}"
                items.append(printed(key,"Escuadra del marco","Carcasa",cleat,
                                     orient(cleat,origin,(-side,0,0),axis),part="P21A" if offset>0 else "P21B"))
                head = (side*(p.inside_x-8),p.depth if rear else 0,z-4)
                items.extend(mounted_hardware(key,head,axis,p.panel+4,16))
                side_head = (side*p.width/2,y+axis[1]*8,z+4)
                items.extend(mounted_hardware(f"{key}L",side_head,(-side,0,0),p.panel+4,16))
    return items


def hinge_leaves(p):
    items = []
    hx, hy = p.hinge_x,p.hinge_y
    for index, z in hinge_specs(p):
        key=f"H{index}"
        fixed_plate=box(-3,8.65,-16,8.5,10,16)
        fixed_web=box(-3,4.2,-16,1,8.65,16)
        fixed = fixed_plate.fuse(fixed_web)
        for low, high in ((-15,-5.25),(5.25,15)):
            fixed=fixed.fuse(box(-3,-1,low,1,4.2,high),cylinder(4.0,high-low,(0,0,low)))
        fixed=fixed.cut(cylinder(2.15,34,(0,0,-17)))
        moving = box(6,-2,-16,32,2.5,16).fuse(box(-0.5,-2,-5,9,2.5,5))
        moving = moving.fuse(cylinder(4,10,(0,0,-5))).cut(cylinder(2.15,12,(0,0,-6)))
        # Local Y=10 is the fixed panel face and Y=2.5 is the moving panel face.
        for dz in (-11,11):
            fixed=fixed.cut(axis_cylinder(p.printed_hole,6,(6.6,7,dz),(0,1,0)))
            moving=moving.cut(axis_cylinder(p.printed_hole,7,(22.5,-3,dz),(0,1,0)))
            items.extend(mounted_hardware(f"{key}F{dz}",(hx+6.6,hy+8.65,z+dz),(0,1,0),p.panel+1.35,12))
            items.extend(mounted_hardware(f"{key}M{dz}",(hx+22.5,hy-2,z+dz),(0,1,0),p.panel+4.5,16,door=True))
        fixed,moving=fixed.clean(),moving.clean()
        items.extend([
            printed(f"{key}_F","Bisagra · hoja fija","Puerta",fixed,translate(fixed,hx,hy,z),part="P22"),
            printed(f"{key}_M","Bisagra · hoja movil","Puerta",moving,translate(moving,hx,hy,z),part="P23",door=True),
            stock(f"{key}_pin","Pasador liso inoxidable Ø4 × 33","Puerta",cylinder(2,33,(hx,hy,z-16.5)),
                  material="Varilla inox Ø4",state="corte a medida"),
        ])
    return items


def door_accessories(p):
    # The solid gasket is modeled in its installed nominal thickness.
    x=p.aperture/2
    y0=-p.door_gap
    outer=box(-x-3,y0,p.sill-3,x+3,0,p.lintel+3)
    inner=box(-x-0.8,y0-0.1,p.sill-0.8,x+0.8,0.1,p.lintel+0.8)
    gasket=outer.cut(inner).clean()
    for _, z in hinge_specs(p):
        for dz in (-11,11):
            gasket=gasket.cut(box(-x-3.1,y0-0.1,z+dz-3.1,p.hinge_x+9.7,0.1,z+dz+3.1))
    gasket=gasket.cut(box(p.latch_x-3.3,y0-0.1,147.7,x+3.1,0.1,154.3)).clean()
    handle=box(-9,13,0,9,20,54).fuse(box(-9,0,0,9,13,14),box(-9,0,40,9,13,54))
    for local_z in (8,46):
        handle=handle.cut(axis_cylinder(p.printed_hole,22,(0,-1,local_z),(0,1,0)))
    handle=handle.clean()
    # Handle feet face the door and keep all hand forces on the door assembly.
    xh=p.aperture/2-34
    items=[
        stock("G01","Junta frontal comprimida","Puerta",gasket,(0.20,0.22,0.22),"Silicona de celda cerrada",door=True),
        printed("P24","Tirador frontal","Puerta",handle,
                orient(handle,(xh,p.door_outer_y,178),(1,0,0),(0,0,-1)),door=True),
    ]
    for z in (132,170):
        items.extend(mounted_hardware(f"PH{z}",(xh,p.door_outer_y-20,z),(0,1,0),p.panel+20,30,door=True))
    latch_x=p.latch_x
    # Pivot axis in the fixed jamb; the closed lever overlaps the outside of the door.
    lever=box(-18,-3,0,3,3,4).fuse(cylinder(3.1,4,(0,0,0))).clean()
    lever=cut_holes(lever,[(0,0)],p.printed_hole,4)
    items.append(printed("P25","Lengueta giratoria de cierre","Puerta",lever,
                         orient(lever,(latch_x,p.door_outer_y-4,151),(1,0,0),(0,1,0))))
    sleeve=cylinder(3,p.door_gap+p.panel,(latch_x,p.door_outer_y,151),(0,1,0))
    sleeve=sleeve.cut(axis_cylinder(3.4,10,(latch_x,p.door_outer_y-1,151),(0,1,0)))
    items.append(stock("G02","Separador tubular del cierre Ø6","Puerta",sleeve,material="Tubo inox cortado"))
    items.extend(mounted_hardware("Latch",(latch_x,p.door_outer_y-4,151),(0,1,0),p.panel+p.door_gap+p.panel+4,20))
    return items


def base_feet(p):
    items=[]
    # Removable feet use the existing holes and keep all floor hardware off the bench.
    for sign in (-1,1):
        for y in (48,260):
            native=box(-12,-14,0,12,14,8)
            native=cut_holes(native,[(0,0)],3.6,8)
            native=native.cut(cylinder(3.2,4.1,(0,0,-0.1))).clean()
            x=sign*(p.inside_x-8)
            items.append(printed(f"F{sign}_{y}","Pie de apoyo con alojamiento para cabeza","Carcasa",native,
                                 translate(native,x,y,-8),part="P29"))
    return items


def vent_baffle(p):
    # Rearward plenum is closed on top and exits downwards.
    p0=box(-54,0,0,54,19,47)
    chamber=box(-43,-0.1,-0.1,43,15.5,43)
    baffle=p0.cut(chamber)
    for x in (-49,49):
        for z in (4,40):
            baffle=baffle.cut(axis_cylinder(p.printed_hole,20,(x,-0.1,z),(0,1,0)))
    baffle=baffle.clean()
    rear=translate(baffle,y=p.depth,z=274)
    items=[printed("P26","Deflector posterior con descarga inferior","Vapor",baffle,rear)]
    for x in (-49,49):
        for z in (278,314):
            items.extend(mounted_hardware(f"V{x}_{z}",(x,p.depth+19,z),(0,-1,0),19+p.panel,30))
    return items


def optical_window(p):
    axis=(0,p.center_y)
    glass=cylinder(p.optical_window/2,p.window_thickness,(*axis,p.window_z))
    seal=cylinder(p.optical_window/2,p.window_gasket,(*axis,p.window_z-p.window_gasket))
    seal=seal.cut(cylinder(p.optical_hole/2,p.window_gasket+0.2,(*axis,p.window_z-p.window_gasket-0.1)))
    ring = cylinder(69,5,(0,0,0))
    ears = [(-72,0),(72,0),(0,-72),(0,72)]
    for x,y in ears:
        ring = ring.fuse(cylinder(6,5,(x,y,0)))
    ring = (ring.cut(cylinder(p.optical_hole/2,5.2,(0,0,-0.1)))
            .cut(cylinder(p.optical_window/2+0.4,p.window_gasket+p.window_thickness+0.25,(0,0,-0.05))))
    ring = cut_holes(ring,ears,p.printed_hole,5).clean()
    items = [
        stock("W01","Ventana optica circular Ø130","Vapor",glass,(0.55,0.79,0.9),"Vidrio optico 2 mm",state="corte a medida"),
        stock("W02","Junta circular de ventana","Vapor",seal,(0.22,0.25,0.23),"Silicona 1 mm",state="corte a medida"),
        printed("P27","Anillo de retencion de ventana","Vapor",ring,translate(ring,y=p.center_y,z=p.shelf+p.panel)),
    ]
    for x,y in ears:
        items.extend(mounted_hardware(f"W{x}_{y}",(x,p.center_y+y,p.shelf+p.panel+5),(0,0,-1),p.panel+5,16))
    return items


def structure(p):
    return [*wood_panels(p),*base_feet(p),*angle_cleats(p),*front_rear_blocks(p),*hinge_leaves(p),
            *door_accessories(p),*vent_baffle(p),*optical_window(p)]
