# Módulo de pesaje Best Modules BMH12M205

El kit de segunda generación se suministra armado y calibrado. Integra la plataforma, la base, el puente de pesaje y su conversor de 24 bits con UART. Su capacidad publicada es de 5 kg. El código y el STEP de esta carpeta representan las dos interfaces que permiten distribuir el volumen del kit en FoodScan. El ensayo dimensional del equipo físico sigue pendiente.

## Dimensiones y estado de verificación

| Referencia | Valor nominal | Evidencia y uso en CAD |
|---|---:|---|
| Envolvente en planta | 120 × 120 mm | Coinciden manual y tienda. Los bordes cuadrados de las dos caras CAD representan una proyección conservadora en planta. Radio de esquina, posición relativa de las placas y huella real de apoyo pendientes. |
| Altura global del manual | 30,7 mm | El manual Rev. 1.00 y el catálogo de selección indican 30,7 mm. Se usa como Z nominal de la cara superior sin carga respecto del plano de apoyo Z = 0. |
| Altura global de la tienda | 36,4 mm | La página del mismo modelo indica 36,4 mm. Hay 5,7 mm de discrepancia entre publicaciones. Medir altura, incluidos pies, sobre el kit recibido y ajustar el montaje en Z antes de liberarlo. |
| Cotas A, B y C de la tabla del manual | 6,2 / 12 / 18,7 mm | Se registran con sus símbolos. Su asignación a los detalles de las piezas sigue pendiente. |
| Reserva de altura FoodScan | 37 mm | Decisión de integración para acomodar ambas alturas publicadas. Incluye 0,6 mm sobre 36,4 mm. A esta reserva de espacio se le deben sumar el recorrido, la holgura del conjunto móvil y la ruta del cable que correspondan. |
| Base fija y placa móvil | Dos referencias separadas | La guía y la foto del ejemplo identifican ambas placas. La foto muestra apoyos bajo la base fija. Espesor, coordenadas de los apoyos, material, tornillos y tolerancias del proveedor pendientes. |
| Salida del arnés | Cuatro hilos desde un extremo del puente | Visible en la foto del fabricante. La orientación hacia el paso trasero es una decisión de integración de FoodScan. Cota de la salida, longitud libre, conector físico y radio de curvatura pendientes de medición. |
| Celda y fijaciones OEM | Pendientes | El manual remite a BMH01105-1 para el protocolo UART. La referencia mecánica, los taladros, las roscas y el par de apriete requieren confirmación aparte. |

`bmh12m205.py` genera el STEP con CadQuery 2.6.1. `build_weighing_components()` retorna una cara para el plano fijo y una para la cara superior móvil, sin espesor. Su argumento `height_mm` permite ajustar la cota al medir el kit en vacío. `build_weighing_clearance()` retorna aparte un sólido de reserva de 120 × 120 × 37 mm con origen inferior y centro XY en cero. El STEP de esta carpeta contiene únicamente las dos superficies de referencia. La reserva sirve para detectar obstáculos fijos y queda fuera del STEP comercial de referencia. Las placas, el puente, el arnés y los elementos de montaje OEM podrán sustituir estas interfaces cuando se disponga de su geometría medida.

## Criterios de montaje y validación

