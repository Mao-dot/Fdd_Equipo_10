"""Planos conceptuales acotados de FoodScan. ReportLab; mm; A3 horizontal."""
from pathlib import Path
import math
import shutil
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase.pdfmetrics import stringWidth

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'output'/'pdf'/'FoodScan_Planos_acotados_v1.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
INK=HexColor('#203440'); BLUE=HexColor('#176980'); GRAY=HexColor('#657882')
LIGHT=HexColor('#e9eef0'); PALE=HexColor('#f5f8f9'); AMBER=HexColor('#a76312')
c=canvas.Canvas(str(OUT),pagesize=(420*mm,297*mm))
c.setTitle('FoodScan | Planos conceptuales acotados | Equipo 10')
c.setAuthor('Equipo 10 - Fundamentos de Diseño')

def text(x,y,s,size=2.8,bold=False,color=INK,align='left'):
    c.setFillColor(color);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
    getattr(c,{'left':'drawString','center':'drawCentredString','right':'drawRightString'}[align])(x,y,str(s))

def line(x1,y1,x2,y2,color=INK,width=.22,dash=None):
    c.setStrokeColor(color);c.setLineWidth(width);c.setDash(dash or [])
    c.line(x1,y1,x2,y2);c.setDash([])

def rect(x,y,w,h,fill=None,stroke=INK,width=.22,dash=None):
    c.setLineWidth(width);c.setStrokeColor(stroke);c.setDash(dash or [])
    if fill: c.setFillColor(fill)
    c.rect(x,y,w,h,fill=int(fill is not None),stroke=1);c.setDash([])

def circle(x,y,r,fill=None,stroke=INK,width=.22):
    c.setLineWidth(width);c.setStrokeColor(stroke)
    if fill: c.setFillColor(fill)
    c.circle(x,y,r,fill=int(fill is not None),stroke=1)

def arrow(x,y,angle,size=1.7,color=BLUE):
    a=math.radians(angle)
    for off in (-24,24):
        q=a+math.radians(off)
        line(x,y,x+size*math.cos(q),y+size*math.sin(q),color,.18)

def dh(x1,x2,y,ext_y,label):
    line(x1,ext_y,x1,y-1,GRAY,.13);line(x2,ext_y,x2,y-1,GRAY,.13)
    line(x1,y,x2,y,BLUE,.16);arrow(x1,y,0);arrow(x2,y,180)
    tw=stringWidth(str(label),'Helvetica',2.7)
    c.setFillColor(white);c.rect((x1+x2-tw)/2-.6,y+.25,tw+1.2,3.7,fill=1,stroke=0)
    text((x1+x2)/2,y+1.3,label,2.7,color=BLUE,align='center')

def dv(y1,y2,x,ext_x,label):
    line(ext_x,y1,x+1,y1,GRAY,.13);line(ext_x,y2,x+1,y2,GRAY,.13)
    line(x,y1,x,y2,BLUE,.16);arrow(x,y1,90);arrow(x,y2,270)
    c.saveState();c.translate(x-1.3,(y1+y2)/2);c.rotate(90)
    tw=stringWidth(str(label),'Helvetica',2.7)
    c.setFillColor(white);c.rect(-tw/2-.6,-.3,tw+1.2,3.7,fill=1,stroke=0)
    text(0,0,label,2.7,color=BLUE,align='center');c.restoreState()

def para(x,y,s,width=90,size=2.8,leading=4.3,color=INK):
    for paragraph in s.split('\n'):
        words=paragraph.split();row=''
        for word in words:
            trial=(row+' '+word).strip()
            if stringWidth(trial,'Helvetica',size)>width and row:
                text(x,y,row,size,color=color);y-=leading;row=word
            else:row=trial
        if row:text(x,y,row,size,color=color);y-=leading
        y-=1.1
    return y

def heading(n,title,subtitle):
    c.saveState();c.scale(mm,mm)
    rect(10,10,400,277,stroke=GRAY,width=.25)
    text(16,277,'FOODSCAN',6.4,True)
    text(407,278,f'EQUIPO 10  /  S11  /  {n:02d}',3,True,color=BLUE,align='right')
    text(16,269,title,4.3,True)
    text(16,262,subtitle,2.8,color=GRAY)
    line(16,258,404,258,GRAY,.2)
    line(10,22,410,22,GRAY,.2)
    text(15,16,'DISEÑO CONCEPTUAL v1.0  |  28/10/2026  |  Unidades: mm  |  No medir sobre el PDF',2.5)
    text(405,16,f'A3 horizontal  |  Hoja {n}/3',2.5,align='right')

