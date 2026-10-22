## Diapositiva 1

A continuación presentamos el avance de nuestro prototipo FoodScan.

## Diapositiva 2

Nuestro avance del prototipo es FoodScan, la aplicación que relaciona la foto y el peso de una comida con información nutricional. Ya implementamos captura, ingreso de peso, reconocimiento con IA, cálculo y revisión antes de guardar.

La pantalla inicial acumula comidas y nutrientes del día. La balanza externa aporta la medición física.

## Diapositiva 3

Para obtener la cantidad usamos una balanza TRUPER de cinco kilogramos. Primero colocamos el plato vacío y aplicamos la tara para descontarlo. Después agregamos la comida y leemos su peso neto en gramos.

Por ahora escribimos la lectura en la aplicación. La transmisión automática queda pendiente. Distinguimos la capacidad de la balanza del rango del formulario: FoodScan admite de diez a tres mil gramos.

## Diapositiva 4

En Escanear podemos abrir la cámara o elegir una foto guardada. Usamos la imagen del plato completo, con buena iluminación. Aquí observamos arroz, una preparación de quinua y huevos.

También podemos describir la preparación. Esto ayuda a distinguir un alimento cocido de uno crudo o a señalar ingredientes poco visibles.

## Diapositiva 5

Ingresamos un solo peso: el total comestible sin el plato. El cuatrocientos veinte de estas capturas es el ejemplo del campo vacío. En la grabación escribiremos la lectura neta real de la balanza.

Podemos añadir una descripción y seleccionar desayuno, almuerzo, cena o snack. Al pulsar Analizar mi plato, enviamos la foto, el peso y los detalles al servicio de reconocimiento. Si falla, podemos reintentar o seleccionar los alimentos manualmente.

## Diapositiva 6

Usamos Gemini tres punto ocho Flash, de Google. Le proporcionamos la foto, el peso total, la descripción y la lista de alimentos disponibles. Su tarea es proponer qué alimentos aparecen y qué proporción de la masa corresponde a cada uno. Estas proporciones son estimaciones que el usuario revisa.

La aplicación tiene cargadas novecientas veinticuatro entradas de las Tablas Peruanas de Composición de Alimentos del INS, décima edición de dos mil diecisiete. Cada entrada conserva nombre, código, página de origen y calorías y macronutrientes por cien gramos. No entrenamos un modelo propio. Gemini utiliza la lista como referencia para elegir alimentos; el programa obtiene los nutrientes de la tabla.

## Diapositiva 7

El programa reparte el peso total según las proporciones propuestas y comprueba que los gramos asignados sumen ese total. Luego multiplica los gramos de cada alimento por su valor nutricional por cien gramos y divide entre cien.

Por ejemplo, ciento cincuenta gramos de arroz cocido equivalen a ciento setenta y dos coma cinco kilocalorías según la referencia cargada. Es una comprobación del cálculo, no el resultado de este plato.

Podemos cambiar alimentos o ajustar sus porciones y el programa recalcula. Si la tabla no informa un nutriente, lo indica como pendiente o parcial, sin inventar un cero.

## Diapositiva 8

Para comprobar la variación de masa durante la grabación, registraremos el peso del alimento, retiraremos una parte y volveremos a pesarlo con el mismo recipiente tarado. Compararemos ambas lecturas y las ingresaremos en FoodScan, conservando la evidencia del pesaje y del formulario.

También podemos comprobar el cálculo con un solo alimento conocido y dos cantidades: al duplicar los gramos, sus nutrientes deben duplicarse. Esto permite verificar la respuesta del programa. La exactitud al reconocer y repartir un plato mixto todavía requiere pruebas con alimentos pesados por separado.

## Diapositiva 9

En este registro ingresamos cuatrocientos cuatro gramos. La aplicación muestra cuatrocientas cincuenta y cinco kilocalorías, veintidós coma ocho gramos de proteínas y catorce coma dos de grasas. Los cincuenta y seis gramos de carbohidratos son parciales porque falta el dato del huevo.

## Diapositiva 10

El reparto estimado asigna ciento setenta y cinco coma siete gramos a quinua, ciento ocho coma siete a arroz y ciento diecinueve coma seis a huevo: suman cuatrocientos cuatro. La referencia de quinua cocida requiere revisión para representar un guiso.

## Diapositiva 11

Tras guardar, Mi día confirma una comida con esos resultados. El historial permanece en el navegador. El teléfono usa batería e Internet para reconocer. La integración automática del pesaje y su validación siguen pendientes.
