"""Esquemático FoodScan v4 para el modelo mecánico v3, commit a936fb1.

Genera una hoja EasyEDA Standard, su vista SVG y un PDF A3. Comprueba
la conectividad de la geometría contra las redes anteriores y el cableado nuevo.
"""

import ast
import json
import uuid
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'EasyEDA'
PDF_OUT = ROOT.parents[1] / 'output' / 'pdf'
WIDTH, HEIGHT = 2050, 1450
STEM = 'FoodScan_Conexiones_v4_COB'
MODEL_COMMIT = 'a936fb142d68106d2c9dbaca25990a7c4b9c1ac4'
DATE = '2026-11-12'

INK, TEXT, WIRE = '#29445C', '#172F43', '#2266A3'
P5, P3, GROUND, SIGNAL, RETURN = '#B24B25', '#7A4BAB', '#465668', '#2266A3', '#09746F'

# Reusar el formato nativo de las revisiones anteriores sin ejecutar sus generadores.
legacy = ast.parse((ROOT / 'generar_esquema.py').read_text(encoding='utf-8'))
helper_names = {'gid', 'text', 'line', 'rect', 'pin', 'lib', 'wire', 'net', 'dot',
                'find', 'union', 'esc', 'svg_shape'}
helpers = [node for node in legacy.body if isinstance(node, (ast.Import, ast.ImportFrom))
           or isinstance(node, ast.FunctionDef) and node.name in helper_names]
exec(compile(ast.Module(body=helpers, type_ignores=[]), 'foodscan_drawing_helpers', 'exec'))

base = json.loads((OUT / 'Verificacion_conexiones_v2.json').read_text(encoding='utf-8'))
specs = {ref: (part['value'], part['description']) for ref, part in base['components_detail'].items()}
specs.update({
    'F1': ('T3.15 A / 5x20 mm', 'Fusible retardado en portafusible de panel'),
    'X1': ('Bornera tornillo 2P 5.08 mm', 'Entrada a la placa de control'),
    'X2A': ('Bornera tornillo 4P 5.08 mm', 'Tiras izquierda LED1 y LED3'),
    'X2B': ('Bornera tornillo 4P 5.08 mm', 'Tiras derecha LED2 y LED4'),
    'X3': ('Bornera enchufable 4P 5.08 mm', 'Cable entre placa de control y HX711'),
    'X4': ('Bornera enchufable 2P 5.08 mm', 'Cable hacia el microswitch de puerta'),
    'X5': ('Bornera tornillo 4P 5.08 mm', 'Conexion de celda de carga junto al HX711'),
})
corners = {
    'LED1': 'Delantera izquierda',
    'LED2': 'Delantera derecha',
    'LED3': 'Trasera izquierda',
    'LED4': 'Trasera derecha',
}
for ref, corner in corners.items():
    specs[ref] = ('COB 5 V / 4000 K / 200 mm', f'Tira monocolor de dos hilos. {corner}.')

shapes, components, wires, labels = [], {}, [], []
counter = 0


def wire_color(name):
    if name in {'+5V', 'VIN_5V', 'VIN_FUSED'}:
        return P5
    return {'+3V3': P3, 'GND': GROUND, 'LED-': RETURN}.get(name, SIGNAL)


def cable(*points, name=None):
    wire(*points)
    fields = shapes[-1].split('~')
    fields[2:4] = [wire_color(name), '1.8']
    shapes[-1] = '~'.join(fields)


def tag(x, y, name, anchor='start'):
    net(x, y, name, anchor)
    fields = shapes[-1].split('~')
    fields[4] = wire_color(name)
    shapes[-1] = '~'.join(fields)


def panel(x, y, w, h, title, footer=None):
    shapes.extend([
        rect(x, y, w, h, '#CBD9E4', fill='#FAFCFE'),
        rect(x, y, w, 49, '#E5EDF4', fill='#E5EDF4'),
        text(x+17, y+32, title, 15, bold=True),
    ])
    if footer:
        shapes.append(text(x+17, y+h-14, footer, 9))


