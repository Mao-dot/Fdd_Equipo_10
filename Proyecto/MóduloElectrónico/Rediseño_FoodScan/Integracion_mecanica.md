# Integración mecánica de la electrónica

La referencia es el [rediseño mecánico vigente](../../MóduloMecánico/Rediseño/README.md). El [STEP cerrado para Onshape](../../MóduloMecánico/Rediseño/exports/step/FoodScan_cerrado_Onshape.step) corresponde al SHA-256 `63690af1e38809cb966eca6699697261d3897e78509ef9cd32b8d5832d623de1`. Las cotas están en mm. X=0 es el eje medio, Y=0 es el frente y Z=0 es la cara inferior del piso. El rediseño usa una carcasa nominal de 320 × 310 × 380 y acceso de mantenimiento por la tapa superior.

## Ubicación del PCB auxiliar

La reserva dibujada en el CAD es X=69…134, Y=223…296 y Z=331…367. La entrada trasera P09a se evaluó con el STEP OEM del conector Tensility y con volúmenes derivados de planos para el balancín NKK y el portafusible Schurter. El portafusible llega hacia delante hasta Y=275,5. Una envolvente de componentes que ocupe toda la reserva original invade nominalmente 1 983,76 mm³ del volumen del portafusible y 1 762,80 mm³ del volumen del interruptor.

El [STEP de la PCB auxiliar poblada](pcb/FoodScan_Auxiliar.step) se situó 19 mm hacia el frente respecto del límite delantero de la reserva original. Para reproducir el montaje, aplicar una traslación de **(+69, +204, +333) mm** al STEP, con sus ejes paralelos a los del ensamblaje y sin rotación. El origen del archivo coincide con la esquina frontal izquierda de la cara inferior del sustrato. La huella es de 60 × 65 mm y el espesor nominal de la PCB es de 1,6 mm.

| Interfaz | Resultado de la comprobación |
| --- | --- |
| PCB poblada | X=69…129, Y=204…269 y Z=330,495…345,995. Se verificaron 34 sólidos válidos. Cero volumen de intersección con el ensamblaje existente. |
| Separación mínima a la carcasa | 2,495 mm entre las puntas inferiores y el divisor P07, 7,071 mm a la escuadra A222 y 28,005 mm a la cara interior de la tapa P02. |
| Variante de entrada P09a | Separación nominal de 12,298 mm al volumen del portafusible, 22,299 mm al del interruptor y 34,767 mm al jack OEM. |
| Fijaciones | Agujeros pasantes no metalizados Ø3,4 en (73,208), (125,208), (73,265) y (125,265). Patrón de 52 × 57. Se comprobaron cuatro separadores Ø6 × 5 entre Z=328 y Z=333. Asientan sobre P07 y la cara inferior de la PCB con 0 mm³ de intersección. |
| RECOM U2 | Los centros de los tres terminales del STEP OEM coinciden con los ejes de los taladros Ø1,0 de la PCB en X=99, 101,54 y 104,08, con Y=240. El cuerpo queda sobre la PCB y los terminales salen por debajo. |
| Despeje preliminar de cables | Los 14 mm de acceso recto a la izquierda de J1 y delante de J2/J3 quedaron libres frente a la estructura en CAD. Los JST XH requieren inserción y extracción desde arriba. Verificar los conectores con sus cables y el radio de curvatura. |

P07 requiere cuatro fijaciones coincidentes con el patrón de la PCB. Si se perfora el divisor, sellar las penetraciones y comprobar la protección contra vapor. Verificar el radio de curvatura, la extracción axial y el acceso de herramienta con los enchufes y la tornillería reales.

## Módulos y cableado

