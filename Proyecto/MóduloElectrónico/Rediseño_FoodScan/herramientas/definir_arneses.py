"""Genera la lista de cables físicos y la contrasta con la matriz eléctrica."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Las referencias U1.1–22 siguen J1.1–22 del DevKit. U1.23–44
# siguen J3.22–1. Los empalmes se realizan en el lado del arnés.
HARNESSES = {
    "Entrada": [
        ("PS1.1", "J13.1"), ("PS1.2", "J13.2"), ("J13.1", "F1.1"),
        ("F1.2", "SW1.1"), ("SW1.2", "J1.1"), ("J13.2", "J1.2"),
    ],
    "COB": [
        (f"J{connector}.{pin}", f"LED{led}.{pole}")
        for connector, first in [(2, 1), (3, 3)]
        for pin, (led, pole) in enumerate(
            [(first, 1), (first, 2), (first + 1, 1), (first + 1, 2)], 1)
    ],
    "ESP32 alimentación y control": [
        (f"J6.{pin}", f"U1.{esp}") for pin, esp in enumerate([21, 22, 1, 39, 4, 44], 1)
    ],
    "Pesaje lado kit": [(f"J4.{pin}", f"U3.{pin}") for pin in range(1, 5)],
    "Pesaje lado ESP32": [
        (f"J9.{pin}", f"U1.{esp}") for pin, esp in enumerate([23, 41, 40], 1)
    ],
    "Cámara alimentación": [("J5.1", "CAM1.1"), ("J5.2", "CAM1.2")],
    "Cámara DVP y SCCB": [
        (f"CAM1.{pin}", f"U1.{esp}") for pin, esp in [
            (3, 15), (4, 12), (5, 19), (6, 20), (7, 27), (9, 11), (10, 10),
            (11, 9), (12, 18), (13, 17), (14, 16), (15, 7), (16, 6),
        ]
    ] + [("CAM1.2", "U1.23")],
    "OLED lado pantalla": [(f"J7.{pin}", f"DS1.{pin}") for pin in range(1, 8)],
    "OLED lado ESP32": [
        (f"J8.{pin}", f"U1.{esp}") for pin, esp in enumerate([24, 36, 37, 38, 28, 29], 1)
    ],
    "Puerta": [("J10.1", "SW2.1"), ("J10.2", "SW2.2"), ("SW2.1", "R9.1"), ("SW2.2", "R9.2")],
    "Pulsadores": [("J11.1", "SW3.1"), ("J11.2", "SW4.1"), ("J11.3", "SW3.2"), ("J11.3", "SW4.2")],
    "Pulsadores lado ESP32": [("J12.1", "U1.5"), ("J12.2", "U1.8")],
}


def main():
    with (ROOT / "Matriz_conexiones.csv").open(encoding="utf-8", newline="") as source:
        terminal = {f"{row['ref']}.{row['pin']}": row for row in csv.DictReader(source)}
    covered = set()
    with (ROOT / "Matriz_arneses.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(("arnés", "origen", "pin origen", "destino", "pin destino", "red"))
        for harness, cables in HARNESSES.items():
            for start, end in cables:
                a, b = terminal[start], terminal[end]
                if not a["net"] or a["net"] != b["net"]:
                    raise ValueError(f"Cable incompatible: {start} → {end}")
                covered.update((start, end))
                writer.writerow((harness, start, a["pin_name"], end, b["pin_name"], a["net"]))
    required = {pin for pin, row in terminal.items()
                if row["net"] and (not row["section"].startswith("01 ") or row["ref"].startswith("J"))}
    if covered != required:
        raise ValueError(f"Terminales sin arnés: {sorted(required - covered)}. Extras: {sorted(covered - required)}.")
    print(f"{sum(map(len, HARNESSES.values()))} conexiones físicas, {len(covered)} terminales de arnés")


if __name__ == "__main__":
    main()
