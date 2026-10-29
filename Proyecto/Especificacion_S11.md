# FoodScan - Especificación técnica para el Taller 11

Equipo 10 · 28 de octubre de 2026 · Propuesta conceptual.

La caja registra la masa de una porción y captura su fotografía. La ESP32-CAM
comunica los datos por Wi-Fi a una aplicación con procesamiento en una laptop.
La cámara ayuda a identificar el alimento; los nutrientes se calculan usando
una referencia nutricional y la masa medida.

## Componentes representados

| ID | Elemento |
|---|---|
| E01 / U1 | ESP32-CAM AI-Thinker con OV2640 y PSRAM |
| E02 / LC1 | Celda de carga de barra de 5 kg, envolvente aproximada 75 × 12 × 12 mm |
| E03 / U2 | HX711 compatible con alimentación de 3.3 V |
| E04 / SW2 | Microswitch de puerta KW11-3Z-3F, COM-NO |
| E05 / D1-D12 | 12 LED blancos de 5 mm |
| E06 / R1-R12 | 12 resistencias de 100 Ω, una por LED |
| E07 / R13 | Resistencia de 10 kΩ para entrada de puerta |
| E08 | Adaptador externo de 5 V / 2.4 A |
| E09 / J1 | Jack DC de panel de 5.5 × 2.1 mm, centro positivo |
| E10 / SW1 | Interruptor general de alimentación |
| E11 / C1 | Condensador de 470 µF / 16 V |
| E12 / C2 | Condensador de 100 nF |
| E13 + E14 / F1 | Fusible de 1.5 A, 5 × 20 mm, y portafusible |
| E15 | Placas universales de distribución e iluminación |

## Conexiones

| Origen | Destino |
|---|---|
| Fuente 5 V | Jack → fusible → interruptor → distribución de 5 V |
| 5 V y GND | ESP32-CAM, condensadores e iluminación |
| ESP32-CAM 3V3 y GND | Alimentación HX711 |
| GPIO13 | HX711 DOUT / DT |
| GPIO14 | HX711 SCK |
| GPIO15 | Detector de puerta, con resistencia de 10 kΩ a 3.3 V y COM-NO a GND |
| HX711 E+ / E- | Excitación de celda |
| HX711 A+ / A- | Señal de celda |
| Iluminación | 12 ramas paralelas: 5 V → 100 Ω → LED → GND |

Todas las masas comparten GND. La microSD queda sin uso porque comparte los
GPIO del proyecto. El adaptador externo y la base USB se usan por separado.
Los módulos se representan por sus terminales funcionales; no es un diseño PCB.

## Montaje mecánico

- Cuerpo propuesto: 320 ancho × 320 fondo × 350 alto, en mm.
- Paneles de MDF blanco de 3; base y plataforma con dos capas para obtener 6.
- Plataforma de 220 × 220, con holgura lateral nominal de 47.
- Un extremo de la celda queda fijo a la base; el otro sostiene la plataforma.
- Topes con holgura nominal de 1 respecto de la plataforma en reposo.
- Plato de referencia Ø200; plano interior Z = 48.
- Lente hacia abajo en Z = 318: distancia nominal de 270 al plano del plato.
- Tres paneles de cuatro LED con difusores, puerta frontal y detector en el marco.
- HX711 y conexiones protegidos al fondo; adaptador de corriente externo.

Las dimensiones principales se toman de la propuesta de montaje del equipo
(`componentes.md`, versión 1.1, secciones 2.1 y 5). El CAD precisa la distribución
y los soportes como primera maqueta. Las medidas comerciales, taladros y óptica
deben confirmarse con las piezas reales antes de fabricar.