def part(ref, caption, x, y, w, h, ports, *, fill='#FFFFFF', compact=False, notes=()):
    """Los lados L/R usan coordenada Y, y T/B usan coordenada X."""
    title_offset, caption_offset = (17, 35) if compact else (24, 44)
    body = [rect(x, y, w, h, '#6D8CA5', fill=fill),
            text(x+w/2, y+title_offset, ref, 11, anchor='middle', bold=True)]
    if caption:
        body.append(text(x+w/2, y+caption_offset, caption, 10, anchor='middle'))
    pins = {}
    for key, side, coord, label in ports:
        px, py, dx, dy = {
            'L': (x-16, coord, 16, 0),
            'R': (x+w+16, coord, -16, 0),
            'T': (coord, y-12, 0, 12),
            'B': (coord, y+h+12, 0, -12),
        }[side]
        body.append(pin(key, px, py, dx, dy, label, 0, bool(label)))
        pins[key] = (px, py)
    body.extend(text(nx, ny, label, size, anchor='middle') for nx, ny, label, size in notes)
    value, description = specs[ref]
    lib(ref, value, x+w/2, y+h/2, body, pins, description, (x+w/2, y+title_offset))
    records = shapes[-1].split('#@$')
    # Mantener referencia y valor nativos. Los rótulos se dibujan sobre el fondo.
    for i in (1, 2):
        fields = records[i].split('~')
        fields[13] = '0'
        records[i] = '~'.join(fields)
    shapes[-1] = '#@$'.join(records)


