# Verificación geométrica de FoodScan

**Estado de entrega** · Revisión para prototipo, medición de componentes y desarrollo en Onshape.

## Comprobaciones ejecutadas

| Ensayo | Método y resultado |
| --- | --- |
| Sólidos en el ensamblaje cerrado | CadQuery/OCP comprobó 260 instancias y 654 sólidos, sin B-Rep inválidas ni choques estructurales por encima de 0,05 mm³. Registró tres contactos de 0,2819 mm³ en la rosca nominal del OLED. [Datos](geometria.json) |
| Giro de puerta | 16 posiciones entre 0° y 105° con pestillo desbloqueado. Sin intersecciones volumétricas entre piezas móviles y fijas en las muestras evaluadas. El giro continuo y la flexión de la junta se ensayan en el prototipo. |
| Inserción de plato | Barrido continuo de un cilindro Ø270 × 24 hasta el centro de pesaje con la puerta abierta a 105°. Sin interferencias a Z=38,2 ni a Z=43,9, alturas calculadas con las dos cotas publicadas del BMH12M205. Holguras nominales de 10 mm por lado en el vano y 14 mm hacia el panel trasero. |
| Alineación de fijaciones | Se compararon 81 ejes de tornillos M3 con el centro de sus tuercas. El desfase radial nominal calculado fue 0,0 mm. La comprobación de volumen común incluye el paso de las fijaciones por las piezas. |
| Aislamiento geométrico de pesaje | La bandeja tiene 16,7 mm de separación mínima a las piezas fijas modeladas del entorno. El kit se representa por dos superficies y falta comprobar el contacto con los apoyos físicos, el cable y el desplazamiento bajo carga. |
| Cámara y ventana | 287,8 mm nominales entre lente y borde del plato. Un cono simétrico de 120° con lente en la posición alta de ajuste deja 2,57 mm de margen radial teórico en el plano inferior del vano. Medir el eje óptico y comprobar el encuadre con el vidrio y el enfoque reales. |
| DXF y STL | Se releyeron 10 DXF con ezdxf, en milímetros, con contornos de origen cerrados. Los 21 STL se comprobaron por arista compartida y recuento de triángulos. [Datos de fabricación](fabricacion.json) |
| Reimportación independiente | FreeCAD 1.1.4 importó 660 objetos en cada configuración, entre ellos seis superficies, y reabrió ambos FCStd con B-Rep válidas. La comparación de cotas tras reabrir usa tolerancia absoluta de 0,002 mm en la envolvente. [Cerrado](FoodScan_cerrado_freecad.json) · [Abierto](FoodScan_abierto_freecad.json) |

FreeCAD, al descomponer el STEP del OLED, identifica diez contactos internos del propio archivo Waveshare. La fijación con tornillos M2,5 modelados como cilindros nominales también da volumen común con el diámetro menor de tres separadores roscados. Verificar calibre de rosca y profundidad útil sobre la pantalla comprada. El informe conserva los volúmenes de ambos casos.

## Verificaciones antes de fabricar y montar

1. **Pesaje.** La caja contiene superficies de referencia de la base y de la placa móvil del BMH12M205. Medir altura, pies, borde de la base fija, holguras, movimiento bajo carga y la salida del cable. Comprobar repetibilidad, retorno a cero y estabilidad con carga excéntrica. La bandeja debe apoyar solo en la placa móvil.
2. **Cámara y arneses.** Medir la posición del eje, altura de cabeceras y volumen del FPC montado en el 5838. Medir USB y pines de la ESP32-S3 disponible. Comprobar los espacios de enchufe, extracción y curvatura con los conectores elegidos. Sustituir la reserva del PCB por el STEP real.
3. **Luminaria y condensación.** Los perfiles se ajustaron al CAD del fabricante. El difusor y los clips requieren una muestra montada. Medir el espesor de la tira y comprobar el anclaje, la protección de cables, la uniformidad de iluminación, las temperaturas y la limpieza. Probar empañamiento y reflejos con comida caliente y la ventana montada.
4. **Pantalla, puerta y alimentación.** Confirmar tornillos del OLED, agarre de los pulsadores, retención axial de los pasadores y carrera del accionador P39. Evaluar la placa de alimentación P09a y sus protecciones después de validar la selección eléctrica en banco.
5. **Primera fabricación.** Confirmar espesores, planitud, kerf y ajuste de herrajes con probetas. Repetir la revisión al importar en Onshape y añadir las relaciones de movimiento requeridas allí.