| Elemento | Integración prevista y dato pendiente |
| --- | --- |
| ESP32-S3-DevKitC-1 N16R8 | Se instala en la cuna independiente P36 al lado izquierdo, con acceso de servicio a USB, BOOT y RESET por la tapa. La guía v1.1 de Espressif indica Micro USB. Verificar revisión, conector real, altura de cabeceras y zona de antena de la placa disponible. [Guía oficial](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html) |
| Cámara Adafruit 5838 | PCB OEM de 22,86 × 35,56 con dos taladros nominales Ø3 separados 17,78. Montaje ajustable, lente en Z=350 nominal y orientada hacia el plato a través de la ventana. Verificar el eje, el FPC y el arnés montados. La distancia calculada lente–borde del plato es de 287,8 o 282,1 según la altura real del kit de pesaje. [Archivos CAD oficiales](https://learn.adafruit.com/adafruit-ov5640-camera-breakout/downloads) |
| BMH12M205 | Base fija de referencia de 120 × 120, con centro en (0,155) y piso de apoyo Z=6. Se reservaron 37 mm para alturas publicadas de 30,7 y 36,4. Conectar el arnés UART de cuatro hilos por el paso de 20 × 10 del divisor. Sujetarlo a la estructura fija y comprobar su holgura con carga y durante el desmontaje. Medir conector, pies y carrera del kit recibido. [Best Modules](https://www.bestmodulescorp.com/en/bmh12m205.html) |
| OLED Waveshare 25742 | Montaje frontal, centro del área activa en (X=0, Z=352), vano de 56,3 × 28,6 y patrón de 55,5 × 32,5 para M2,5. Comprobar penetración de los tornillos en los separadores y espacio para el enchufe posterior. La variante Onshape conserva las interfaces de montaje del CAD OEM, según `documentacion/OLED_Onshape.md` en el proyecto mecánico. [STEP OEM del OLED](https://files.waveshare.com/wiki/2.42inch%20OLED%20Module/2.42inch%20OLED%20Module_3D.zip) |
| Detector Panasonic ASQ10228 | Está previsto en el compartimento seco, en soporte ajustable P38 y con accionador P39. El CAD deja una separación mínima de 0,189 mm entre P39 y el detector OEM con la puerta cerrada, y de 2,670 mm a 0,5° de apertura. Ajustar P39 con la muestra para rebasar el punto de conmutación dentro de la carrera admisible. Comprobar continuidad del contacto NC en apertura y cierre antes de habilitar la captura. [Ficha Panasonic](https://industry.panasonic.com/global/en/products/control/switch/micro-seal/number/asq10228) |
| Cuatro COB de 200 mm | Los cuatro pasos de 14 × 8 del divisor llevan los ramales de las esquinas al compartimento seco. Mantener acceso a las conexiones y proteger los bordes de paso. Ensayar el conjunto de perfil, difusor y cierre con la tira física y vapor. |

## Alcance de la comprobación

Se reimportaron los 605 sólidos de `FoodScan_cerrado_Onshape.step` y los 34 de `FoodScan_Auxiliar.step` con CadQuery 2.8.0 y OpenCascade 7.9.3.1. Se descartaron pares separados por su caja envolvente y se comprobó el volumen común entre cada par de sólidos candidato, con umbral de 0,000001 mm³. La distancia mínima se obtuvo de la topología B-Rep. La variante P09a se evaluó con los sólidos paramétricos en sus datums de montaje. La distancia P39–detector se obtuvo mediante distancia mínima de sólidos en poses discretas. El SHA-256 del STEP de la PCB comprobado es `7793f7c9fa5bf80726d0a64ddf057020c0f566f22d7b84062ce0f814e9a1d22a`. El CAD de origen se conservó intacto.

Quedan pendientes el montaje físico de los arneses y tornillería, la inspección del acceso a los enchufes y USB, el retorno a cero del pesaje con cargas excéntricas y las capturas con platos de Ø220 y Ø270. Probar ciclos con comida caliente y comprobar la ventana sellada, el recorrido del vapor hacia el deflector trasero y el estado del compartimento seco.