def inline(ref, caption, x, y, w, h):
    part(ref, caption, x, y, w, h, [('1', 'L', y+h//2, ''), ('2', 'R', y+h//2, '')])


def pt(ref, key):
    return components[ref]['pins'][key]


def no_connect(ref, key):
    x, y = pt(ref, key)
    path = f'M {x-4} {y-4} L {x+4} {y+4} M {x+4} {y-4} L {x-4} {y+4}'
    shapes.append(f'O~{x}~{y}~{gid()}~{path}~{GROUND}~0')


def link(ref1, pin1, ref2, pin2, name=None, label_x=None):
    a, b = pt(ref1, pin1), pt(ref2, pin2)
    cable(*a, *b, name=name)
    if label_x is not None:
        tag(label_x, a[1], name)


shapes.extend([
    rect(0, 0, WIDTH, HEIGHT, 'none', fill='#FFFFFF'),
    text(40, 54, 'FOODSCAN | ESQUEMA DE CONEXIONES', 25, bold=True),
    text(40, 86, 'Equipo 10  /  ESP32-S3 + OV5640 (C)  /  Iluminación COB de 5 V', 13),
    text(2010, 54, 'ESQUEMA REV. 4  /  MODELO 3D REV. 3', 12, anchor='end', bold=True),
])
for x, color, label in [(40, P5, '5 V'), (175, P3, '3,3 V'), (340, GROUND, 'GND común'),
                        (560, SIGNAL, 'Señal / control'), (810, RETURN, 'LED- conmutado')]:
    shapes.extend([line([x, 116, x+36, 116], color, 2.5), text(x+46, 121, label, 10)])
shapes.append(text(1240, 121, 'Etiquetas iguales representan la misma red.', 10))

panel(40, 150, 875, 790, '01  CONTROL Y CÁMARA',
      'GPIO por nombre de placa. P1 por número de contacto. X indica terminal libre.')
panel(945, 150, 1065, 355, '02  ALIMENTACIÓN Y PROTECCIÓN',
      'C1-C2 en la placa de control. C3-C4 junto a la cámara.')
panel(945, 520, 1065, 250, '03  PESAJE',
      'Identificar los hilos de la celda por función. X3 permite retirar la repisa.')
panel(945, 785, 1065, 155, '04  PUERTA',
      'Al cerrar, COM se une a NO y GPIO1 lee 0. NC queda libre. X4 es enchufable.')
panel(40, 958, 1970, 375, '05  CUATRO TIRAS COB EN PARALELO',
      'GPIO42 alto activa Q1. Los cuatro retornos LED- llegan al drenador y la fuente de Q1 va a GND.')

# Cámara y GPIO de la revisión anterior.
control = [('5V', 302, '5V IN', '+5V'), ('GND', 340, 'GND', 'GND'),
           ('3V3', 378, '3V3 OUT', '+3V3'), ('IO4', 456, 'GPIO4 / DT', 'HX_DOUT'),
           ('IO2', 498, 'GPIO2 / SCK', 'HX_SCK'), ('IO1', 540, 'GPIO1 / puerta', 'DOOR_N'),
           ('IO42', 582, 'GPIO42 / luces', 'LED_EN')]
control_ports = [(key, 'L', y, title) for key, y, title, _ in control]
camera_ports = []
for i, row in enumerate(base['camera_header']):
    y = 300+26*i
    camera_ports.append((str(row['pin']), 'L', y, f"{row['pin']}: {row['signal']}"))
    if row['gpio'] is not None:
        control_ports.append((f"IO{row['gpio']}", 'R', y, f"GPIO{row['gpio']}"))
part('U1', 'ESP32-S3 DevKitC-1', 197, 221, 220, 571, control_ports, fill='#EAF3FA',
     notes=[(277, 635, 'N16R8', 13), (277, 660, '16 MB Flash', 9), (277, 682, '8 MB PSRAM', 9),
            (307, 754, 'Wi-Fi hacia app FoodScan', 10), (307, 775, 'USB para programación', 9)])
part('CAM1', 'Waveshare OV5640 (C)', 665, 221, 223, 571, camera_ports, fill='#EAF3FA')
for key, y, _, name in control:
    cable(62, y, *pt('U1', key), name=name)
    tag(62, y, name)
for row in base['camera_header']:
    key, gpio, name = str(row['pin']), row['gpio'], row['net']
    if gpio is not None:
        link('U1', f'IO{gpio}', 'CAM1', key, name)
    elif name:
        x, y = pt('CAM1', key)
        cable(520, y, x, y, name=name)
        tag(520, y, name)
    else:
        no_connect('CAM1', key)
shapes.extend([
    text(62, 828, 'CAM1: 17 conexiones externas por cable plano de hasta 10 cm.', 11, bold=True),
    text(62, 853, 'P1.18 / PWDN queda libre en el cable y unido a GND dentro del módulo.', 9),
    text(62, 877, 'La captura, la tara y el envío por Wi-Fi se controlan por firmware.', 9),
])

# J1 -> F1 -> SW1 -> X1. X1 aporta +5V y GND a las redes de la placa.
shapes.append(text(967, 218, 'Adaptador WODE WA-24-5  /  5 V CC, 4,8 A  /  centro positivo', 11, bold=True))
part('J1', 'Jack 5,5 x 2,1', 969, 234, 112, 145, [('CENTER', 'R', 289, '+'), ('SLEEVE', 'R', 365, '-')])
inline('F1', 'T3,15 A', 1165, 263, 110, 52)
inline('SW1', 'KCD1-102', 1330, 263, 132, 52)
part('X1', 'Bornera 2P', 1540, 234, 138, 145, [('1', 'L', 289, '1 / +5V'), ('2', 'L', 365, '2 / GND')],
     fill='#EDF3F7')
link('J1', 'CENTER', 'F1', '1', 'VIN_5V', 1102)
link('F1', '2', 'SW1', '1', 'VIN_FUSED')
link('SW1', '2', 'X1', '1', '+5V', 1484)
link('J1', 'SLEEVE', 'X1', '2', 'GND', 1120)
for cap, caption, x, w, y, high_y, low_y, supply in [
    ('C1', '470 uF / 16 V', 1745, 116, 305, 289, 365, '+5V'),
    ('C2', '100 nF', 1885, 100, 305, 289, 365, '+5V'),
    ('C3', '100 uF / 10 V', 1246, 156, 419, 402, 478, '+3V3'),
    ('C4', '100 nF', 1450, 146, 419, 402, 478, '+3V3'),
]:
    cx = x+w//2
    fill = '#FFF4EE' if supply == '+5V' else '#F4EFF9'
    part(cap, caption, x, y, w, 42, [('1', 'T', cx, ''), ('2', 'B', cx, '')], fill=fill, compact=True)
    cable(cx, high_y, *pt(cap, '1'), name=supply)
    cable(*pt(cap, '2'), cx, low_y, name='GND')
    if cap in {'C1', 'C3'}:
        shapes.append(text(x+8, y+16, '+', 10, bold=True))
for x, end, high, low, supply, first_cap in [
    (1708, 1935, 289, 365, '+5V', 1803),
    (969, 1523, 402, 478, '+3V3', 1324),
]:
    cable(x, high, end, high, name=supply)
    tag(x, high, supply)
    cable(x, low, end, low, name='GND')
    tag(x, low, 'GND')
    dot(first_cap, high)
    dot(first_cap, low)
shapes.extend([
    text(1630, 436, '3,3 V regulados por U1', 11, bold=True),
    text(1630, 459, 'Alimenta CAM1, HX711 y R13.', 9),
])

# Borneras de pesaje. El orden A- antes de A+ reproduce el modelo 3D.
weight_rows = (635, 663, 691, 719)
harness = [('VCC', '3V3', '+3V3'), ('GND', 'GND', 'GND'), ('DT', 'DT', 'HX_DOUT'), ('SCK', 'SCK', 'HX_SCK')]
cell = [('E+', 'E+', 'EXC_P'), ('E-', 'E-', 'EXC_N'), ('A-', 'S-', 'SIG_N'), ('A+', 'S+', 'SIG_P')]
part('X3', 'Enchufable 4P', 968, 575, 138, 158,
     [(str(i), 'R', y, f'{i} / {title}') for i, ((_, title, _), y) in enumerate(zip(harness, weight_rows), 1)],
     fill='#EDF3F7')
part('U2', 'HX711', 1230, 575, 140, 158,
     [(key, 'L', y, key) for (key, _, _), y in zip(harness, weight_rows)] +
     [(key, 'R', y, key) for (key, _, _), y in zip(cell, weight_rows)], fill='#EAF3FA')
part('X5', 'Tornillo 4P', 1526, 575, 154, 158,
     [(str(i), 'R', y, f'{i} / {key}') for i, ((key, _, _), y) in enumerate(zip(cell, weight_rows), 1)],
     fill='#EDF3F7')
part('LC1', 'Celda de 5 kg', 1820, 575, 164, 158,
     [(key, 'L', y, key) for (_, key, _), y in zip(cell, weight_rows)], fill='#EAF3FA')
for i, (key, _, name) in enumerate(harness, 1):
    link('X3', str(i), 'U2', key, name, 1126)
for i, (key, load_pin, name) in enumerate(cell, 1):
    x, y = pt('U2', key)
    cable(x, y, 1500, y, name=name)
    tag(1400, y, name)
    link('X5', str(i), 'LC1', load_pin, name, 1705)

# Puerta. R13 eleva DOOR_N y el microswitch la lleva a GND al cerrar.
inline('R13', '10 kohm', 1054, 852, 120, 48)
part('X4', '', 1400, 843, 145, 68, [('1', 'R', 876, '1 / DOOR_N'), ('2', 'R', 901, '2 / GND')],
     fill='#EDF3F7', compact=True)
part('SW2', 'Microswitch', 1795, 845, 188, 70,
     [('NO', 'L', 876, 'NO'), ('COM', 'L', 901, 'COM'), ('NC', 'R', 866, 'NC')], compact=True)
cable(967, 876, *pt('R13', '1'), name='+3V3')
tag(967, 876, '+3V3')
cable(*pt('R13', '2'), 1358, 876, name='DOOR_N')
tag(1210, 876, 'DOOR_N')
link('X4', '1', 'SW2', 'NO', 'DOOR_N', 1640)
link('X4', '2', 'SW2', 'COM', 'GND', 1640)
no_connect('SW2', 'NC')

# Un solo Q1 conmuta el retorno de las cuatro tiras COB de dos hilos.
inline('R14', '100 ohm', 155, 1085, 110, 52)
part('Q1', 'AO3400A', 388, 1048, 177, 155, [('1', 'L', 1111, '1 G'), ('2', 'B', 478, ''), ('3', 'R', 1111, '3 D')],
     fill='#EAF3FA', notes=[(477, 1167, 'Control de luces', 10), (491, 1196, '2 S', 9)])
part('R15', '100 kohm', 249, 1180, 110, 47, [('1', 'T', 304, ''), ('2', 'B', 304, '')])
cable(62, 1111, *pt('R14', '1'), name='LED_EN')
tag(62, 1111, 'LED_EN')
link('R14', '2', 'Q1', '1')
cable(304, 1111, *pt('R15', '1'))
dot(304, 1111)
cable(*pt('R15', '2'), 304, 1264, 478, 1264, *pt('Q1', '2'), name='GND')
tag(387, 1264, 'GND')
cable(*pt('Q1', '3'), 617, 1111, name='LED-')
tag(617, 1111, 'LED-', 'end')

strip_pairs = {'X2A': ('LED1', 'LED3'), 'X2B': ('LED2', 'LED4')}
for side, block, connector, strip_x in [('IZQUIERDO', 638, 'X2A', 1040), ('DERECHO', 1325, 'X2B', 1727)]:
    shapes.extend([rect(block, 1020, 663, 268, '#CFDCE5', fill='#F7FAFC'),
                   text(block+16, 1047, f'LADO {side} / {connector}', 11, bold=True)])
    rows = (1116, 1140, 1196, 1220)
    part(connector, 'Tornillo 4P / 5,08 mm', block+22, 1061, 213, 184,
         [(str(i), 'R', y, f'{i} / {name}') for i, (y, name) in enumerate(zip(rows, ('+5V', 'LED-', '+5V', 'LED-')), 1)],
         fill='#EDF3F7')
    for slot, ref in enumerate(strip_pairs[connector]):
        pos, neg = rows[2*slot:2*slot+2]
        top = pos-27
        part(ref, corners[ref], strip_x, top, 231, 76,
             [('+', 'L', pos, '+'), ('-', 'L', neg, '-')], fill='#FFF8E4',
             notes=[(strip_x+115, top+67, 'COB 5 V / 200 mm / 4000 K', 9)])
        label_x = block+267
        link(connector, str(2*slot+1), ref, '+', '+5V', label_x)
        link(connector, str(2*slot+2), ref, '-', 'LED-', label_x)

shapes.extend([
    text(40, 1372, 'Modelo 3D: a936fb1 / modelo-3d-v3. Borneras numeradas según este plano.', 10, bold=True),
    text(40, 1397, 'Antes del montaje: confirmar polaridad del jack, corriente de las tiras y capacidad de Q1, F1 y borneras.', 10),
    text(2010, 1397, '12 NOV 2026  /  A3 horizontal  /  Hoja 1 de 1', 10, anchor='end'),
])

# Verificar los pines a partir de la geometría, no de los nombres usados al dibujar.
parent = {}
points = {(x, y) for x, y, _ in labels}
for component in components.values():
    points.update(map(tuple, component['pins'].values()))
for path in wires:
    points.update(path)
for path in wires:
    for a, b in zip(path, path[1:]):
        assert a != b and (a[0] == b[0] or a[1] == b[1]), ('Tramo inválido', a, b)
        for x, y in points:
            if ((a[0] == b[0] == x and min(a[1], b[1]) <= y <= max(a[1], b[1]))
                    or (a[1] == b[1] == y and min(a[0], b[0]) <= x <= max(a[0], b[0]))):
                union(a, (x, y))
anchors = {}
for x, y, name in labels:
    if name in anchors:
        union((x, y), anchors[name])
    anchors[name] = (x, y)
groups = defaultdict(set)
for ref, component in components.items():
    for key, location in component['pins'].items():
        groups[find(tuple(location))].add(f'{ref}.{key}')

removed = {f'{prefix}{i}' for prefix in ('R', 'D') for i in range(1, 13)}
expected = {}
for network in base['netlist']:
    pins = {pin_id for pin_id in network['pins'] if pin_id.split('.')[0] not in removed}
    if pins:
        expected[network['name']] = pins
expected['LED-'] = expected.pop('LED_RETURN')
expected['VIN_FUSED'] = expected.pop('Net_25')
expected['LED_GATE'] = expected.pop('Net_31')
additions = {
    '+5V': {'X1.1', 'X2A.1', 'X2A.3', 'X2B.1', 'X2B.3', *(f'{ref}.+' for ref in corners)},
    'LED-': {'X2A.2', 'X2A.4', 'X2B.2', 'X2B.4', *(f'{ref}.-' for ref in corners)},
    'GND': {'X1.2', 'X3.2', 'X4.2'},
    '+3V3': {'X3.1'},
    'HX_DOUT': {'X3.3'},
    'HX_SCK': {'X3.4'},
    'DOOR_N': {'X4.1'},
    'EXC_P': {'X5.1'},
    'EXC_N': {'X5.2'},
    'SIG_N': {'X5.3'},
    'SIG_P': {'X5.4'},
}
for name, pins in additions.items():
    expected[name].update(pins)
assert len(components) == 26 and sum(len(p['pins']) for p in components.values()) == 106
assert {frozenset(g) for g in groups.values()} == {frozenset(g) for g in expected.values()}
assert all(groups[find((x, y))] == expected[name] for x, y, name in labels)

doc = {
    'head': {'docType': '1', 'editorVersion': '6.5.61', 'newgId': True, 'hasIdFlag': True,
             'uuid': uuid.uuid5(uuid.NAMESPACE_URL, STEM).hex, 'x': '0', 'y': '0',
             'c_para': {'Prefix Start': '1'}},
    'canvas': f'CA~{WIDTH}~{HEIGHT}~#FFFFFF~none~#CCCCCC~5~{WIDTH}~{HEIGHT}~line~5~pixel~5~0~0',
    'shape': shapes,
    'BBox': {'x': 0, 'y': 0, 'width': WIDTH, 'height': HEIGHT},
    'colors': {},
    'title': STEM,
}
report = {
    'status': 'PASS',
    'revision': 4,
    'date': DATE,
    'model_commit': MODEL_COMMIT,
    'components': len(components),
    'pins': sum(len(component['pins']) for component in components.values()),
    'nets': len(groups),
    'validation': 'Conectividad de pines, segmentos y etiquetas. Incluye dos pines intencionalmente libres.',
    'netlist': [{'name': name, 'pins': sorted(pins)} for name, pins in expected.items()],
}
(OUT / f'{STEM}.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding='utf-8')
(OUT / 'Verificacion_conexiones_v4.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">'
svg += ''.join(svg_shape(shape) for shape in shapes) + '</svg>'
(OUT / f'{STEM}.svg').write_text(svg, encoding='utf-8')

# Usar el mismo exportador vectorial que la revisión anterior.
PDF_OUT.mkdir(parents=True, exist_ok=True)
exporter = ROOT / 'exportar_pdf.py'
source = exporter.read_text(encoding='utf-8')
source = source.replace('FoodScan_Esquematico_v1', STEM).replace('1620', str(WIDTH)).replace('1145', str(HEIGHT))
source = source.replace(f"out=ROOT/'EasyEDA'/'{STEM}.pdf'", f"out=Path({str(PDF_OUT / (STEM + '.pdf'))!r})")
source = source.replace('Interconexion ESP32-CAM, HX711, celda de carga, puerta e iluminacion',
                        'FoodScan v4: cuatro tiras COB, borneras y modelo mecanico v3')
exec(compile(source, str(exporter), 'exec'), {'__file__': str(exporter)})
print(json.dumps({k: report[k] for k in ('status', 'components', 'pins', 'nets')}))
