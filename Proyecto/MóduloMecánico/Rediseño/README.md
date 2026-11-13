# FoodScan · Rediseño mecánico

FoodScan pesa y fotografía un plato en una misma operación. La pantalla frontal muestra el peso neto y el estado de la captura. El conjunto usa la Adafruit 5838, la ESP32-S3 disponible y el kit de pesaje Best Modules. Este ensamblaje es una **revisión de ingeniería para prototipo y verificación física**. La [electrónica de revisión A](../../MóduloElectrónico/Rediseño_FoodScan/README.md) incluye el esquemático y la PCB auxiliar.

## Abrir y continuar el diseño

| Entregable | Uso |
| --- | --- |
| [FoodScan_cerrado_Onshape.step](exports/step/FoodScan_cerrado_Onshape.step) y [FoodScan_abierto_Onshape.step](exports/step/FoodScan_abierto_Onshape.step) | Variantes de importación con la topología reparada del OLED Waveshare. Conservan la posición y cotas de montaje. [Detalle de la corrección](documentacion/OLED_Onshape.md) |
| [FoodScan_cerrado.step](exports/step/FoodScan_cerrado.step) | Conjunto en posición de captura. Importar en Onshape o inspeccionar en FreeCAD. |
| [FoodScan_abierto.step](exports/step/FoodScan_abierto.step) | Conjunto con puerta abierta 105° para revisar carga del plato y acceso. |
| [Fuentes de CAD](cad_model/) | Modelo paramétrico en Python y CadQuery 2.6.1. [Parámetros nominales](cad_model/parameters.py), [carcasa y acceso](cad_model/structure.py) e [integración de módulos](cad_model/integration.py). |
| [FreeCAD cerrado](exports/step/FoodScan_cerrado.FCStd) y [FreeCAD abierto](exports/step/FoodScan_abierto.FCStd) | Documentos para inspeccionar los sólidos y las interfaces importadas. |
| [Vista del ensamblaje abierto](exports/FoodScan_vista_abierta.png) | Vista calculada desde el CAD, con el espacio del plato en transparencia. |
| [FoodScan_referencias.step](exports/step/FoodScan_referencias.step) | Envolventes del plato, el PCB pendiente y el espacio de pesaje para comprobar el montaje. |
| [DXF](exports/dxf/) y [STL](exports/stl/) | Perfiles nominales de corte láser y piezas destinadas a impresión FDM. |
| [BOM del CAD](exports/BOM.md) | Inventario de piezas, materiales y componentes del modelo. |
| [Verificación geométrica](exports/validacion/Verificacion_geometrica.md) y [datos de comprobación](exports/validacion/geometria.json) | Resultados y alcance de los ensayos de interferencias y holguras del CAD. |
| [Comprobación de fabricación](exports/validacion/fabricacion.json) | Lectura de perfiles DXF y mallas STL exportados. |
| [Dimensiones y tolerancias](documentacion/Dimensiones_y_tolerancias.md) | Cotas de diseño, datums, tolerancias objetivo y medidas físicas pendientes. |
| [Fuentes e inventario SHA-256](documentacion/Fuentes_CAD.md) | Origen, formato, estado y trazabilidad de los CAD comerciales. |
| [Registro de cámara y ESP32](commercial/electronics/README.md) y [registro de pesaje](commercial/weighing/README.md) | Originales, procedencia y límites de cada modelo. |
| [Auxiliares](commercial/auxiliary/README.md) | Fuentes CAD de pantalla, detector y perfiles de iluminación, controles y entrada de alimentación. |
| [PCB auxiliar poblada](../../MóduloElectrónico/Rediseño_FoodScan/pcb/FoodScan_Auxiliar.step) | STEP separado. Consultar las [cotas de montaje](../../MóduloElectrónico/Rediseño_FoodScan/Integracion_mecanica.md) y perforaciones pendientes en P07. |

