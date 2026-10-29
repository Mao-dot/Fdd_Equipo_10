"""Genera el esquema editable de FoodScan en el formato abierto EasyEDA Std.

Referencia de formato: https://github.com/easyeda/easyeda-std-file-format
Los simbolos de modulos muestran los terminales usados, identificados por su
serigrafia. No se asignan huellas ni numeros de pads para fabricar una PCB.
"""
from pathlib import Path
import json
import uuid
import html
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'EasyEDA'
OUT.mkdir(exist_ok=True)
shapes, components, wires, labels = [], {}, [], []
counter = 0
INK, TEXT, WIRE = '#880000', '#000080', '#008800'

def gid():
    global counter
    counter += 1
    return f'gge{counter}'

def text(x, y, value, size=10, color=TEXT, anchor='start', mark='L', bold=False):
    return '~'.join(map(str, ['T',mark,x,y,0,color,'Arial',f'{size}pt',
                             'bold' if bold else '', '', '', 'comment',value,1,anchor,gid(),0,'']))

def line(points, color=INK, width=1):
    return f'PL~{" ".join(map(str, points))}~{color}~{width}~0~none~{gid()}~0'

def rect(x,y,w,h,color=INK,width=1,fill='none'):
    return f'R~{x}~{y}~~~{w}~{h}~{color}~{width}~0~{fill}~{gid()}~0~'

def circle(x,y,r,color=INK):
    return f'C~{x}~{y}~{r}~{color}~1~0~none~{gid()}~0'

def pin(key,x,y,dx,dy,name='',electric=0,show=False):
    # The dot is the electrical endpoint; path runs from that dot into the symbol.
    rot = 180 if dx>0 else 0 if dx<0 else 90 if dy>0 else 270
    if dx:
        nx,ny,anchor=x+dx+(5 if dx>0 else -5),y+4,'start' if dx>0 else 'end'
    else:
        nx,ny,anchor=x+7,y+dy,'start'
    return (f'P~show~{electric}~{key}~{x}~{y}~{rot}~{gid()}~0'
            f'^^{x}~{y}^^M {x} {y} l {dx} {dy}~{INK}'
            f'^^{int(show)}~{nx}~{ny}~0~{name or key}~{anchor}~Arial~9pt~{TEXT}'
            f'^^0~{x}~{y-3}~0~{key}~start~Arial~7pt~{TEXT}'
            f'^^0~{x}~{y}^^0~M {x} {y}')

def lib(ref,value,x,y,body,pins,description='',label_pos=None):
    ident=uuid.uuid5(uuid.NAMESPACE_URL,'foodscan-symbol:'+value).hex
    attrs=f'package`NONE`name`{value}`pre`{ref.rstrip("0123456789")}?`Contributor`Equipo 10`spicePre`{ref[0]}`Description`{description}'
    px,py=label_pos or (x,y-27)
    body=[text(px,py,ref,10,mark='P',bold=True),text(px,py+15,value,10,mark='N')]+body
    shapes.append(f'LIB~{x}~{y}~{attrs}~0~0~{gid()}~~{ident}~0~~yes~yes'+ '#@$'+'#@$'.join(body))
    components[ref]={'value':value,'description':description,'pins':{str(k):list(v) for k,v in pins.items()}}

def wire(*pts):
    wires.append(list(zip(pts[::2],pts[1::2])))
    shapes.append(f'W~{" ".join(map(str,pts))}~{WIRE}~1~0~none~{gid()}~0')

def net(x,y,name,anchor='start'):
    labels.append((x,y,name))
    shapes.append(f'N~{x}~{y}~0~{TEXT}~{name}~{gid()}~{anchor}~{x}~{y-5}~Arial~9pt~0')

def dot(x,y):
    shapes.append(f'J~{x}~{y}~2~{WIRE}~{gid()}~0')

def section(x,y,w,h,title):
    shapes.append(rect(x,y,w,h,'#9AA8B5'))
    shapes.append(text(x+15,y+25,title,13,bold=True))

