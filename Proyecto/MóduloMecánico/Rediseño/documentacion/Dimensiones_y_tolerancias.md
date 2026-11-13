# Dimensiones y tolerancias del prototipo

Todas las dimensiones están en milímetros. El cero Z corresponde a la cara inferior del piso, Y=0 al plano del frente y X=0 al eje medio de la caja. El centro de pesaje y de ventana está en X=0, Y=155. Las tolerancias de taller indicadas son objetivos para las primeras probetas. El CAD usa cotas nominales. El proveedor o el taller deberán confirmar las tolerancias que pueden cumplir.

## Carcasa, puerta y pesaje

| Interfaz | Nominal de CAD | Proceso y tolerancia objetivo | Comprobación física |
| --- | --- | --- | --- |
| Cuerpo P01–P08 | 320 × 310 × 380 | Contrachapado de abedul sellado. Corte láser, objetivo ±0,20 en contorno tras compensar el kerf. | Medir espesor de placa y escuadra tras ensamblar. Las dimensiones del cuerpo excluyen salientes y espacio de servicio. |
| Espacio ocupado en reposo | 326 × 362,5 × 391 medidos al reimportar el conjunto cerrado | Incluye patas, cabezas de fijación, tirador y deflector. | Añadir acceso para cables, extracción de tapa y el giro de puerta. |
| Espesor de panel y divisor | 6,0 | Medir el lote y adaptar el parámetro si se desvía más de 0,20 del nominal. | Comprobar unión panel–escuadra, cierre y planitud del divisor. |
| Vano frontal | 290 × 265, umbral Z=18 y dintel Z=283 | Corte láser, objetivo ±0,20 en contorno. | Introducir plato Ø270 con puerta abierta. Los 20 mm de diferencia diametral son nominales y se comprueba el paso frente a herrajes y luces. |
| Puerta P08 | 300 × 275, junta instalada 1,5, giro de revisión 105° | Contrachapado de 6 mm sellado y junta de silicona de celda cerrada. | Comprobar compresión uniforme y cierre. Medir junta libre según la seleccionada y recorrido del pestillo. |
| Bisagras P22/P23 | Dos ejes a Z=86 y 222, pasador Ø4 × 33, taladro nominal Ø4,30 | PETG FDM y varilla inoxidable. Objetivo ±0,25 en plástico tras calibración. Repasar el taladro a medida del pasador si se requiere. | Confirmar giro libre, coaxialidad y holgura axial con pasadores y panel reales. |
| Fijaciones de panel | Paso libre Ø3,4 en madera y Ø3,6 en escuadras FDM para M3 | Tornillos ISO 4762 y tuercas ISO 4032. Objetivo ±0,15 en centros de corte y ±0,25 en FDM. | Cotejar pares de agujeros con piezas montadas. Ajustar si el corte o la contracción consumen la holgura. |
| Módulo BMH12M205 | 120 × 120, altura 30,7 de manual, 36,4 de ficha | Componente comercial. Reserva de diseño de 37 sobre el piso de apoyo. | Medir altura total con pies, carrera bajo carga, forma de borde fijo y salida del arnés. |
| Localizadores P34 y mordazas P35 | Puntos de anclaje X=±65, Y=155±57. Localizador a Z=6…11 y mordaza nominal a Z=11…14. | PETG FDM, objetivo ±0,25. Las mordazas tienen ranura y admiten ajuste de posición. | Retener solo la base fija. Comprobar que las piezas y el cable dejan libre la trayectoria de la plataforma. |
| Bandeja portante P10 | Ø240 × 1,5. Cara superior Z=38,2 con kit nominal y Z=43,9 si el kit mide 36,4. | Acero inoxidable 304 cortado a láser. Objetivo ±0,20 de diámetro, desbarbar y verificar planitud. | Comprobar contacto firme con la cara móvil, concentricidad y extracción. Ensayar vuelco y repetibilidad con carga excéntrica. |
| Plato de referencia | Ø270, borde 24 sobre su base | Envolvente de diseño para pruebas con el plato real. | Revisar paso, estabilidad sobre bandeja, altura del contenido y campo de visión. |

## Óptica, ventilación y electrónica

