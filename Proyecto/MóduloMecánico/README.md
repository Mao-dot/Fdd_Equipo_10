# Modelo 3D de FoodScan - Taller S11

**Equipo 10 · Revisión conceptual 1.0 · 28 de octubre de 2026 · Unidades: mm**

**[Abrir el modelo en Onshape](https://cad.onshape.com/documents/6371db0cdada012e678cb023/w/355e492b405585520bd45e0d/e/5fa7184819c33dff05c63f25?renderMode=0&uiState=6ae2cee7440795f4516e4027)**

[Entrega del Taller 11: documentos PDF y enlaces](../../Fundamentos%20de%20diseño/Talleres/Taller_11.md).

Modelo sencillo de la caja de captura y pesaje. Incluye piezas separadas de
carcasa y puerta, plataforma, celda de carga, cámara, HX711, tres paneles de
cuatro LED, alimentación y detector de puerta. La propuesta parte del montaje
resumido en la [especificación técnica de S11](../Especificacion_S11.md).

## Qué abrir

| Archivo | Para qué sirve |
|---|---|
| [FoodScan_Conjunto_v1.step](CAD/FoodScan_Conjunto_v1.step) | Modelo principal con puerta cerrada, nombres y colores de piezas. Importar en Onshape. |
| [FoodScan_Puerta_abierta_v1.step](CAD/FoodScan_Puerta_abierta_v1.step) | El mismo conjunto en posición de presentación, puerta abierta 105°. |
| [FoodScan_Multipartes_v1.step](CAD/FoodScan_Multipartes_v1.step) | Alternativa plana con todos los sólidos en sus posiciones, sin jerarquía ni colores. |
| [Planos acotados](Planos/FoodScan_Planos_acotados_v1.pdf) | PDF A3 de tres hojas: conjunto, paneles y detalles de montaje. |
| [Vista del interior](Vistas/FoodScan_Interior.png) | Tapa y lateral derecho ocultos para mostrar los módulos internos. |
| [Vista abierta](Vistas/FoodScan_Abierto.png) | Presentación de la puerta y la caja completa. |
| [STL provisionales](STL_provisionales/) | Adaptadores, soporte de cámara, manija y una escuadra para revisar o adaptar. |
| [Verificación geométrica](CAD/Verificacion_geometrica.json) | Validez, interferencias y holguras comprobadas por el generador. |
| [Inventario](CAD/Inventario_modelo.csv) | Piezas, materiales y envolventes del modelo. |

## Abrir en Onshape

1. Crear un documento, por ejemplo **FoodScan - Equipo 10 - S11**.
2. Pulsar **+ → Import** en las pestañas inferiores y seleccionar
   `FoodScan_Conjunto_v1.step`.
3. Para tener un modelo multipartes sencillo, elegir **Combine to a single
   Part Studio**. Para conservar la estructura del conjunto, elegir **Import
   to a single document**. Mantener **Import appearances** para los colores.
4. El modelo usa **Z hacia arriba**. No hace falta activar Y Axis Up. Las
   unidades declaradas en el STEP son milímetros.
5. Abrir la pestaña creada por la traducción, ajustar la vista y comprobar
   una dimensión de 320 mm del cuerpo. Ocultar la tapa y el lateral derecho
   para enseñar cámara, iluminación y pesaje.
6. Si desean mostrar la puerta abierta, importar el segundo STEP en otra
   pestaña. Son dos posiciones estáticas; no contienen un mecanismo animado.

El STEP transfiere sólidos editables y sus posiciones. No transfiere un árbol
de croquis y extrusiones nativo de Onshape ni relaciones de ensamblaje.
La edición paramétrica original está en `generar_modelo.py`; también se pueden
añadir operaciones sobre los cuerpos importados en Onshape.

Referencia: [importación oficial de Onshape](https://cad.onshape.com/help/Content/Document/importing_files.htm).
La verificación local del STEP no sustituye una importación comprobada en una
cuenta de Onshape.

## Medidas y decisiones

| Elemento | Dimensiones / posición nominal |
|---|---|
| Cuerpo de la caja | 320 ancho × 320 fondo × 350 alto; excluye patas, manija y herrajes |
| Patas | 6 de alto; altura total del modelo cerrado, incluidas patas: 356 |
| Material de paneles | MDF blanco de 3 |
| Base | 320 × 320 × 6, dos capas de 3 |
| Laterales | 320 × 341 × 3, dos unidades |
| Fondo | 314 × 341 × 3 |
| Tapa | 320 × 320 × 3 |
| Puerta | 311 × 338 × 3; 1.5 de holgura perimetral dentro del hueco 314 × 341 |
| Plataforma | 220 × 220 × 6, dos capas de 3; cara inferior Z = 38 |
| Celda de carga | Envolvente aproximada de 75 × 12 × 12, entre Z = 18 y 30 |
| Adaptador fijo / móvil | 30 × 20 × 12 / 30 × 20 × 8 |
| Topes | Cara superior Z = 37; holgura nominal de 1 respecto de la plataforma |
| Plato | Ø200; plano interior de referencia Z = 48 |
| Cámara | Lente orientada hacia abajo, extremo inferior Z = 318: distancia nominal 270 al plano del plato |
| Holgura plataforma-pared | 47 a los planos interiores de referencia |
| Manija | 24 de saliente hacia el frente |

El cuerpo y la plataforma usan las medidas propuestas por el equipo. La
distribución precisa, el soporte fijo de cámara, adaptadores y huecos son
decisiones de esta primera maqueta. El ajuste de cámara se consigue cambiando
el soporte o usando calces; esta revisión no incorpora una articulación regulable.

## Montaje y explicación para el taller

1. **Carcasa:** laminar las dos bases, montar laterales y fondo con escuadras,
   y dejar la tapa desmontable para mantenimiento.
2. **Balanza:** fijar un extremo de la celda al adaptador de la base; el extremo
   opuesto recibe el adaptador móvil y la plataforma. La zona central de la
   celda queda libre. La plataforma no debe tocar paredes ni topes en reposo.
3. **Captura:** colocar el plato, fijar la ESP32-CAM arriba y comprobar encuadre.
   Las tres luces con difusores iluminan desde izquierda, derecha y fondo.
4. **Electrónica:** HX711 y distribución quedan al fondo bajo una cubierta
   desmontable. Jack e interruptor se ubican al lateral derecho. El adaptador
   de corriente queda fuera de la caja.
5. **Puerta:** montar bisagras y manija. Colocar el microswitch en el marco
   superior derecho para que la puerta lo accione. Ajustar el cierre real.

Para exponer: explicar por qué la cámara está fija, cómo se aísla el pesaje de
la carcasa y dónde se protege la electrónica. El esquema eléctrico y el CAD
representan los mismos módulos; el cableado se consulta en el esquema.

## Alcance de esta revisión

Es una maqueta de distribución para revisar el diseño, con sólidos CAD reales.
Los componentes comerciales llevan `APROX` o se describen como referencia:
no son modelos certificados de fabricante. Confirmar sus medidas, conectores,
roscas y sujeciones antes de fabricar. Los taladros Ø3.4 de la celda y de sus
adaptadores son provisionales y deben ajustarse a la celda real.

No se modelan cableado, todas las resistencias y condensadores individuales,
toda la tornillería ni el cierre magnético definitivo. Los STL son para revisión
y ajuste; no incluyen orientación de impresión, soportes ni parámetros de
laminador. Las holguras y topes son geométricos, no una validación de tolerancias,
resistencia, precisión de pesaje o desempeño óptico.

## Herramientas y reproducción

CAD: **Python 3.12 + CadQuery 2.6.1 / Open CASCADE (OCP 7.8)**. STEP con sólidos
independientes; STL en mm. Vistas del propio modelo con VTK. Planos vectoriales
con ReportLab; revisión visual del PDF rasterizado con Poppler.

```powershell
python -m pip install cadquery==2.6.1 reportlab
python .\generar_modelo.py
python .\generar_planos.py
```

`parametros_modelo.json` resume las dimensiones generadas. Para cambiar la
geometría hay que editar el generador y mantener coherentes las cotas del PDF;
no se lee ese JSON como archivo de configuración. Los generadores reemplazan
sus propias salidas; conservar aparte cualquier modificación manual.

## Entrega S11

- Llevar el esquema en **EasyEDA Pro** y el documento 3D importado en **Onshape**.
- El esquema existente se entrega originalmente en EasyEDA Standard y se
  puede importar en Pro; comprobar y guardar esa conversión en Pro.
- El PDF del esquema ya existe en el módulo electrónico. El PDF de planos se
  entrega aquí y en `output/pdf/`.
- Ambos PDF y el enlace de Onshape se reúnen en la carpeta del Taller 11.