def resistor(ref,x,y,value='100 ohm',vertical=True):
    if vertical:
        b=[rect(x-5,y-12,10,24),pin('1',x,y-25,0,13),pin('2',x,y+25,0,-13)]
        p={'1':(x,y-25),'2':(x,y+25)}
        pos=(x+13,y-4)
    else:
        b=[rect(x-15,y-5,30,10),pin('1',x-30,y,15,0),pin('2',x+30,y,-15,0)]
        p={'1':(x-30,y),'2':(x+30,y)}
        pos=(x-22,y-27)
    lib(ref,value,x,y,b,p,'Resistencia 1/4 W',pos)

def capacitor(ref,x,y,value,polar=False):
    b=[line([x-10,y-4,x+10,y-4],width=2),line([x-10,y+4,x+10,y+4],width=2),
       pin('1',x,y-25,0,21),pin('2',x,y+25,0,-21)]
    if polar: b.append(text(x-21,y-9,'+',10))
    lib(ref,value,x,y,b,{'1':(x,y-25),'2':(x,y+25)},'Desacoplo entre +5V y GND',(x+15,y-6))

def led(ref,x,y):
    b=[pin('A',x,y-20,0,10),pin('K',x,y+20,0,-10),
       f'PG~{x-9} {y-10} {x+9} {y-10} {x} {y+8}~{INK}~1~0~none~{gid()}~0',
       line([x-10,y+9,x+10,y+9],width=2),
       line([x+12,y-5,x+23,y-16]),line([x+18,y-16,x+23,y-16,x+23,y-11]),
       line([x+16,y+3,x+27,y-8]),line([x+22,y-8,x+27,y-8,x+27,y-3])]
    lib(ref,'Blanco',x,y,b,{'A':(x,y-20),'K':(x,y+20)},'LED 5 mm; Vf 3.2-3.4 V',(x+35,y-7))

# Hoja A3 apaisada, margenes y rotulo.
shapes += [rect(20,20,1580,1100,'#405063'),text(45,58,'FOODSCAN | ESQUEMA ELECTRICO',23,bold=True),
           text(45,82,'Equipo 10 - Fundamentos de Diseno - UPCH | Interconexion de modulos del prototipo',11)]
section(45,105,690,260,'1. ALIMENTACION Y PROTECCION - 5 V DC')
section(765,105,810,395,'3. PESAJE - HX711 + CELDA DE CARGA')
section(45,390,690,380,'2. CONTROL, CAMARA Y WI-FI')
section(765,525,350,245,'4. DETECTOR DE PUERTA')
section(1135,525,440,245,'NOTAS DE MONTAJE')
section(45,795,1530,255,'5. ILUMINACION FIJA - 12 RAMAS EN PARALELO')

# J1: simbolo funcional de jack de panel (sin contacto conmutado).
lib('J1','Jack 5.5 x 2.1 mm',135,225,
    [rect(95,170,80,130),circle(120,215,13),text(105,267,'DC',10),
     pin('CENTER',195,190,-20,0,'+',0,True),pin('SLEEVE',195,290,-20,0,'-',0,True)],
    {'CENTER':(195,190),'SLEEVE':(195,290)},'Centro positivo; confirmar adaptador',(80,145))
lib('F1','1.5 A',300,190,
    [rect(280,184,40,12),line([280,190,320,190]),pin('1',270,190,10,0),pin('2',330,190,-10,0)],
    {'1':(270,190),'2':(330,190)},'Fusible 5 x 20 mm',(280,147))
lib('SW1','KCD1-102',435,190,
    [pin('1',405,190,12,0),pin('2',465,190,-12,0),circle(417,190,2),circle(453,190,2),line([417,190,448,174])],
    {'1':(405,190),'2':(465,190)},'Interruptor general SPST',(398,147))
capacitor('C1',520,245,'470 uF / 16 V',True)
capacitor('C2',660,245,'100 nF')
wire(195,190,270,190); net(225,190,'VIN_5V')
wire(330,190,405,190)
wire(465,190,520,190,660,190); net(620,190,'+5V')
wire(520,190,520,220); wire(660,190,660,220)
wire(195,290,520,290,660,290); net(230,290,'GND')
wire(520,270,520,290); wire(660,270,660,290)
dot(520,190); dot(520,290)
shapes += [text(65,326,'Fuente externa: 5 V / 2.4 A, centro positivo. C1 y C2 cerca de U1.',10),
           text(65,348,'Abrir SW1 antes de conectar la base USB-MB. Usar una sola fuente.',10)]