def end():
    c.restoreState();c.showPage()

def bullet(x,y,num,title,body,width=89):
    circle(x+2,y,2.5,BLUE,BLUE);text(x+2,y-.9,num,2.5,True,white,'center')
    text(x+7,y-1,title,3,True)
    return para(x+7,y-7,body,width-7,2.65,4)-5

# 1. Conjunto: vistas y ubicacion interior.
heading(1,'Conjunto y distribución interna','Caja de captura y pesaje con puerta frontal, cámara superior, iluminación y electrónica integrada.')
s=.30
# Planta, sin tapa.
x,y=29,155
text(x,y+99,'PLANTA - TAPA OCULTA',3.0,True)
rect(x,y,320*s,320*s,PALE)
rect(x+3*s,y+3*s,314*s,314*s,white)
rect(x+50*s,y+50*s,220*s,220*s,stroke=GRAY,dash=[1.3,1])
circle(x+160*s,y+160*s,100*s,stroke=GRAY)
rect(x+65*s,y+277*s,215*s,38*s,LIGHT)
rect(x+146.5*s,y+140*s,27*s,40*s,stroke=BLUE)
line(x+160*s,y+40*s,x+160*s,y+270*s,GRAY,.13,[2,1,.4,1])
line(x+40*s,y+160*s,x+280*s,y+160*s,GRAY,.13,[2,1,.4,1])
dh(x,x+96,y-7,y,'320');dv(y,y+96,x-8,x,'320')
text(x+48,y+3,'FRENTE / PUERTA',2.5,color=GRAY,align='center')
text(x+50,y+85,'Conexiones',2.3,color=BLUE,align='center')
text(x+48,y+27,'Plataforma 220 × 220',2.5,align='center')

# Frontal cerrado.
x,y=29,34
text(x,y+110,'VISTA FRONTAL - PUERTA CERRADA',3,True)
rect(x,y,96,105,PALE)
rect(x+4.5*s,y+7.5*s,311*s,338*s,white)
for z in (65,260):rect(x-1.5,y+z*s,7,25*s,LIGHT)
rect(x+273*s,y+175*s,14*s,40*s,BLUE)
for px in (20,300):rect(x+px*s-2.4,y-1.8,4.8,1.8,LIGHT)
dh(x,x+96,y-7,y,'320');dv(y,y+105,x-8,x,'350')
text(x+48,y+51,'PUERTA MDF 3 mm',3.1,True,align='center')
text(x+48,y+45,'311 × 338',2.8,align='center')

# Lateral y alturas de referencia.
x,y=172,34
text(x,y+110,'LATERAL - SECCIÓN DE REFERENCIA',3,True)
rect(x,y,96,105,PALE)
rect(x+3*s,y+6*s,314*s,341*s,white)
rect(x-7.2,y+175*s,7.2,40*s,BLUE)
rect(x+50*s,y+38*s,220*s,6*s,LIGHT)
rect(x+60*s,y+44*s,200*s,9*s,stroke=GRAY)
rect(x+154*s,y+18*s,12*s,12*s,LIGHT)
rect(x+150*s,y+6*s,20*s,12*s,BLUE)
rect(x+150*s,y+30*s,20*s,8*s,BLUE)
rect(x+140*s,y+325*s,40*s,1.6*s,BLUE)
circle(x+160*s,y+318*s,1.3,fill=INK)
line(x+160*s,y+318*s,x+160*s,y+48*s,BLUE,.15,[2,1])
dv(y+48*s,y+318*s,x+106,x+160*s,'270')
dh(x,x+96,y-7,y,'320')
text(x+48,y+62,'Eje óptico',2.5,color=BLUE,align='center')
text(x+48,y+17,'Plato Ø200',2.5,align='center')

# Vista real del CAD.
img=HERE/'Vistas'/'FoodScan_Interior.png'
if img.exists():
    c.drawImage(str(img),149,159,width=137,height=93,preserveAspectRatio=True,anchor='c',mask='auto')
