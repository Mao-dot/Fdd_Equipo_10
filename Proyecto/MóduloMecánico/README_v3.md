# FoodScan: modelo 3D, revisión 3

**Equipo 10 · 11 de noviembre de 2026 · Unidades: mm**

El [STEP completo](CAD/FoodScan_Conjunto_Completo_v3.step) contiene los 92 sólidos
en milímetros, incluida la puerta y la tapa. El [FeatureScript de la revisión 3](CAD/FoodScan_Onshape_v3.fs)
permite regenerar el modelo con otros parámetros.

El [documento editable de Onshape](https://cad.onshape.com/documents/45e3d926c78c8605f6f81458/w/91fa14538bcd65fd6b70d7cb/e/b685e9ed6cbeabbb007e5a59)
requiere acceso desde Onshape. Contiene el modelo generado en **Part Studio 1**
y el código en **Feature Studio 1**.

Es código **FeatureScript 3112** (`onshape/std/geometry.fs` versión `3112.0`).
Exporta `foodScanPrototipoV3`, que aparece como **FoodScan - Prototipo Concepto C v3**.
Se sustituyó `fSphere` por `opSphere` para construir esferas a partir de sus
coordenadas. En Onshape se verificó la compilación y la regeneración de las
92 piezas con los parámetros predeterminados.

## Cambios respecto a la revisión 2

| Tema | Revisión 2 | Revisión 3 |
|---|---|---|
| Alto exterior | 415 mm | **380 mm** |
| Compartimento electrónico | 48 mm | 32 mm |
| Separadores de la celda | 8 mm | 5 mm |
| Encuadre del plato Ø220 | 10 mm de margen | 5 mm de margen (lente a 287 mm del borde del plato) |
| Iluminación | 12 LED de 5 mm en 3 paneles con marcos PLA y difusores de acrílico | 4 tiras COB 5 V de 200 mm, verticales en las esquinas, en perfiles esquineros de aluminio con difusor opal |
| Borneras | 2 bloques de 2 polos | X1, X2A, X2B, X3, X4 en la placa de control y X5 junto al HX711 |
| Cables | No representados | Recorridos de alimentación, tiras, HX711, celda, puerta y cable plano de la cámara |
| HX711 | Bajo la bandeja | Esquina trasera izquierda, fuera de la bandeja |
| Otros | — | Canaletas PLA, pasacables en la repisa, parasol del lente, conectores de ensamble |

### Por qué las tiras van en las esquinas

- **Fuera de la foto:** la cámara (67,4° en diagonal, 43,6° en el lado corto) no
  alcanza a ver las esquinas de la caja.
- **Sin reflejo en el plato:** en una superficie brillante, el reflejo de cada
  tira cae entre 116 y 187 mm del eje, fuera del radio del plato (110 mm).
  Con tiras horizontales bajo la repisa, el reflejo caería a unos 70 mm del
  centro, dentro del plato.
- **Luz pareja:** cuatro direcciones diagonales y alturas de 60 a 260 mm. El
  cálculo de luz directa da unos ±15 % entre el centro y el borde del plato.

El código avisa en Onshape si, al cambiar parámetros, la cámara deja de
encuadrar el plato con margen o si el reflejo de las tiras entra en el plato.

## Parámetros

| Parámetro | Predeterminado | Intervalo |
|---|---:|---:|
| Ancho exterior X | 310 mm | 280-600 mm |
| Fondo exterior Y, sin puerta | 300 mm | 260-600 mm |
| Alto exterior Z, sin patas | **380 mm** | 330-800 mm |
| Espesor MDF | 3,5 mm | 2,5-6 mm |
| Ancho de dedo | 20 mm | 8-60 mm |
| Diámetro del plato de referencia | 220 mm | 150-250 mm |
| Mostrar puerta abierta | No | Sí / No |
| Mostrar electrónica simplificada | Sí | Sí / No |

Alturas principales con los valores predeterminados:

| Elemento | z (mm) |
|---|---:|
| Cara superior de la bandeja | 34,7 |
| Borde del plato | 54,7 |
| Tiras LED | 59,7 a 259,7 |
| Vano de la puerta | 39 a 259 |
| Repisa (cara inferior / superior) | 341 / 344,5 |
| Cara inferior del lente | 342 |
| Cara inferior de la tapa | 376,5 |

## Borneras y conexiones

| Ref | Dónde | Tipo | Conexión |
|---|---|---|---|
| X1 | Placa de control | Tornillo 2P, 5,08 mm | +5V de entrada (después de SW1 y F1) y GND |
| X2A | Placa de control, izquierda | Tornillo 4P, 5,08 mm | Tiras LED1 (delantera izq.) y LED3 (trasera izq.): +5V y LED− |
| X2B | Placa de control, derecha | Tornillo 4P, 5,08 mm | Tiras LED2 (delantera der.) y LED4 (trasera der.): +5V y LED− |
| X3 | Placa de control, izquierda | Enchufable 4P, 5,08 mm | HX711: 3V3, GND, DT (GPIO4), SCK (GPIO2) |
| X4 | Placa de control, derecha | Enchufable 2P, 5,08 mm | Puerta: DOOR_N (GPIO1) y GND, hacia SW2 COM/NO |
| X5 | Soporte del HX711 | Tornillo 4P, 5,08 mm | Celda: E+, E−, A−, A+ |

LED− es el drenador de Q1. Las borneras enchufables X3 y X4 permiten retirar la
repisa con la electrónica sin soltar cables. Los recorridos del modelo son
representativos: los cables de las tiras suben por las esquinas y cruzan la
repisa por agujeros de Ø6; el del HX711 y el de la puerta suben por canaletas
PLA. El cable de la celda va sujeto al piso y no toca la bandeja. El cable plano
entre la cámara y la ESP32 mide menos de 10 cm.

## Modelos STEP de componentes comerciales

La operación crea conectores de ensamble (mate connectors) en los puntos de
montaje de U1, CAM1, LC1, U2, SW2, Q1, X1-X5, J1, F1 y SW1. Están en piezas que
no se ocultan: placa de control, repisa, piso, soportes y panel trasero. Para
usar modelos STEP descargados (por ejemplo, de SnapEDA):

1. Importar los STEP en el mismo documento nuevo de Onshape.
2. En la operación, desactivar **Mostrar electronica simplificada**.
3. En un ensamble, insertar el Part Studio y los STEP, y unir cada STEP a su conector.

## Abrir en Onshape (documento nuevo)

1. Crear un **documento nuevo** en Onshape.
2. Crear una pestaña **Feature Studio**, copiar todo el contenido de
   `FoodScan_Onshape_v3.fs` y guardar con **Commit**.
3. Revisar los mensajes de compilación.
4. En el Part Studio del mismo documento, insertar la operación
   **FoodScan - Prototipo Concepto C v3**, generar el modelo y comprobar
   piezas, holguras y avisos.

## Esquemático correspondiente

El [esquemático v4](../MóduloElectrónico/README_v4.md) documenta las cuatro tiras
COB, las borneras y la alimentación de esta revisión. La lista de compra del
módulo electrónico corresponde a la revisión 2.