# ESP32-CAM: terminales usados. La OV2640 y regulador forman parte de la placa.
b=[rect(240,470,260,180)]
up={}
for key,name,x,y,dx,e in [('5V','5V',220,500,20,4),('GND','GND',220,540,20,4),
                         ('3V3','3V3 OUT',220,580,20,4),('IO13','GPIO13',520,500,-20,1),
                         ('IO14','GPIO14',520,540,-20,2),('IO15','GPIO15',520,580,-20,1)]:
    b.append(pin(key,x,y,dx,0,name,e,True)); up[key]=(x,y)
b += [text(370,616,'OV2640 + PSRAM',11,anchor='middle'),text(370,637,'Regulador 3.3 V integrado',9,anchor='middle')]
lib('U1','ESP32-CAM AI-Thinker',370,560,b,up,'Solo terminales usados; conexion por serigrafia',(250,438))
for y,n in [(500,'+5V'),(540,'GND'),(580,'+3V3')]:
    wire(135,y,220,y); net(135,y,n)
for y,n in [(500,'HX_DOUT'),(540,'HX_SCK'),(580,'DOOR_N')]:
    wire(520,y,625,y); net(625,y,n,'end')
shapes += [text(65,687,'Solo se muestran los terminales usados del modulo U1.',10),
           text(65,711,'No usar microSD: comparte GPIO13, GPIO14 y GPIO15.',10),
           text(65,735,'Flash integrado apagado (GPIO4). Camara conectada por su flex.',10),
           text(65,755,'Wi-Fi hacia laptop/celular; sin cableado adicional en este esquema.',9)]

# HX711: conectores funcionales del modulo, sin repetir el circuito interno del IC.
b=[rect(915,200,200,195)]; hp={}
for key,x,y,dx,e in [('VCC',895,225,20,4),('GND',895,265,20,4),('DT',895,305,20,2),('SCK',895,345,20,1),
                     ('E+',1135,225,-20,4),('E-',1135,265,-20,4),('A+',1135,305,-20,1),('A-',1135,345,-20,1)]:
    b.append(pin(key,x,y,dx,0,key,e,True)); hp[key]=(x,y)
lib('U2','Modulo HX711',1015,290,b,hp,'ADC 24 bits; modulo apto para 3.3 V',(925,163))
for y,n in [(225,'+3V3'),(265,'GND'),(305,'HX_DOUT'),(345,'HX_SCK')]:
    wire(800,y,895,y); net(800,y,n)

# Celda de carga: representacion funcional de puente completo con cuatro hilos.
b=[rect(1325,200,200,195),text(1425,240,'PUENTE COMPLETO',10,anchor='middle'),
   line([1425,260,1450,285,1425,310,1400,285,1425,260]),
   text(1425,369,'4 hilos / 5 kg',11,anchor='middle')]
lp={}
for key,name,y in [('E+','EXC+',225),('E-','EXC-',265),('S+','SIG+',305),('S-','SIG-',345)]:
    b.append(pin(key,1305,y,20,0,name,0,True)); lp[key]=(1305,y)
lib('LC1','Celda de carga 5 kg',1425,290,b,lp,'Confirmar E+/E-/S+/S- de los cables reales',(1328,163))
for y,n in [(225,'EXC_P'),(265,'EXC_N'),(305,'SIG_P'),(345,'SIG_N')]:
    wire(1135,y,1305,y); net(1215,y,n,anchor='middle')
shapes += [text(785,430,'U2 se alimenta a 3.3 V: DT/SCK compatibles con los GPIO de U1.',10),
           text(785,454,'Celda: E+/E- = excitacion; S+/S- = senal hacia A+/A-.',10),
           text(785,478,'Verificar cables; no asumir colores. Canal B sin usar. Calibrar y tarar.',10)]

# Detector SPDT: COM a GND, NO a GPIO15. Posicion dibujada sin accionar.
resistor('R13',830,610,'10 kohm')
wire(830,570,830,585); net(830,570,'+3V3')
wire(830,635,830,665,900,665); dot(830,665); net(830,665,'DOOR_N')
b=[pin('COM',960,705,0,-15),pin('NO',900,665,20,0),pin('NC',1020,665,-20,0),
   circle(920,665,2),circle(1000,665,2),circle(960,690,2),line([960,690,998,667]),
   text(913,650,'NO',9),text(1000,650,'NC',9),text(971,690,'COM',9)]