text(217,154,'VISTA DEL MODELO 3D',3,True,align='center')
text(217,149,'Tapa y lateral derecho ocultos para mostrar el interior.',2.35,color=GRAY,align='center')

yy=248
yy=bullet(302,yy,'1','Envolvente','Cuerpo: 320 × 320 × 350. Patas: 6 de alto. Manija: 24 hacia el frente.')
yy=bullet(302,yy,'2','Captura','ESP32-CAM arriba, lente hacia el plato. Distancia nominal: 270 al plano del plato.')
yy=bullet(302,yy,'3','Pesaje','Plataforma 220 × 220 × 6. Holgura lateral: 47. Celda de barra: 75 × 12 × 12 aprox.')
yy=bullet(302,yy,'4','Luz y puerta','Tres placas de cuatro LED y difusores. Microswitch al marco superior derecho.')
yy=bullet(302,yy,'5','Conexiones','HX711 y distribución al fondo. Jack y encendido en el lateral derecho. Adaptador externo.')
para(302,yy-2,'Las medidas principales vienen de componentes.md, sección 5. Distribución, soportes y huecos son una propuesta CAD pendiente de prueba física.',89,2.6,4,color=AMBER)
end()

# 2. Despiece de paneles: seis tarjetas.
heading(2,'Paneles de MDF y dimensiones de corte','MDF blanco de 3 mm. Base y plataforma: laminar dos piezas iguales para obtener 6 mm de espesor.')
cards=[
 ('M01','BASE',320,320,'2 piezas de 3 mm','Conjunto laminado: 320 × 320 × 6.'),
 ('M05','TAPA SUPERIOR',320,320,'1 pieza de 3 mm','Desmontable para acceso a la cámara.'),
 ('M02 / M03','LATERALES',320,341,'2 piezas de 3 mm','Derecho: jack y switch, detalle en hoja 3.'),
 ('M04','PANEL POSTERIOR',314,341,'1 pieza de 3 mm','Entre laterales; sobre base de 6 mm.'),
 ('M06','PUERTA FRONTAL',311,338,'1 pieza de 3 mm','Holgura nominal: 1.5 por lado del hueco.'),
 ('M07','PLATAFORMA',220,220,'2 piezas de 3 mm','Conjunto laminado: 220 × 220 × 6.'),
]
for i,(ref,title,w,h,qty,note) in enumerate(cards):
    col=i%3;row=i//3;xx=15+132*col;bottom=143 if row==0 else 29
    rect(xx,bottom,126,110,PALE,stroke=LIGHT)
    text(xx+4,bottom+102,ref,2.5,True,color=BLUE)
    text(xx+4,bottom+95,title,3.5,True)
    scale=.205
    rw,rh=w*scale,h*scale
    rx=xx+63-rw/2;ry=bottom+19+(72-rh)/2
    rect(rx,ry,rw,rh,white)
    dh(rx,rx+rw,ry-5,ry,str(w));dv(ry,ry+rh,rx-6,rx,str(h))
    text(xx+122,bottom+102,qty,2.6,align='right')
    text(xx+4,bottom+8,note,2.45)
text(15,25,'Cortes nominales sin compensación de herramienta. Taladros de fijación y uniones: ajustar al material y a las piezas reales.',2.6,color=AMBER)
end()

# 3. Detalles de pesaje, huecos y soporte de camara.
heading(3,'Detalles críticos de montaje','Cotas nominales del concepto. Confirmar la rosca y el patrón real de la celda antes de fabricar adaptadores.')
text(18,249,'A  |  RUTA DE CARGA Y SEPARACIÓN',3.5,True)
x0,y0=21,181
# Vista frontal del conjunto de pesaje, escala geometrica 1:1.
rect(x0,y0,220,6,LIGHT)
line(x0,y0+3,x0+220,y0+3,GRAY,.13)
rect(x0+72.5,y0+6,30,12,BLUE)
rect(x0+72.5,y0+18,75,12,fill=HexColor('#d1d9dd'))
rect(x0+117.5,y0+30,30,8,BLUE)
rect(x0,y0+38,220,6,LIGHT)
line(x0,y0+41,x0+220,y0+41,GRAY,.13)
for dx in (30,190):rect(x0+dx-4,y0+6,8,31,stroke=GRAY,dash=[1,1])
for dx in (80,95,125,140):
    line(x0+dx,y0+4,x0+dx,y0+45,GRAY,.15,[1,.6])
