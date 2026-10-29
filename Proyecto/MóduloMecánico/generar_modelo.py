"""FoodScan: modelo conceptual multipartes, unidades en mm.

Requiere cadquery==2.6.1. No modifica el esquema electrico.
Las medidas comerciales son envolventes aproximadas, no fichas de fabricante.
"""
from pathlib import Path
import csv
import json
import math
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
LIBS = ROOT / 'tmp' / 'foodscan_cad_libs'
if LIBS.exists():
    sys.path.insert(0, str(LIBS))
import cadquery as cq

HERE = Path(__file__).resolve().parent
CAD = HERE / 'CAD'
IMG = HERE / 'Vistas'
STL = HERE / 'STL_provisionales'
WORK = ROOT / 'tmp' / 'foodscan_cad_work'
for folder in (CAD, IMG, STL, WORK):
    folder.mkdir(parents=True, exist_ok=True)

P = dict(ancho=320, fondo=320, alto=350, panel=3, base=6,
         plataforma=220, plataforma_z=38, plataforma_espesor=6,
         plato_diametro=200, plano_plato_z=48, lente_z=318,
         puerta_ancho=311, puerta_alto=338, apertura_grados=105)
WHITE = (.87, .89, .87)
BLUE = (.10, .39, .53)
GREEN = (.10, .43, .31)
BLACK = (.10, .13, .16)
METAL = (.65, .69, .72)
YELLOW = (.96, .82, .34)
parts = []

def box(dx, dy, dz, x, y, z):
    return cq.Workplane('XY').box(dx, dy, dz, centered=(False,False,False)).translate((x,y,z))

def cyl(r, h, x, y, z, axis='z'):
    result = cq.Workplane('XY').circle(r).extrude(h)
    if axis == 'x':
        result = result.rotate((0,0,0),(0,1,0),90)
    elif axis == 'y':
        result = result.rotate((0,0,0),(1,0,0),-90)
    return result.translate((x,y,z))

def holes_z(shape, coords, diameter, z, height):
    for x, y in coords:
        shape = shape.cut(cyl(diameter/2, height, x,y,z))
    return shape

def add(name, shape, color, material, kind, moving=False):
    shape = shape.val() if isinstance(shape, cq.Workplane) else shape
    assert shape.isValid(), name
    assert len(shape.Solids()) == 1, (name, len(shape.Solids()))
    parts.append(dict(name=name, shape=shape, color=color, material=material,
                      kind=kind, moving=moving))
    return shape

