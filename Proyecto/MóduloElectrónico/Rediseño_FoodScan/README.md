# FoodScan · Rediseño electrónico

Revisión A para prototipo, 12 de noviembre de 2026. La entrega parte de la BOM del rediseño y de su ensamblaje mecánico de trabajo. El sistema utiliza la Adafruit 5838, una DevKitC-1 N16R8 v1.1, el módulo UART Best Modules BMH12M205, el OLED Waveshare 25742 y cuatro tiras COB.

| Archivo | Uso |
| --- | --- |
| [FoodScan.epro2](easyeda/FoodScan.epro2) | Proyecto nativo para EasyEDA Pro 3.2.209, con cuatro hojas, símbolos, huellas y PCB de dos capas enrutada. |
| [Vistas de esquemático](easyeda/vistas/) | Hojas de PCB auxiliar, entrada e iluminación, ESP32 y cámara, y pesaje, pantalla y controles. |
| [PCB editable de KiCad](pcb/FoodScan_Auxiliar.kicad_pcb) | Fuente física de la placa. Las bibliotecas `.pretty`, el archivo `fp-lib-table` y los STEP individuales se incluyen al lado. |
| [STEP poblado](pcb/FoodScan_Auxiliar.step) · [Vista 3D](pcb/FoodScan_Auxiliar.png) | Exportación de la PCB real, para revisar el montaje e incorporarla al ensamblaje. |
| [BOM](BOM.md) · [Fuentes comerciales](fuentes/README.md) | Referencias de compra, documentación, biblioteca y modelos de origen. |
| [Matriz de pines y redes](Matriz_conexiones.csv) · [Matriz de arneses](Matriz_arneses.csv) | Numeración de pines y 66 conexiones físicas de extremo a extremo, incluidos retornos y empalmes. |
| [Verificación eléctrica](Verificacion_electrica.md) · [Integración mecánica](Integracion_mecanica.md) | Cálculos y comprobaciones realizadas, límites y procedimiento para el banco. |
| [Informe DRC](validacion/DRC_KiCad.json) · [Verificación del proyecto](easyeda/Verificacion_EasyEDA.json) | Resultados de KiCad y del conversor local de EasyEDA. |

## Abrir en EasyEDA Pro

