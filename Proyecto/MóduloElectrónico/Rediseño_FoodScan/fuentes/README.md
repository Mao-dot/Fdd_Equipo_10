# Fuentes comerciales y modelos de FoodScan

La selección de cámara, controlador y módulo de pesaje procede de la BOM de la rama `rediseño` y su copia de trabajo, con base en el [commit de selección de pesaje](https://github.com/Mao-dot/Fdd_Equipo_10/commit/de536443a028184165824cff16a31466040ab7d6). Las referencias de pantalla, puerta, pulsadores, iluminación y entrada se cotejaron con [registro de fuentes del CAD mecánico](../../../MóduloMecánico/Rediseño/documentacion/Fuentes_CAD.md). La pantalla figura como selección propuesta en ese CAD. La entrada de panel corresponde a la variante mecánica P09a.

Se consultaron primero EasyEDA y LCSC por número de parte. La biblioteca del ESP32-S3-WROOM-1-N16R8 ([LCSC C2913202](https://www.lcsc.com/product-detail/wifi%20modules_espressif%20systems_esp32-s3-wroom-1-n16r8_C2913202.html)) corresponde al módulo soldado dentro del DevKitC, con patillaje y contorno distintos de la placa completa. Para los módulos externos se priorizaron las interfaces documentadas por cada fabricante y los conectores físicos de la PCB de control.

## Cámara y controlador

| Referencia | Fuente | Correspondencia y límites |
| --- | --- | --- |
| Adafruit 5838, OV5640 con autofocus de 120° | [Eagle SCH](Adafruit-OV5640-Breakout.sch), [Eagle BRD](Adafruit-OV5640-Breakout.brd), [pieza Fritzing](Adafruit-OV5640-Camera-Breakout.fzpz) y [plano óptico C19939-001](https://cdn-shop.adafruit.com/product-files/5838/C19939-001+datasheet+FD5640+-120D-AF-Model.pdf). [Producto 5838](https://www.adafruit.com/product/5838) · [guía de patillaje](https://learn.adafruit.com/adafruit-ov5640-camera-breakout/pinouts) · [fuente Eagle](https://github.com/adafruit/Adafruit-OV5640-Camera-Breakout-PCB/tree/adf6a654e8dfffa9a6b9d84681128a27a9fea257) · [fuente Fritzing](https://github.com/adafruit/Fritzing-Library/blob/master/parts/Adafruit%20OV5640%20Camera%20Breakout.fzpz) | Las bibliotecas identifican el breakout compartido con 5673. La lente y el actuador AF se identifican mediante la ficha del 5838 y el plano óptico. Se cotejaron 18 pads JP2 en el BRD con las 18 conexiones del SCH. Adafruit indica cerrar el jumper VM y cargar firmware de autofocus por I²C. El fabricante publica CAD 2D y DigiKey no ofrece un STEP integral verificable. [Catálogo CAD del 5838](https://www.digikey.com/en/models/22163173) |
| ESP32-S3-DevKitC-1-N16R8, Espressif v1.1 | [Esquema OEM v1.1](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20221130.pdf), [DXF](https://dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.dxf), [plano](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html#hardware-reference), [símbolo y huella de la comunidad EasyEDA](https://easyeda.com/component/f202b75334f94af1a1a7ebbcbafb3fae). [Guía oficial J1/J3](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html#header-block) · [biblioteca original](https://easyeda.com/component/f202b75334f94af1a1a7ebbcbafb3fae) | El símbolo de aliawrang usa 1–22 para J1.1–22 y 23–44 para J3.22–1. Sus 44 pines coinciden con el orden y los nombres OEM. Su huella tiene filas separadas 23,00 mm, frente a 22,86 mm en el DXF. La huella se conserva como fuente comparativa. Verificar en la unidad la revisión, los dos conectores Micro USB y la altura de los pines. GPIO35–37 quedan reservados para la memoria en la variante N16R8. |
| ESP32-S3-WROOM-1, módulo interno | [STEP original](https://www.espressif.com/sites/default/files/3dmodel/ESP32-S3-WROOM-1%203D%20Model.STEP) y [datasheet de la familia](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf). [Descarga STEP oficial](https://www.espressif.com/sites/default/files/3dmodel/ESP32-S3-WROOM-1%203D%20Model.STEP) | 18,00 × 25,50 × 3,10 mm. El STEP cubre el módulo WROOM-1. Para el DevKitC completo se documentan el DXF y la reserva de sus cabeceras, puertos y envolvente. |

### Numeración física de la cámara

Usar JP2, el conector de 2 × 9 a 2,54 mm. La siguiente tabla está vista desde la cara de la lente, con el borde recto de cabeceras abajo. En el BRD original, el origen queda en el vértice inferior izquierdo y X crece a la derecha. El pad 1 queda en X=21,59 e Y=1,27 mm. Los impares están a Y=1,27 y los pares a Y=3,81. X decrece 2,54 mm por columna hasta los pads 17/18 a X=1,27. JP1 duplica la fila par como montaje alternativo.

| JP2 | Señal OEM | JP2 | Señal OEM |
| ---: | --- | ---: | --- |
| 1 | 3,3 V | 2 | GND |
| 3 | SCL | 4 | SDA |
| 5 | VSYNC | 6 | HSYNC / HREF |
| 7 | PCLK | 8 | EXT_XCLK |
| 9 | DATA9 / D7 | 10 | DATA8 / D6 |
| 11 | DATA7 / D5 | 12 | DATA6 / D4 |
| 13 | DATA5 / D3 | 14 | DATA4 / D2 |
| 15 | DATA3 / D1 | 16 | DATA2 / D0 |
| 17 | RESET activo bajo | 18 | PWDN activo alto |

EXT_XCLK recibe 24 MHz con el jumper en EXT, su posición de fábrica. SCL y SDA tienen pull-ups en el breakout. RESET y PWDN tienen polarización en el breakout. El jumper VM (SJ2 en Eagle) alimenta el motor AF a través de DATA1 **interno** del flex. D1 del bus de captura corresponde a DATA3 en JP2.15. Confirmar con continuidad la orientación del cable en ambos extremos. La disponibilidad de la cámara debe confirmarse con el proveedor.

El esquema de la revisión A utiliza el oscilador interno. Abre la unión XCLK a EXT, cierra XCLK a INT y verifica que JP2.8 quede sin cable. Cierra VM para el actuador de autofocus y comprueba el firmware de enfoque. [Guía Adafruit](https://learn.adafruit.com/adafruit-ov5640-camera-breakout/pinouts)

## Pesaje y pantalla

| Referencia | Fuente | Correspondencia y límites |
| --- | --- | --- |
| Best Modules BMH12M205 Gen2 de 5 kg | [Diagrama de conexión del fabricante](BMH12M205_Arduino_example_layout.png), [librería 1.0.2](BestModules-BMH12M205-1.0.2.zip), [licencia BSD 3-Clause](BMH12M205_Arduino_library_LICENSE.md). [Ficha](https://www.bestmodulescorp.com/en/bmh12m205.html) · [manual Rev. 1.00](https://www.bestmodulescorp.com/en/amfile/file/download/file/2030/product/1300/) · [guía de firmware](https://www.bestmodulescorp.com/en/amfile/file/download/file/2034/product/1300/) · [repositorio OEM](https://github.com/BestModules-Libraries/BMH12M205/tree/adf1eab2195b76263274a646036e4ce54f2b1839) | Kit armado con puente completo y ADC de 24 bits integrados. La interfaz externa tiene cuatro hilos digitales: 1 GND, 2 VDD, 3 TXD, 4 RXD. UART 38 400 bit/s, 8N1, con cruce TX↔RX. VDD de 2,6–5,5 V, 5 mA máx. a 3,3 V. Confirmar polaridad, carcasas y crimpado del arnés recibido. El acceso de descarga directa al PDF devolvió HTML, por lo que se conserva el enlace oficial consultado. No se localizó un STEP comercial verificable. La altura de catálogo 36,4 mm difiere de 30,7 mm en el manual. |
| Waveshare OLED 2,42″ blanca SKU 25742, SSD1309 | [STEP OEM](https://www.waveshare.com/wiki/2.42inch_OLED_Module#Resources), [plano mecánico](https://files.waveshare.com/wiki/2.42inch%20OLED%20Module/2_42inch_oled_module-sku25742.pdf), [esquema OEM](https://www.waveshare.com/wiki/2.42inch_OLED_Module#Resources), [datasheet SSD1309](https://www.waveshare.com/wiki/2.42inch_OLED_Module#Resources). [Producto](https://www.waveshare.com/product/ai/2.42inch-oled-module.htm) · [configuración, CAD y firmware](https://www.waveshare.com/wiki/2.42inch_OLED_Module) | OEM J1 y P1 llevan 1 VCC, 2 GND, 3 DIN, 4 CLK, 5 CS, 6 DC, 7 RST. SPI de cuatro señales en su configuración de fábrica, más reset. El cable OEM tiene 7 vías de paso 1,25 mm. El otro acceso es por cabecera de 2,54 mm. PCB de 61,5 × 39,5 mm y patrón de fijación de 55,5 × 32,5 mm. La cara visible apunta a +Z en el STEP original. El CAD mecánico registró 55 de 165 sólidos con problemas de curvas sobre superficies en OpenCascade. Conservar el original y usar la variante de intercambio del proyecto mecánico cuando el traductor de ensamblaje la requiera. |

## Controles, iluminación y entrada

| Referencia | Fuente y verificación |
| --- | --- |
| Panasonic ASQ10228 | [STEP OEM exacto](https://mediap.industry.panasonic.eu/assets/imported/industrial.panasonic.com/ac/cdn/e/control/switch/micro/cad/3d_step/asq10228_step.zip) y [ficha de la serie](https://industry.panasonic.com/ac/cdn/e/control/switch/micro/catalog/sw_m_eng_turq-st.pdf). SPST normalmente cerrado, cables hacia la derecha. El fabricante especifica desde 1 mA a 5 V CC. Verificar la transición al accionar y al soltar la puerta. [Ficha de referencia y descarga](https://industry.panasonic.eu/pd-386273/switches/switches/seal-type-switches/turquoise-stroke-switches/asq10228) |
| Adafruit 1505, Tara y Captura | [Plano publicado](https://cdn-shop.adafruit.com/datasheets/R13diagram.jpg) y ficha del pulsador momentáneo normalmente abierto. El cuello M16 y las cotas de panel proceden del plano. Confirmar terminales y agarre real. No se localizó CAD integral verificable. [Producto](https://www.adafruit.com/product/1505) |
| Ephycob `5v-COB-8mm-300D-10~15W-Ra80-cut2.5cm`, 4000 K | Cuatro tiras de 200 mm, ancho 8 mm y corte en incrementos de 25 mm. Ficha de 10–15 W/m a 5 V, equivalente a 0,4–0,6 A por tira y 1,6–2,4 A en total. IP20. Confirmar la variante adquirida, corriente, posición de pads y polaridad. No se localizó STEP verificable. [Ficha OEM](https://www.yhcob.com/lmV1/139.html) |
| Tensility 54-00406 | [STEP OEM](https://tensility.s3.us-west-2.amazonaws.com/imports/product_3d_models/54-00406.STEP), [plano Rev. A](https://tensility.s3.us-west-2.amazonaws.com/imports/product_spec_sheets/54-00406.pdf). Jack de panel 5,5 × 2,1 mm, dos contactos, 13 A a 48 V CC. Confirmar polaridad de la fuente, contacto central y retorno con multímetro. [Producto y recursos OEM](https://www.tensility.com/products/54-00406) |
| NKK JWMW11RAA | [Ficha de la serie](https://www.nkkswitches.com/pdf/JW.pdf). SPST ON/OFF con rating resistivo de 10 A a 30 V CC para JWMW. El exportador OEM muestra el código, pero no se obtuvo un modelo validado. [Ficha serie](https://www.nkkswitches.com/pdf/JW.pdf) · [CAD OEM](https://www.nkkswitches.com/distributor-landing-page/?part_no=JWMW11RAA&vendor=digikey) |
| Schurter 3101.0120, FPG2 | [Ficha del fabricante](https://www.schurter.com/en/datasheet/typ_fpg2.pdf). Portafusible 5 × 20 mm de panel con terminales soldables. El enlace STEP del fabricante publicado por Mouser devuelve 404. [Ficha](https://www.schurter.com/en/datasheet/typ_fpg2.pdf) · [registro de distribuidor](https://www.mouser.co.uk/en/ProductDetail/Schurter/31010120?qs=PRB6hLq1s9eKLrp6nNAvpg%3D%3D) |

## Integridad y condiciones de uso

El PCB utiliza los símbolos de los códigos LCSC indicados en la [BOM](../BOM.md). Los archivos EasyEDA originales se recuperan mediante el procedimiento de descarga de esta página. La huella asociada a C3817931 en EasyEDA es de 5,08 mm y no coincide con los 5,00 mm del Phoenix 1935187. La placa usa la huella KiCad de 5,00 mm con taladros de Ø1,30 mm. Las huellas JST de placa provienen de KiCad y conservan 2,50 mm de paso. Para el RECOM R-78K3.3-1.0 se usó el [STEP OEM](https://recom-power.com/en/products/switching-regulators/switching-regulators-sip/rec-p-R-78K3.3-1.0.html) y su [ficha](https://recom-power.com/pdf/Innoline/R-78K-1.0.pdf). Su huella local usa las cotas OEM. Los originales C7836, C157991 y C15849 y la ficha TI corresponden a alternativas investigadas.

- Los archivos de Adafruit para Eagle se distribuyen bajo [CC BY-SA 3.0](Adafruit-OV5640-PCB-license.txt). La [biblioteca Fritzing de Adafruit](https://github.com/adafruit/Fritzing-Library) declara CC Attribution Share-Alike. Sus gráficos se conservan como referencia.
- Best Modules publica el ejemplo y la librería bajo [BSD 3-Clause](BMH12M205_Arduino_library_LICENSE.md).
- Los documentos y modelos comerciales se consultan en sus fuentes. El inventario de hashes identifica las copias usadas durante la verificación.
- [SHA256SUMS.txt](SHA256SUMS.txt) permite verificar las copias de referencia. Se cotejaron los archivos copiados del CAD contra el inventario de hashes de ese diseño. Los PDF recibidos directamente se identificaron por su firma de archivo y los STEP conservan las unidades y el origen nativos.

## Recuperar fuentes para reproducir la entrega

El proyecto `FoodScan.epro2` incluye los símbolos y las huellas utilizados. Para regenerarlo a partir de los originales, ejecutar desde el directorio de la revisión:

```powershell
python fuentes/descargar_bibliotecas.py
```

El script recupera 19 entradas de EasyEDA por UUID y comprueba sus SHA-256 antes de guardar. Si una revisión de biblioteca cambia, el script muestra el archivo afectado y conserva la copia local.

Para mostrar el regulador RECOM en la vista 3D de KiCad o regenerar el STEP poblado, abrir la ficha del R-78K3.3-1.0, pulsar **R-78K-1.0.STEP** en **Documents & Media** y guardar el archivo como `fuentes/RECOM-R-78K-1.0-original.STEP`. Su SHA-256 de referencia es `ecccfe1c22482a3027a58e833983ba0b48335354601b9bb0ee4e917a8db27751`. El STEP poblado de la placa está disponible en `pcb/FoodScan_Auxiliar.step`. [Descarga RECOM](https://recom-power.com/en/products/switching-regulators/switching-regulators-sip/rec-p-R-78K3.3-1.0.html)

Documentación adicional consultada. [AO3400A](https://www.aosmd.com/res/data_sheets/AO3400A.pdf) · [SN74LVC1G17](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf) · [JST XH](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf) · [Phoenix Contact 1935187](https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-pt-15-4-50-h-1935187) · [Schurter SPT](https://www.schurter.com/en/datasheet/typ_spt_5x20.pdf).