dh(x0,x0+220,y0+51,y0+44,'220')
dh(x0+72.5,x0+147.5,y0-9,y0+18,'75 (celda aprox.)')
dv(y0,y0+44,x0-6,x0,'44')
line(x0+30,y0+37,x0+13,y0+60,BLUE,.2)
text(x0+13,y0+63,'Tope: 1 de holgura',2.6,color=BLUE)
text(x0+132.5,y0+32,'MÓVIL',2.2,True,color=white,align='center')
text(x0+87.5,y0+10,'FIJO',2.2,True,color=white,align='center')
text(x0+110,y0-17,'Base 6 + adaptador 12 + celda 12 + adaptador 8 + plataforma 6',2.7,align='center')
para(18,151,'El extremo izquierdo de la celda se fija a la base. El extremo derecho sostiene la plataforma. La zona central deformable queda libre. Los topes se muestran proyectados; no deben tocar la plataforma durante el pesaje.',225,2.7,4.2)

# Adaptadores, planta acotada.
text(18,126,'ADAPTADORES P01 Y P02 - MISMA PLANTA',3.3,True)
ax,ay=31,80;sc=1.6
rect(ax,ay,30*sc,20*sc,PALE)
for dx in (7.5,22.5):circle(ax+dx*sc,ay+10*sc,1.7*sc,white)
dh(ax,ax+48,ay-6,ay,'30');dv(ay,ay+32,ax-7,ax,'20')
dh(ax+12,ax+36,ay+39,ay+16,'15')
text(92,108,'2 taladros pasantes Ø3.4',2.9,True)
text(92,101,'Centrados en el ancho de 20.',2.8)
text(92,94,'A 7.5 de cada extremo longitudinal.',2.8)
text(92,87,'P01 fijo: altura 12. P02 móvil: altura 8.',2.8)
para(92,78,'Patrón propuesto de la maqueta; reemplazar por las medidas de la celda recibida.',149,2.7,4.2,color=AMBER)
para(18,56,'Base: agujeros en X = -30 y -15, Y = 0. Plataforma: X = +15 y +30, Y = 0. Origen en el centro de cada panel, con X paralelo a la barra. Ø3.4 provisionales; la selección final de tornillos depende de la celda.',222,2.65,4.1)

# Lateral derecho: huecos provisionales con referencia inequívoca.
text(265,249,'B  |  LATERAL DERECHO',3.5,True)
sx,sy,sc=275,173,.205
rect(sx,sy,320*sc,341*sc,PALE)
# En coordenadas de panel, y=0 es borde frontal, z=0 borde inferior zglobal=6.
cx=sx+290*sc;cz=sy+61*sc
circle(cx,cz,4*sc,white)
rect(sx+239.5*sc,sy+54.5*sc,21*sc,13*sc,white)
dh(sx,cx,sy-6,sy,'290 al centro del jack')
dv(sy,cz,sx+73,cx,'61')
line(sx,sy,sx,sy-2,BLUE,.3)
text(sx-1,sy-12,'FRENTE',2.4,True,color=BLUE)
para(265,151,'Jack: hueco Ø8; centro a 290 del borde frontal y 61 del borde inferior del panel.\nSwitch: hueco 21 × 13; centro a 250 del frente y 61 del borde inferior.\nAmbos centros quedan a Z = 67 respecto de la cara inferior de la base.',130,2.65,4.1)
para(265,112,'Estos huecos son referencias de ubicación. Medir jack e interruptor reales y ajustar sus recortes antes de cortar.',130,2.7,4.2,color=AMBER)
text(265,88,'C  |  SOPORTE DE CÁMARA P04',3.5,True)
para(265,80,'Anillo inferior: 46 × 54 × 3. Ventana central: 20 × 30. Cuatro pilares de 6 × 6 y altura 22. Altura total: 25.\nPCB apoyada a Z = 325; lente inferior a Z = 318. Plato: plano interior a Z = 48. Distancia nominal: 270.\nSoporte, lente y placa requieren ajuste con la unidad real. Verificar encuadre antes de cerrar dimensiones.',130,2.65,4.1)
end()
c.save()
(HERE/'Planos').mkdir(exist_ok=True)
shutil.copy2(OUT,HERE/'Planos'/OUT.name)
print(OUT)