1. Descarga `easyeda/FoodScan.epro2`. En EasyEDA Pro 3.2.209, usa **File → Import → EasyEDA (Professional)** e importa el archivo como proyecto nuevo. El proyecto incluye los símbolos y huellas necesarios. Para reutilizarlos en otro proyecto, usa la extracción de biblioteca de la importación si tu modo de trabajo la ofrece. [Guía de importación](https://prodocs.easyeda.com/en/import-export/export-easyeda-pro/) · [Notas de la versión](https://prodocs.easyeda.com/en/faq/update-record/)
2. Abre las cuatro hojas y la PCB desde el árbol. Comprueba que haya 29 referencias eléctricas en la placa, cuatro agujeros, dos polígonos de GND y el contorno de 60 × 65 mm. Desde el esquemático usa **Design → Check DRC** y revisa la lista de cambios de **Update/Convert Schematic to PCB**. Los módulos comerciales y los elementos de panel deben figurar como externos. Comprueba los cambios en una copia antes de aplicarlos. [Reglas de esquemático](https://prodocs.easyeda.com/en/schematic/design-design-rule/) · [Actualización de PCB](https://prodocs.easyeda.com/en/schematic/design-update-convert-schematic-to-pcb/)
3. En el PCB, ajusta las reglas a las especificaciones del fabricante, reconstruye los dos polígonos de GND y ejecuta **Design → Check DRC**. Revisa el resultado y compáralo con el archivo de KiCad y la matriz. [Guía de DRC](https://prodocs.easyeda.com/en/pcb/design-check-drc/)
4. El STEP poblado está disponible directamente para CAD. Para regenerar el STEP desde EasyEDA, importa los STEP individuales, asígnalos en **Tools → 3D Model Manager** y verifica pin 1, cara superior y asiento sobre la PCB. Las transformaciones verificadas para la exportación se encuentran en los modelos de la placa KiCad. Los modelos KiCad usan la transformación de su huella y escala unitaria. Para RECOM, usa el STEP OEM, giro de 180° sobre X y ajuste de origen respecto al pad 1 según [integración mecánica](Integracion_mecanica.md). Exporta **Export → 3D File → STEP**, con PCB y componentes activados. La asociación de STEP dentro de EasyEDA queda pendiente de esta comprobación en el editor. [Gestor 3D](https://prodocs.easyeda.com/en/pcb/tools-3d-model-manager/) · [Exportación STEP](https://prodocs.easyeda.com/en/pcb/export-3d-file/)

## Decisiones de circuito y montaje

- **Pesaje.** J4 lleva GND, 3,3 V, TXD y RXD al BMH12M205. J9 lleva UART y masa a la DevKitC. Los cuatro hilos de puente forman parte del conjunto comercial y el arnés externo tiene cuatro vías digitales. La interconexión se cablea según la numeración OEM, cruzando TX y RX. [Manual Best Modules](https://www.bestmodulescorp.com/en/amfile/file/download/file/2030/product/1300/)
- **Cámara y pantalla.** El DVP y SCCB van directamente a la DevKitC por un arnés corto. La alimentación sale de la placa auxiliar. El puente XCLK del 5838 se configura a INT de 24 MHz y VM se cierra para el actuador de autofocus. El OLED conserva el SPI de fábrica y usa 3,3 V de U2. Confirmar la versión de firmware y los niveles de señal con los arneses definitivos. [Adafruit](https://learn.adafruit.com/adafruit-ov5640-camera-breakout/pinouts) · [Waveshare](https://www.waveshare.com/wiki/2.42inch_OLED_Module)
- **Alimentación y puerta.** Un RECOM dedicado alimenta los periféricos. Dos AO3400A separan los retornos de las tiras en pares. El detector NC y su resistencia al final del arnés permiten distinguir el cierre de la desconexión. La posición de P39 requiere ajuste y la tensión sobre el contacto debe calificarse. El fusible T4 A y el comportamiento de limitación del adaptador siguen sujetos a ensayo. [Verificación de diseño y pasos de banco](Verificacion_electrica.md)
- **Bibliotecas y geometría.** Se reutilizaron símbolos de EasyEDA/LCSC, el símbolo comunitario cotejado del DevKit y fuentes OEM de Adafruit. Los símbolos de interfaz documentados de los módulos externos se basan en sus pines oficiales. Las huellas incompatibles de catálogo se sustituyeron por huellas KiCad con paso correcto y la huella RECOM se construyó con el plano OEM. El STEP poblado usa el STEP OEM de RECOM y los modelos de biblioteca de los conectores y encapsulados montados. Los modelos disponibles de OLED, detector y jack son de fabricante. El STEP completo de la cámara, la DevKitC y el pesaje sigue sin una fuente exacta verificable. [Inventario de fuentes](fuentes/README.md)

## Estado de verificación

El conversor incluido en EasyEDA reabrió el proyecto y conservó las cuatro hojas, 45 símbolos colocados y la geometría de la PCB. Su exportación de lista de redes coincidió con las 35 redes y los 162 terminales conectados de la matriz. La verificación local cotejó los pads y los 17 terminales intencionalmente libres. El DRC de KiCad 10.0.8 sobre la placa fuente reportó **0 infracciones y 0 conexiones pendientes**. La PCB tiene 241 segmentos de pista, 10 vías y dos planos de GND. La visualización y el STEP proceden de esa placa.

La entrega sirve para revisión de prototipo. Quedan pendientes la importación y ERC/DRC en el editor de EasyEDA, el enlace 3D en EasyEDA y las pruebas de banco y de montaje. Para alimentar por USB durante programación, desconecta la DevKitC de la alimentación y señales del sistema.

## Reproducir

Para regenerar el proyecto con sus referencias de origen, ejecutar `python fuentes/descargar_bibliotecas.py` y seguir las instrucciones para recuperar el STEP del regulador RECOM. [Fuentes y descargas](fuentes/README.md)

`herramientas/definir_circuito.py` genera la matriz y `herramientas/definir_arneses.py` valida los arneses con ella. `herramientas/generar_pcb.py` usa Python, NumPy, sexpdata y la carpeta `share/kicad` de KiCad 10. Tras generarla, rellena zonas y guarda con `kicad-cli pcb drc --refill-zones --save-board`. Luego ejecuta `python herramientas/generar_easyeda.py --pcb pcb/FoodScan_Auxiliar.kicad_pcb` desde esta carpeta. El generador usa Node.js y el conversor de la instalación local de EasyEDA 3.2.209. Exporta el STEP con origen de usuario `80x135mm`.