En Onshape, importar el STEP cerrado en un documento con unidades en milímetros. Revisar la estructura importada y medir el ancho del cuerpo de 320 mm y el vano nominal de 290 mm como control de escala. El STEP conserva la geometría exportada. Para cambiar la cota que gobierna varias piezas, modificar el parámetro en la fuente y regenerar. La configuración abierta sirve para inspección. Las restricciones de movimiento y las futuras revisiones del PCB se pueden definir en el ensamblaje de Onshape. Los documentos de FreeCAD sirven para inspeccionar los sólidos importados. Las comprobaciones independientes se registran para el [modelo cerrado](exports/validacion/FoodScan_cerrado_freecad.json) y el [modelo abierto](exports/validacion/FoodScan_abierto_freecad.json).

Para regenerar el conjunto, ejecutar estos comandos desde este directorio con Python 3.11.

```powershell
python -m pip install -r requirements-cad.txt
python tools/descargar_cad_oem.py
python -m cad_model.export
python -m cad_model.oled_onshape
```

Para repetir la importación y las intersecciones con FreeCAD, ejecutar `tools/freecad_verify.py` con el Python de FreeCAD 1.1.4 y pasar las rutas de los dos STEP.

Los DXF contienen contornos nominales en milímetros. Aplicar la compensación del corte con la máquina y el material reales después de cortar una probeta. En STL confirmar unidades de importación, orientación, diámetro efectivo de agujeros y ajuste de herrajes antes de imprimir la serie de piezas. La tabla dimensional indica las tolerancias iniciales de trabajo.

## Distribución y mantenimiento

La carcasa de 320 × 310 × 380 mm tiene paneles de contrachapado de abedul sellado de 6 mm, un marco frontal con vano de 290 × 265 mm y una puerta opaca con junta y bisagras de pasador. Las cotas del cuerpo excluyen tirador, bisagras salientes y deflector trasero. El diseño reserva un plato de hasta Ø270 mm, con 20 mm de diferencia nominal respecto del ancho del vano. Confirmar el paso del plato con su contenido, las manos del operador y la puerta abierta. El plato portante de acero inoxidable 304 es desmontable para limpieza.

El divisor horizontal separa la cámara de alimentos de la zona alta de electrónica. La ventana óptica se sujeta con un anillo desmontable, con junta de silicona y acceso por la tapa. La salida de vapor queda alta en la parte posterior y descarga por debajo del deflector. Los perfiles de esquina orientan cuatro luces hacia el plato y permiten desmontar sus difusores. La ventana es la superficie expuesta a condensación. Probar ciclos con alimentos calientes y revisar vaho, reflejos y salpicaduras en la cámara seca. El posible calentador de borde depende del resultado de esas pruebas.

El centro de la lente está a Z=350 mm nominal. Con la placa móvil a la altura del manual y el borde del plato de referencia de 24 mm, la distancia al borde es de 287,8 mm. El travesaño ranurado permite ajustar el eje y los separadores permiten revisar la altura. La posición XY inicial del eje se dedujo de una foto oficial del 5838 y se comprueba con una unidad física. Verificar encuadre, enfoque y contraste en el plato completo con la ventana y las luces instaladas. [Documentación de cámara](commercial/electronics/README.md)

Se accede al montaje superior levantando la tapa. La cuna de la ESP32 sujeta el PCB por sus bordes y deja el extremo Micro USB hacia el fondo. Identificar la revisión de la placa disponible y sus conectores antes de cerrar la cuna. La placa posterior ciega P09 es reemplazable. La [variante de prueba P09a](commercial/auxiliary/power/P09a_trial/) permite evaluar el montaje de la entrada eléctrica. En el divisor hay pasos para los ramales LED y para el arnés de pesaje. La PCB auxiliar de 60 × 65 mm se entrega en un STEP separado. Su posición comprobada queda más adelante que la reserva original, para dejar espacio al portafusible. Siguen pendientes los cuatro agujeros de montaje en P07 y la comprobación de arneses y conectores físicos. [Integración de la PCB](../../MóduloElectrónico/Rediseño_FoodScan/Integracion_mecanica.md)

## Montaje del pesaje

