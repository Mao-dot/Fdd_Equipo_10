"""Revisión electrónica del informe. Conserva el PDF original y su paginación.

Ejecutar con el Python del runtime de Codex (reportlab, pymupdf y Pillow).
Las páginas no intervenidas se conservan sin recomponer su contenido.
"""
from pathlib import Path
from io import BytesIO
import json
import re
import shutil
import pymupdf as fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Fundamentos de diseño/Entregables/Informe_Entregable_2_Equipo10._.pdf'
OUT = ROOT / 'output/pdf/Informe_Entregable_2_Equipo10_Corregido_v2.pdf'
TMP = ROOT / 'tmp/pdfs/informe_revision'
TMP.mkdir(parents=True, exist_ok=True)
OUT.parent.mkdir(parents=True, exist_ok=True)
for name, filename in [('TNR', 'times.ttf'), ('TNR-B', 'timesbd.ttf'), ('TNR-I', 'timesi.ttf'), ('TNR-BI', 'timesbi.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / filename)))
pdfmetrics.registerFontFamily('TNR', normal='TNR', bold='TNR-B', italic='TNR-I', boldItalic='TNR-BI')

doc = fitz.open(SOURCE)
W, H = doc[0].rect.width, doc[0].rect.height
LEFT, WIDTH = 72, 454
changed = set()
source_hash = __import__('hashlib').sha256(SOURCE.read_bytes()).hexdigest()

class Layer:
    def __init__(self, page_no, top=80, bottom=780):
        self.n, self.y, self.bottom = page_no, top, bottom
        self.buf = BytesIO()
        self.c = canvas.Canvas(self.buf, pagesize=(W, H))

    def para(self, text, size=11.5, leading=None, after=7, bold=False, italic=False, align=0, width=WIDTH, x=LEFT):
        font = 'TNR-B' if bold else 'TNR-I' if italic else 'TNR'
        st = ParagraphStyle('p', fontName=font, fontSize=size, leading=leading or size*1.31,
                            alignment=align, spaceAfter=0, textColor=colors.black)
        p = Paragraph(text, st)
        _, h = p.wrap(width, 1000)
        self.check(h)
        p.drawOn(self.c, x, H-self.y-h)
        self.y += h + after

    def heading(self, text):
        self.para(text, bold=True, size=12, after=10)

    def check(self, h):
        if self.y + h > self.bottom:
            raise ValueError(f'Página {self.n}: contenido excede el límite ({self.y+h:.1f}>{self.bottom})')

    def table(self, rows, widths, size=10.5, leading=None, fills=None, pad=4, header=True):
        st = ParagraphStyle('cell', fontName='TNR', fontSize=size, leading=leading or size*1.16)
        data = [[Paragraph(str(cell), st) for cell in row] for row in rows]
        t = Table(data, colWidths=widths, hAlign='LEFT')
        cmds = [('GRID',(0,0),(-1,-1),.45,colors.HexColor('#333333')),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('LEFTPADDING',(0,0),(-1,-1),pad),('RIGHTPADDING',(0,0),(-1,-1),pad),
                ('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad)]
        if header: cmds += [('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E6ECDE'))]
        for col, color in (fills or {}).items():
            cmds += [('BACKGROUND',(col,1),(col,-1),colors.HexColor(color))]
        t.setStyle(TableStyle(cmds))
        _, h = t.wrap(WIDTH,1000)
        self.check(h)
        t.drawOn(self.c, LEFT, H-self.y-h)
        self.y += h+8

    def crop(self, source_page, rect, width, height):
        pix = doc[source_page-1].get_pixmap(matrix=fitz.Matrix(2,2), clip=fitz.Rect(rect))
        self.check(height)
        im = Image(BytesIO(pix.tobytes('png')), width=width, height=height)
        im.drawOn(self.c, LEFT+(WIDTH-width)/2, H-self.y-height)
        self.y += height+8

    def finish(self, clear_rect=None, clear_graphics=True):
        self.c.save()
        p = doc[self.n-1]
        if clear_rect:
            p.add_redact_annot(fitz.Rect(clear_rect), fill=(1,1,1))
            p.apply_redactions(images=2 if clear_graphics else 0, graphics=2 if clear_graphics else 0)
        overlay = fitz.open(stream=self.buf.getvalue(), filetype='pdf')
        p.show_pdf_page(p.rect,overlay,0)
        # show_pdf_page copia contenido, pero no anotaciones de enlace.
        for link in overlay[0].get_links():
            if link.get('uri'):
                p.insert_link({'kind':fitz.LINK_URI,'from':link['from'],'uri':link['uri']})
        changed.add(self.n)

def patch(n, rect, text, size=10, fill=(1,1,1), align=0):
    p = doc[n-1]
    p.add_redact_annot(fitz.Rect(rect), fill=fill)
    p.apply_redactions(images=0,graphics=0)
    ly = Layer(n, rect[1]+1, rect[3])
    ly.para(text,size=size,leading=size*1.13,after=0,width=rect[2]-rect[0]-4,x=rect[0]+2,align=align)
    ly.finish()

# Portada: fecha de revisión, sin atribuir una fecha nueva a la investigación original.
patch(1,(180,680,420,735),'Revisión electrónica 2 · 4 de noviembre de 2026<br/>Informe base: octubre de 2026',11,align=1)

# Exigencias de energía y estado de integración: actualizar las celdas, no los requisitos ajenos.
patch(14,(243,591,299,698),'Módulo:<br/>5 V DC<br/>por jack.<br/>Batería no<br/>definida.',10,align=1)
patch(14,(302,591,365,698),'Medir 5 V<br/>y 3,3 V<br/>durante<br/>captura y<br/>Wi-Fi;<br/>verificar<br/>temperatura.',9.5,align=1)
patch(14,(472,591,522,698),'Revisado<br/>04/11/26.<br/>Prueba<br/>pendiente.',9,align=1)
patch(18,(472,84,522,253),'Wi-Fi<br/>2,4 GHz<br/>previsto.<br/>Integración<br/>y prueba<br/>pendientes.',9,align=1)

# Página 20: mantener las capturas originales de la app y corregir la operación objetivo.
p=Layer(20,80,466)
p.para('<b>Secuencia objetivo del concepto C.</b> La orden Registrar y la adquisición automática descritas aquí requieren firmware e integración con la app; la Figura 1 conserva la etapa manual ya documentada.',11,after=7)
steps=[
('Preparar y tarar','Colocar el plato vacío dentro, encender y registrar la tara: la lectura neta debe quedar en 0 g.'),
('Servir','Retirar ese plato, servir la comida y reintroducirlo. Se conserva la tara aunque aparezca una lectura negativa al retirarlo.'),
('Cerrar','Cerrar la puerta y abrir FoodScan en el celular; comprobar conexión y disponibilidad del módulo.'),
('Registrar','Enviar la orden desde la app. El equipo valida tara, puerta cerrada y masa estable; luego enciende luces, enfoca y captura.'),
('Esperar','La app muestra el estado de carga mientras recibe foto y gramos y solicita el análisis a Gemini por Internet.'),
('Revisar','Al terminar se apagan las luces y cesa la captura. El equipo queda en espera; se puede retirar el plato y revisar alimentos y cantidades.'),
('Corregir y confirmar','Corregir las estimaciones antes de guardar; consultar gramos, kcal, macronutrientes, fuente e historial.')]
for i,(title,text) in enumerate(steps,1):p.para(f'<b>Paso {i}. {title}.</b> {text}',11,leading=14,after=6)
p.para('La masa total es medida; el reparto por alimento es estimado. Las capturas siguientes corresponden al registro actual con balanza externa (24).',10.5,italic=True,after=0)
p.finish((68,77,530,467))

p=Layer(21)
p.heading('5.2.2.     Nivel Dispositivo')
p.para('Lógica prevista del sistema objetivo C. La revisión define conexiones y secuencia; todavía no acredita un ciclo físico implementado ni probado (17, 23, 30-33).')
steps=[
('Arranque y tara','Iniciar la ESP32-S3, HX711 y cámara; mantener Q1 y los LED apagados. Con el plato vacío dentro, guardar la tara y mostrar 0 g. La calibración con masa conocida se realiza por separado, no en cada encendido.'),
('Conservar la referencia','Al retirar el plato no recalcular el cero. Mantener la tara hasta reponer el mismo recipiente; invalidarla si cambia el plato o la configuración de pesaje.'),
('Recibir Registrar','Con Wi-Fi e Internet disponibles, recibir la orden y comprobar puerta cerrada, tara válida, carga admisible y señal estable. No aceptar una lectura negativa como porción.'),
('Iluminar y capturar','Activar GPIO42 y Q1, esperar estabilización de iluminación/exposición y ejecutar autofocus. Capturar una imagen y una lectura neta estable con el mismo identificador.'),
('Transmitir','Enviar foto, gramos y estado por Wi-Fi a la integración de FoodScan. La app muestra cargando. La autenticación de Gemini corresponde al backend; no se requiere laptop conectada por cable.'),
('Identificar y calcular','Gemini propone alimentos y proporciones. El software consulta las TPCA INS, 10.ª edición de 2017, y calcula masa × valor por 100 g / 100. El usuario puede corregir antes de confirmar.'),
('Finalizar','Desactivar Q1 al completar el ciclo o ante error/tiempo agotado; cesar la captura y volver a espera. El reposo por SCCB se verificará en firmware: no se corta físicamente toda la alimentación.')]
for i,(title,text) in enumerate(steps,1):p.para(f'<b>{i}. {title}.</b> {text}',11,leading=14.3,after=6)
p.para('<b>Interbloqueos:</b> puerta abierta, sobrecarga o peso inestable bloquean la captura y generan un aviso. Ante apertura o fallo durante el ciclo, apagar luces y cancelar el registro incompleto. El apagado general es manual mediante SW1.',10.5,after=9)
p.table([['<b>1. Preparar</b>','<b>2. Adquirir</b>','<b>3. Analizar</b>','<b>4. Cerrar ciclo</b>'],['Plato vacío y tara; conservar al retirarlo.','Registrar; puerta y peso; LED, enfoque, foto y masa.','Wi-Fi, app, Gemini y TPCA; revisión del usuario.','LED apagados; resultado, confirmación y espera.']],[113.5]*4,size=10,pad=5)
p.para('Figura 2: Secuencia prevista del dispositivo, revisión electrónica 2<br/>Fuente: Elaboración propia a partir de (16)-(19), (23), (24) y (30)-(33)',10.5,italic=True,align=1,after=0)
p.finish((68,77,530,782))

p=Layer(22)
p.heading('5.3.     Estructura de funciones')
p.para('Se conservan las once funciones parciales. La revisión concreta los portadores electrónicos del concepto C sin modificar la comparación entre alternativas A, B y C.',11.5)
sections=[
('5.3.1.     Dominio de Energía','F1 (Energizar) distribuye 5 V a la DevKit y los LED, y 3,3 V a la cámara y al HX711, con GND común. La base es un adaptador externo de 5 V / 2,4 A con jack, fusible e interruptor. La DevKit oficial tiene regulación de 800 mA nominales compartidos por las cargas de 3,3 V; deben medirse tensión y temperatura durante captura y Wi-Fi. No se ha seleccionado batería ni validado autonomía (17, 33).'),
('5.3.2.     Dominio de Comunicación','F2 establece el enlace Wi-Fi de 2,4 GHz con la aplicación; F4 intercambia órdenes, foto, masa y estado para un mismo registro. Se requiere Internet para Gemini. La cámara se conecta internamente por DVP de 8 bits y SCCB, no por USB a una laptop. El firmware y la recepción automática en la app están pendientes (23, 24, 30, 32).'),
('5.3.3.     Dominio de Adquisición y Medición','F3 controla iluminación por MOSFET, exposición y autofocus antes de capturar. F5 obtiene masa neta con celda de 5 kg y HX711 a 3,3 V, previa calibración y tara con plato vacío. Conservar la tara durante retiro y reposición; comprobar estabilidad. La capacidad nominal incluye plataforma, plato y comida, incluso después de tarar (18, 19, 30-32).'),
('5.3.4.     Dominio Mecánico','F11 sostiene la carga, evita roces y permite retirar y lavar el plato. Las dimensiones y vistas existentes son referencias conceptuales; su adaptación al nuevo módulo de cámara y placa no forma parte de esta corrección electrónica.'),
('5.3.5.     Dominio de Procesamiento y Datos','F6 propone alimentos con Gemini y permite revisión. F7 consulta la entrada nutricional por código y conserva fuente y edición. F8 normaliza gramos, escala y suma nutrientes con las TPCA del INS de 2017. F10 guarda el registro en el historial local solo después de confirmar. El backend ya acepta foto y masa; la integración automática del dispositivo falta implementar (16, 24, 32).'),
('5.3.6.     Dominio de Interfaz','F9 informa conexión, carga y errores y muestra el resultado: masa total medida, reparto por alimento estimado y nutrientes calculados. Los 5 MP del sensor y los 24 bits del HX711 no acreditan por sí solos exactitud nutricional ni metrológica.')]
for title,text in sections:
 p.para(title,bold=True,size=11.5,after=5);p.para(text,size=11,leading=14.1,after=9)
p.finish((68,77,530,782))

# La matriz y las alternativas conservan su diseño original; se cambian celdas y nota.
green=(228/255,236/255,222/255)
patch(24,(412,622,522,658),'OV5640 (C), 5 MP AF;<br/>12 LED + Q1.<br/>Control: S3 N16R8',8.7,fill=green)
patch(25,(71,77,527,109),'Compatibilidad en C: DevKitC-1 N16R8 a 5 V; OV5640 (C) y HX711 a 3,3 V. LED mediante Q1. Se reemplaza el mapa GPIO anterior por el esquema v2; véase p. 31. Fuentes: (17)-(19), (23), (30)-(33).',9.5)

p=Layer(27)
p.heading('6.3.3.     Concepto de solución C: Caja integrada')
p.para('Tabla 16: Portadores de función del Concepto C, revisión 2',11,italic=True,align=1)
rows=[['<b>Función parcial</b>','<b>Portador de función</b>'],
['F1 Energizar','Adaptador 5 V / 2,4 A; fusible 1,5 A; regulación a 3,3 V.'],
['F2 Conectar','ESP32-S3-DevKitC-1 N16R8; Wi-Fi 2,4 GHz + Internet.'],
['F3 Capturar','Waveshare OV5640 Camera Board (C), 5 MP AF; 12 LED con Q1 AO3400A.'],
['F4 Transmitir','Foto, masa y estado del mismo registro a la app.'],
['F5 Determinar cantidad','Celda de carga 5 kg + HX711 a 3,3 V; calibración y tara.'],
['F11 Sostener y limpiar','Plataforma flotante de 220 × 220 mm, referencia mecánica previa.'],
['F6 Identificar y corregir','Gemini en backend + revisión del usuario.'],
['F7 Consultar referencia','TPCA INS, 10.ª ed., 2017.'],
['F8 Calcular','Masa en gramos × valor por 100 g / 100 por alimento.'],
['F9 Informar','Pantalla del celular; carga, errores y resultado.'],
['F10 Guardar','Historial local después de confirmar.']]
p.table(rows,[188,266],size=10.5,pad=4.2)
p.para('<b>Análisis de compatibilidad.</b> Se utiliza una sola placa S3 y una cámara separada; la captura y los sensores permanecen dentro de la máquina. La fuente de 5 V alimenta la DevKit y las ramas LED. Cámara y HX711 reciben 3,3 V y comparten GND; el GPIO controla Q1, no alimenta directamente los LED. La cámara requiere el mapa DVP/SCCB v2, distinto del anterior (17-19, 23, 30-33).',11,leading=14.3)
p.para('La plataforma debe evitar roces. El conector P1 de la cámara seleccionada tiene 18 contactos, con 17 conexiones externas; PWDN queda libre externamente por su puente interno a GND. Otro módulo denominado OV5640 puede tener un conector y alimentación diferentes. Enfoque, alimentación, señal de pesaje y enlace completo requieren pruebas de montaje.',11,leading=14.3)
p.heading('6.4.     Evaluación de conceptos y selección del concepto óptimo')
p.para('Los tres caminos son alternativas conceptuales: A estima visualmente la masa; B mide con balanza externa y exige transcribirla; C propone medir y transmitir masa y foto automáticamente. Se conserva la comparación de Pugh de la sección 8 como evaluación preliminar. La electrónica corregida no equivale todavía a una integración física validada.',11.5,after=0)
p.finish((68,77,530,782))

# Página 30: se conserva la ilustración conceptual; la leyenda ahora describe la electrónica v2.
p=Layer(30)
p.heading('7.3.     Boceto del Concepto de solución C: Caja integrada')
p.para('FoodScan: sistema de información nutricional de porciones',11.5,bold=True,align=1,after=6)
p.para('Boceto previo conservado como referencia de distribución; no representa una actualización del modelo 3D ni el conector de la cámara nueva.',10.5,italic=True,align=1,after=5)
p.crop(30,(174,198,424,454),250,256)
p.table([['<b>Pieza</b>','<b>Componentes / función en la revisión 2</b>'],
['1','U1: ESP32-S3-DevKitC-1 N16R8, 16 MB Flash / 8 MB PSRAM. CAM1: Waveshare OV5640 (C), 5 MP AF, separada de U1. Posición cenital nominal: verificar encuadre.'],
['2','D1-D12: 12 LED blancos de 6000 K; R1-R12: 100 Ω, 1/4 W, una por LED. Q1 AO3400A controla el retorno; R14: 100 Ω de compuerta; R15: 100 kΩ a GND.'],
['3','LC1: celda de 5 kg, puente completo y cuatro hilos; U2: HX711 a 3,3 V. Plataforma flotante, sin roces. Tara con el plato vacío.'],
['4','SW2: microswitch KW11 SPDT; R13: pull-up de 10 kΩ a 3,3 V. Puerta cerrada habilita la captura. Estructura y soportes: disposición anterior pendiente de revisión.'],
['5','Adaptador 5 V / 2,4 A; J1 jack 5,5 × 2,1 mm centro positivo; F1 de 1,5 A con portafusible; SW1 KCD1 SPST. C1: 470 µF / 16 V; C2: 100 nF en 5 V. C3: 100 µF / 10 V; C4: 100 nF cerca de cámara en 3,3 V.'],
['6','Wi-Fi con la app y su backend Gemini. Orden Registrar, foto y gramos vinculados. No se necesita una segunda ESP32 ni una laptop para operar.']],[35,419],size=10.4,pad=4)
p.para('Dimensiones conceptuales previas: caja 320 × 320 × 350 mm; plataforma 220 × 220 mm. Lista, cantidades y cableado vigentes: BOM y esquemático electrónico v2 (32).',10.5,italic=True,after=0)
p.finish((67,77,530,782))

p=Layer(31)
p.para('<b>Funcionamiento actualizado del concepto C.</b> Tarar con plato vacío, retirarlo para servir y volver a colocarlo sin borrar la tara. Tras cerrar la puerta, Registrar inicia comprobaciones, iluminación, autofocus y captura. Foto y masa viajan por Wi-Fi a FoodScan; el backend consulta Gemini y el programa calcula con las TPCA. Al concluir o fallar el ciclo se apagan las luces y el módulo vuelve a espera (16, 24, 30-32).',11.5)
p.para('<b>Asignación resumida del esquema v2.</b> Cámara a 3,3 V, GND común; todas las señales corresponden a la Waveshare (C). El orden físico del conector debe comprobarse antes de energizar.',11,after=7)
p.table([['<b>Señal / módulo</b>','<b>GPIO de U1 / conexión</b>'],
['Cámara SCCB','SIOD → 8; SIOC → 9.'],
['Cámara sincronía / reloj','VSYNC → 13; HREF → 14; PCLK → 21; XCLK → 15.'],
['Cámara D0-D7 (Y2-Y9)','6, 7, 10, 11, 12, 16, 17, 18, respectivamente.'],
['Cámara RESET / PWDN','RESET → 5. P1.18 / PWDN sin conexión externa: puente interno a GND. Flash de cámara sin uso.'],
['Pesaje U2 / HX711','DT → 4; SCK → 2; alimentación a 3,3 V.'],
['Puerta SW2','NO → 1; COM → GND; NC libre. R13 de 10 kΩ a 3,3 V.'],
['Iluminación Q1','GPIO42 → R14 → compuerta. R15 a GND. Fuente a GND, drenador al retorno LED. Encendido con nivel alto.']],[155,299],size=10.5,pad=4)
p.para('Los GPIO35, 36 y 37 se reservan para la memoria en esta variante; se evitan también los pines de arranque y los de USB/UART usados para programación. El mapa completo y la verificación local de redes están en el esquema v2 (17, 32).',10.8)
p.para('<b>Pruebas pendientes.</b> Calibración con masas conocidas, repetibilidad al retirar/reponer el plato, detección de puerta y sobrecarga, enfoque/encuadre, consumo y temperatura con captura y Wi-Fi. La celda de 5 kg soporta plataforma, plato y comida: la tara no elimina esa carga física. Los archivos comprobados no sustituyen pruebas del montaje.',11,leading=14.2)
p.heading('7.3.1.     Vistas técnicas del Concepto C')
p.para('Las Figuras 4, 5 y 6 se conservan como <b>bocetos previos</b> de disposición mecánica: isométrica con puerta entreabierta, corte A-A y planta. Sus rótulos y soportes pertenecen a la versión anterior. La sustitución por DevKitC-1 N16R8 y OV5640 (C) aún requiere revisar fijaciones, cableado, separación y encuadre; esta entrega corrige electrónica y componentes, no el modelo 3D.',11.5)
p.para('La distancia cenital aproximada de 270 mm y las dimensiones anteriores son referencias geométricas, no un montaje validado para la nueva cámara. El soporte definitivo se definirá después de las pruebas ópticas.',11.5)
p.table([['<b>Dibujado por:</b>','Equipo 10 · Vistas de la versión anterior']],[110,344],size=11,header=False)
p.finish((67,77,530,782))

for n in [32,33,34]:
    ly=Layer(n,552,600)
    ly.para('Boceto de la versión anterior. Adaptación a ESP32-S3 N16R8 y OV5640 (C) pendiente; el modelo 3D no se modifica en esta revisión.',10.5,italic=True,align=1)
    ly.finish()

p=Layer(38)
p.heading('8.2.3.     Concepto de Solución C')
p.para('Tabla 22: Justificación conceptual de puntajes del Concepto C',11,italic=True,align=1)
rows=[['<b>N.º</b>','<b>Criterio</b>','<b>Peso</b>','<b>Valor</b>','<b>Justificación actualizada</b>'],
['1','Masa total medida','3','+1','Celda de 5 kg con HX711 sobre plataforma flotante; requiere calibración (18, 19).'],
['2','Iluminación controlada','2','+1','12 LED blancos con resistencias individuales y Q1 AO3400A (22, 31, 32).'],
['3','Encuadre fijo','2','+1','OV5640 (C) cenital; ≈270 mm como referencia previa. Verificar enfoque, campo de visión y nuevo soporte (30).'],
['4','Ingreso automático de masa y foto','3','+1','Función objetivo por Wi-Fi: foto, gramos y estado vinculados. Integración aún pendiente (24, 32).'],
['5','Corrección y fuente trazable','2','0','Corrección en app; fuente TPCA INS, edición 2017 (16, 24).'],
['6','Recipiente lavable','2','0','Plato removible apoyado en la plataforma; comparable a A.'],
['7','Facilidad de transporte','1','-1','Caja conceptual 320 × 320 × 350 mm; más voluminosa que A.'],
['8','Costo con recursos disponibles','1','-1','S/ 150 reservados solo para ESP32 y cámara. Cotización de ambas y del resto pendiente; el total antiguo ya no rige.'],
['9','Esfuerzo de fabricación','1','-1','Añade cableado, estructura, calibración y firmware.']]
p.table(rows,[24,100,29,39,262],size=10.2,pad=4)
p.para('Se conservan los puntajes preliminares para comparar conceptos, no como resultados de ensayos. La selección del nuevo hardware exige revisar el criterio económico con cotizaciones reales antes de confirmar el total (32).',10.8)
p.heading('8.3.     Concepto de Solución Óptimo')
p.para('La matriz de Pugh original asigna 7 puntos a C, 4 a B y 0 a A. Se conserva C como objetivo de diseño por combinar medición de masa, captura controlada y enlace automático con la app. La electrónica propuesta usa una ESP32-S3 N16R8 y una OV5640 (C), con Gemini en el backend existente.',11.5)
p.para('El presupuesto deseable de S/ 500 permanece como referencia de diseño, pero su cumplimiento no está confirmado para esta revisión. Los S/ 150 del equipo corresponden exclusivamente a placa y cámara; alimentación, sensores, iluminación, montaje y entrega requieren cotización separada. Se retiran como presupuesto vigente el total anterior y su reserva.',11.5)
p.para('La elección sigue sujeta a comprobar pesaje, captura, transmisión, estabilidad eléctrica y consumo. Mientras se integra la máquina, la ruta B permite continuar con balanza independiente e ingreso manual en la misma app y con la misma referencia nutricional.',11.5,after=0)
p.finish((68,77,530,782))

# Bibliografía: conservar numeración existente, reemplazar fuentes obsoletas y sumar fuentes v2.
p=Layer(40,80,782)
refs=[
('16','Reyes García M, Gómez-Sánchez Prieto I, Espinoza Barrientos C. Tablas peruanas de composición de alimentos. 10.ª ed. Lima: Instituto Nacional de Salud; 2017. 142 p. Disponible en: repositorio del INS.'),
('17','Espressif Systems. ESP32-S3-DevKitC-1 v1.1: guía de usuario y variantes de memoria [Internet; citado 4 nov 2026]. <link href="https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html" color="#244e42">docs.espressif.com · ESP32-S3-DevKitC-1</link>.'),
('18','Naylamp Mechatronics. Celda de carga 5 kg, SKU 000155 [Internet; citado 7 oct 2026]. Disponible en: Naylamp.'),
('19','Naylamp Mechatronics. Módulo HX711 transmisor de celda de carga, SKU 000147 [Internet; citado 7 oct 2026]. Disponible en: Naylamp.'),
('20','Naylamp Mechatronics. Adaptador WODE WA-12-5, 5 V, 2,4 A [Internet; citado 7 oct 2026]. Disponible en: Naylamp.'),
('21','Nanoparuro. Microswitch KW11-3Z-3F con palanca y rueda [Internet; citado 7 oct 2026]. Disponible en: Nanoparuro.'),
('22','Nanoparuro. LED blanco straw hat 5 mm, 6000 K, Vf 3,2-3,4 V [Internet; citado 7 oct 2026]. Disponible en: Nanoparuro.'),
('23','Espressif Systems. ESP32-S3-WROOM-1/1U: ficha técnica; controlador esp32-camera [Internet; citado 4 nov 2026]. <link href="https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf" color="#244e42">Ficha del módulo</link>; <link href="https://github.com/espressif/esp32-camera" color="#244e42">github.com/espressif/esp32-camera</link>.'),
('24','Equipo 10. Lista de exigencias, informe Taller 7 y documentación FoodScan. Lima: UPCH; 2026. Documentos internos. App: <link href="https://github.com/Mao-dot/FoodScan" color="#244e42">github.com/Mao-dot/FoodScan</link> (backend Gemini y motor nutricional).'),
('25','Whitton C, et al. A systematic review examining contributors to misestimation of food and beverage intake. Adv Nutr. 2022;13(6):2620-2665. doi:10.1093/advances/nmac085.'),
('26','Amoutzopoulos B, et al. Portion size estimation in dietary assessment: a systematic review of existing tools, their strengths and limitations. Nutr Rev. 2020;78(11):885-900. doi:10.1093/nutrit/nuz107.'),
('27','König LM, Ziesemer K, Renner B. Quantifying actual and perceived inaccuracy when estimating the sugar, energy content and portion size of foods. Nutrients. 2019;11(10):2425. doi:10.3390/nu11102425.'),
('28','Somocurcio Carrión LF. Influencia del etiquetado de alimentos procesados en el comportamiento del consumidor universitario peruano [tesis]. Lima: Universidad del Pacífico; 2021. <link href="https://hdl.handle.net/11354/3271" color="#244e42">hdl.handle.net/11354/3271</link>.'),
('29','Equipo 10. Taller 6: Desk Research en el marco del VDI 2206; Clase 6: Caja negra y estructura de funciones. Material de Blackboard. Fundamentos de Diseño; 2026-2.'),
('30','Waveshare. OV5640 Camera Board (C), SKU 13802: ficha y esquema [Internet; citado 4 nov 2026]. <link href="https://www.waveshare.com/ov5640-camera-board-c.htm" color="#244e42">waveshare.com/ov5640-camera-board-c.htm</link>; <link href="https://files.waveshare.com/upload/1/1e/OV5640-Camera-Board-Schematic.pdf" color="#244e42">esquema del conector P1</link>.'),
('31','Alpha &amp; Omega Semiconductor. AO3400A, 30 V N-Channel MOSFET. Rev. 3.1; jul 2023 [citado 4 nov 2026]. <link href="https://www.aosmd.com/res/data_sheets/AO3400A.pdf" color="#244e42">aosmd.com/res/data_sheets/AO3400A.pdf</link>.'),
('32','Equipo 10. Componentes_v2.md, BOM.md y FoodScan_Esquematico_v2: corrección electrónica. Proyecto/MóduloElectrónico; 4 nov 2026. Diseño e interconexión; montaje y firmware pendientes.'),
('33','Espressif Systems. Esquema ESP32-S3-DevKitC-1 v1.1, 13 abr 2022 [citado 4 nov 2026]. <link href="https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20220413.pdf" color="#244e42">dl.espressif.com · SCH_ESP32-S3-DevKitC-1_V1.1</link>.')]
for num,ref in refs:p.para(f'{num}. &nbsp; {ref}',size=9.8,leading=12,after=5)
p.finish((68,77,530,782))

# Marcar la revisión sin interferir con encabezados, numeración ni índice.
for n in sorted(changed):
    ly=Layer(n,785,800)
    ly.para('FoodScan · Revisión electrónica 2 · 04/11/2026',size=8,italic=True,after=0)
    ly.finish()
meta=doc.metadata
meta.update(title='FoodScan - Informe técnico del proyecto (Entregable 2), corregido v2',
            subject='Corrección de componentes, esquema y operación; modelo 3D pendiente',
            author='Equipo 10',keywords='ESP32-S3 N16R8, OV5640 (C), revisión electrónica 2')
doc.set_metadata(meta)
doc.save(OUT,garbage=4,deflate=True)
doc.close()

destinations=[]
for folder in ['Fundamentos de diseño/Entregables','Fundamentos de diseño/Presentaciones de Proyecto']:
    dest=ROOT/folder/OUT.name
    shutil.copy2(OUT,dest)
    destinations.append(str(dest.relative_to(ROOT)))
check=fitz.open(OUT)
assert len(check)==40
all_text='\n'.join(p.get_text() for p in check)
assert 'OV2640' not in all_text
assert 'ESP32-CAM' not in all_text
assert '404,43' not in all_text
assert 'GPIO13, GPIO14 y GPIO15' not in all_text
for token in ['N16R8','OV5640','AO3400A','PWDN','S/ 150','Gemini','800 mA']:
    assert token in all_text,token
(TMP/'informe_corregido.txt').write_text(all_text,encoding='utf-8')
manifest={'source':str(SOURCE.relative_to(ROOT)),'source_sha256':source_hash,
          'output':str(OUT.relative_to(ROOT)),'copies':destinations,
          'pages':len(check),'changed_pages':sorted(changed),
          'preserved':'Investigación, alternativas A/B, índice y numeración; bocetos mecánicos señalados como previos.',
          'scope':'Esquema y componentes; sin validación física, firmware nuevo ni actualización 3D.'}
original=fitz.open(SOURCE)
unchanged=[]
for n in range(1,41):
    if n not in changed:
        assert original[n-1].get_pixmap().samples==check[n-1].get_pixmap().samples, f'Cambio inesperado p{n}'
        unchanged.append(n)
for n in changed:
    for region in [fitz.Rect(0,0,595,72),fitz.Rect(460,800,595,842)]:
        assert original[n-1].get_pixmap(clip=region).samples==check[n-1].get_pixmap(clip=region).samples
assert 'Somocurcio' in all_text and 'Moscosurio' not in all_text
assert len(check[39].get_links())>=9
assert __import__('hashlib').sha256(SOURCE.read_bytes()).hexdigest()==source_hash
output_hash=__import__('hashlib').sha256(OUT.read_bytes()).hexdigest()
for path in destinations:
    assert __import__('hashlib').sha256((ROOT/path).read_bytes()).hexdigest()==output_hash
manifest['checks']={'unchanged_pages_pixel_identical':unchanged,
                    'headers_and_page_numbers_preserved':True,
                    'original_sha256_unchanged':True,
                    'output_copies_sha256_match':True,
                    'bibliography_hyperlinks':len(check[39].get_links()),
                    'output_sha256':output_hash,
                    'obsolete_components_removed_from_text':True}
(ROOT/'output/pdf/Informe_Corregido_v2_verificacion.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
