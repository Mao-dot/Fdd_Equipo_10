"""Fuente de la matriz de pines de FoodScan. Requiere solo Python."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PCB = "01 Placa auxiliar"
POWER = "02 Entrada e iluminación"
CAMERA = "03 ESP32 y cámara"
CONTROL = "04 Pesaje, pantalla y controles"
rows = []


def part(section, ref, model, pins, *, mpn="", note="", symbol=""):
    for number, name, net, *pin_type in pins:
        rows.append({
            "ref": ref, "model": model, "pin": str(number), "pin_name": name,
            "net": net, "section": section,
            "pin_type": pin_type[0] if pin_type else "Passive",
            "library_mpn": mpn, "footprint": "", "symbol": symbol, "note": note,
        })


def connector(ref, model, mpn, nets, note):
    part(PCB, ref, model, [
        (pin, net, net) for pin, net in enumerate(nets, 1)
    ], mpn=mpn, note=note)


def passive(ref, model, mpn, first, second, *, section=PCB, labels=("1", "2"), note=""):
    part(section, ref, model, [(1, labels[0], first), (2, labels[1], second)], mpn=mpn, note=note)


connector("J1", "1935161", "C3819953", ["5V_SW", "GND"], "Desde panel posterior F1 / SW1")
for ref, suffix in (("J2", "A"), ("J3", "B")):
    connector(ref, "1935187", "C3817931",
              ["5V_SW", "LED_RET_" + suffix] * 2,
              "Dos tiras COB; cada par tiene alimentación y retorno")
connector("J4", "B4B-XH-A(LF)(SN)", "C144395",
          ["GND", "3V3_AUX", "PESO_TX", "PESO_RX"], "Al Best Modules BMH12M205")
connector("J5", "B2B-XH-A(LF)(SN)", "C158012",
          ["3V3_AUX", "GND"], "Ramal de alimentación de cámara")
connector("J6", "B6B-XH-A(LF)(SN)", "C144397",
          ["5V_SW", "GND", "3V3_ESP", "LED_EN", "PUERTA_ADC", "GND"], "Al ESP32 J1 / J3")
connector("J7", "B7B-XH-A(LF)(SN)", "C144398",
          ["3V3_AUX", "GND", "OLED_DIN", "OLED_CLK", "OLED_CS_N", "OLED_DC", "OLED_RST_N"],
          "Al cable Waveshare de 7 contactos")
connector("J8", "B6B-XH-A(LF)(SN)", "C144397",
          ["GND", "OLED_DIN", "OLED_CLK", "OLED_CS_N", "OLED_DC", "OLED_RST_N"], "SPI desde ESP32")
connector("J9", "B3B-XH-A(LF)(SN)", "C144394",
          ["GND", "PESO_TX", "PESO_RX"], "UART hacia y desde ESP32")
connector("J10", "B2B-XH-A(LF)(SN)", "C158012",
          ["PUERTA_5V", "GND"], "Interruptor NC y R9 en el extremo del arnés")
connector("J11", "B3B-XH-A(LF)(SN)", "C144394",
          ["TARA_N", "CAPTURA_N", "GND"], "Dos pulsadores de panel")
connector("J12", "B2B-XH-A(LF)(SN)", "C158012",
          ["TARA_N", "CAPTURA_N"], "GPIO del ESP32 para pulsadores")

part(PCB, "U2", "R-78K3.3-1.0", [
    (1, "VIN", "5V_SW", "Power"), (2, "GND", "GND", "Power"),
    (3, "VOUT", "3V3_AUX", "Out"),
], mpn="R-78K3.3-1.0", note="3.3 V para cámara, OLED y pesaje")
passive("C1", "470 uF / 16 V", "C242145", "5V_SW", "GND", labels=("+", "-"))
passive("C2", "10 uF / 10 V", "C19702", "5V_SW", "GND")
passive("C3", "10 uF / 10 V", "C19702", "3V3_AUX", "GND")
passive("C4", "100 nF / 50 V", "C14663", "3V3_AUX", "GND")
passive("C5", "100 nF / 50 V", "C14663", "PUERTA_ADC", "GND")

for number, suffix in enumerate(("A", "B"), 1):
    gate = "LED_GATE_" + suffix
    part(PCB, f"Q{number}", "AO3400A", [
        (1, "G", gate, "In"), (2, "S", "GND"), (3, "D", "LED_RET_" + suffix),
    ], mpn="C20917", note="Un canal por dos tiras, hasta 1.2 A nominal")
    passive(f"R{number}", "100 ohm", "C22775", "LED_EN", gate)
    passive(f"R{number + 2}", "100 kohm", "C22936", gate, "GND")

passive("R5", "2.2 kohm", "C114662", "5V_SW", "PUERTA_5V")
passive("R6", "10 kohm", "C25804", "PUERTA_5V", "PUERTA_ADC")
passive("R7", "10 kohm", "C25804", "PUERTA_ADC", "GND")
passive("R8", "10 kohm", "C25804", "3V3_ESP", "TARA_N")
passive("R10", "10 kohm", "C25804", "3V3_ESP", "CAPTURA_N")

part(POWER, "PS1", "Adaptador 5 V CC / 4.8 A de referencia", [
    (1, "CENTRO +", "ADAPTADOR_5V", "Out"), (2, "MANGA -", "GND"),
], note="Salida SELV centro positivo; comprobar la unidad y el cable")
part(POWER, "J13", "Tensility 54-00406", [
    (1, "CENTRO", "ADAPTADOR_5V"), (2, "MANGA", "GND"),
], note="Jack de panel 5.5 x 2.1 mm")
passive("F1", "Schurter SPT 0001.2510, T4 A", "", "ADAPTADOR_5V", "5V_FUS",
        section=POWER, note="Portafusible Schurter FPG2 3101.0120; validar coordinación")
passive("SW1", "NKK JWMW11RAA", "", "5V_FUS", "5V_SW", section=POWER,
        note="Balancín SPST, corte del positivo")
for number, suffix in enumerate(("A", "A", "B", "B"), 1):
    passive(f"LED{number}", "COB 5 V / 4000 K / 200 mm", "", "5V_SW", "LED_RET_" + suffix,
            section=POWER, labels=("+", "-"))

left_header = ["3V3", "3V3", "RST", 4, 5, 6, 7, 15, 16, 17, 18, 8, 3, 46,
               9, 10, 11, 12, 13, 14, "5V", "GND"]
right_header = ["GND", 43, 44, 1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45,
                48, 47, 21, 20, 19, "GND", "GND"]
esp_gpio = {
    1: "PESO_TX", 2: "PESO_RX", 4: "PUERTA_ADC", 5: "TARA_N", 15: "CAPTURA_N",
    6: "CAM_D0", 7: "CAM_D1", 8: "CAM_SDA", 9: "CAM_SCL", 10: "CAM_D2",
    11: "CAM_D3", 12: "CAM_D4", 13: "CAM_VSYNC", 14: "CAM_HREF",
    16: "CAM_D5", 17: "CAM_D6", 18: "CAM_D7", 21: "CAM_PCLK",
    39: "OLED_DIN", 40: "OLED_CLK", 41: "OLED_CS_N", 47: "OLED_DC",
    48: "OLED_RST_N", 42: "LED_EN",
}
esp_pins = []
for index, name in enumerate(left_header + list(reversed(right_header)), 1):
    if isinstance(name, int):
        esp_pins.append((index, f"GPIO{name}", esp_gpio.get(name, ""), "I/O"))
    else:
        net = {1: "3V3_ESP", 21: "5V_SW", 22: "GND", 23: "GND", 24: "GND", 44: "GND"}.get(index, "")
        esp_pins.append((index, name, net, "Power" if name != "RST" else "In"))
part(CAMERA, "U1", "ESP32-S3-DevKitC-1-N16R8 v1.1", esp_pins,
     note="Pines 1-22 = J1.1-22; pines 23-44 = J3.22-1")

camera_pins = [
    ("3.3V", "3V3_AUX", "Power"), ("GND", "GND", "Power"),
    ("SCL", "CAM_SCL", "In"), ("SDA", "CAM_SDA", "I/O"),
    ("VSYNC", "CAM_VSYNC", "Out"), ("HREF", "CAM_HREF", "Out"),
    ("PCLK", "CAM_PCLK", "Out"), ("XC", "", "In"),
] + [(f"DATA{bit + 2}", f"CAM_D{bit}", "Out") for bit in range(7, -1, -1)] + [
    ("RESET_N", "", "In"), ("PWDN", "", "In"),
]
part(CAMERA, "CAM1", "Adafruit OV5640 5838", [
    (i, *pin) for i, pin in enumerate(camera_pins, 1)
], note="JP2 de 2x9; XCLK a INT 24 MHz; cerrar VM para autofoco")

part(CONTROL, "U3", "Best Modules BMH12M205", [
    (1, "GND", "GND", "Power"), (2, "VDD", "3V3_AUX", "Power"),
    (3, "TXD", "PESO_TX", "Out"), (4, "RXD", "PESO_RX", "In"),
], note="UART 38400 8N1; tara por comando; celda interna del conjunto")
part(CONTROL, "DS1", "Waveshare 25742 / SSD1309", [
    (1, "VCC", "3V3_AUX", "Power"), (2, "GND", "GND", "Power"),
    (3, "DIN", "OLED_DIN", "In"), (4, "CLK", "OLED_CLK", "In"),
    (5, "CS_N", "OLED_CS_N", "In"), (6, "DC", "OLED_DC", "In"),
    (7, "RST_N", "OLED_RST_N", "In"),
], note="SPI de fábrica; cable OEM de 7 contactos")
passive("SW2", "Panasonic ASQ10228, NC", "", "PUERTA_5V", "GND", section=CONTROL,
        note="La puerta cerrada debe accionar el detector y abrir el contacto")
passive("R9", "2.2 kohm", "C114662", "PUERTA_5V", "GND", section=CONTROL,
        note="Montar junto al microswitch, al final del arnés")
passive("SW3", "Adafruit 1505, Tara", "", "TARA_N", "GND", section=CONTROL)
passive("SW4", "Adafruit 1505, Captura", "", "CAPTURA_N", "GND", section=CONTROL)


if __name__ == "__main__":
    with (ROOT / "Matriz_conexiones.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
