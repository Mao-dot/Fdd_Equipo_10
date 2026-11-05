# FoodScan: lista de componentes del esquema v2

**Equipo 10 · Revisión 2 · 4 de noviembre de 2026**

Corresponde al [esquemático editable v2](EasyEDA/FoodScan_Esquematico_v2.json), su [PDF](EasyEDA/FoodScan_Esquematico_v2.pdf) y la [lista general de compra](Componentes_v2.md). Enumera los símbolos de interconexión y sus valores; no acredita compras o montaje físico. El modelo 3D no forma parte de esta corrección.

## Componentes representados

| Referencia | Cantidad | Componente y valor | ID de compra |
|---|---:|---|---|
| U1 | 1 | Placa ESP32-S3-DevKitC-1 N16R8, módulo ESP32-S3-WROOM-1, 16 MB Flash y 8 MB PSRAM | E01 |
| CAM1 | 1 | Waveshare OV5640 Camera Board (C), SKU 13802, 5 MP, autofocus, DVP de 8 bits, 3.3 V | E19 |
| U2 | 1 | Módulo HX711 compatible con alimentación y lógica de 3.3 V | E03 |
| LC1 | 1 | Celda de carga de barra de 5 kg, puente completo y cuatro hilos | E02 |
| SW1 | 1 | Interruptor general KCD1-102, ON/OFF SPST | E10 |
| SW2 | 1 | Microswitch KW11-3Z-3F SPDT, palanca y rueda | E04 |
| J1 | 1 | Jack DC hembra de panel, 5.5 × 2.1 mm, centro positivo | E09 |
| F1 | 1 | Fusible de vidrio de 1.5 A, 5 × 20 mm | E13 |
| C1 | 1 | Electrolítico de 470 µF / 16 V, sobre +5V | E11 |
| C2 | 1 | Cerámico de 100 nF / ≥16 V, sobre +5V | E12 |
| C3 | 1 | Electrolítico de 100 µF / 10 V, junto a cámara, sobre +3V3 | E23 |
| C4 | 1 | Cerámico de 100 nF / ≥16 V, junto a cámara, sobre +3V3 | E24 |
| R1–R12 | 12 | Resistencia de 100 Ω, 1/4 W, 5 %; una por LED | E06 |
| R13 | 1 | Resistencia de 10 kΩ, 1/4 W; entrada de puerta | E07 |
| R14 | 1 | Resistencia de 100 Ω, 1/4 W; compuerta de Q1 | E21 |
| R15 | 1 | Resistencia de 100 kΩ, 1/4 W; compuerta de Q1 a GND | E22 |
| D1–D12 | 12 | LED blanco straw hat de 5 mm, aproximadamente 6000 K; Vf 3.2–3.4 V | E05 |
| Q1 | 1 | MOSFET AO3400A de canal N, SOT-23, control con lógica de 3.3 V | E20 |

**Total: 40 componentes representados.** Los tres paneles conservan cuatro ramas resistencia–LED cada uno: panel 1 = R1/D1 a R4/D4; panel 2 = R5/D5 a R8/D8; panel 3 = R9/D9 a R12/D12. Sus retornos se conmutan juntos mediante Q1.

## Accesorios del sistema

| Cantidad | Accesorio | ID de compra |
|---:|---|---|
| 1 | Adaptador regulado externo de 5 V / 2.4 A, 5.5 × 2.1 mm, centro positivo | E08 |
| 1 | Portafusible de 5 × 20 mm para F1 | E14 |
| 4 | Placas universales de montaje: distribución/control y tres paneles LED | E15 |
| 1 juego | Jumpers y cables de prueba compatibles con las placas recibidas | E16 |
| 1 lote | Cable AWG22, pines y conectores internos | E17 |
| 1 | Cable USB de datos compatible con U1, para programación y diagnóstico | E18 |
| 1 conjunto | Conector/cableado entre P1 de 18 terminales de CAM1 y U1: 17 conexiones externas utilizadas | E25 |
| 1 | Adaptador SOT-23 o placa de montaje para Q1 | E26 |
| 3 | Difusores de los paneles LED | A01 |
| 1 lote | Separadores, fijaciones y aislantes de placas | A02 |

El portafusible y los adaptadores de montaje no añaden símbolos a la hoja. CAM1 es un módulo comercial completo; su electrónica interna no se desglosa como compras adicionales. La base programadora MB del antiguo diseño AI-Thinker se sustituye por el USB de U1. El flash de cámara queda apagado.

## Conexiones de la revisión 2