def build():
    # Paneles independientes; base y plataforma tienen dos laminas de 3 mm.
    for i in range(2):
        base = holes_z(box(320,320,3,-160,-160,3*i), [(-30,0),(-15,0)],3.4,-1,8)
        add(f'M01_Base_capa_{i+1}',base,WHITE,'MDF blanco 3 mm','panel')
    left = box(3,320,341,-160,-160,6)
    right = box(3,320,341,157,-160,6)
    # Huecos de referencia de panel: comprobar con jack e interruptor reales.
    right = right.cut(cyl(4,8,155,130,67,'x'))
    right = right.cut(box(8,21,13,155,79.5,60.5))
    add('M02_Lateral_izquierdo',left,WHITE,'MDF blanco 3 mm','panel')
    add('M03_Lateral_derecho',right,WHITE,'MDF blanco 3 mm','panel')
    add('M04_Fondo',box(314,3,341,-157,157,6),WHITE,'MDF blanco 3 mm','panel')
    add('M05_Tapa_superior',box(320,320,3,-160,-160,347),WHITE,'MDF blanco 3 mm','panel')
    door = box(311,3,338,-155.5,-160,7.5)
    for z in (179,211):
        door = door.cut(cyl(1.7,7,120,-162,z,'y'))
    add('M06_Puerta',door,WHITE,'MDF blanco 3 mm','panel',True)
    for i in range(2):
        platform = holes_z(box(220,220,3,-110,-110,38+3*i),[(15,0),(30,0)],3.4,37,9)
        add(f'M07_Plataforma_capa_{i+1}',platform,(.80,.83,.82),'MDF blanco 3 mm','panel')

    # Ruta de carga: base -> soporte fijo -> celda -> soporte movil -> plataforma.
    fixed = holes_z(box(30,20,12,-37.5,-10,6),[(-30,0),(-15,0)],3.4,5,15)
    add('P01_Adaptador_fijo',fixed,BLUE,'PLA+','impresa')
    cell = box(75,12,12,-37.5,-6,18)
    for x in (-5,5):
        cell = cell.cut(cyl(4,14,x,-7,24,'y'))
    cell = holes_z(cell,[(x,0) for x in (-30,-15,15,30)],3.4,17,15)
    add('E02_LC1_Celda_5kg_APROX',cell,METAL,'Aluminio - envolvente aproximada','electronica')
    mobile = holes_z(box(30,20,8,7.5,-10,30),[(15,0),(30,0)],3.4,29,11)
    add('P02_Adaptador_movil',mobile,BLUE,'PLA+','impresa')
    for i,(x,y) in enumerate([(-80,-80),(80,-80),(-80,80),(80,80)],1):
        add(f'P03_Tope_{i}_holgura_1mm',cyl(4,31,x,y,6),BLUE,'PLA+','impresa')
    # Plato con fondo plano de 4 mm y borde de 5 mm. Plano de referencia z=48.
    plate = cyl(100,9,0,0,44).cut(cyl(96,6,0,0,48))
    add('M08_Plato_200mm_REFERENCIA',plate,(.97,.97,.95),'Plato lavable - referencia','referencia')

    # Camara: lente mirando a -Z; anillo y cuatro pilares conectados a la tapa.
    holder = box(46,54,3,-23,-27,322).cut(box(20,30,5,-10,-15,321))
    for x in (-20,20):
        for y in (-19,19):
            holder = holder.union(box(6,6,22,x-3,y-3,325))
    add('P04_Soporte_camara',holder,BLUE,'PLA+','impresa')
    pcb = box(27,40,1.6,-13.5,-20,325)
    add('E01_U1_ESP32_CAM_PCB_APROX',pcb,GREEN,'PCB - 27 x 40 aprox.','electronica')
    add('E01_U1_Blindaje_APROX',box(20,16,4,-10,2,326.6),METAL,'Metal - referencia','electronica')
    add('E01_OV2640_Lente_APROX',cyl(4,7,0,0,318),BLACK,'Camara - referencia','electronica')

    # Tres placas LED recortadas de 90 x 22, cuatro emisores por placa.
    for side in ('izquierdo','derecho','posterior'):
        if side == 'izquierdo':
            board = box(1.6,90,22,-153,-45,266)
            diffuser = box(.8,90,22,-143,-45,266)
            for j,y in enumerate((-33.75,-11.25,11.25,33.75),1):
                add(f'E05_LED_izq_{j}',cyl(2.5,5,-151.4,y,277,'x'),YELLOW,'LED blanco 5 mm','electronica')
            rails = box(4,96,3,-157,-48,266).union(box(4,96,3,-157,-48,285))
            rails = rails.union(box(12,3,22,-153,-48,266)).union(box(12,3,22,-153,45,266))
        elif side == 'derecho':
            board = box(1.6,90,22,151.4,-45,266)
            diffuser = box(.8,90,22,142.2,-45,266)
            for j,y in enumerate((-33.75,-11.25,11.25,33.75),1):
                add(f'E05_LED_der_{j}',cyl(2.5,5,146.4,y,277,'x'),YELLOW,'LED blanco 5 mm','electronica')
            rails = box(4,96,3,153,-48,266).union(box(4,96,3,153,-48,285))
            rails = rails.union(box(12,3,22,141,-48,266)).union(box(12,3,22,141,45,266))
        else:
            board = box(90,1.6,22,-45,151.4,266)
            diffuser = box(90,.8,22,-45,142.2,266)
            for j,x in enumerate((-33.75,-11.25,11.25,33.75),1):
                add(f'E05_LED_post_{j}',cyl(2.5,5,x,146.4,277,'y'),YELLOW,'LED blanco 5 mm','electronica')
            rails = box(96,4,3,-48,153,266).union(box(96,4,3,-48,153,285))
            rails = rails.union(box(3,12,22,-48,141,266)).union(box(3,12,22,45,141,266))
        add(f'P05_Soporte_LED_{side}',rails,BLUE,'PLA+','impresa')
        add(f'E15_Placa_LED_{side}',board,GREEN,'PCB recortada - referencia','electronica')
        add(f'M09_Difusor_{side}',diffuser,(.95,.94,.77),'Polipropileno translucido','estructura')

    # Electronica separada de la plataforma, junto al fondo.
    hx = box(33,20,1.6,-75,123,16)
    add('E03_U2_HX711_PCB_APROX',hx,GREEN,'PCB - envolvente aproximada','electronica')
    add('E03_U2_HX711_IC_APROX',box(10,6,2,-63,130,17.6),BLACK,'IC - referencia','electronica')
    for i,(x,y) in enumerate([(-72,126),(-45,126),(-72,140),(-45,140)],1):
        add(f'P06_Separador_HX711_{i}',cyl(2.5,10,x,y,6),BLUE,'PLA+','impresa')
    add('E15_Placa_distribucion_90x30',box(90,30,1.6,20,121,12),GREEN,'PCB recortada - referencia','electronica')
    for i,(x,y) in enumerate([(24,125),(106,125),(24,147),(106,147)],1):
        add(f'P07_Separador_distribucion_{i}',cyl(2.5,6,x,y,6),BLUE,'PLA+','impresa')
    add('E11_C1_470uF_APROX',cyl(5,13,97,137,13.6),BLACK,'Condensador - referencia','electronica')
    add('E14_Portafusible_APROX',box(28,9,6,35,130,13.6),BLACK,'Portafusible - referencia','electronica')
    add('E13_F1_5x20',cyl(2.5,20,39,134.5,22.1,'x'),(.80,.83,.80),'Fusible - referencia','electronica')
    cover = box(215,38,34,-95,117,6).cut(box(211,34,33,-93,119,5))
    cover = cover.cut(box(12,5,5,-84,115,9)).cut(box(12,5,5,96,115,9))
    add('P08_Cubierta_conexiones',cover,BLUE,'PLA+ - cubierta desmontable','impresa')

    # Jack e interruptor al lateral, con huecos nominales de referencia.
    jack = cyl(4,15,145,130,67,'x').union(cyl(6,2,160,130,67,'x'))
    jack = jack.cut(cyl(2.75,5,159,130,67,'x'))
    add('E09_J1_Jack_DC_APROX',jack,BLACK,'Jack DC - referencia','electronica')
    switch = box(8,21,13,149,79.5,60.5).union(box(2,23,15,160,78.5,59.5))
    switch = switch.union(box(3,19,11,157,80.5,61.5))
    add('E10_SW1_Interruptor_APROX',switch,BLACK,'Interruptor - referencia','electronica')
    bracket = box(22,18,3,135,-157,291)
    bracket = bracket.union(box(3,18,20,154,-157,294))
    add('P09_Soporte_detector_puerta',bracket,BLUE,'PLA+','impresa')
    add('E04_SW2_Microswitch_APROX',box(18,6,10,136,-153,294),BLACK,'Microswitch - referencia','electronica')
    add('E04_SW2_Palanca_APROX',box(15,4,1,138,-157,304),METAL,'Palanca - referencia','electronica')

    # Uniones simples de paneles, dos alturas en las cuatro esquinas.
    for i,(sx,sy,z) in enumerate([(sx,sy,z) for z in (6,327) for sx in (-1,1) for sy in (-1,1)],1):
        corner = box(20,3,20,0,0,0).union(box(3,20,20,0,0,0))
        if sx == 1:
            corner = corner.mirror('YZ')
        if sy == 1:
            corner = corner.mirror('XZ')
        corner = corner.translate((157*sx,157*sy,z))
        add(f'P10_Escuadra_{i}',corner,BLUE,'PLA+','impresa')
    # Bisagras ilustrativas sin relaciones cinematicas exportadas.
    for i,z in enumerate((65,260),1):
        fixed_leaf = box(3,22,25,-163,-164,z)
        fixed_leaf = fixed_leaf.cut(cyl(2.6,9,-160,-164,z+8))
        fixed_leaf = fixed_leaf.union(cyl(2.5,8,-160,-164,z)).union(cyl(2.5,8,-160,-164,z+17))
        moving_leaf = box(25,3,25,-155.5,-163,z)
        moving_leaf = moving_leaf.union(box(28,2,9,-160,-165,z+8)).union(cyl(2.5,9,-160,-164,z+8))
        add(f'M10_Bisagra_{i}_fija',fixed_leaf,METAL,'Bisagra 25 mm - simplificada','estructura')
        add(f'M10_Bisagra_{i}_movil',moving_leaf,METAL,'Bisagra 25 mm - simplificada','estructura',True)
    handle = box(14,18,8,113,-178,175).union(box(14,18,8,113,-178,207))
    handle = handle.union(box(14,6,40,113,-184,175))
    for z in (179,211):
        handle = handle.cut(cyl(1.7,22,120,-185,z,'y'))
    add('P11_Manija',handle,BLUE,'PLA+','impresa',True)
    for i,(x,y) in enumerate([(-140,-140),(140,-140),(-140,140),(140,140)],1):
        add(f'M11_Pata_goma_{i}',cyl(8,6,x,y,-6),BLACK,'Goma','estructura')

