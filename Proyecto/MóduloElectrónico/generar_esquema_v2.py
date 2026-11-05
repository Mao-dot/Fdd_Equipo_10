"""Esquema v2 editable EasyEDA Std, SVG y comprobacion de redes.

Reutiliza exclusivamente funciones de dibujo de v1; no ejecuta ni sustituye v1.
Los modulos se representan por terminales funcionales, no por huellas PCB.
"""
from pathlib import Path
import ast
import json
import uuid
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
INK, TEXT, WIRE = '#880000', '#000080', '#008800'
legacy = ast.parse((ROOT / 'generar_esquema.py').read_text(encoding='utf-8'))
helpers = [n for n in legacy.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
exec(compile(ast.Module(body=helpers, type_ignores=[]), 'foodscan_v1_helpers', 'exec'))
OUT = ROOT / 'EasyEDA'
OUT.mkdir(exist_ok=True)
shapes, components, wires, labels = [], {}, [], []
counter = 0
INK, TEXT, WIRE = '#880000', '#000080', '#008800'

# GPIOs de DevKitC-1 N16R8: no usar GPIO35/36/37 (PSRAM), straps,
# USB19/20 ni UART43/44. P1 es la cabecera 2x9 de Waveshare, no un FPC.
CAMERA = [
    (1,'3.3V',None,'+3V3'), (2,'GND',None,'GND'),
    (3,'SIOC',9,'CAM_SIOC'), (4,'SIOD',8,'CAM_SIOD'),
    (5,'VSYNC',13,'CAM_VSYNC'), (6,'HREF',14,'CAM_HREF'),
    (7,'PCLK',21,'CAM_PCLK'), (8,'XCLK',15,'CAM_XCLK'),
    (9,'Y9 / D7',18,'CAM_D7'), (10,'Y8 / D6',17,'CAM_D6'),
    (11,'Y7 / D5',16,'CAM_D5'), (12,'Y6 / D4',12,'CAM_D4'),
    (13,'Y5 / D3',11,'CAM_D3'), (14,'Y4 / D2',10,'CAM_D2'),
    (15,'Y3 / D1',7,'CAM_D1'), (16,'Y2 / D0',6,'CAM_D0'),
    (17,'RESET_N',5,'CAM_RESET_N'), (18,'PWDN',None,None),
]

shapes += [rect(20,20,1580,1100,'#405063'),
           text(45,58,'FOODSCAN | ESQUEMATICO CORREGIDO',23,bold=True),
           text(45,82,'Equipo 10 | ESP32-S3 N16R8 + OV5640 (C) | Foto y peso por Wi-Fi a la app con Gemini',11)]
section(45,105,775,705,'1. CONTROL Y CAMARA INTERNA - DVP / 3.3 V')
section(845,105,730,310,'2. ALIMENTACION Y DESACOPLO')
section(845,435,730,250,'3. PESAJE - HX711 + CELDA DE 5 kg')
section(845,705,730,105,'4. PUERTA - CERRADA = NIVEL BAJO')
section(45,830,1530,225,'5. LUCES CONTROLADAS POR GPIO42 - MOSFET / 12 LED')

# U1: se muestran solo los terminales usados. Los demas quedan disponibles
# o reservados segun el esquema oficial de la DevKitC-1 seleccionada.
ub = [rect(210,190,220,500)]
up = {}
for key,name,y in [('5V','5V IN',235),('GND','GND',265),('3V3','3V3 OUT',295),
                   ('IO4','GPIO4 / DT',365),('IO2','GPIO2 / SCK',405),
                   ('IO1','GPIO1 / DOOR',445),('IO42','GPIO42 / LED',485)]:
    ub.append(pin(key,190,y,20,0,name,0,True)); up[key]=(190,y)
    netname = {'5V':'+5V','GND':'GND','3V3':'+3V3','IO4':'HX_DOUT',
               'IO2':'HX_SCK','IO1':'DOOR_N','IO42':'LED_EN'}[key]
    wire(75,y,190,y); net(75,y,netname)
cb = [rect(625,190,170,500)]
cp = {}
for i,(number,name,gpio,netname) in enumerate(CAMERA):
    y=235+24*i
    cb.append(pin(str(number),605,y,20,0,f'{number}: {name}',0,True)); cp[str(number)]=(605,y)
    if gpio is not None:
        key=f'IO{gpio}'
        ub.append(pin(key,450,y,-20,0,f'GPIO{gpio}',0,True)); up[key]=(450,y)
        wire(450,y,605,y); net(525,y,netname,'middle')
    elif netname:
        wire(510,y,605,y); net(510,y,netname)
    else:
        shapes.append(f'O~605~{y}~{gid()}~M 601 {y-4} L 609 {y+4} M 609 {y-4} L 601 {y+4}~#008800~0')
ub += [text(320,550,'N16R8',13,anchor='middle',bold=True),
       text(320,575,'16 MB Flash',10,anchor='middle'),text(320,595,'8 MB PSRAM',10,anchor='middle'),
       text(320,635,'Wi-Fi / Internet',10,anchor='middle'),text(320,660,'USB: programar',9,anchor='middle')]
lib('U1','ESP32-S3 DevKitC-1',320,440,ub,up,'Variante N16R8; modulo WROOM-1; terminales usados',(210,155))
lib('CAM1','Waveshare OV5640 (C)',710,440,cb,cp,'SKU13802; P1 cabecera 2x9; autofocus; DVP de 8 bits',(625,155))
for i,n in enumerate([
    'CAM1.P1.18: SIN conexion externa. R7 del modulo publicado une PWDN a GND.',
    'No conducir PWDN a nivel alto. Reposo por SCCB; flash de camara desactivado.',
    'P1.17 RESET activo bajo. Inicializar autofocus por firmware y comprobar enfoque.',
    'No usar GPIO35/36/37, USB19/20 ni straps0/3/45/46 para estas conexiones.',
    'Conexiones por nombre de GPIO y numero P1; comprobar serigrafia de las piezas.'
]): shapes.append(text(65,716+i*18,n,9))

# J1/F1/SW1 y rail5V, fuente externa DC existente.
lib('J1','Jack 5.5 x 2.1 mm',910,230,
    [rect(875,170,65,125),circle(900,225,12),
     pin('CENTER',960,190,-20,0,'+',0,True),pin('SLEEVE',960,290,-20,0,'-',0,True)],
    {'CENTER':(960,190),'SLEEVE':(960,290)},'Centro positivo',(868,145))
lib('F1','1.5 A',1040,190,
    [rect(1020,184,40,12),line([1020,190,1060,190]),pin('1',1010,190,10,0),pin('2',1070,190,-10,0)],
    {'1':(1010,190),'2':(1070,190)},'Fusible5x20; portafusible accesorio',(1020,147))
lib('SW1','KCD1-102',1160,190,
    [pin('1',1130,190,12,0),pin('2',1190,190,-12,0),circle(1142,190,2),circle(1178,190,2),line([1142,190,1173,174])],
    {'1':(1130,190),'2':(1190,190)},'Interruptor general',(1120,147))
capacitor('C1',1290,245,'470 uF / 16 V',True)
capacitor('C2',1450,245,'100 nF')
wire(960,190,1010,190); net(980,190,'VIN_5V')
wire(1070,190,1130,190)
wire(1190,190,1290,190,1450,190); net(1390,190,'+5V')
wire(1290,190,1290,220); wire(1450,190,1450,220)
wire(960,290,1290,290,1450,290); net(1010,290,'GND')
wire(1290,270,1290,290); wire(1450,270,1450,290)
dot(1290,190); dot(1290,290)
capacitor('C3',1080,355,'100 uF / 10 V',True)
capacitor('C4',1240,355,'100 nF')
for ref in ('C3','C4'):
    components[ref]['description']='Desacoplo entre +3V3 y GND, junto a CAM1'
for i,s in enumerate(shapes):
    if s.startswith('LIB~') and any(part.startswith('T~P~') and part.split('~')[12] in ('C3','C4') for part in s.split('#@$')[1:]):
        shapes[i]=s.replace('Description`Desacoplo entre +5V y GND',
                            'Description`Desacoplo entre +3V3 y GND, junto a CAM1')
wire(960,315,1080,315,1240,315); net(960,315,'+3V3')
wire(1080,315,1080,330); wire(1240,315,1240,330)
wire(960,395,1080,395,1240,395); net(960,395,'GND')
wire(1080,380,1080,395); wire(1240,380,1240,395)
dot(1080,315); dot(1080,395)
for i,n in enumerate(['Fuente:5 V / 2.4 A.', 'C3/C4 junto a CAM1.',
                      'Probar rail3.3V con', 'Wi-Fi, camara y AF.', 'USB y fuente separados.']):
    shapes.append(text(1340,320+i*17,n,9))

# HX711 y puente completo de cuatro hilos.
hb=[rect(960,500,160,140)]; hp={}
for key,x,y,dx in [('VCC',940,520,20),('GND',940,550,20),('DT',940,580,20),('SCK',940,610,20),
                    ('E+',1140,520,-20),('E-',1140,550,-20),('A+',1140,580,-20),('A-',1140,610,-20)]:
    hb.append(pin(key,x,y,dx,0,key,0,True)); hp[key]=(x,y)
lib('U2','Modulo HX711',1040,570,hb,hp,'Modulo apto para3.3V; canal A',(965,480))
for y,n in [(520,'+3V3'),(550,'GND'),(580,'HX_DOUT'),(610,'HX_SCK')]:
    wire(865,y,940,y); net(865,y,n)
lb=[rect(1360,500,180,140),text(1450,545,'PUENTE COMPLETO',9,anchor='middle'),
    line([1450,560,1470,580,1450,600,1430,580,1450,560])]; lp={}
for key,name,y in [('E+','EXC+',520),('E-','EXC-',550),('S+','SIG+',580),('S-','SIG-',610)]:
    lb.append(pin(key,1340,y,20,0,name,0,True)); lp[key]=(1340,y)
lib('LC1','Celda 5 kg / 4 hilos',1450,570,lb,lp,'Verificar hilos, montaje y calibracion',(1360,480))
for y,n in [(520,'EXC_P'),(550,'EXC_N'),(580,'SIG_P'),(610,'SIG_N')]:
    wire(1140,y,1340,y); net(1240,y,n,'middle')
shapes.append(text(865,668,'Calibrar con masa conocida. Tara con plato vacio; conservar al retirar el plato.',9))

# Puerta: NO a DOOR_N; COM a GND; NC aislado.
resistor('R13',1000,770,'10 kohm',False)
wire(870,770,970,770); net(870,770,'+3V3')
wire(1030,770,1150,770); net(1070,770,'DOOR_N')
sb=[pin('COM',1210,795,0,-10),pin('NO',1150,770,20,0),pin('NC',1270,770,-20,0),
    circle(1170,770,2),circle(1250,770,2),circle(1210,785,2),line([1210,785,1248,772]),
    text(1170,757,'NO',8),text(1250,757,'NC',8)]
lib('SW2','KW11-3Z-3F',1210,780,sb,{'COM':(1210,795),'NO':(1150,770),'NC':(1270,770)},
    'Al cerrar acciona COM-NO; rebote por firmware',(1330,750))
wire(1210,795,1210,800,1310,800); net(1310,800,'GND')
shapes.append(f'O~1270~770~{gid()}~M 1266 766 L 1274 774 M 1274 766 L 1266 774~#008800~0')

# Q1 AO3400A: pin1gate, pin2source, pin3drain. Retorno conmutado LED_RETURN.
resistor('R14',130,955,'100 ohm',False)
wire(65,955,100,955); net(65,955,'LED_EN')
wire(160,955,210,955)
resistor('R15',85,1010,'100 kohm')
wire(170,955,170,975,85,975,85,985); dot(170,955)
wire(85,1035,85,1045,260,1045,260,1005); net(175,1045,'GND')
qb=[pin('1',210,955,35,0),pin('2',260,1005,0,-30),pin('3',260,910,0,24),
    line([245,937,245,975]),line([260,934,260,946]),line([260,951,260,961]),line([260,966,260,975]),
    line([260,937,280,937,280,943]),line([260,975,280,975,280,958]),
    f'PG~272 958 288 958 280 945~{INK}~1~0~none~{gid()}~0',line([272,943,288,943]),
    text(212,946,'1 G',8),text(265,1004,'2 S',8),text(265,915,'3 D',8)]
lib('Q1','AO3400A',260,955,qb,{'1':(210,955),'2':(260,1005),'3':(260,910)},
    'N-MOS logic-level; SOT23 en adaptador, sin huellaPCB',(200,874))
wire(260,910,260,890,300,890,300,1000,1510,1000); net(980,1000,'LED_RETURN')
wire(345,865,1510,865); net(1370,865,'+5V')
for i in range(12):
    x=345+i*100
    resistor(f'R{i+1}',x,900)
    led(f'D{i+1}',x,960)
    wire(x,865,x,875); wire(x,925,x,940); wire(x,980,x,1000)
    dot(x,865); dot(x,1000)
shapes.append(text(345,1035,'3 paneles x 4 LED con difusor. 16-18 mA por rama; total ~0.19-0.22 A. GPIO42 alto = luces ON.',9))
shapes += [rect(45,1072,1530,35,'#405063'),text(60,1095,'FoodScan - Interconexion de modulos',12,bold=True),
           text(640,1095,'Rev.2.0 | 04/11/2026 | A3 | Hoja1/1',11),
           text(1140,1095,'Sin huellas PCB / pruebas fisicas pendientes',9)]

# Separar la etiqueta del retorno de las ramas verticales LED.
for i,s in enumerate(shapes):
    a=s.split('~')
    if a[0]=='N' and a[5]=='LED_RETURN':
        a[8]='1050'; a[9]='1020'; shapes[i]='~'.join(a)

# Validar geometria y conexiones; no se presenta como ERC del editor.
parent={}
points=set((x,y) for x,y,_ in labels)
for c in components.values(): points.update(map(tuple,c['pins'].values()))
for w in wires: points.update(w)
for w in wires:
    for a,b in zip(w,w[1:]):
        assert a[0]==b[0] or a[1]==b[1], ('Cable no ortogonal',a,b)
        for p in points:
            if ((a[0]==b[0]==p[0] and min(a[1],b[1])<=p[1]<=max(a[1],b[1])) or
                (a[1]==b[1]==p[1] and min(a[0],b[0])<=p[0]<=max(a[0],b[0]))): union(a,p)
names={}
for x,y,n in labels:
    if n in names: union((x,y),names[n])
    names[n]=(x,y)
nets=defaultdict(list)
for ref,c in components.items():
    for key,pos in c['pins'].items(): nets[find(tuple(pos))].append(f'{ref}.{key}')
net_names=defaultdict(set)
for x,y,n in labels: net_names[find((x,y))].add(n)
assert all(len(ns)<=1 for ns in net_names.values()), ('Redes en corto',dict(net_names))
pin_net={p:r for r,ps in nets.items() for p in ps}
same('J1.CENTER','F1.1'); same('F1.2','SW1.1')
same('SW1.2','U1.5V','C1.1','C2.1')
same('J1.SLEEVE','U1.GND','U2.GND','CAM1.2','SW2.COM','Q1.2','R15.2','C1.2','C2.2','C3.2','C4.2')
same('U1.3V3','U2.VCC','CAM1.1','R13.1','C3.1','C4.1')
same('U1.IO4','U2.DT'); same('U1.IO2','U2.SCK'); same('U1.IO1','R13.2','SW2.NO')
same('U1.IO42','R14.1'); same('R14.2','Q1.1','R15.1')
for number,_,gpio,_ in CAMERA:
    if gpio is not None: same(f'CAM1.{number}',f'U1.IO{gpio}')
for a,b in [('E+','E+'),('E-','E-'),('A+','S+'),('A-','S-')]: same('U2.'+a,'LC1.'+b)
for i in range(1,13):
    same('U1.5V',f'R{i}.1'); same(f'R{i}.2',f'D{i}.A'); same('Q1.3',f'D{i}.K')
assert len({pin_net[p] for p in ['U1.5V','U1.3V3','U1.GND','Q1.3','Q1.1','U1.IO42']})==6
assert len(components)==40,len(components)
assert sorted(ps for ps in nets.values() if len(ps)==1)==[['CAM1.18'],['SW2.NC']]
gpio=[p for p in up if p.startswith('IO')]
assert len(gpio)==len(set(gpio))==19
assert not ({int(p[2:]) for p in gpio} & {0,3,19,20,35,36,37,43,44,45,46})

doc={'head':{'docType':'1','editorVersion':'6.5.51','newgId':True,'c_para':{'Prefix Start':'1'},
             'c_spiceCmd':None,'hasIdFlag':True,'uuid':uuid.uuid5(uuid.NAMESPACE_URL,'foodscan-rev2').hex,'x':'0','y':'0'},
     'canvas':'CA~1620~1145~#FFFFFF~none~#CCCCCC~5~1620~1145~line~5~pixel~5~0~0',
     'shape':shapes,'BBox':{'x':20,'y':20,'width':1580,'height':1100},'colors':{},'title':'FoodScan_Esquematico_v2'}
(OUT/'FoodScan_Esquematico_v2.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')
report={'status':'PASS','revision':'2.0','date':'2026-11-04','components':len(components),
        'pins':sum(len(c['pins']) for c in components.values()),'nets':len(nets),
        'format':'EasyEDA Standard, docType1','validation':'Conectividad local; no ERC oficial ni ensayo fisico',
        'checks':['40 componentes; 12 resistencias limitadoras independientes',
                  'Sin union de redes con nombres distintos','Camara: P1 de18pines; PWDN sin salidaGPIO',
                  'GPIO sin repetidos y fuera de memoria, USB, UART y straps',
                  '12 catodos a drenador Q1; source a GND; gate con100ohm y pulldown100kohm',
                  'SoloCAM1.18 y SW2.NC sin conexion externa'],
        'camera_header':[{'pin':n,'signal':s,'gpio':g,'net':net} for n,s,g,net in CAMERA],
        'components_detail':components,
        'netlist':[{'name':next(iter(net_names[r]),f'Net_{i}'),'pins':ps} for i,(r,ps) in enumerate(nets.items(),1)]}
(OUT/'Verificacion_conexiones_v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="1620" height="1145" viewBox="0 0 1620 1145"><rect width="1620" height="1145" fill="white"/>'+''.join(svg_shape(s) for s in doc['shape'])+'</svg>'
(OUT/'FoodScan_Esquematico_v2.svg').write_text(svg,encoding='utf-8')
print(json.dumps({'revision':'2.0','status':report['status'],'components':len(components),'nets':len(nets)},ensure_ascii=False))
