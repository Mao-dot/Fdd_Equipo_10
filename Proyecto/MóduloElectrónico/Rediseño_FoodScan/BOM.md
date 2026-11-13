# Lista de materiales de FoodScan

Revisión A para prototipo. Las referencias de la placa auxiliar corresponden a la PCB de 60 × 65 mm. Los módulos comerciales conservan sus propias tarjetas y se conectan con los [arneses indicados](Matriz_arneses.csv).

| Referencias | Cant. | Fabricante y número de parte | Fuente |
| --- | ---: | --- | --- |
| J1 | 1 | Phoenix Contact 1935161, 2 vías, 5,00 mm | [LCSC C3819953](https://www.lcsc.com/product-detail/C3819953.html) |
| J2, J3 | 2 | Phoenix Contact 1935187, 4 vías, 5,00 mm | [Ficha de Phoenix Contact](https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-pt-15-4-50-h-1935187) · [LCSC C3817931](https://www.lcsc.com/product-detail/C3817931.html) |
| J5, J10, J12 | 3 | JST B2B-XH-A(LF)(SN), 2 vías, 2,50 mm | [LCSC C158012](https://www.lcsc.com/product-detail/C158012.html) |
| J9, J11 | 2 | JST B3B-XH-A(LF)(SN), 3 vías, 2,50 mm | [LCSC C144394](https://www.lcsc.com/product-detail/C144394.html) |
| J4 | 1 | JST B4B-XH-A(LF)(SN), 4 vías, 2,50 mm | [LCSC C144395](https://www.lcsc.com/product-detail/C144395.html) |
| J6, J8 | 2 | JST B6B-XH-A(LF)(SN), 6 vías, 2,50 mm | [LCSC C144397](https://www.lcsc.com/product-detail/C144397.html) |
| J7 | 1 | JST B7B-XH-A(LF)(SN), 7 vías, 2,50 mm | [LCSC C144398](https://www.lcsc.com/product-detail/C144398.html) |
| U2 | 1 | RECOM R-78K3.3-1.0, convertidor 3,3 V / 1 A, SIP3 | [Ficha y CAD OEM](https://recom-power.com/en/products/switching-regulators/switching-regulators-sip/rec-p-R-78K3.3-1.0.html) |
| Q1, Q2 | 2 | AOS AO3400A, MOSFET N, SOT-23 | [LCSC C20917](https://www.lcsc.com/product-detail/C20917.html) |
| C1 | 1 | Panasonic EEUFR1C471, 470 µF, 16 V, radial Ø8 mm, paso 3,5 mm | [LCSC C242145](https://www.lcsc.com/product-detail/C242145.html) |
| C2, C3 | 2 | Samsung CL10A106KP8NNNC, 10 µF, 10 V, 0603 | [LCSC C19702](https://www.lcsc.com/product-detail/C19702.html) |
| C4, C5 | 2 | Yageo CC0603KRX7R9BB104, 100 nF, 50 V, 0603 | [LCSC C14663](https://www.lcsc.com/product-detail/C14663.html) |
| R1, R2 | 2 | UNI-ROYAL 0603WAF1000T5E, 100 Ω, 0603 | [LCSC C22775](https://www.lcsc.com/product-detail/C22775.html) |
| R3, R4 | 2 | UNI-ROYAL 0603WAF100KT5E, 100 kΩ, 0603 | [LCSC C22936](https://www.lcsc.com/product-detail/C22936.html) |
| R5 | 1 | Yageo RC0603FR-072K2L, 2,2 kΩ, 0603 | [LCSC C114662](https://www.lcsc.com/product-detail/C114662.html) |
| R6, R7, R8, R10 | 4 | UNI-ROYAL 0603WAF1002T5E, 10 kΩ, 0603 | [LCSC C25804](https://www.lcsc.com/product-detail/C25804.html) |

La placa lleva dos capas de cobre, espesor nominal de 1,6 mm y cuatro agujeros Ø3,4 mm sin metalizar. Los agujeros H1–H4 se fijan con separadores M3 de 5 mm. El espesor de cobre y las condiciones térmicas se confirman con la prueba de carga antes de la orden.

| Referencias | Cant. | Componente externo |
| --- | ---: | --- |
| U1 | 1 | Espressif ESP32-S3-DevKitC-1-N16R8 v1.1. Confirmar revisión y cabeceras de la placa del equipo. |
| CAM1 | 1 | Adafruit 5838, breakout OV5640 con lente 120° y autofocus. Incluye la placa de interfaz JP2. |
| U3 | 1 | Best Modules BMH12M205, kit de pesaje Gen2 de 5 kg con UART y tara. |
| DS1 | 1 | Waveshare 25742, OLED blanco SSD1309 de 2,42″, con su cable de siete vías. Selección adoptada del CAD. |
| SW2 | 1 | Panasonic ASQ10228, contacto NC. Selección del CAD sujeta a la prueba de carga de contacto y de recorrido. |
| R9 | 1 | 2,2 kΩ ±1 %, instalada en paralelo con SW2 en el extremo del arnés. Puede usarse la referencia de R5 en una unión mecánicamente protegida o una versión axial de igual tolerancia. |
| SW3, SW4 | 2 | Adafruit 1505, pulsadores momentáneos NO para tara y captura. |
| LED1–LED4 | 4 | Tiras COB Ephycob de referencia, 5 V, 4000 K, 8 mm de ancho y 200 mm de largo. Confirmar potencia de la variante adquirida. |
| J13 | 1 | Tensility 54-00406, jack de panel 5,5 × 2,1 mm. |
| F1 | 1 | Schurter SPT 0001.2510, T4 A, 5 × 20 mm, con portafusible de panel FPG2 3101.0120. Dimensionamiento inicial sujeto a la coordinación con la fuente. |
| SW1 | 1 | NKK JWMW11RAA, SPST de panel. |
| PS1 | 1 | Adaptador regulado externo de referencia, 5 V CC, 4,8 A, centro positivo. Confirmar el modelo y la curva de protección del adaptador disponible. |

Preparar contrapartes JST XHP-2/3/4/6/7 y terminales XH compatibles con el calibre elegido. Los ramales hacia los módulos se adaptan a sus conectores OEM. Antes de crimpar, confirmar el lado de inserción, el orden del pin 1 y el conector real del BMH12M205. Verificar el calibre de entrada y COB según corriente medida y temperatura. [Ficha JST XH](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf) · [Fuentes, CAD y límites](fuentes/README.md) · [Procedimiento de banco](Verificacion_electrica.md)
