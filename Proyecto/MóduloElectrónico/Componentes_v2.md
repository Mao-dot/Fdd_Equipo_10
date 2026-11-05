# FoodScan: componentes electrónicos y funcionamiento

**Equipo 10 · Fundamentos de Diseño · Revisión 2 · 4 de noviembre de 2026**

Esta lista corresponde a la corrección del **esquemático y los componentes electrónicos**. La revisión del modelo 3D se realizará en otra etapa. Se utilizará una **ESP32-S3 N16R8**, una **Waveshare OV5640 Camera Board (C)** comprada aparte, pesaje con **celda de carga de 5 kg + HX711**, detector de puerta y doce LED con control de encendido.

Cámara, sensores y electrónica se instalan dentro de la máquina. Durante el uso, las órdenes, la foto y los gramos se comunican por **Wi-Fi**, sin un cable de datos a una laptop. La IA es Gemini mediante API y se conserva la app existente de FoodScan. La alimentación base del esquema es un adaptador externo de 5 V; una batería y su circuito de carga todavía no se han seleccionado.

## 1. Archivos de esta revisión

| Archivo | Contenido |
|---|---|
| [Esquemático editable v2](EasyEDA/FoodScan_Esquematico_v2.json) | Interconexión en EasyEDA Standard; importable en EasyEDA Pro. |
| [Esquemático PDF v2](EasyEDA/FoodScan_Esquematico_v2.pdf) | Vista del esquema corregido para revisar o presentar. |
| [BOM del esquema](BOM.md) | Referencias de símbolos y cantidades representadas. |
| [Verificación de conexiones v2](EasyEDA/Verificacion_conexiones_v2.json) | Comprobaciones locales del archivo y lista de redes. |
| [Esquemático anterior v1](EasyEDA/FoodScan_Esquematico_v1.json) | Referencia histórica de la ESP32-CAM AI-Thinker con OV2640. |

