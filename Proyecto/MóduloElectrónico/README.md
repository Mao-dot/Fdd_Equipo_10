# Módulo electrónico de FoodScan

Esquema de interconexión del prototipo del Equipo 10, basado en la
[especificación técnica de S11](../Especificacion_S11.md), que resume las
conexiones definidas por el equipo en `componentes.md`, versión 1.1.
Revisión 1.0 del esquema: **22 de octubre de 2026**.

## Archivos entregados

| Archivo | Uso |
|---|---|
| [FoodScan_Esquematico_v1.json](EasyEDA/FoodScan_Esquematico_v1.json) | **Esquema editable nativo de EasyEDA Standard**. Abrir/importar en el editor. |
| [FoodScan_Pro_Importado_sin_anotar.epro](EasyEDA/FoodScan_Pro_Importado_sin_anotar.epro) | Copia nativa de Pro del proyecto importado; revisar anotación según [notas de Pro](EasyEDA/LEEME_Pro.md). |
| [FoodScan_Esquematico_v1.pdf](EasyEDA/FoodScan_Esquematico_v1.pdf) | Copia vectorial de una página A3 horizontal, para revisión o entrega. |
| [FoodScan_Esquematico_v1.png](EasyEDA/FoodScan_Esquematico_v1.png) | Vista previa del PDF. |
| [FoodScan_Esquematico_v1.svg](EasyEDA/FoodScan_Esquematico_v1.svg) | Vista vectorial del esquema. |
| [Verificacion_conexiones.json](EasyEDA/Verificacion_conexiones.json) | Resultado de la comprobación local y lista de redes. |
| [BOM.md](BOM.md) | Lista de componentes y correspondencia con el presupuesto. |

El JSON contiene símbolos, pines, cables eléctricos y etiquetas de red editables;
no contiene una imagen incrustada. Los símbolos están incluidos en el archivo,
de modo que no hace falta instalar una biblioteca para abrirlo.

## Abrir en EasyEDA Standard

