# Cámara y controlador

Este directorio conserva los originales descargados, las dos referencias STEP y el generador reproducible de su geometría. Todas las coordenadas están en milímetros. Los STEP de referencia contienen la geometría disponible para el ensamblaje y tienen las limitaciones indicadas a continuación. Los nombres de originales se conservan en el registro y los archivos se pueden cotejar con [SHA256SUMS](originals/SHA256SUMS).

## Adafruit OV5640 5838

Referencia exacta **Adafruit 5838**, lente autofocus de 120° con módulo óptico **FD5640 500W‑V11**. El CAD de Adafruit contiene el PCB del breakout. El plano C19939‑001 documenta el módulo óptico que monta ese PCB. Se comprobó el catálogo de DigiKey para la referencia 5838, incluidas sus opciones de fabricantes y bibliotecas. No presenta un archivo 3D que se pueda descargar y validar. [Producto](https://www.adafruit.com/product/5838) · [Documentación CAD](https://learn.adafruit.com/adafruit-ov5640-camera-breakout/downloads) · [DigiKey 5838](https://www.digikey.com/en/models/22163173)

En el CAD local el origen X coincide con el centro transversal del PCB. Y=0 es el borde recto de las cabeceras y +Y apunta a las esquinas redondeadas. Z=0 es la cara del PCB que recibe el módulo, con la lente mirando hacia +Z. La pieza se construye a partir del contorno del Eagle y los taladros de sus huellas. [Eagle oficial](https://github.com/adafruit/Adafruit-OV5640-Camera-Breakout-PCB/blob/adf6a654e8dfffa9a6b9d84681128a27a9fea257/Adafruit%20OV5640%20Breakout.brd)

| Rasgo | Valor | Estado |
| --- | --- | --- |
| Contorno PCB | 22,86 × 35,56, dos esquinas de aproximadamente R2,54 | Extraído de Eagle, capa 20 |
| Montaje | Ø3,0 en X=±8,89, Y=33,02, separación 17,78 | Extraído de Eagle, huellas U$1 y U$17. Ø3,0 es el taladro nominal de agujeros metalizados. Falta medir el diámetro acabado para elegir el tornillo y su holgura. |
| Espesor PCB | 1,57 en el modelo, hacia –Z | Stack nominal de Eagle, dieléctrico 1,50 y dos capas de cobre de 0,035. Confirmar el espesor de la unidad con calibre. |
| Cabeceras | 2 × 9, paso 2,54, taladros Ø1,016 y Y=1,27 y 3,81. Alternativa 1 × 9, Ø1,00 y Y=8,89. X desde –10,16 hasta +10,16. | Extraído de Eagle, huellas JP2 y JP1. La cabecera soldada y la altura de su enchufe están pendientes. |
| Conector FPC | Huella X1 en X=0, Y=12,70, 24 contactos, paso 0,5 | Posición y huella extraídas de Eagle. La referencia exacta del conector y su altura instalada están pendientes. |
| Cuerpo óptico | 8,50 ±0,20 × 8,50 ±0,20, refuerzo posterior de 8,50 ±0,20 × 8,70 ±0,20 y chapa de 0,20 | Plano C19939‑001. El STEP incluye la envolvente mecánica, con esquinas nominales R0,5 según nota general del plano. |
| Altura del módulo óptico | 5,10 ±0,20 en enfoque normal, 5,25 ±0,20 en macro | Plano C19939‑001. El STEP usa 5,10 nominal. Verificar el montaje del módulo sobre el PCB. |
| Eje óptico respecto del PCB | X≈+0,20, Y≈30,65 y dirección +Z en el modelo | Registro aproximado de la foto frontal oficial con los dos agujeros como escala de 17,78. Alinear y medir la unidad. |
| FPC desplegado | Longitud del conjunto 21,0 ±0,20, cuello de 5,5, lengüeta de 12,5 × 4,5 y espesor de lengüeta 0,3 | Plano C19939‑001. Curvatura y altura instalada pendientes. |
| Campo de visión | 120° nominal | Plano C19939‑001 y ficha del 5838. El eje de referencia, la cobertura y la influencia de la ventana se verifican con imágenes. |

El STEP contiene el PCB y la envolvente del cuerpo y del refuerzo óptico. El generador permite editar la posición estimada del eje y la altura seleccionada de enfoque. El flex curvado, el conector y la cabecera se comprueban en el montaje físico. Los pasantes de montaje y las cabezas de fijación deben respetar la holgura alrededor del módulo y dejar accesibles las cabeceras. [Plano C19939‑001](https://cdn-shop.adafruit.com/product-files/5838/C19939-001+datasheet+FD5640+-120D-AF-Model.pdf) · [Foto frontal Adafruit 5838](https://cdn-shop.adafruit.com/970x728/5838-02.jpg)

## Espressif ESP32‑S3‑DevKitC‑1‑N16R8

La referencia seleccionada usa **ESP32‑S3‑WROOM‑1‑N16R8**, 16 MB de flash, 8 MB de PSRAM y antena en PCB. Espressif publica el DXF de la placa de desarrollo v1.1 y el STEP de WROOM‑1. Se integró el módulo STEP mediante traslación rígida sobre el PCB reconstruido con el DXF. Confirmar la serigrafía de la placa disponible, su revisión y que el PCB corresponde a Espressif, ya que el nombre del módulo WROOM‑1 también aparece en placas de terceros. [Guía de Espressif v1.1](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html) · [Catálogo de módulos](https://www.espressif.com/products/modules)

El origen X=0 está en el borde largo del lado UART, Y=0 en el borde corto de los conectores, y Z=0 en la cara inferior del PCB. La antena se extiende hacia +Y. Los puertos se enchufan desde –Y. [DXF oficial](https://dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.dxf)

| Rasgo | Valor | Estado |
| --- | --- | --- |
| Contorno del PCB | X=0…25,40 y Y=0…62,865, cuatro esquinas R0,50 | Geometría del DXF. El plano PDF de abril acota 62,74 en Y. Usar la envolvente mayor para prototipo y resolver la diferencia de 0,125 con la unidad disponible. |
| Espesor PCB | 1,60 | Nominal de la referencia secundaria. Verificación física pendiente. |
| GPIO J1 y J3 | 44 taladros Ø1,016, X=1,27 y 24,13, Y=7,96…61,30 con paso 2,54 | Geometría DXF, capa TOOL_BOT. En el PDF el primer centro se rotula a 8,00. Altura de cabeceras y pines en la unidad pendiente. |
| Sujeción | Apoyo de bordes con retención desmontable o por cabeceras | El PCB oficial no tiene taladros de fijación. La zona bajo los pines y sobre ellos debe quedar libre para la conexión seleccionada. |
| Puertos J2/J4 | Micro USB, X=6,00 y 19,40, nariz Y≈–0,873 | Tipo confirmado por guía y esquemas de abril y noviembre. Posiciones extraídas del DXF. El número de parte, altura, clavija y radio de cable de la unidad se verifican antes de definir recortes. |
| Módulo WROOM‑1 | 18,00 × 25,50 × 3,10. X=3,75…21,75, Y=43,64…69,14, Z=1,60…4,70. | Medidas del STEP oficial y posición DXF. La altura del conjunto depende del espesor de PCB y de la unión soldada real. |
| Antena | Sobresale 6,275 del PCB según el DXF | Dejar libre de metal la zona de antena y verificar conectividad en la carcasa. |

El STEP incluye el PCB con taladros de GPIO y el módulo WROOM‑1 íntegro. Los cuerpos de Micro USB, los pines, los pulsadores y los SMD del PCB quedan pendientes. Dejar acceso de servicio al lado de ambos puertos y comprobar BOOT y RESET desde la abertura de mantenimiento. La guía indica el cable Micro‑B y el esquema confirma Micro USB en J2 y J4. La copia Xem Studio se conservó como referencia histórica para el cotejo. El autor identifica USB‑C en la descripción, el STEP simplifica conectores, y la ficha discrepa de la cota PDF de longitud. El modelo Xem Studio quedó fuera del ensamblaje. [Esquema abril](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20220413.pdf) · [Esquema noviembre](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20221130.pdf) · [Xem Studio](https://xemstudio.com/objects/esp32-s3-devkitc-1/)

## Registro de originales

| Archivo | Fuente y condición |
| --- | --- |
| [Adafruit-OV5640-Breakout.brd](originals/Adafruit-OV5640-Breakout.brd) | Adafruit Industries, Eagle XML oficial. CC BY-SA 3.0 según [licencia original](originals/Adafruit-OV5640-PCB-license.txt). La reconstrucción del PCB se atribuye a Adafruit y se conserva con la misma licencia. [Repositorio](https://github.com/adafruit/Adafruit-OV5640-Camera-Breakout-PCB) |
| [Adafruit-5838-C19939-001-FD5640-120D-AF.pdf](https://cdn-shop.adafruit.com/product-files/5838/C19939-001+datasheet+FD5640+-120D-AF-Model.pdf) | Plano de Shenzhen Dechuangxin Imaging Technology distribuido por Adafruit. Referencia dimensional local. No se indica licencia abierta en el PDF. [Plano del fabricante](https://cdn-shop.adafruit.com/product-files/5838/C19939-001+datasheet+FD5640+-120D-AF-Model.pdf) |
| [ESP32-S3-DevKitC-1-v1.1.dxf](https://dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.dxf) | Espressif Systems, CAD 2D oficial v1.1 del 29-04-2022. Documentación marcada propietaria. [DXF](https://dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.dxf) |
| [ESP32-S3-DevKitC-1-v1.1-dimensions.pdf](https://dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.pdf) y [PCB layout](https://dl.espressif.com/dl/schematics/PCB_ESP32-S3-DevKitC-1_V1.1_20220429.pdf) | Espressif Systems, documentación oficial de referencia v1.1, 29-04-2022. [Dimensiones](https://dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.pdf) · [PCB layout](https://dl.espressif.com/dl/schematics/PCB_ESP32-S3-DevKitC-1_V1.1_20220429.pdf) |
| [Esquema abril](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20220413.pdf) y [esquema noviembre](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20221130.pdf) | Espressif Systems, esquemas oficiales v1.1 usados para corroborar Micro USB. [Abril](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20220413.pdf) · [Noviembre](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20221130.pdf) |
| [Espressif-ESP32-S3-WROOM-1.step](https://www.espressif.com/sites/default/files/3dmodel/ESP32-S3-WROOM-1%203D%20Model.STEP) | Espressif Systems, STEP AP214 fechado 21-10-2021. 234 sólidos válidos y dimensiones 18,00 × 25,50 × 3,10 contrastadas con ficha. Descarga oficial para referencia de diseño. La página no especifica licencia abierta. [STEP original](https://www.espressif.com/sites/default/files/3dmodel/ESP32-S3-WROOM-1%203D%20Model.STEP) · [Ficha](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) |
| [XemStudio-ESP32-S3-DevKitC-1-v1.1.step](https://xemstudio.com/objects/esp32-s3-devkitc-1/) | Xem Studio, referencia secundaria CC BY 4.0. Contiene un sólido válido, 25,40 × 69,14 × 4,80. Se descarta su uso para cotas de conectores. [Modelo y licencia](https://xemstudio.com/objects/esp32-s3-devkitc-1/) |

El enlace oficial del paquete de referencia de Espressif devolvió HTML al consultarlo. No se encontró STEP integral oficial del DevKitC‑1 en sus documentos. La copia Altium de un tercero identifica en su README un diseño propio con cambios, por lo que no se utilizó para cotas de la placa de Espressif. [Paquete indicado por Espressif](https://documentation.espressif.com/ESP32-S3-DevKitC-1_Reference_Design.zip) · [Diseño alternativo](https://github.com/Yousef4008/ESP32-S3-DevKitC-1-PCB)

## Generación y verificación

Ejecutar con Python y CadQuery 2.6.1.

```powershell
python component_models.py
```

El generador comprueba geometría válida y reabre ambos STEP antes de informar dimensiones y número de sólidos. La cámara mide 22,860 × 35,560 × 6,670 y tiene 3 sólidos. El DevKitC mide 25,400 × 69,140 × 4,700 y tiene 235 sólidos, incluido el PCB y los 234 del STEP oficial del WROOM‑1. Estas son cotas de los sólidos incluidos. Las dimensiones de los elementos que faltan, los cables y las tolerancias de fabricación se verifican de manera independiente.

También se midieron las superficies cilíndricas completas del CAD generado. Se confirmaron 29 perforaciones del PCB Adafruit, incluidos los dos centros de montaje Ø3 en X=±8,89 e Y=33,02, y 44 perforaciones Ø1,016 del ESP32 distribuidas entre las dos filas indicadas.
