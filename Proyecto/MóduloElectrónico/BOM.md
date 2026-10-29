# Lista de componentes del esquema FoodScan

Revisión 1.0, 22/10/2026. Valores tomados de `componentes.md` versión 1.1.
Se enumeran los componentes instalados, sin volver a cotizar los precios.

| Referencia | Cantidad | Componente / valor | ID en componentes.md |
|---|---:|---|---|
| U1 | 1 | ESP32-CAM formato AI-Thinker con OV2640 y PSRAM | E01 |
| U2 | 1 | Módulo HX711 compatible con alimentación de 3.3 V | E03 |
| LC1 | 1 | Celda de carga de 5 kg, barra, puente completo, 4 hilos | E02 |
| SW1 | 1 | Interruptor general KCD1-102, ON/OFF SPST | E10 |
| SW2 | 1 | Microswitch KW11-3Z-3F, SPDT, palanca y rueda | E04 |
| J1 | 1 | Jack DC de panel 5.5 × 2.1 mm, centro positivo | E09 |
| F1 | 1 | Fusible de vidrio de 1.5 A, 5 × 20 mm, con portafusible | E13 + E14 |
| C1 | 1 | Condensador electrolítico de 470 µF / 16 V | E11 |
| C2 | 1 | Condensador cerámico de 100 nF / ≥16 V | E12 |
| R1–R12 | 12 | Resistencia de 100 Ω, 1/4 W, 5 %; una por LED | E06 |
| R13 | 1 | Resistencia de 10 kΩ, 1/4 W | E07 |
| D1–D12 | 12 | LED blanco straw hat de 5 mm, 6000 K; Vf 3.2–3.4 V | E05 |

**Total: 34 componentes representados**. El portafusible es un accesorio de F1,
no un símbolo adicional.

Accesorios del sistema: adaptador externo de 5 V / 2.4 A (E08), base programadora
MB incluida en E01, cableado, conectores y montaje según el presupuesto original.
El adaptador se conecta a J1; la base MB se utiliza por separado para programar.

Los paneles de iluminación se agrupan así: panel 1 = R1/D1 a R4/D4;
panel 2 = R5/D5 a R8/D8; panel 3 = R9/D9 a R12/D12.

Los módulos y piezas de panel no tienen huellas asignadas. Para fabricar una PCB
hay que seleccionar los conectores, sus medidas y las huellas de las piezas reales.
