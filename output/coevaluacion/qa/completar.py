from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
import json
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\Users\Mao\Downloads\Formato de Coevaluación Grupal.docx')
OUTPUT = ROOT.parent / 'Coevaluacion_Grupal_Equipo10_FoodScan.docx'
PHOTOS = Path(r'C:\Users\Mao\Desktop\para la coevaluacion')
reference_hash = sha256(SOURCE.read_bytes()).hexdigest()
with ZipFile(SOURCE) as z:
    inventory = {n: {'size': len(z.read(n)), 'sha256': sha256(z.read(n)).hexdigest()} for n in z.namelist()}
(ROOT / 'inventario_referencia.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
(ROOT / 'artifact.md').write_text(f'''# Contrato de edición del formato de coevaluación
Referencia: {SOURCE}
SHA256: {reference_hash}
Render de referencia: qa/referencia/page-1.png y page-2.png, exportadas con Word.
Dos páginas, una sección horizontal Carta de 11 × 8,5 pulgadas. Márgenes 1 pulgada en todos los lados. Encabezado 0 y pie 0,5 pulgadas.
Arial 11 puntos por defecto. Título original centrado, negrita, 16 puntos, subrayado. Instrucciones y aviso en cuadro de texto se conservan completos. Metadatos en dos párrafos con etiquetas en negrita.
Tabla de seis columnas, ancho 13033 twips y rejilla 468,1651,3118,3544,1134,3118 twips. Bordes negros y cabecera gris clara, según el original. Cabecera repetida. Distribución original: dos integrantes en la primera página y tres en la segunda.
Slots: word/document.xml / body/p[4] proyecto y equipo; p[5] curso, semestre y fecha. Tabla 1, filas 2 a 6: columna 2 fotografía, 3 nombre completo, 4 labor, 5 porcentaje. Columna 6 queda vacía para firma personal; no se crean firmas. Números, cabeceras, instrucciones, nota y aviso legal se conservan.
Fotos JPEG sin edición, proporción original y ancho máximo 0,86 pulgadas. Se ajusta exclusivamente el espaciado de las celdas de foto para insertar imágenes sin ampliar las filas originales. Texto nuevo Arial 11 negro, centrado verticalmente; nombres y labores alineados a la izquierda, porcentaje centrado.
Partes preservadas: todas las incluidas en inventario_referencia.json, salvo document.xml, document.xml.rels y Content_Types, que deben incorporar texto, dibujos y relaciones. Se añaden únicamente cinco fotos JPEG. No se alteran estilos, tema, fuentes, propiedades, configuración ni relaciones ajenas a fotos.
Datos: README remoto de Mao-dot/Fdd_Equipo_10 para nombres y roles; certificado de Julio en el mismo repositorio identifica su segundo apellido Bernilla. FoodScan consta en los materiales locales del proyecto. Porcentajes provistos por el usuario, fecha 22/10/2026. Firmas intencionalmente en blanco.
Validación: revisar todas las páginas de Word, seis columnas, cinco fotos, porcentajes 100/95/100/90/95, ausencia de marcadores por rellenar salvo firmas, misma geometría y preservación byte por byte de partes ajenas.
''', encoding='utf-8')

d = Document(SOURCE)

def run_format(r, bold=False):
    r.font.name = 'Arial'
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r.bold = bold

def metadata(p, fields):
    p.clear()
    for i, (label, value) in enumerate(fields):
        if i:
            run_format(p.add_run('\t'))
        run_format(p.add_run(label), True)
        run_format(p.add_run(value))

metadata(d.paragraphs[3], [('Nombre del Proyecto: ', 'FoodScan'), ('Equipo: ', '10')])
metadata(d.paragraphs[4], [('Curso: ', 'Fundamentos de Diseño'), ('Semestre: ', '2026-2'), ('Fecha: ', '22 / 10 / 2026')])

members = [
    ('Mao', 'Mao Arceni Capcha Pumacahua', 'Liderazgo y coordinación del equipo; programación, análisis de datos y simulación.', '100%'),
    ('Katherine', 'Katherine Jireh Cruz Oyarce', 'Documentación del proyecto y redacción técnica de los entregables.', '95%'),
    ('Lucero', 'Lucero Sofía Tarazona Gonzales', 'Investigación del proyecto, revisión de fuentes y análisis de la problemática.', '100%'),
    ('Renzo', 'Renzo Jair Cruz Vega', 'Diseño de prototipos y desarrollo de propuestas de solución.', '90%'),
    ('Julio', 'Julio Maguiña Bernilla', 'Coordinación de investigación, análisis de información y desarrollo de propuestas.', '95%'),
]

t = d.tables[0]
for row, (photo, name, work, percent) in zip(t.rows[1:], members):
    # Normalize the number/photo padding so actual photos fit the original
    # two-page form without the placeholder's accumulated blank spacing.
    row.height = Inches(1.40)
    row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    ncell = row.cells[0]
    ncell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    np = ncell.paragraphs[0]
    np.paragraph_format.space_before = Pt(0)
    np.paragraph_format.space_after = Pt(0)
    nmar = ncell._tc.get_or_add_tcPr().find(qn('w:tcMar'))
    for side in ['top', 'bottom']:
        nmar.find(qn('w:' + side)).set(qn('w:w'), '120')
    for col, text in [(2, name), (3, work), (4, percent)]:
        c = row.cells[col]
        p = c.paragraphs[0]
        p.clear()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col == 4 else WD_ALIGN_PARAGRAPH.LEFT
        run_format(p.add_run(text), col == 4)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    c = row.cells[1]
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    tcpr = c._tc.get_or_add_tcPr()
    mar = tcpr.find(qn('w:tcMar'))
    if mar is None:
        mar = OxmlElement('w:tcMar')
        tcpr.append(mar)
    for side in ['top', 'bottom']:
        el = mar.find(qn('w:' + side))
        if el is None:
            el = OxmlElement('w:' + side)
            mar.append(el)
        el.set(qn('w:w'), '120')
        el.set(qn('w:type'), 'dxa')
    p = c.paragraphs[0]
    p.clear()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1
    raw = (PHOTOS / (photo + '.jpeg')).read_bytes()
    # WhatsApp's JFXX application marker precedes the real JFIF header in
    # Lucero's file. Drop only that metadata segment, retaining JPEG pixels.
    if raw[2:4] == b'\xff\xe0' and raw[6:11] == b'JFXX\x00':
        raw = raw[:2] + raw[4 + int.from_bytes(raw[4:6], 'big'):]
    picture = p.add_run().add_picture(BytesIO(raw), width=Inches(.86))
    picture._inline.docPr.set('descr', 'Fotografía de ' + name)

working = ROOT / 'trabajo.docx'
d.save(working)

# Only transplant intentional edited parts. Preserve the reference's other
# package parts byte for byte, including its embedded fonts and legal notice.
changed = {'word/document.xml', 'word/_rels/document.xml.rels', '[Content_Types].xml'}
with ZipFile(SOURCE) as original, ZipFile(working) as modified, ZipFile(OUTPUT, 'w') as out:
    for info in original.infolist():
        out.writestr(info, modified.read(info.filename) if info.filename in changed else original.read(info.filename))
    for info in modified.infolist():
        if info.filename.startswith('word/media/') and info.filename not in original.namelist():
            out.writestr(info, modified.read(info.filename))

with ZipFile(SOURCE) as original, ZipFile(OUTPUT) as final:
    for n in original.namelist():
        if n not in changed:
            assert original.read(n) == final.read(n), n
    assert len([n for n in final.namelist() if n.startswith('word/media/')]) == 5
check = Document(OUTPUT)
assert len(check.inline_shapes) == 5
assert [r.cells[4].text for r in check.tables[0].rows[1:]] == ['100%', '95%', '100%', '90%', '95%']
assert all(not r.cells[5].text.strip() for r in check.tables[0].rows[1:])
assert sha256(SOURCE.read_bytes()).hexdigest() == reference_hash
print(OUTPUT)
(ROOT / 'artifact.md').write_text((ROOT / 'artifact.md').read_text(encoding='utf-8') + '\nAjuste de inserción: espaciado vertical de las celdas de número y foto reducido a 120 twips; filas mínimas de 1,40 pulgadas para conservar dos páginas con las fotos reales.\n', encoding='utf-8')