El esquema representa módulos y piezas de interconexión. No es una PCB fabricada ni una prueba del montaje. La app existente sí está en [FoodScan/](https://github.com/Mao-dot/FoodScan/blob/main/README.md), una carpeta excluida del Git del curso por `.gitignore`. Su código Next.js incluye el backend de Gemini y el motor nutricional; su README indica que la integración del prototipo de hardware todavía está pendiente. `Proyecto/MóduloSoftware/Código fuente/` contiene un README de organización y no sustituye a ese proyecto. Esta revisión no modifica la app.

## 2. Lista de componentes para comprar

### 2.1 Control, cámara y sensores

| ID | Referencia | Cantidad | Componente y especificación de compra | Función |
|---|---|---:|---|---|
| E01 | U1 | 1 | **Placa de desarrollo ESP32-S3-DevKitC-1 N16R8**, módulo ESP32-S3-WROOM-1, **16 MB Flash y 8 MB PSRAM**, USB de programación y pines accesibles. Sin cámara incluida. | Leer sensores, controlar luces, capturar imagen DVP y transmitir por Wi-Fi. |
| E19 | CAM1 | 1 | **Waveshare OV5640 Camera Board (C), SKU 13802**, 5 MP, autofocus, DVP de 8 bits, SCCB y **3.3 V**. | Fotografiar el plato dentro de la máquina. |
| E02 | LC1 | 1 | **Celda de carga de barra de 5 kg, puente completo y cuatro hilos**, referencia Naylamp SKU 000155 o unidad con ficha equivalente. | Medir la carga de plataforma, plato y comida. |
| E03 | U2 | 1 | **Módulo HX711 compatible con 3.3 V**, referencia Naylamp SKU 000147. | Amplificar y digitalizar la señal de la celda; obtener gramos después de calibrar. |
| E04 | SW2 | 1 | **Microswitch KW11-3Z-3F SPDT**, palanca y rueda, contactos COM/NO/NC. | Detectar puerta cerrada y habilitar captura. |

La cámara seleccionada es la **versión (C)** con autofocus. Su conector P1 tiene 18 terminales según la ficha del módulo, de los cuales se utilizan **17 conexiones externas** en esta revisión: P1.18/PWDN queda libre externamente. Se conecta por señales DVP/SCCB a U1 y no por USB a una computadora. El flash incorporado queda sin usar. **P1.18/PWDN no se conecta externamente**, porque el esquema del módulo incorpora un puente de 0 Ω hacia GND; no se debe conducir ese terminal desde un GPIO sin modificar y revisar el módulo. La gestión de reposo por registros SCCB se verificará en firmware.

### 2.2 Iluminación y control

| ID | Referencia | Cantidad | Componente y especificación de compra | Función |
|---|---|---:|---|---|
| E05 | D1–D12 | 12 | LED blanco tipo straw hat de 5 mm, aproximadamente 6000 K; **Vf 3.2–3.4 V**. | Tres paneles de cuatro LED para izquierda, derecha y fondo. |
| E06 | R1–R12 | 12 | Resistencia de **100 Ω, 1/4 W, 5 %**, una por LED. | Limitar corriente de cada rama. |
| E20 | Q1 | 1 | **MOSFET AO3400A**, canal N, SOT-23, montado en adaptador o pequeña placa. | Conectar/desconectar los retornos de las luces con señal de 3.3 V. |
| E21 | R14 | 1 | Resistencia de **100 Ω, 1/4 W**, para compuerta. | Limitar el pico de corriente de la compuerta. |
| E22 | R15 | 1 | Resistencia de **100 kΩ, 1/4 W**, entre compuerta y GND. | Mantener Q1 y luces apagados durante arranque o reinicio. |
| E07 | R13 | 1 | Resistencia de **10 kΩ, 1/4 W**, para entrada de puerta. | Fijar el estado lógico de la entrada. |

Las doce ramas van en paralelo y conservan una resistencia por LED. A 5 V, con el Vf indicado, la corriente calculada total es aproximadamente **0.19–0.22 A**; cada resistencia disipa menos de 0.04 W. El GPIO solamente gobierna Q1; no alimenta los LED. El AO3400A especifica resistencia de conducción a 2.5 V de compuerta y es apto para esta etapa con lógica de 3.3 V. Si se compra una placa equivalente, debe documentar operación con señal de 3.3 V y la corriente de carga prevista.

### 2.3 Alimentación, protección y desacoplo

| ID | Referencia | Cantidad | Componente y especificación de compra | Función |
|---|---|---:|---|---|
| E08 | Accesorio | 1 | Adaptador regulado **5 V DC / 2.4 A**, conector 5.5 × 2.1 mm, centro positivo; referencia WODE WA-12-5. | Alimentación base del prototipo. |
| E09 | J1 | 1 | Jack DC hembra de panel **5.5 × 2.1 mm**, centro positivo. | Entrada de alimentación. |
| E10 | SW1 | 1 | Interruptor **KCD1-102 ON/OFF SPST**, dos terminales. | Encendido y apagado general manual. |
| E13 | F1 | 1 | Fusible de vidrio **1.5 A, 5 × 20 mm**. | Protección del ramal de entrada. |
| E14 | Accesorio de F1 | 1 | Portafusible de **5 × 20 mm**. | Montaje y sustitución del fusible. |
| E11 | C1 | 1 | Electrolítico **470 µF / 16 V**. | Reserva local en +5V. |
| E12 | C2 | 1 | Cerámico **100 nF / ≥16 V**. | Desacoplo en +5V. |
| E23 | C3 | 1 | Electrolítico **100 µF / 10 V**. | Reserva local en +3V3 junto a la cámara. |
| E24 | C4 | 1 | Cerámico **100 nF / ≥16 V**. | Desacoplo en +3V3 junto a la cámara. |

U1 recibe +5V; su salida regulada +3V3 alimenta CAM1, U2 y la entrada de puerta. GND es común. La capacidad nominal de la fuente externa no sustituye la comprobación del regulador de 3.3 V de la placa recibida: las placas de terceros pueden usar componentes distintos de los oficiales. Se debe medir estabilidad de +5V y +3V3 durante autofocus, captura, luces y Wi-Fi. El flash de cámara queda apagado. Si la regulación real resulta insuficiente, se revisa una fuente de 3.3 V dedicada sin unir en paralelo salidas de reguladores.

El adaptador de 2.4 A y F1 de 1.5 A son la base del esquema, pendiente de comprobación con los picos reales. Para programación se utiliza el USB de U1 siguiendo sus opciones de alimentación; no se conectan dos fuentes de 5 V sin comprobar el circuito de la placa.

### 2.4 Accesorios de montaje y pruebas

Estos artículos se reúnen con la electrónica pero no son símbolos adicionales del esquema.

| ID | Cantidad | Artículo | Condición de compra |
|---|---:|---|---|
| E15 | 4 | Placas universales perforadas, aproximadamente 7 × 9 cm. | Una para distribución/control y tres para paneles LED. Ajustar si ya hay material adecuado. |
| E16 | 1 juego | Jumpers y cables de prueba compatibles con los pines. | Para banco; fijar o soldar conexiones en el montaje final. |
| E17 | 1 lote | Cable AWG22 rojo/negro, pines y conectores internos. | Mantener conexiones firmes y cortas, separando iluminación y señal de celda. |
| E18 | 1 | Cable **USB de datos** con el conector de la placa recibida. | Programación y diagnóstico; no es enlace de datos durante uso normal. |
| E25 | 1 conjunto | Conector/cableado entre **P1 de 18 pines de la Waveshare (C)** y U1. | Confirmar paso, orientación y orden físico con la placa; seguir señales del esquema. |
| E26 | 1 | Adaptador SOT-23 a pines o placa de montaje para Q1. | El AO3400A no se inserta directamente en una protoboard. |
| A01 | 3 | Difusores translúcidos de los paneles LED. | Probar sombras y reflejos con el plato real. |
| A02 | 1 lote | Tornillería, separadores y aislantes de las placas. | Confirmar medidas de las piezas; no se cambia aún el modelo 3D. |
| A03 | 1 | Plato lavable y masas conocidas o acceso a una balanza de referencia. | Calibración y ensayos de tara, retiro/reposición y repetibilidad. |

La DevKitC-1 oficial usa un regulador SGM2212 de 800 mA nominales **compartidos entre la ESP32, la cámara, el HX711 y las demás cargas de +3V3**. No son 800 mA adicionales disponibles para la cámara; se comprobarán tensión y temperatura con el módulo recibido. Referencia: [esquema oficial de DevKitC-1 v1.1](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20220413.pdf).

## 3. Asignación de señales de la revisión v2

Esta asignación corresponde a la placa DevKitC-1 N16R8 y al módulo **Waveshare (C)**. No es el mapa GPIO de la ESP32-CAM AI-Thinker anterior.

| Terminal de cámara P1 | Señal | U1 / destino |
|---|---|---|
| 1 | VCC | +3V3 |
| 2 | GND | GND |
| 3 | SIOC | GPIO9 |
| 4 | SIOD | GPIO8 |
| 5 | VSYNC | GPIO13 |
| 6 | HREF | GPIO14 |
| 7 | PCLK | GPIO21 |
| 8 | XCLK | GPIO15 |
| 9 | Y9 / D7 | GPIO18 |
| 10 | Y8 / D6 | GPIO17 |
| 11 | Y7 / D5 | GPIO16 |
| 12 | Y6 / D4 | GPIO12 |
| 13 | Y5 / D3 | GPIO11 |
| 14 | Y4 / D2 | GPIO10 |
| 15 | Y3 / D1 | GPIO7 |
| 16 | Y2 / D0 | GPIO6 |
| 17 | RESET, activo bajo | GPIO5 |
| 18 | PWDN | Sin conexión externa; puente interno R7 a GND |

| Función | Conexión |
|---|---|
| HX711 DT / DOUT | GPIO4 |
| HX711 SCK / PD_SCK | GPIO2 |
| Puerta DOOR_N | GPIO1, R13 a +3V3 y contacto SW2.COM–NO hacia GND |
| Luces LED_EN | GPIO42 → R14 → Q1.G; R15 de Q1.G a GND |
| Salida de luces | Cada rama: +5V → 100 Ω → LED → Q1.D; Q1.S a GND |
| Celda → HX711 | E+/E− a excitación; A+/A− a señal diferencial |

SIOC/SIOD ya tienen sus pull-ups en la placa de cámara; no se añaden resistencias externas en paralelo en esta revisión. SW2.NC queda libre. Los colores de cables de la celda se identifican con ficha o medición. No se usan GPIO35/36/37, reservados por la memoria del N16R8; tampoco USB GPIO19/20, UART GPIO43/44 ni los pines de arranque GPIO0/3/45/46. GPIO42 queda para luces y no se utiliza JTAG externo. La microSD queda fuera de esta revisión.

La numeración P1 de la cámara se sigue por documentación/serigrafía; los bloques de módulo no equivalen a huellas de PCB. La hoja no incluye ruteo, Gerber ni fabricación de una placa propia.

## 4. Cambios y presupuesto

| Parte | Revisión anterior | Revisión 2 |
|---|---|---|
| Controlador | ESP32-CAM AI-Thinker | Una ESP32-S3 N16R8. |
| Cámara | OV2640 incluida | Waveshare OV5640 Camera Board (C), independiente y con autofocus. |
| Programación | Base MB separada | USB de la placa de desarrollo. |
| Luces | Encendidas con interruptor general | Q1, R14 y R15 para control desde Registrar. |
| Desacoplo de cámara | Integrado en ESP32-CAM | C3 y C4 en la entrada +3V3 del módulo independiente. |
| IA | Propuesta SigLIP local en laptop | Gemini mediante API, conforme a la app del equipo. |
| Historial | Propuesta SQLite en laptop | Se conserva el flujo documentado de la app, con historial en navegador. |

La reserva indicada por el equipo es **S/ 150 para ESP32 y cámara**, S/ 30 por cada uno de los cinco integrantes. Los demás componentes se presupuestan aparte.

- La placa **sin cámara** necesita cotización propia. La oferta de S/ 50 mencionada durante la planificación incluía cámara; no se presenta como precio confirmado de esta placa sola.
- La referencia consultada de Waveshare publica **US$ 26.99** por la **Camera Board (C), SKU 13802**, antes de cotizar entrega a Perú. No confirma stock ni precio en Paruro.
- Los precios anteriores eran referencias del 7 de octubre de 2026. Se deben actualizar al comprar; no se reproduce el total antiguo de S/ 410 como presupuesto de esta revisión.
- No se incorpora todavía una batería, pantalla, segunda ESP32 ni otra cámara. El costo de API/tokens de Gemini corresponde al software, no a un componente electrónico adicional.

Para llevar al taller y comenzar las pruebas: **U1, CAM1 y su conexión, HX711, celda, microswitch, fuente y cable USB de datos**. Para ensayar las luces, añadir **los doce LED con sus resistencias y la etapa Q1/R14/R15**. Se requieren multímetro, soldadura y referencia de masa; no se consideran compras si ya están disponibles.

## 5. Secuencia de funcionamiento acordada

1. El plato vacío está dentro al preparar el equipo. Tras confirmar recipiente vacío y esperar estabilidad, se establece la tara y la app muestra **0 g**.
2. Se retira ese plato, se sirve la comida y se vuelve a introducir. La tara queda guardada; retirar el plato y obtener una lectura negativa no provoca una nueva tara.
3. Se cierra la puerta y se pulsa **Registrar** en la app.
4. U1 comprueba puerta cerrada, tara válida y peso estable dentro del rango de trabajo. Enciende los paneles mediante Q1.
5. Se estabilizan iluminación y exposición y se ejecuta el enfoque. Se obtiene una foto asociada a la masa neta de esa medición.
6. Foto, gramos y estado se comunican por Wi-Fi al flujo de la app. La consulta a Gemini requiere una red con Internet, como un router o un hotspot.
7. La app muestra carga, recibe las propuestas de Gemini, calcula con la tabla nutricional y permite revisar/corregir alimentos y porciones.
8. Al terminar se apagan las luces y se detiene la captura. Se retira el plato. U1 queda en espera para otra orden; SW1 proporciona apagado general manual.

Si se abre la puerta o cambia el peso durante la captura, se cancela o repite la medición. El firmware debe apagar las luces al completar, cancelar, agotar el tiempo o detectar un error, aun si falla Gemini. La cámara se utiliza para capturas puntuales; el reposo por SCCB y su comportamiento térmico se comprueban con el montaje real.

La **calibración** usa una masa conocida y se conserva entre encendidos. Una nueva **tara** se hace con el recipiente vacío al comenzar o cambiarlo; no equivale a recalibrar. La tara no elimina la carga física del plato y la plataforma sobre la celda.

## 6. App, datos y validación

Se conserva la [app FoodScan existente](https://github.com/Mao-dot/FoodScan/blob/main/README.md), implementada con Next.js/PWA. En [lib/gemini.ts](https://github.com/Mao-dot/FoodScan/blob/main/lib/gemini.ts) se consulta la API Interactions de Gemini con el modelo configurado en el servidor o `gemini-3.8-flash` por defecto. En [lib/nutrition.ts](https://github.com/Mao-dot/FoodScan/blob/main/lib/nutrition.ts) se calculan los nutrientes a partir del catálogo; Gemini identifica alimentos y propone proporciones, sin proporcionar los valores de macros. El README documenta **924 entradas de las Tablas Peruanas de Composición de Alimentos del INS, décima edición de 2017**, revisión de alimentos/porciones e historial en el navegador. No se cambia esa tabla ni se entrena un modelo nuevo en esta revisión electrónica.

| Dato | Obtención |
|---|---|
| Masa neta total | Medida con celda/HX711, calibración y tara. |
| Identidad y preparación | Propuesta de Gemini, confirmada o corregida por usuario. |
| Gramos de cada alimento de un plato mixto | Reparto estimado y revisable; la celda mide el total. |
| kcal y macronutrientes | Cálculo con los valores de tabla por 100 g y los gramos asignados. |

**Valor de la porción = masa en g × valor de tabla por 100 g / 100.** Los datos ausentes se indican como no disponibles o parciales, conservando código y fuente; no se convierten en cero. El contrato de análisis existente recibe foto y gramos; falta implementar y probar la conexión automática de la máquina, el firmware y los estados del ciclo.

Las comprobaciones del JSON/esquema verifican conectividad del archivo; no equivalen a ERC oficial ni prueban el equipo. En el taller se debe verificar:

- Modelo N16R8, PSRAM disponible, regulación de 3.3 V y ausencia de reinicios durante enfoque/captura/transmisión.
- Foto, autofocus, encuadre del plato, transferencia y reposo real de cámara.
- Variación de peso con masas conocidas, repetibilidad y retiro/reposición del mismo plato.
- Luces apagadas al arrancar y tras finalizar/cancelar/fallar; sombras, reflejos y estabilidad del peso durante conmutación.
- Registro completo y revisable en la app.

El límite previo de **2 kg de carga total**, incluyendo plataforma/plato/comida, se conserva como criterio provisional hasta ensayar el montaje. Los 24 bits del HX711 y los 5 MP del sensor no acreditan por sí solos precisión de pesaje ni calidad de reconocimiento.

### Contrato existente para fotografía y peso

La ruta [POST /api/analyze](https://github.com/Mao-dot/FoodScan/blob/main/app/api/analyze/route.ts) ya recibe JSON con los siguientes campos:

| Campo | Formato y validación actual |
|---|---|
| `image` | Cadena Data URL con imagen JPEG, PNG o WebP codificada en base64. |
| `totalGrams` | Número finito entre **10 y 3000 g** de alimento neto; no es el límite validado del hardware. |
| `description` | Texto opcional de preparación; se limita a 500 caracteres al construir la consulta. |

El cuerpo se limita a **3.000.000 bytes/caracteres** en la ruta, incluidos imagen codificada, campos y envoltura JSON. El tamaño de la imagen JPEG debe dejar margen para la expansión de base64 y los demás datos. La resolución/calidad de captura se ajustará para cumplir ese límite.

La ruta existente devuelve el análisis con alimentos, gramos y nutrientes. Usa una clave de Gemini de variable del servidor y un límite de seis análisis por minuto y dirección IP en memoria. El [cliente de análisis](https://github.com/Mao-dot/FoodScan/blob/main/lib/analysis-request.ts) aplica 45 s de espera; la llamada a Google aplica 40 s. [GET /api/status](https://github.com/Mao-dot/FoodScan/blob/main/app/api/status/route.ts) únicamente informa si hay configuración de Gemini; **no** representa conexión, puerta, peso o estado de la máquina.

Por tanto, se aprovecha el backend de la app y su contrato de análisis. La recepción de órdenes de Registrar, transferencia automática desde la ESP32, identificación de medición y seguimiento del ciclo físico siguen pendientes de integración y prueba; no se consideran ya implementados por existir `/api/analyze`. La revisión de electrónica no cambia rutas ni credenciales.

## 7. Referencias técnicas y de compra

1. Espressif. [ESP32-S3-DevKitC-1 v1.1: conexiones y variantes](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html) y [ficha de ESP32-S3-WROOM-1](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf).
2. Waveshare. [OV5640 Camera Board (C), SKU 13802](https://www.waveshare.com/catalog/product/view/id/3494/s/ov5640-camera-board-c/category/37/) y [recursos/esquema del módulo](https://www.waveshare.com/wiki/OV5640_Camera_Board_%28C%29).
3. Espressif. [Controlador esp32-camera](https://github.com/espressif/esp32-camera).
4. Alpha & Omega Semiconductor. [AO3400A: ficha técnica](https://www.aosmd.com/res/data_sheets/AO3400A.pdf).
5. Naylamp. [Celda 5 kg, SKU 000155](https://naylampmechatronics.com/sensores/155-celda-de-carga-5kg.html), [HX711, SKU 000147](https://naylampmechatronics.com/fuerza-peso/147-modulo-hx711-transmisor-de-celda-de-carga.html) y [adaptador WODE 5 V / 2.4 A](https://naylampmechatronics.com/fuentes-1a-2a/1461-fuente-de-alimentacion-acdc-12w-5v-2a-wode-adaptador.html).
6. Nanoparuro. [LED blanco straw hat 5 mm](https://nanoparuro.com/shop/lb-sh-5mm-wc-led-blanco-straw-5mm-3-2-3-4v-6000k-blanco-frio-1881) y [microswitch KW11](https://nanoparuro.com/shop/kw11-3z-3f-microswitch-20x6-5x13-5spdt-de-palanca-con-rueda-5a-250vac-1109).
7. Equipo 10. [App FoodScan: README](https://github.com/Mao-dot/FoodScan/blob/main/README.md), [backend de análisis](https://github.com/Mao-dot/FoodScan/blob/main/app/api/analyze/route.ts), [Gemini](https://github.com/Mao-dot/FoodScan/blob/main/lib/gemini.ts), [motor nutricional](https://github.com/Mao-dot/FoodScan/blob/main/lib/nutrition.ts), [guion del avance](../../output/guiones/Guion_FoodScan_Avance_Prototipo_5_minutos.md) y [revisión de decisiones](../Revision_componentes_2026-11-04.md).

Las fichas definen las piezas y el comportamiento previsto. Una publicación de precio no equivale a cotización local ni a compra realizada. Las piezas recibidas y el montaje requieren las pruebas indicadas.
