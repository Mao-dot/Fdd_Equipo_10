# FoodScan: modelo 3D vigente, revisión 2

**Equipo 10 · Archivo recibido el 5 de noviembre de 2026 · Unidades: mm**

El modelo vigente es [FoodScan_Onshape_v2.fs](CAD/FoodScan_Onshape_v2.fs).
Se incorpora sin modificar el contenido de `FoodScan_Onshape (2).fs`, entregado
por el equipo, y sustituye como referencia principal al conjunto STEP v1.

Es código **FeatureScript 3112**, con la biblioteca `onshape/std/geometry.fs`
versión `3112.0`. Exporta `foodScanPrototipo`, que aparece como
**FoodScan - Prototipo Concepto C**. El archivo define el modelo; la compilación
y la geometría resultante deben comprobarse dentro de Onshape.

## Contenido de esta versión

- Carcasa de MDF con uniones de dedos, puerta frontal, repisa superior y bandeja de pesaje.
- Soportes de PLA, tres difusores de acrílico, bisagras y patas.
- ESP32-S3-DevKitC-1 N16R8 y cámara Waveshare OV5640 Camera Board (C) separadas.
- Celda de 5 kg, HX711, microswitch KW11, doce LED con sus resistencias y placas de montaje.
- Q1 AO3400A, R13-R15, C1-C4, jack, interruptor y portafusible.
- Plato de referencia de Ø220 mm y opción de mostrar la puerta abierta 100°.

Los cuerpos comerciales son representaciones del archivo recibido; contrastar
medidas y fijaciones con las piezas compradas. La lista eléctrica y el cableado
siguen en [Componentes_v2.md](../MóduloElectrónico/Componentes_v2.md) y en el
[esquemático v2](../MóduloElectrónico/EasyEDA/FoodScan_Esquematico_v2.pdf).

## Parámetros declarados

Estos son los valores predeterminados del código, no medidas tomadas de un
ensamble físico ni necesariamente los valores de una instancia ya configurada
en Onshape.

| Parámetro | Predeterminado | Intervalo declarado |
|---|---:|---:|
| Ancho exterior X | 310 mm | 280-600 mm |
| Fondo exterior Y, sin puerta | 300 mm | 260-600 mm |
| Alto exterior Z, sin patas | 415 mm | 330-800 mm |
| Espesor MDF | 3,5 mm | 2,5-6 mm |
| Ancho de dedo | 20 mm | 8-60 mm |
| Diámetro del plato de referencia | 220 mm | 150-250 mm |
| Mostrar puerta abierta | No | Sí / No |

El diámetro de bandeja se calcula como diámetro del plato + 30 mm: **250 mm**
con los valores predeterminados. El código reserva 48 mm de altura para el
compartimento electrónico superior. La revisión reemplaza las medidas nominales
del modelo v1; los parámetros y planos antiguos no se aplican automáticamente.
Los intervalos son independientes: al modificarlos, comprobar que la bandeja y
el plato caben en el interior y conservan sus holguras.

## Abrir en Onshape

1. En un documento de Onshape, crear una pestaña **Feature Studio**.
2. Abrir el archivo `.fs` como texto y copiar su contenido completo en esa pestaña.
3. Guardar con **Commit** y comprobar los mensajes de compilación. El código declara las versiones 3112 / 3112.0; revisar cualquier incompatibilidad que indique Onshape antes de cambiar la fuente.
4. En un **Part Studio** del mismo documento, seleccionar la operación **FoodScan - Prototipo Concepto C** desde el menú de operaciones personalizadas.
5. Revisar los parámetros, generar el modelo y comprobar piezas, fijaciones, holguras y la opción de puerta abierta.

Referencias oficiales: [Feature Studios y Commit](https://cad.onshape.com/help/Content/FeatureStudio/feature_studios.htm)
y [operaciones personalizadas del mismo documento](https://cad.onshape.com/help/Content/PartStudio/add_custom_features.htm).

## Estado de los archivos

| Archivo / grupo | Estado |
|---|---|
| [FoodScan_Onshape_v2.fs](CAD/FoodScan_Onshape_v2.fs) | Fuente vigente recibida del equipo; contenido conservado íntegro. |
| [Registro_modelo_v2.json](CAD/Registro_modelo_v2.json) | Hash, versiones y parámetros extraídos del archivo. Revisión documental. |
| STEP, STL, PDF de planos, vistas e inventarios v1 | Archivo histórico del modelo anterior. |
| Nuevos STEP, STL, planos y capturas v2 | No incluidos en el archivo recibido; pendientes de exportar desde el modelo nuevo. |

Se comprobó la identidad de la copia y la presencia de los componentes en el
código, que declara 86 grupos de pieza; ese recuento no acredita 86 sólidos
válidos. No se ejecutó ni compiló en Onshape y no se atribuyen a v2 las pruebas
geométricas del generador v1. El documento en línea previamente enlazado se
conserva como referencia en el [archivo histórico](README.md); su actualización
no se presupone por recibir este archivo.