- **Alimentación:** J1 → F1 → SW1 → +5V. U1 recibe +5V; su salida +3V3 alimenta CAM1, U2 y la entrada de puerta. C1/C2 desacoplan +5V; C3/C4 se colocan cerca de la entrada +3V3 de CAM1. GND común.
- **Luces:** +5V → resistencia individual de 100 Ω → LED → Q1.D. Q1.S → GND. GPIO42 → R14 → Q1.G; R15 entre Q1.G y GND.
- **Puerta:** GPIO1 y R13 a +3V3; SW2.NO a esa entrada, SW2.COM a GND, SW2.NC libre. Cerrada y accionada = nivel bajo.
- **Pesaje:** U2.DT → GPIO4; U2.SCK → GPIO2. Celda a E+/E− y A+/A−; identificar hilos por ficha o medición.
- **Cámara P1:** 1=+3V3; 2=GND; 3/SIOC→GPIO9; 4/SIOD→GPIO8; 5/VSYNC→GPIO13; 6/HREF→GPIO14; 7/PCLK→GPIO21; 8/XCLK→GPIO15; 9/Y9(D7)→GPIO18; 10/Y8(D6)→GPIO17; 11/Y7(D5)→GPIO16; 12/Y6(D4)→GPIO12; 13/Y5(D3)→GPIO11; 14/Y4(D2)→GPIO10; 15/Y3(D1)→GPIO7; 16/Y2(D0)→GPIO6; 17/RESET activo bajo→GPIO5.
- **CAM1.P1.18/PWDN:** sin conexión externa; existe un puente interno de 0 Ω a GND en la Waveshare (C). No conducir desde un GPIO sin revisar/modificar el módulo. Reposo por SCCB pendiente de verificar en firmware.
- **SCCB:** la placa de cámara ya incorpora pull-ups de SIOC/SIOD; no se duplican externamente.
- **Pines reservados:** no se usan GPIO35/36/37 del N16R8, USB GPIO19/20, UART GPIO43/44 ni straps GPIO0/3/45/46. GPIO42 se destina a las luces y no a JTAG externo.

Los bloques muestran terminales de módulos. La numeración P1 corresponde al conector de la cámara y debe contrastarse con su orientación física. El conector tiene 18 terminales; se realizan 17 conexiones externas, pues P1.18/PWDN queda libre externamente. No se trasladan GPIO de la antigua ESP32-CAM AI-Thinker a esta placa.

La DevKitC-1 oficial usa un regulador SGM2212 de 800 mA nominales **compartidos entre la ESP32, la cámara, el HX711 y las demás cargas de +3V3**. No son 800 mA adicionales disponibles para la cámara; se comprobarán tensión y temperatura con el módulo recibido. Referencia: [esquema oficial de DevKitC-1 v1.1](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20220413.pdf).

## Funcionamiento y verificación

El ciclo conserva la tara del plato vacío al retirarlo, comprueba puerta cerrada/peso estable, enciende luces y obtiene foto y gramos de la misma medición. Las órdenes y datos usan Wi-Fi; la app existente consulta Gemini mediante Internet y calcula con su tabla nutricional. Al finalizar o fallar se apagan luces y U1 queda en espera; SW1 corta la alimentación general manualmente. El USB solo se usa para programar y diagnosticar.

La [verificación de conexiones v2](EasyEDA/Verificacion_conexiones_v2.json) comprueba el archivo y su lista de redes. No equivale a ERC oficial de EasyEDA ni prueba eléctrica. Se debe verificar con piezas reales la regulación de 3.3 V, autofocus, calentamiento, comunicación, control de luces, puerta y calibración/repetibilidad del pesaje. Una placa de terceros puede incorporar un regulador distinto; si se requiere uno dedicado, no se deben unir salidas de reguladores.

La app sí está implementada en [FoodScan/](https://github.com/Mao-dot/FoodScan/blob/main/README.md), carpeta excluida del Git del curso. Su backend [POST /api/analyze](https://github.com/Mao-dot/FoodScan/blob/main/app/api/analyze/route.ts) ya recibe `image` como Data URL base64, `totalGrams` entre 10 y 3000 g y `description` opcional, con cuerpo máximo de 3.000.000 bytes/caracteres. Gemini se consulta en el servidor; el motor de la app calcula con la tabla nutricional. La conexión de la ESP32 y los estados físicos siguen pendientes; `/api/status` informa configuración de Gemini, no estado de hardware. Esta revisión no modifica código ni credenciales.

Esta hoja no contiene huellas de PCB, ruteo ni Gerber. La versión anterior permanece en [FoodScan_Esquematico_v1.json](EasyEDA/FoodScan_Esquematico_v1.json). Las referencias técnicas, condiciones de compra y presupuesto se reúnen en [lista ampliada](Componentes_v2.md); esta BOM no presenta una cotización nueva.