- Apoyar el módulo sobre una base estructural plana y rígida bajo los apoyos OEM. Sujetar el módulo por su lado fijo si se necesita retención. Los topes externos de la base deben permitir extraerlo y no invadir la trayectoria de la placa móvil. Confirmar con la muestra la altura de los topes y la retención de transporte. Conservar el ensamblaje OEM y sus tornillos.
- La bandeja ampliada necesita retención contra levantamiento por carga excéntrica. El kit libre de 293 g ofrece aproximadamente 0,17 N·m de restitución si su centro de masa está centrado y el borde de apoyo está a 60 mm. Una carga de ensayo de 2 kg a 135 mm del centro produciría 1,47 N·m alrededor de ese mismo borde. Un soporte de base extraíble puede prever mordazas ajustables al ala fija de la base OEM. Medir dicha ala y los pies para definir su geometría y confirmar la separación frente a la placa móvil.
- Apoyar el adaptador de bandeja solo sobre la placa móvil. Dejar espacio para su movimiento, flexión y desmontaje frente a paredes, bandeja fija, juntas, cables y protector de derrames. La carcasa debe absorber las cargas de la puerta. Cualquier protección contra salpicaduras fija debe mantener luz respecto del conjunto móvil en todo el recorrido.
- Orientar el extremo del arnés hacia el corredor de cableado, dejar bucle de servicio y anclar el alivio de tracción a la estructura fija. Verificar que ni el arnés ni su guía transmitan tracción a la placa móvil. Medir cable, terminación y espacio de desconexión antes de fijar la apertura.
- Mantener el total de la carga aplicada en 5 kg como máximo, contando el adaptador, el plato y su contenido. La tara es un ajuste de la lectura. El fabricante no publica para este kit el momento admisible ni la superficie admisible de una bandeja ampliada. A modo de carga de ensayo, 2 kg colocados a 135 mm del centro ejercen un momento de 2,65 N·m alrededor de ese centro. El momento respecto del extremo de carga del puente se determinará con su ubicación real.
- Antes de usar el módulo con un plato grande, ensayar repetibilidad con masas conocidas en el centro y en posiciones excéntricas representativas. Verificar retorno a cero, ausencia de contacto o basculación y deriva después de ciclos de vapor. Registrar dimensiones y luces con el módulo vacío y bajo carga. Esta verificación física también debe confirmar si el adaptador requiere retención propia.

Se propone alimentar el kit a 3,3 V para trabajar en el dominio lógico de la ESP32-S3. El manual indica 4 mA típicos y 5 mA máximos a 3,3 V, velocidad UART 38 400 bit/s y GND/VDD/TXD/RXD. La integración electrónica debe validar niveles UART bajo esa alimentación y los detalles del conector. Véase la guía para las condiciones del proveedor.

## Fuentes y disponibilidad de CAD

| Fuente | Formato y registro |
|---|---|
| [Manual del usuario BMH12M205 Rev. 1.00, 31 julio 2024](https://www.bestmodulescorp.com/en/amfile/file/download/file/2030/product/1300/) | PDF oficial consultado, pp. 3–6. El sitio entregó una página intermedia en las descargas directas y no se guardó ese HTML como PDF. |
| [Ficha comercial BMH12M205](https://www.bestmodulescorp.com/en/bmh12m205.html) | Página oficial, referencia del kit, lista de descargas y altura de 36,4 mm. Las descargas públicas listadas corresponden a guías y software. |
| [Manual de la primera generación BMH12M105 Rev. 1.10](https://www.bestmodulescorp.com/en/amfile/file/download/file/896/product/1091/) | PDF oficial, p. 10, confirma 36,4 mm para la primera generación. La coincidencia con la ficha de segunda generación queda pendiente de aclaración. |
| [Catálogo Best Modules de selección BMduino 2024](https://www.bestmodulescorp.com.cn/pub/media/amasty/amfile/attach/BMduino_SG_SC_V4.pdf) | PDF oficial, p. 13, refuerza la altura nominal de 30,7 mm. |
| [Ejemplo de conexión en el repositorio oficial](https://github.com/BestModules-Libraries/BMH12M205/blob/adf1eab2195b76263274a646036e4ce54f2b1839/examples/readWeight/layout.png) | PNG original en `sources/` con el archivo de licencia del repositorio. SHA-256 `3385e70661ba5bdd461f5163e908bb6bf0ac3a0f5f444685f85c4f56716e428d`. Confirma disposición visual y salida del arnés, sin escala. |
| [Hoja de datos BMH01105-1](https://www.bestmodulescorp.com/en/amfile/file/download/file/2115/product/1205/) | PDF oficial del sensor citado para el protocolo. No se usó su geometría en el modelo. |

La búsqueda del número exacto de parte en el fabricante, su repositorio y las bibliotecas técnicas SnapMagic, Ultra Librarian, TraceParts, 3D ContentCentral y GrabCAD no localizó un CAD comercial compatible. El archivo STEP de esta carpeta se generó a partir de los datums publicados y se identifica como referencia parcial.

## Comprobación del archivo CAD

El STEP se reimportó con CadQuery 2.6.1. Las dos caras son válidas, cada una mide 120 × 120 mm y sus cotas Z se conservan en 0 y 30,7 mm. La reserva generada aparte es un sólido válido de 532 800 mm³. La validación física del kit sigue pendiente.