lib('SW2','KW11-3Z-3F',960,675,b,{'COM':(960,705),'NO':(900,665),'NC':(1020,665)},'Puerta cerrada acciona COM-NO',(932,582))
wire(960,705,960,725); net(960,725,'GND')
shapes.append(f'O~1020~665~{gid()}~M 1016 661 L 1024 669 M 1024 661 L 1016 669~#008800~0')
shapes += [text(785,748,'Cerrada = 0; abierta = 1. NC libre.',10)]
notes=['Todas las masas comparten GND.',
       'No aplicar 5 V al pin 3V3 ni a GPIO.',
       'LED con una resistencia por rama.',
       'U1/U2: simbolos de modulos,',
       'terminales segun su serigrafia.',
       'GPIO15 es pin de arranque:',
       'probar encendido con puerta en',
       'ambas posiciones; bajo silencia',
       'los mensajes ROM de arranque.',
       'Sin huellas PCB / sin simulacion.']
for i,n in enumerate(notes): shapes.append(text(1152,572+i*18,n,10))

# 12 ramas reales, ninguna resistencia compartida.
wire(95,850,1505,850); net(110,850,'+5V')
wire(95,1010,1505,1010); net(110,1010,'GND')
for i in range(12):
    x=125+i*120
    resistor(f'R{i+1}',x,895)
    led(f'D{i+1}',x,965)
    wire(x,850,x,870); wire(x,920,x,945); wire(x,985,x,1010)
    dot(x,850); dot(x,1010)
shapes += [text(65,1037,'3 paneles de 4 LED: R1-D1 a R4-D4 | R5-D5 a R8-D8 | R9-D9 a R12-D12. 16-18 mA por LED; total aprox. 0.19-0.22 A.',10),
           rect(45,1070,1530,35,'#405063'),
           text(60,1093,'FoodScan - Interconexion del prototipo',12,bold=True),
           text(700,1093,'Rev. 1.0 | 22/10/2026 | A3 apaisado | Hoja 1/1',11),
           text(1255,1093,'Base: componentes.md v1.1',10)]

doc={'head':{'docType':'1','editorVersion':'6.5.51','newgId':True,
             'c_para':{'Prefix Start':'1'},'c_spiceCmd':None,'hasIdFlag':True,
             'uuid':uuid.uuid5(uuid.NAMESPACE_URL,'foodscan-rev1').hex,'x':'0','y':'0'},
     'canvas':'CA~1620~1145~#FFFFFF~none~#CCCCCC~5~1620~1145~line~5~pixel~5~0~0',
     'shape':shapes,'BBox':{'x':20,'y':20,'width':1580,'height':1100},'colors':{},
     'title':'FoodScan_Esquematico_v1'}
dest=OUT/'FoodScan_Esquematico_v1.json'
dest.write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')

# Validacion de conectividad a partir de los pines y de la geometria real de W/N.
parent={}
def find(x):
    parent.setdefault(x,x)
    if parent[x]!=x: parent[x]=find(parent[x])
    return parent[x]
def union(a,b): parent[find(a)]=find(b)
points=set((x,y) for x,y,_ in labels)
for c in components.values(): points.update(map(tuple,c['pins'].values()))
for w in wires: points.update(w)
for w in wires:
    for a,b in zip(w,w[1:]):
        assert a[0]==b[0] or a[1]==b[1], ('Nonorthogonal wire',a,b)
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
assert all(len(ns)<=1 for ns in net_names.values()), ('Shorted named nets',dict(net_names))
pin_net={p:r for r,ps in nets.items() for p in ps}
def same(*pins): assert len({pin_net[p] for p in pins})==1, pins
same('J1.CENTER','F1.1'); same('F1.2','SW1.1')
same('SW1.2','C1.1','C2.1','U1.5V')
same('J1.SLEEVE','C1.2','C2.2','U1.GND','U2.GND','SW2.COM')
same('U1.3V3','U2.VCC','R13.1')
same('U1.IO13','U2.DT'); same('U1.IO14','U2.SCK')
same('U1.IO15','R13.2','SW2.NO')
for a,b in [('E+','E+'),('E-','E-'),('A+','S+'),('A-','S-')]: same('U2.'+a,'LC1.'+b)
for i in range(1,13):
    same('U1.5V',f'R{i}.1'); same(f'R{i}.2',f'D{i}.A'); same('U1.GND',f'D{i}.K')
