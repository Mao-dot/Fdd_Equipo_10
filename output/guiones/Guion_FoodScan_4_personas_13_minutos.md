## Diapositiva 1

Buenos días. Somos el Equipo 10 y presentamos FoodScan, nuestro sistema de información nutricional de porciones, desarrollado con la metodología VDI.

## Diapositiva 2

Nuestro público inicial son personas físicamente activas que registran sus comidas. El problema es relacionar una porción real con una referencia nutricional por cien gramos.

Por ejemplo, el arroz cocido aporta ciento quince kilocalorías por cien gramos en la tabla peruana. Una porción de doscientos cincuenta gramos aporta doscientas ochenta y siete coma cinco. Registrar solo la referencia subestima ese resultado en sesenta por ciento.

Por eso buscamos vincular cantidad, identidad del alimento y fuente nutricional.

## Diapositiva 3

Revisamos tres artículos. Fang comparó geometría y profundidad para estimar volumen. La profundidad sobreestimó nueve de diez réplicas. Trabajó con máscaras conocidas, por lo que ese resultado no representa platos mixtos reales. Su aporte es controlar captura y escala.

El segundo estudio estimó peso desde imágenes. XGBoost obtuvo un error absoluto medio de tres coma noventa y tres gramos y un error porcentual absoluto medio de tres coma setenta y tres por ciento. Utilizó platos mediterráneos y captura específica. FoodScan necesita su propia validación.

La revisión de Dalakleidi incluyó setenta y ocho estudios y separó captura, segmentación, reconocimiento, cantidad y consulta nutricional.

El factor común es que reconocer el alimento no determina su peso. Por eso separamos captura, cantidad e identificación.

## Diapositiva 4

Las seis patentes aportan principios que relacionamos con nuestro prototipo.

La primera integra pesaje, cámara, identificación y base nutricional. Nos aporta la arquitectura de masa más identidad, aunque no declara el error del sistema.

La segunda aplica tara y lecturas sucesivas para distinguir comida servida de consumida. Adoptamos el descuento del recipiente y la conexión entre medición y aplicación.

La tercera convierte referencias de cien gramos a valores por gramo. Sustenta el cálculo proporcional de nutrientes, dejando fuera la planificación personalizada.

La cuarta combina imagen con voz o texto para aclarar la identidad del alimento. Nos aporta corrección del usuario, aunque sus capturas adicionales aumentan el esfuerzo.

La quinta conecta una balanza con una aplicación. Orienta cómo vincular foto, peso y registro, sin acreditar precisión metrológica.

La sexta combina identificación, peso y calorías por unidad. Refuerza el cálculo a partir de masa, pero no publica métricas de reconocimiento.

El factor común es vincular cantidad, identidad, referencia y cálculo. Estas decisiones aparecen en nuestra estructura funcional.

## Diapositiva 5

Las tesis aportan método, contexto y validación. Fang estudió reconstrucción desde una imagen y reportó un error energético inferior al seis por ciento en una etapa que supone identificación y segmentación correctas.

Checkifood aporta contexto peruano y registro mediante fotografías para usuarios de dieciocho a cuarenta y cinco años. Su ficha no informa error en gramos.

La tesis del IPD pesó alimentos servidos y consumidos de treinta deportistas durante una semana. Sustenta usar pesajes independientes como referencia.

En conjunto, justifican adaptar la interacción y validar nuestras propias porciones.

## Diapositiva 6

Etekcity integra pesaje, tara y consulta nutricional. Su incremento de un gramo no demuestra una exactitud de más o menos un gramo. Además, el usuario debe seleccionar el alimento.

Fitia aporta entradas por fotografía, voz, texto y código de barras. SnapCalorie propone fotografiar, revisar y guardar.

Ambos orientan una interacción breve con corrección, pero sus fuentes comerciales no justifican una precisión en gramos para FoodScan.

Así, los cuatro ámbitos sustentan medición, revisión y validación, además de una interfaz sencilla.

## Diapositiva 7

Las exigencias deben poder comprobarse. Informaremos gramos, calorías y macronutrientes con fuente, permitiendo correcciones y usando un recipiente apto y lavable.

El error de cálculo será máximo de uno por ciento, con recálculo independiente. Validaremos cantidad por alimento en treinta porciones como mínimo, con error porcentual medio máximo de veinte por ciento.

La meta de uso es registrar en sesenta segundos y cinco acciones. Estas metas aún requieren validación.

## Diapositiva 8

La integración debe intercambiar cantidad, estado y comandos entre prototipo y aplicación. Como deseos, consideramos tamaño, masa, costo máximo de quinientos soles, historial y entradas alternativas.

Para hacer coherente el diseño proponemos treinta y cinco centímetros de dimensión máxima, fuente externa de cinco voltios y validación inicial entre cincuenta y mil gramos.

En ese rango, la meta de pesaje es un error máximo igual al mayor entre cinco gramos y dos por ciento de la masa de referencia.

## Diapositiva 9

La caja negra muestra qué entra y qué sale del sistema completo.

En materia, el usuario coloca la porción y el recipiente, que salen sin modificación intencional. En energía, conecta y enciende la alimentación. El funcionamiento consume electricidad y disipa calor.

Todos los datos y órdenes de la web son señales. El usuario aporta foto, peso, descripción y tipo de comida. También ordena analizar, modificar, cancelar el registro o confirmar el guardado.