def posed(p, opened=False):
    shape = p['shape']
    if opened and p['moving']:
        shape = shape.rotate((-160,-164,0),(-160,-164,1),-105)
    return shape

def export():
    manifest = []
    for p in parts:
        bb = p['shape'].BoundingBox()
        manifest.append(dict(nombre=p['name'], material=p['material'], tipo=p['kind'],
            volumen_mm3=round(p['shape'].Volume(),3),
            envolvente_mm=[round(v,3) for v in (bb.xlen,bb.ylen,bb.zlen)],
            min_mm=[round(v,3) for v in (bb.xmin,bb.ymin,bb.zmin)],
            max_mm=[round(v,3) for v in (bb.xmax,bb.ymax,bb.zmax)]))
    for opened, filename in ((False,'FoodScan_Conjunto_v1.step'),(True,'FoodScan_Puerta_abierta_v1.step')):
        assy = cq.Assembly(name='FoodScan_Equipo10_v1')
        for p in parts:
            assy.add(posed(p,opened),name=p['name'],color=cq.Color(*p['color']))
        target = WORK / filename
        assy.save(str(target),'STEP',mode='default')
        reread = cq.importers.importStep(str(target)).val()
        assert reread.isValid(), filename
        assert len(reread.Solids()) == len(parts), (filename,len(reread.Solids()),len(parts))
        shutil.copy2(target,CAD/filename)
    # Un unico compuesto de cuerpos independientes para importacion directa multipartes.
    target = WORK / 'FoodScan_Multipartes_v1.step'
    cq.exporters.export(cq.Compound.makeCompound([p['shape'] for p in parts]),str(target))
    reread = cq.importers.importStep(str(target)).val()
    assert reread.isValid() and len(reread.Solids()) == len(parts)
    shutil.copy2(target,CAD/target.name)
    for name in ('P01_Adaptador_fijo','P02_Adaptador_movil','P04_Soporte_camara','P11_Manija','P10_Escuadra_1'):
        p = next(p for p in parts if p['name'] == name)
        sh = p['shape']
        bb = sh.BoundingBox()
        sh = sh.translate((-bb.xmin,-bb.ymin,-bb.zmin))
        target = WORK / (name+'.stl')
        cq.exporters.export(sh,str(target),tolerance=.03,angularTolerance=.1)
        shutil.copy2(target,STL/target.name)
    (CAD/'Inventario_modelo.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    with (CAD/'Inventario_modelo.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f)
        w.writerow(['Pieza','Material','Tipo','X mm','Y mm','Z mm'])
        for p in manifest:
            w.writerow([p['nombre'],p['material'],p['tipo'],*p['envolvente_mm']])
    return manifest

