# FoodScan: corrección electrónica, revisión 2

**Equipo 10 · Fundamentos de Diseño · 4 de noviembre de 2026**

Corrección del esquemático y de la lista de componentes para llevar al taller.
Utiliza una ESP32-S3-DevKitC-1 N16R8, una cámara Waveshare OV5640 Camera Board (C)
independiente y un MOSFET para encender las luces desde la app. Se conservan
celda de carga, HX711, microswitch y tres paneles de cuatro LED. Las órdenes y
los datos se transmiten por Wi-Fi; la app FoodScan existente consulta Gemini
mediante Internet. El modelo 3D permanece en la revisión anterior.

## Archivos para revisar y presentar

| Archivo | Uso |
|---|---|
| [BOM.md](BOM.md) | Lista nueva: 40 componentes representados, accesorios y conexiones. |
| [lista ampliada](Componentes_v2.md) | Lista ampliada de compra, funcionamiento, mapa GPIO y presupuesto. |
| [FoodScan_Esquematico_v2.json](EasyEDA/FoodScan_Esquematico_v2.json) | Esquema editable nativo de EasyEDA Standard. |
| [FoodScan_Esquematico_v2.pdf](EasyEDA/FoodScan_Esquematico_v2.pdf) | Una hoja A3 horizontal para revisar o imprimir. |
| [FoodScan_Esquematico_v2.svg](EasyEDA/FoodScan_Esquematico_v2.svg) | Copia vectorial de la misma hoja. |
| [FoodScan_Esquematico_v2.png](EasyEDA/FoodScan_Esquematico_v2.png) | Vista previa del PDF. |
| [Verificacion_conexiones_v2.json](EasyEDA/Verificacion_conexiones_v2.json) | Lista de redes y comprobaciones locales de conectividad. |

Los bloques de módulos contienen terminales y cables editables; no son una
imagen incrustada. Las etiquetas de red iguales unen bloques. Las referencias
son U1, CAM1, U2, LC1, SW1/SW2, J1, F1, C1-C4, R1-R15, D1-D12 y Q1.
No se asignan huellas de PCB ni se generan Gerber.

## Cambios eléctricos

- U1: sustituye la ESP32-CAM AI-Thinker por una DevKitC-1 N16R8 con PSRAM.
- CAM1: cámara separada de 5 MP y autofocus; conexión P1 de 18 contactos,
  mediante DVP y SCCB. P1.18/PWDN queda sin conexión externa, por el puente
  interno a GND del módulo publicado. Se necesitan 17 conexiones externas.
- Q1/R14/R15: AO3400A, compuerta con 100 ohm y descarga de 100 kohm. Conmutan
  el retorno de los doce LED; quedan apagados durante el arranque.
- C3/C4: desacoplo adicional de 100 uF/10 V y 100 nF junto a la cámara.
- GPIO: asignación nueva para la S3; se evitan memoria, USB, UART y straps.
- Alimentación base: adaptador externo 5 V/2.4 A; U1 regula a 3.3 V para
  cámara y HX711. Medir este rail durante Wi-Fi/autofocus y comprobar temperatura.
  La opción de batería no está seleccionada.

La máquina mantiene la tara del plato vacío al retirarlo, espera puerta cerrada
y peso estable, enciende luces y registra foto y gramos asociados. Al terminar
o fallar, las luces se apagan y U1 queda en espera. SW1 corta la alimentación
manualmente. El autofocus y reposo de CAM1 requieren firmware.

## Abrir el editable

En **EasyEDA Standard**, usar Archivo/Abrir/EasyEDA y seleccionar el JSON v2;
ajustar la vista a la hoja. Guardarlo como proyecto propio si se desea editar
en una cuenta. En **EasyEDA Pro**, usar la importación de EasyEDA Standard y
revisar las referencias y valores después de convertirlo.

La importación de la revisión 2 en la aplicación y el ERC oficial no se han
ejecutado en esta entrega local. El archivo `.epro` existente y
[LEEME_Pro.md](EasyEDA/LEEME_Pro.md) corresponden exclusivamente a la versión 1;
no contienen estas correcciones.

## Comprobaciones realizadas

El generador comprueba **40 componentes y 44 redes**, el mapa de los 18
terminales P1, los GPIO empleados, las ramas individuales de LED y la etapa
MOSFET. Confirma que no hay unión entre redes con nombres distintos y que los
únicos terminales sin conexión externa son CAM1.18 y SW2.NC.

La vista SVG se genera con los mismos símbolos del JSON; el PDF se obtiene de
esa vista y se renderiza a PNG para revisión visual. Son comprobaciones del
archivo, no ensayos eléctricos ni de precisión de pesaje. Se deben llevar al
taller las piezas para verificar alimentación, cámara, enfoque, luces, puerta,
comunicación, calibración y repetibilidad.

## Reproducir sin cambiar la versión 1

```powershell
python .\generar_esquema_v2.py
python .\exportar_pdf_v2.py
pdftoppm -scale-to 2600 -singlefile -png .\EasyEDA\FoodScan_Esquematico_v2.pdf .\EasyEDA\FoodScan_Esquematico_v2
```

El generador reutiliza las funciones de dibujo de `generar_esquema.py`, sin
ejecutar ni sobrescribir su salida v1. La exportación reutiliza el pintor de
`exportar_pdf.py` y requiere ReportLab; Poppler sirve para rasterizar. Conservar
cualquier edición manual antes de regenerar los archivos v2.

## Fuentes técnicas

- [Esquema de cámara Waveshare, cabecera P1](https://files.waveshare.com/upload/1/1e/OV5640-Camera-Board-Schematic.pdf).
- [ESP32-S3-DevKitC-1: conexiones y variantes](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html).
- [Controlador de cámara y autofocus de Espressif](https://github.com/espressif/esp32-camera).
- [AO3400A, Alpha & Omega Semiconductor](https://www.aosmd.com/res/data_sheets/AO3400A.pdf).
- [Formato EasyEDA Standard](https://github.com/easyeda/easyeda-std-file-format) y [conversión a Pro](https://prodocs.easyeda.com/en/import-export/import-easyeda/).
