# FoodScan - Archivos para el taller S11

## Qué pide la tarea

1. Esquema eléctrico del subproyecto en EasyEDA Pro.
2. Modelo 3D del prototipo con las partes electrónicas en un ensamble o modelo multipartes de Onshape.
3. PDF del esquema y de los planos con medidas en el GitHub del equipo, antes de las 23:59 del día anterior al taller.

El plazo se toma del aviso adjunto. No se indicó aquí la fecha exacta del taller.

## Modelo en Onshape

https://cad.onshape.com/documents/6371db0cdada012e678cb023/w/355e492b405585520bd45e0d/e/5fa7184819c33dff05c63f25?renderMode=0&uiState=6ae2cee7440795f4516e4027

## Cómo usar lo preparado

1. Descomprimir este paquete.
2. Entrar a Onshape y crear un documento llamado **FoodScan - Equipo 10 - S11**.
3. Pulsar **+ → Import**, seleccionar `Mecanica/CAD/FoodScan_Conjunto_v1.step` y elegir **Combine to a single Part Studio** para una presentación multipartes sencilla.
4. Mantener los colores de importación y Z hacia arriba. Comprobar que el cuerpo mide 320 mm de ancho.
5. Ocultar la tapa y un lateral para mostrar cámara, luces y electrónica. La plataforma se apoya sobre una celda de carga. El archivo `FoodScan_Puerta_abierta_v1.step` muestra otra posición estática para exponer.
6. Abrir `PDF/FoodScan_Planos_acotados_v1.pdf`: contiene tres hojas del conjunto, los paneles y detalles del pesaje.
7. Abrir el esquema del equipo en EasyEDA Pro. Revisar las referencias y valores de componentes después de convertir desde Standard, guardar el proyecto y exportar el PDF desde Pro si el profesor exige esa exportación.
8. Subir los dos PDF revisados a GitHub y llevar el documento de Onshape abierto para la exposición.

La geometría del STEP se verificó localmente: 79 sólidos válidos, sin solapes volumétricos en la posición cerrada, y lectura de retorno de los tres STEP. No se ha probado la importación dentro de una cuenta de Onshape.

## Qué explica el modelo

- Caja de MDF de 320 × 320 × 350 mm con puerta frontal.
- Plataforma de 220 × 220 mm, aislada de las paredes.
- Un extremo de la celda se fija a la base; el otro sostiene la plataforma.
- Cámara superior a una distancia nominal de 270 mm del plano del plato.
- Tres paneles de cuatro LED y difusores.
- HX711 y alimentación al fondo, separados del plato; detector de puerta en el marco.

Es una propuesta conceptual basada en las medidas del equipo. Las medidas de los módulos comerciales, taladros y soportes requieren ajuste con las piezas reales antes de fabricar. El modelo importado es editable como sólidos; no incluye el historial de croquis de Onshape ni movimiento de bisagras.

## Reparto sugerido para el equipo

- Una persona: importar el 3D y preparar las vistas.
- Una persona: revisar el esquema en Pro y exportar su PDF.
- Una persona: revisar las medidas de planos contra las piezas compradas.
- Una persona: reunir y subir los PDF al repositorio.
- Todos: practicar la explicación del funcionamiento y del montaje.

Guía oficial de importación: https://cad.onshape.com/help/Content/Document/importing_files.htm

La entrega del repositorio se organiza desde Fundamentos de diseño/Talleres/Taller_11.md, con ambos PDF y el enlace de Onshape.