El BMH12M205 es un módulo armado y calibrado de 5 kg. Su manual da 30,7 mm de altura y su ficha de venta da 36,4 mm. La revisión modela la primera cota y conserva 37 mm de reserva para el kit. El CAD del kit usa dos superficies de referencia de 120 × 120 mm. Medir altura total, pies, contorno y borde de la base fija antes de ajustar los localizadores y las mordazas. La bandeja debe apoyar exclusivamente sobre la placa móvil y conservar holgura frente a la carcasa y al cableado incluso con carga excéntrica.

La capacidad de 5 kg comprende bandeja, plato y contenido. Ensayar retorno a cero, repetibilidad y estabilidad con masa conocida y con el peso desplazado en el plato. La tara cambia la lectura. Confirmar con el proveedor o mediante una prueba del montaje la capacidad frente al momento de una carga excéntrica. Fijar el alivio de tracción del arnés en la estructura fija y comprobar que la puerta no transmite carga al pesaje. [Fuentes y comprobaciones del BMH12M205](commercial/weighing/README.md)

## Interfaces eléctricas y comprobaciones de montaje

| Componente | Justificación y compatibilidad |
| --- | --- |
| Adafruit 5838 | Integra cámara OV5640 de 5 MP con lente autofocus de 120°. Verificar interfaz paralela, I²C, asignación de GPIO y picos de 3,3 V con enfoque y Wi‑Fi. La operación de autofocus requiere firmware y la configuración VM indicada por Adafruit. [Guía del 5838](https://www.adafruit.com/product/5838) |
| Best Modules BMH12M205 | Se propone el dominio de 3,3 V para su UART con la ESP32. El manual indica 38 400 bit/s. Confirmar polaridad, orden del conector y niveles TX/RX del kit. [Manual](https://www.bestmodulescorp.com/en/amfile/file/download/file/2030/product/1300/) |
| Waveshare 25742 | OLED frontal de 128 × 64 para gramos y estados. El esquema de revisión A usa SPI a 3,3 V. Verificar el enchufe posterior y el estado de arranque. [Wiki Waveshare](https://www.waveshare.com/wiki/2.42inch_OLED_Module) |
| Dos pulsadores Adafruit 1505 | Entradas locales propuestas para tara y captura. Verificar muestra, profundidad de rosca, terminales y conmutación a nivel lógico. [Adafruit 1505](https://www.adafruit.com/product/1505) |
| Panasonic ASQ10228 | Detector normalmente cerrado en el compartimento seco. La revisión A usa una entrada supervisada por ADC. El accionador y el comportamiento del contacto requieren verificación física. [Verificación eléctrica](../../MóduloElectrónico/Rediseño_FoodScan/Verificacion_electrica.md#detección-de-puerta) |
| Cuatro COB 5 V de 200 mm | La opción de Ephycob de 8 mm y 4000 K indica un consumo conjunto de referencia de 1,6 a 2,4 A para la longitud elegida. Medir corriente real, temperatura y efecto de condensación. La selección de perfil, difusor y protección frente a vapor se valida como conjunto. |
| Fuente externa 5 V, entrada e interruptor | La revisión A usa las referencias de entrada Tensility, NKK y Schurter en P09a. Verificar acoplamiento, polaridad, corriente de régimen y de arranque y coordinación con el fusible. [BOM electrónica](../../MóduloElectrónico/Rediseño_FoodScan/BOM.md) |

## Comprobaciones de liberación

- Medir las interfaces del kit de pesaje, el PCB ESP32 disponible, el eje y las cabeceras de cámara, y los pasantes del OLED y del detector. Trasladar medidas verificadas a la fuente.
- Cortar e imprimir probetas de ajuste para validar espesores, holguras, escala, retención de tornillos y cierre de juntas. Repetir la inspección con el herraje real.
- Ensayar apertura y cierre con plato y comida, acceso al USB y la tapa, extracción de ventana y bandeja, y recorridos de los arneses.
- Validar pesar, encuadrar y capturar en una misma secuencia con platos de 220 y 270 mm. Registrar repetibilidad, luz, enfoque y condensación en frío y después de ciclos de vapor.
- Verificar la revisión A en banco y confirmar el montaje de la PCB poblada, sus fijaciones y arneses antes de fabricar P07.
