# Taller 11 - FoodScan: esquema eléctrico y modelo 3D

**Equipo 10 · Fundamentos de Diseño · Actualizado el 12 de noviembre de 2026**

## Rediseño

- [Ensamblaje 3D para Onshape](../../Proyecto/MóduloMecánico/Rediseño/exports/step/FoodScan_cerrado_Onshape.step) y [documentación mecánica](../../Proyecto/MóduloMecánico/Rediseño/README.md).
- [Esquemático y PCB editables en EasyEDA Pro](../../Proyecto/MóduloElectrónico/Rediseño_FoodScan/easyeda/FoodScan.epro2) y [guía de la revisión A](../../Proyecto/MóduloElectrónico/Rediseño_FoodScan/README.md).
- [Lista de componentes del rediseño](../../Proyecto/MóduloElectrónico/BOM.md).

## Entregables anteriores

| Trabajo | Documento / enlace |
|---|---|
| Esquema eléctrico en PDF | [FoodScan v4 con tiras COB](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/output/pdf/FoodScan_Conexiones_v4_COB.pdf) |
| Electrónica editable | [Esquema v4 en EasyEDA Standard](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/EasyEDA/FoodScan_Esquematico_EasyEDA_Standard_v4_COB.json) y [guía de conexiones](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/README_v4.md) |
| Informe técnico corregido | [Entregable 2: corrección electrónica del 04/11/2026](../Entregables/Informe_Entregable_2_Equipo10_Corregido_v2.pdf) |

## Prototipo de la entrega anterior

La entrega usaba una ESP32-S3 N16R8, cámara Waveshare OV5640 (C), celda de
carga de 5 kg, HX711, cuatro tiras COB y detector de puerta. Su modelo de
referencia medía **310 × 300 × 380 mm** (ancho, fondo sin puerta y alto sin
patas), con MDF de **3,5 mm** y plato de **Ø220 mm**. Los planos y las figuras
del informe del 04/11 corresponden a bocetos anteriores.

## Archivo histórico: entrega v1 del 28 de octubre de 2026

Los siguientes archivos, imágenes, cotas y comprobaciones corresponden
exclusivamente al modelo anterior.

| Archivo anterior | Enlace |
|---|---|
| Planos acotados v1 | [Conjunto, paneles y detalles de montaje](Taller_11/FoodScan_Planos_acotados_v1.pdf) |
| STEP, STL y vistas v1 | [Documentación mecánica anterior](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloMec%C3%A1nico/README.md) |
| Paquete descargable v1 | [Modelo y planos S11 anteriores](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/output/mecanica/FoodScan_S11_Modelo_y_Planos.zip) |

![Distribución interior del prototipo](https://raw.githubusercontent.com/Mao-dot/Fdd_Equipo_10/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloMec%C3%A1nico/Vistas/FoodScan_Interior.png)

El cuerpo propuesto mide **320 × 320 × 350 mm**, con plataforma de
**220 × 220 mm** y cámara superior orientada al plato. Los planos incluyen
las dimensiones del conjunto, el despiece de paneles y los detalles de pesaje.

### Alcance y comprobaciones de v1

- Esquema de interconexión de 34 componentes y 25 redes, con verificación local.
- Modelo CAD de 79 sólidos válidos, sin solapes volumétricos en la posición cerrada;
  los archivos STEP se volvieron a leer después de exportarlos.
- Planos vectoriales de tres hojas A3, revisados visualmente.
- Componentes comerciales y soportes de referencia: medidas y taladros pendientes
  de ajuste con las piezas reales. La maqueta no demuestra desempeño físico.
- La copia nativa de EasyEDA Pro conserva referencias provisionales; su estado se
  explica en las [notas de importación a Pro](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/EasyEDA/LEEME_Pro.md).

[Especificación técnica y conexiones](../../Proyecto/Especificacion_S11.md).