assert pin_net['U1.5V']!=pin_net['U1.3V3']!=pin_net['U1.GND']
assert len(components)==34, len(components)
assert sum(c['value']=='100 ohm' for c in components.values())==12
isolated=[ps for ps in nets.values() if len(ps)==1]
assert isolated==[['SW2.NC']],isolated
report={'status':'PASS','components':len(components),'pins':sum(len(c['pins']) for c in components.values()),
        'nets':len(nets),'format':'EasyEDA Standard, docType 1','source':'componentes.md v1.1, seccion 2.1',
        'checks':['34 componentes; 12 LED y 12 resistencias independientes',
                  'Ningun cortocircuito entre redes con nombre','Pines y cables coinciden geometricamente',
                  'Alimentacion de HX711 a 3.3 V','GPIO13=DT; GPIO14=SCK; GPIO15=puerta',
                  'Unico terminal aislado: SW2.NC, marcado no conectar'],
        'netlist':[{'name':next(iter(net_names[r]),f'Net_{i}'),'pins':ps} for i,(r,ps) in enumerate(nets.items(),1)]}
(OUT/'Verificacion_conexiones.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

# Vista vectorial generada leyendo los elementos del mismo archivo nativo.
def esc(s): return html.escape(str(s),quote=True)
def svg_shape(s):
    a=s.split('~'); cmd=a[0]
    if cmd=='LIB': return ''.join(svg_shape(v) for v in s.split('#@$')[1:])
    if cmd in ('PL','W','PG'):
        tag='polygon' if cmd=='PG' else 'polyline'
        return f'<{tag} points="{esc(a[1])}" stroke="{a[2]}" stroke-width="{a[3]}" fill="{a[5]}"/>'
    if cmd=='R': return f'<rect x="{a[1]}" y="{a[2]}" width="{a[5]}" height="{a[6]}" stroke="{a[7]}" stroke-width="{a[8]}" fill="{a[10]}"/>'
    if cmd=='C': return f'<circle cx="{a[1]}" cy="{a[2]}" r="{a[3]}" stroke="{a[4]}" stroke-width="{a[5]}" fill="{a[7]}"/>'
    if cmd=='T':
        if a[13]!='1': return ''
        return f'<text x="{a[2]}" y="{a[3]}" fill="{a[5]}" font-family="Arial,sans-serif" font-size="{a[7]}" font-weight="{a[8] or "normal"}" text-anchor="{a[14]}">{esc(a[12])}</text>'
    if cmd=='N': return f'<text x="{a[8]}" y="{a[9]}" fill="{a[4]}" font-family="Arial,sans-serif" font-size="{a[11]}" text-anchor="{a[7]}">{esc(a[5])}</text>'
    if cmd=='J': return f'<circle cx="{a[1]}" cy="{a[2]}" r="{a[3]}" fill="{a[4]}"/>'
    if cmd=='O': return f'<path d="{a[4]}" fill="none" stroke="{a[5]}"/>'
    if cmd=='P':
        z=s.split('^^'); p=z[2].split('~'); out=f'<path d="{p[0]}" stroke="{p[1]}" fill="none"/>'
        n=z[3].split('~')
        if n[0]=='1': out+=f'<text x="{n[1]}" y="{n[2]}" font-family="Arial,sans-serif" font-size="{n[7]}" fill="{n[8]}" text-anchor="{n[5]}">{esc(n[4])}</text>'
        return out
    raise ValueError(cmd)
svg='<svg xmlns="http://www.w3.org/2000/svg" width="1620" height="1145" viewBox="0 0 1620 1145"><rect width="1620" height="1145" fill="white"/>'+''.join(svg_shape(s) for s in doc['shape'])+'</svg>'
(OUT/'FoodScan_Esquematico_v1.svg').write_text(svg,encoding='utf-8')
print(json.dumps({'file':str(dest),'status':report['status'],'components':report['components'],'nets':report['nets']}))