1. Abrir [EasyEDA Standard](https://easyeda.com/editor).
2. Seleccionar **Archivo → Abrir → EasyEDA...**.
3. Seleccionar `EasyEDA/FoodScan_Esquematico_v1.json`.
4. Mantener **Importar archivo** y pulsar **Importar**.
5. Abrir la hoja `Sheet_1`, si no queda seleccionada automáticamente.
6. Usar **Ver / Ajustar a la pantalla** para localizar el plano. Después se
   puede ampliar la zona necesaria.

Para conservarlo en una cuenta, guardarlo como proyecto propio desde el editor.
El JSON adjunto ya es la copia local editable para compartir con el equipo.
La exportación PDF del editor web puede exigir guardar primero el proyecto;
por eso se incluye también una copia PDF generada localmente.

## Abrir en EasyEDA Pro

Usar la función **Importar EasyEDA (Standard Edition)** y seleccionar el mismo
JSON. La documentación de Pro admite archivos Standard tanto JSON como ZIP.
También se incluye una copia nativa `.epro` guardada desde EasyEDA Pro 3.2.209.
Conserva 34 componentes; la importación deja referencias provisionales como
`R?` y `U?`. Revisar su anotación y la visibilidad de referencias y valores
antes de usar esa copia como versión final. No se realizó ERC oficial en Pro.

Referencia oficial: [Import EasyEDA Standard Edition](https://prodocs.easyeda.com/en/import-export/import-easyeda/).

La [entrega del Taller 11](../../Fundamentos%20de%20diseño/Talleres/Taller_11.md)
reúne el PDF del esquema, los planos acotados y el enlace del modelo en Onshape.

## Qué representa la hoja

1. **Alimentación:** adaptador externo de 5 V / 2.4 A, jack de centro positivo,
   fusible F1 de 1.5 A, interruptor SW1 y condensadores C1/C2.
2. **Control:** ESP32-CAM AI-Thinker U1, con cámara OV2640, PSRAM y regulador
   integrados. El dibujo muestra los seis terminales utilizados del módulo.
3. **Pesaje:** módulo HX711 U2 alimentado a 3.3 V y celda LC1 de cuatro hilos.
4. **Puerta:** microswitch SPDT SW2, contacto COM a GND, NO a GPIO15 y R13
   de 10 kΩ a 3.3 V. NC queda sin conectar. La posición dibujada es sin accionar;
   al cerrar la puerta, el mecanismo debe accionar COM–NO.
5. **Iluminación:** doce ramas paralelas, cada una con su propia resistencia
   de 100 Ω y un LED blanco. Se encienden con el interruptor general.

Las etiquetas iguales corresponden a la misma conexión aunque no haya un cable
largo entre los bloques: `+5V`, `+3V3`, `GND`, `HX_DOUT`, `HX_SCK` y `DOOR_N`.

| Origen | Destino |
|---|---|
| +5 V después de F1 y SW1 | U1 `5V`, C1/C2 e iluminación |
| U1 `3V3` | U2 `VCC` y extremo superior de R13 |
| U1 `GPIO13` | U2 `DT` / `DOUT` |
| U1 `GPIO14` | U2 `SCK` / `PD_SCK` |
| U1 `GPIO15` | SW2 `NO` y extremo inferior de R13 |
| U2 `E+`, `E−` | LC1 excitación positiva y negativa |
| U2 `A+`, `A−` | LC1 señal positiva y negativa |
| GND | Masas de alimentación, U1, U2, LED y SW2 `COM` |

Los identificadores de los pines de U1/U2 corresponden a su función o serigrafía,
no a una numeración de pads para PCB. Los módulos se representan con símbolos
funcionales propios; no se reproduce su electrónica interna. En U2 se muestran
los terminales utilizados; el canal B queda sin usar. En LC1 se representa el
puente completo como bloque funcional, sin asignar colores de cables.

## Montaje y límites

- Confirmar **centro positivo** en el adaptador recibido antes de conectar J1.
- Conectar por las etiquetas de la placa real. No aplicar 5 V a `3V3` ni a GPIO.
- Confirmar que el módulo HX711 concreto funcione a 3.3 V, como el seleccionado
  en `componentes.md`.
- Identificar los hilos de LC1 con la ficha o mediciones; los colores pueden variar.
- Mantener C1/C2 cerca de la alimentación de U1 y cables cortos en la celda.
- Dejar la microSD sin usar y el flash de GPIO4 apagado en firmware.
- GPIO15 es un pin de configuración de arranque. Probar el encendido con puerta
  abierta y cerrada; un nivel bajo puede silenciar los mensajes iniciales de ROM.
- Usar la fuente externa y la base USB-MB por separado. Desconectar la fuente
  externa antes de programar. La base MB es un accesorio de mantenimiento y
  no está incluida como circuito permanente en esta hoja.
- La captura, tara, calibración y comunicación requieren firmware. Este esquema
  no demuestra funcionamiento físico ni precisión de pesaje.
- El diseño es un **esquema de interconexión para el prototipo**, sin huellas
  de PCB, ruteo ni modelos de simulación. No produce Gerber de fabricación.

## Verificación realizada

- Se importó el JSON en **EasyEDA Standard web 6.5.60** y se observó la hoja
  completa con los cinco bloques, símbolos, cables y etiquetas.
- El generador comprobó **34 componentes y 25 redes**, incluidos el contacto
  NC libre y las doce conexiones intermedias resistencia–LED. El recuento de
  terminales y la lista de redes se encuentran en `Verificacion_conexiones.json`.
- La comprobación local pasó: alimentación y GPIO según la documentación,
  ninguna unión entre redes de distinto nombre y únicamente SW2.NC aislado.
  Es una comprobación de conectividad del archivo, no un ERC oficial de EasyEDA
  ni una prueba eléctrica del montaje.
- El PDF se generó con ReportLab a partir de la vista del mismo JSON; se
  rasterizó con Poppler y se revisó visualmente. No se exportó desde una cuenta
  de EasyEDA ni se guardó un proyecto en la nube.

## Reproducir los archivos

El esquema se generó por código con la especificación abierta de EasyEDA Std:

```powershell
python .\generar_esquema.py
python .\exportar_pdf.py
pdftoppm -scale-to 2200 -singlefile -png .\EasyEDA\FoodScan_Esquematico_v1.pdf .\EasyEDA\FoodScan_Esquematico_v1
```

El primer script usa solamente la biblioteca estándar de Python. El segundo
requiere `reportlab`; `pdftoppm` pertenece a Poppler. Si se cambia el JSON dentro
de EasyEDA, volver a exportar sus vistas desde el editor: ejecutar el generador
reemplaza el esquema con el diseño definido en el script.

## Referencias técnicas

- [Formato oficial EasyEDA Standard](https://github.com/easyeda/easyeda-std-file-format).
  Especificación y ejemplo descargados en `referencias/` para consultar el formato.
- [Pines de cámara de Espressif, CAMERA_MODEL_AI_THINKER](https://github.com/espressif/arduino-esp32/blob/master/libraries/ESP32/examples/Camera/CameraWebServer/camera_pins.h).
- [Espressif: selección del modo de arranque y GPIO15](https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html).
- Modelos, valores y presupuesto: [`componentes.md`](../../componentes.md).