def verify():
    # Verifica interferencias volumetricas de todos los cuerpos de la pose cerrada.
    clashes=[]
    for i,a in enumerate(parts):
        aa=a['shape'].BoundingBox()
        for b in parts[i+1:]:
            bb=b['shape'].BoundingBox()
            if min(aa.xmax,bb.xmax)-max(aa.xmin,bb.xmin) <= 1e-5: continue
            if min(aa.ymax,bb.ymax)-max(aa.ymin,bb.ymin) <= 1e-5: continue
            if min(aa.zmax,bb.zmax)-max(aa.zmin,bb.zmin) <= 1e-5: continue
            vol=a['shape'].intersect(b['shape']).Volume()
            if vol>1e-3:
                clashes.append([a['name'],b['name'],round(vol,4)])
    info=dict(herramienta='CadQuery '+cq.__version__,unidades='mm',
              cuerpos=len(parts),cuerpos_validos=all(p['shape'].isValid() for p in parts),
              holgura_plataforma_pared_mm=47,holgura_topes_mm=1,
              distancia_lente_plano_plato_mm=318-48,
              solapes_volumetricos=clashes,
              limites='Geometria conceptual. No valida resistencia, optica, tolerancias, ni piezas comerciales reales.')
    (CAD/'Verificacion_geometrica.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(info,ensure_ascii=False,indent=2))
    assert not clashes, 'Corregir interferencias antes de entregar'

def render_view(filename,opened=False,cutaway=False,weighing=False):
    import vtk
    renderer=vtk.vtkRenderer()
    renderer.SetBackground(.965,.973,.978)
    renderer.SetBackground2(.90,.93,.95)
    renderer.GradientBackgroundOn()
    for p in parts:
        if cutaway and p['name'] in ('M03_Lateral_derecho','M05_Tapa_superior','M06_Puerta','P11_Manija'):
            continue
        if cutaway and 'Bisagra' in p['name']: continue
        if weighing and not (p['name'].startswith(('M01','M07','P01','P02','P03','E02'))): continue
        verts, triangles = posed(p,opened).tessellate(.3,.18)
        points=vtk.vtkPoints()
        for v in verts: points.InsertNextPoint(v.x,v.y,v.z)
        cells=vtk.vtkCellArray()
        for tri in triangles:
            cells.InsertNextCell(3)
            for k in tri: cells.InsertCellPoint(k)
        data=vtk.vtkPolyData();data.SetPoints(points);data.SetPolys(cells)
        normals=vtk.vtkPolyDataNormals();normals.SetInputData(data);normals.Update()
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
        actor=vtk.vtkActor();actor.SetMapper(mapper)
        prop=actor.GetProperty();prop.SetColor(*p['color']);prop.SetAmbient(.62);prop.SetDiffuse(.38)
        prop.SetSpecular(.16);prop.SetSpecularPower(22)
        prop.EdgeVisibilityOff();prop.SetInterpolationToPhong()
        if 'Difusor' in p['name']: prop.SetOpacity(.5)
        if weighing and p['name'].startswith('M07'): prop.SetOpacity(.30)
        renderer.AddActor(actor)
        edges=vtk.vtkFeatureEdges();edges.SetInputData(data)
        edges.BoundaryEdgesOn();edges.FeatureEdgesOn();edges.SetFeatureAngle(35)
        edges.ManifoldEdgesOff();edges.NonManifoldEdgesOff();edges.ColoringOff()
        edge_mapper=vtk.vtkPolyDataMapper();edge_mapper.SetInputConnection(edges.GetOutputPort())
        edge_actor=vtk.vtkActor();edge_actor.SetMapper(edge_mapper)
        edge_actor.GetProperty().SetColor(.25,.31,.34)
        edge_actor.GetProperty().SetLineWidth(.8)
        if weighing and p['name'].startswith('M07'):edge_actor.GetProperty().SetOpacity(.35)
        renderer.AddActor(edge_actor)
    camera=renderer.GetActiveCamera()
    if weighing:
        camera.SetPosition(230,-360,165);camera.SetFocalPoint(0,0,20)
    elif cutaway:
        camera.SetPosition(650,-950,660);camera.SetFocalPoint(0,0,164)
    else:
        camera.SetPosition(680,-1000,530);camera.SetFocalPoint(-40,-30,165)
    camera.SetViewUp(0,0,1);camera.ParallelProjectionOn();renderer.ResetCamera()
    camera.Zoom(1.1)
    window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1)
    window.AddRenderer(renderer);window.SetSize(1500,1350);window.SetMultiSamples(8)
    window.Render()
    shot=vtk.vtkWindowToImageFilter();shot.SetInput(window);shot.SetScale(1);shot.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(WORK/filename));writer.SetInputConnection(shot.GetOutputPort());writer.Write()
    window.Finalize();shutil.copy2(WORK/filename,IMG/filename)

if __name__=='__main__':
    build()
    verify()
    export()
    (HERE/'parametros_modelo.json').write_text(json.dumps(P,ensure_ascii=False,indent=2),encoding='utf-8')
    for args in [('FoodScan_Abierto.png',True,False,False),('FoodScan_Interior.png',False,True,False),('FoodScan_Pesaje.png',False,False,True)]:
        render_view(*args)
    print('Modelo, STEP, STL y vistas generados.')