| Interfaz | Nominal de CAD | Proceso y tolerancia objetivo | Comprobación física |
| --- | --- | --- | --- |
| Ventana W01 y divisor P07 | Vidrio óptico Ø130 × 2, apertura libre Ø116, Z=329…331 para el vidrio | Vidrio cortado a medida, diámetro objetivo ±0,20 y espesor objetivo ±0,10. Divisor de corte láser. | Confirmar material, planitud y cantos pulidos. Medir apertura real y registrar vaho y reflejos con la cámara. |
| Anillo P27 y junta W02 | Alojamiento nominal Ø130,8, cuatro fijaciones de radio 72, junta de silicona nominal 1,0 | PETG FDM, objetivo ±0,25. Centrar el anillo sobre la ventana con los tornillos todavía flojos. | Probar holgura radial, compresión continua, extracción para limpieza y asentamiento del vidrio. |
| Cámara Adafruit 5838 | PCB 22,86 × 35,56, dos taladros nominales Ø3 a 17,78 entre centros | CAD Eagle oficial. Travesaño con dos ranuras de ancho nominal 3,3 y recorrido de centro de ±3 en Y. | Medir diámetro acabado, posición óptica y altura de módulos/cabeceras. Verificar tornillos M2,5 y accesibilidad. |
| Lente y recorrido óptico | Z=350 nominal. Distancia al borde del plato 287,8 con altura de kit 30,7 y 282,1 con altura 36,4. | Separadores P32 de 4,0 nominal en PETG. Cambiar configuración en CAD tras la prueba. | Con plato real comprobar encuadre, enfoque y posible viñeteo de ventana. El FOV de 120° es nominal y el plano no especifica su eje. |
| Salida de vapor | Tres ranuras de 78 × 5, deflector de descarga inferior P26 | Ranuras de corte láser y deflector FDM. Objetivos ±0,20 en corte y ±0,25 en FDM. | Confirmar evacuación, ausencia de luz intrusa y flujo de condensado lejos del compartimento electrónico. |
| OLED Waveshare 25742 | PCB 61,5 × 39,5, patrón 55,5 × 32,5 M2,5, área activa 55,01 × 27,49, centro Z=352 | STEP OEM. Vano 56,3 × 28,6, objetivo ±0,15 en apertura y ±0,20 en posición respecto de soportes. | Revisar alineación, longitud real de tornillos, profundidad de rosca y espacio para enchufar. |
| Pulsadores Adafruit 1505 | Centros X=±54, Z=352 y recorte actual Ø16 | Si se necesita antirrotación, validar muestra para corte Ø16 con dos caras a 15,0. | Medir agarre de rosca en 6 mm sellados, altura de actuador y terminales con conector. |
| Accionador de puerta P39 | X=128. Paso de 12 × 8 a Z=336…344 | PETG, objetivo ±0,25. Pieza de ajuste experimental. | Acotar punto de contacto y carrera frente al ASQ10228 físico. |
| ESP32 y cuna P36 | PCB DXF 25,40 × 62,865, módulo WROOM hasta 69,14 en Y local | Cuna FDM, objetivo ±0,25. Pasar probeta con la placa física antes de imprimir la pieza. | Resolver longitud DXF/PDF de 62,865/62,74, posición y tipo de USB, y holguras de pines y antena. |
| Iluminación | Cuatro perfiles de 220, cuatro COB activas de 200, perfiles nominales 16 × 16 | KLUŚ A08504A_1 de aluminio anodizado y difusores HS-11. Cortar y desbarbar a medida. | Probar acople de clips, tapas, salida de cable y cobertura del plato. Comprobar humedad con la tira seleccionada. |
| Pasos de arnés | Cuatro pasos de 14 × 8 y un paso de 20 × 10 en el divisor | Corte láser. Elegir protección de borde y sellado después de definir arneses. | Medir conectores instalados y radio de curvatura. Comprobar que el arnés de pesaje queda libre de tracción. |
| PCB de control auxiliar | Reserva 65 × 73 × 36. X=69…134, Y=223…296 y Z=331…367. | Volumen de referencia para la futura exportación de EasyEDA. | Verificar forma, altura de componentes, fijaciones, conectores y holgura del arnés de la revisión definitiva. |
| Acceso posterior P09 | Abertura 57 × 27, tapa de 74 × 36 × 3 y patrón 65 × 31 | Contrachapado de 3 mm sellado. Corte nominal sin la perforación de los componentes candidatos. | Validar la entrada de 5 V, fusible, interruptor, cableado y acceso. |

Para el trazado de los arneses se toma 10 mm como radio preliminar. Conservar acceso de extracción axial en los conectores. El radio definitivo depende del cable elegido y puede exigir un pasacables o una salida diferente.

Los objetivos de corte y FDM se aplican a las piezas propias. Las tolerancias de fabricante y cotas incompletas de las piezas comerciales están en sus registros. [Cámara y ESP32](../commercial/electronics/README.md) · [Pesaje](../commercial/weighing/README.md) · [Auxiliares](../commercial/auxiliary/)