Automáticamente se obtiene la propuesta de identidad y proporciones de la IA, se consulta la referencia TPCA y se calculan los nutrientes. Las salidas incluyen gramos, kilocalorías, macronutrientes, fuente, estados e historial.

El usuario revisa y decide, sin calcular manualmente los nutrientes. En el parcial, el peso neto se ingresa desde una balanza externa.

## Diapositiva 10

El usuario fotografía el plato completo. Descuenta el recipiente con la tara e ingresa un único peso neto total.

Después solicita el análisis, revisa los alimentos y su reparto en gramos, y corrige lo necesario. Al confirmar, guarda y consulta el historial.

## Diapositiva 11

En el dispositivo propuesto se habilitarán alimentación, conexión, calibración y tara. Con puerta cerrada y masa estable se adquirirán foto y peso del mismo registro.

Se mostrará el resultado para revisión y guardado. Con puerta abierta, sobrecarga o señal inestable, se bloqueará la captura y se informará el estado. La integración física sigue pendiente.

## Diapositiva 12

La estructura organiza dominios y subfunciones. Energizar suministra cinco voltios y regula tres coma tres. Conectar verifica el enlace.

Capturar encuadra, ilumina y adquiere imagen. Determinar cantidad calibra, tara y comprueba estabilidad. Transmitir vincula foto, masa y estado.

La función mecánica es transversal: sostiene la porción, evita roces que alteren el peso y permite retirar el recipiente para limpiarlo.

## Diapositiva 13

Identificar propone alimentos y permite corregirlos. Consultar referencia recupera código, nutrientes y fuente. Calcular normaliza el reparto de gramos, escala los valores por cien gramos y suma el plato.

Informar muestra cantidades y nutrientes. Guardar conserva el registro confirmado.

La flecha de retorno indica que una corrección obliga a consultar y recalcular. Distinguimos masa total medida, reparto por alimento estimado y nutrientes calculados.

## Diapositiva 14

La matriz relaciona funciones con alternativas tecnológicas. Las flechas conectan tres conceptos compatibles.

A usa celular, luz ambiental y estimación visual de masa total. B incorpora soporte fijo y balanza externa, con peso ingresado manualmente. C combina cámara OV2640, iluminación controlada, celda de carga, HX711 y enlace a la aplicación.

C exige cinco voltios para la placa y tres coma tres para el HX711. Para evitar conflictos entre pines, no utilizaremos microSD.

## Diapositiva 15

Aquí aparecen procesamiento, datos, interfaz y registro. Los tres conceptos conservan revisión del usuario, referencia peruana, cálculo proporcional e historial.

Usamos la décima edición de las Tablas Peruanas de Composición de Alimentos. Multiplicamos los gramos del alimento por su valor nutricional por cien gramos y dividimos entre cien.

Cada concepto cubre las once funciones. Se diferencian en captura y determinación de masa. Ahora comparamos sus bocetos.

## Diapositiva 16

El concepto A usa una fotografía y pretende estimar también la masa total. Reduce los componentes físicos, pero depende de forma, escala y captura.

Esa estimación total necesitaría desarrollo y validación. Es una alternativa conceptual y no una capacidad implementada actualmente en FoodScan.

## Diapositiva 17

B combina soporte fijo y balanza externa. El usuario aplica tara e ingresa el peso total en la aplicación.

Para el parcial usaremos una balanza independiente de cinco kilogramos. Su precisión deberá comprobarse; el peso no se transmite automáticamente.

## Diapositiva 18

C propone una caja de treinta y dos por treinta y dos por treinta y cinco centímetros, con cámara superior y doce LED.

La celda de cinco kilogramos transforma la deformación por carga en una señal eléctrica. El HX711 la digitaliza y el ESP32 la procesa. La plataforma debe evitar roces y requiere calibración.

La fuente suministra cinco voltios, con capacidad de dos coma cuatro amperios. Alimenta placa y LED; el HX711 recibe tres coma tres voltios. Incluimos fusible y microswitch.

El enlace previsto usa Wi-Fi. Construcción, consumo total y comunicación física requieren comprobación.

## Diapositiva 19

Pugh ponderada compara con A. Cero significa comparable; más uno, ventaja; menos uno, desventaja.

Asignamos peso tres a masa medida y enlace automático por nuestras exigencias. Captura controlada, trazabilidad y limpieza reciben peso dos.

B obtiene tres puntos por masa y dos por encuadre fijo: suma cinco. C añade iluminación controlada y transmisión automática: suma diez.

Corrección y recipiente lavable son comparables, por eso reciben cero. Estos puntajes son valoraciones de diseño, pendientes de pruebas.

## Diapositiva 20

En la evaluación económica usamos peso uno. B recibe menos uno por transportar balanza y soporte, suponiendo que ya están disponibles.

C recibe tres penalizaciones por transporte, costo y fabricación adicional. Su presupuesto con provisiones es de cuatrocientos cuatro soles con cuarenta y tres céntimos, con reserva de cuatrocientos diez. Es una previsión, no un gasto ejecutado.

## Diapositiva 21

Al sumar, A obtiene cero; B, cuatro; y C, siete. Con estos criterios y pesos, C es el objetivo de diseño propuesto.

Su selección depende de calibrar, comprobar estabilidad y validar el enlace. B permite continuar el parcial mientras completamos esa integración.

## Diapositiva 22

Las fuentes se presentan en formato Vancouver.

## Diapositiva 23

Nuestra propuesta vincula cada antecedente con una función, una exigencia y una validación. Así buscamos información nutricional corregible y trazable. Muchas gracias.
