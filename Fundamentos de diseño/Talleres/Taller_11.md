# Taller 11 - FoodScan: esquema eléctrico y modelo 3D

**Equipo 10 · Fundamentos de Diseño · Actualizado el 12 de noviembre de 2026**

## Entregables

| Trabajo | Documento / enlace |
|---|---|
| Modelo 3D vigente | [FoodScan v3 en STEP](../../Proyecto/MóduloMecánico/CAD/FoodScan_Conjunto_Completo_v3.step) |
| Cómo abrir el modelo | [Onshape, FeatureScript y parámetros](../../Proyecto/MóduloMecánico/README_v3.md) |
| Esquema eléctrico en PDF | [FoodScan v4 con tiras COB](../../output/pdf/FoodScan_Conexiones_v4_COB.pdf) |
| Electrónica editable | [Esquema v4 en EasyEDA Standard](../../Proyecto/MóduloElectrónico/EasyEDA/FoodScan_Esquematico_EasyEDA_Standard_v4_COB.json) y [guía de conexiones](../../Proyecto/MóduloElectrónico/README_v4.md) |
| Informe técnico corregido | [Entregable 2: corrección electrónica del 04/11/2026](../Entregables/Informe_Entregable_2_Equipo10_Corregido_v2.pdf) |

## Prototipo

FoodScan integra una ESP32-S3 N16R8, cámara OV5640 (C) independiente, celda de
carga de 5 kg, HX711, iluminación blanca con control MOSFET y detector de puerta.
El modelo vigente define carcasa, puerta, bandeja y ubicación de los módulos.
Sus valores predeterminados son **310 × 300 × 380 mm** (ancho, fondo sin puerta
y alto sin patas), MDF de **3,5 mm** y plato de referencia de **Ø220 mm**.

Onshape regeneró las 92 piezas con los parámetros predeterminados. Los planos
y las figuras del informe del 04/11 corresponden a los bocetos anteriores.

## Archivo histórico: entrega v1 del 28 de octubre de 2026

Los siguientes archivos, imágenes, cotas y comprobaciones corresponden
exclusivamente al modelo anterior.

| Archivo anterior | Enlace |
|---|---|
| Planos acotados v1 | [Conjunto, paneles y detalles de montaje](Taller_11/FoodScan_Planos_acotados_v1.pdf) |
| STEP, STL y vistas v1 | [Documentación mecánica anterior](../../Proyecto/MóduloMecánico/README.md) |
| Paquete descargable v1 | [Modelo y planos S11 anteriores](../../output/mecanica/FoodScan_S11_Modelo_y_Planos.zip) |

![Distribución interior del prototipo](../../Proyecto/MóduloMecánico/Vistas/FoodScan_Interior.png)

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
  explica en las [notas de importación a Pro](../../Proyecto/MóduloElectrónico/EasyEDA/LEEME_Pro.md).

[Especificación técnica y conexiones](../../Proyecto/Especificacion_S11.md).
