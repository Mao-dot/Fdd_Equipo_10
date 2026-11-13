# FoodScan: corrección del esquemático y componentes

**Equipo 10 · Fundamentos de Diseño · 4 de noviembre de 2026**

Entrega de la revisión electrónica 2 para levantar las observaciones y llevar
las piezas al taller. El modelo 3D no se modifica en esta etapa.

| Entregable | Enlace |
|---|---|
| Informe técnico corregido | [Informe del Entregable 2, revisión v2](../Entregables/Informe_Entregable_2_Equipo10_Corregido_v2.pdf) |
| Lista de componentes | [BOM v2](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/BOM_v2.md) |
| Lista ampliada de compra y funcionamiento | [Componentes_v2.md](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/Componentes_v2.md) |
| Esquemático PDF A3 | [FoodScan_Esquematico_v2.pdf](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/output/pdf/FoodScan_Esquematico_v2.pdf) |
| Esquemático editable EasyEDA Standard | [FoodScan_Esquematico_v2.json](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/EasyEDA/FoodScan_Esquematico_v2.json) |
| Instrucciones de apertura y alcance | [README v2](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/README_v2.md) |
| Comprobación local de conexiones | [Verificacion_conexiones_v2.json](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/EasyEDA/Verificacion_conexiones_v2.json) |
| Paquete para compartir | [FoodScan_Electronica_Corregida_v2.zip](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/output/electronica/FoodScan_Electronica_Corregida_v2.zip) |

Se sustituye la ESP32-CAM por una ESP32-S3 N16R8 y una cámara Waveshare OV5640
Camera Board (C) independiente; se añade Q1 con sus resistencias para controlar
la iluminación y C3/C4 junto a la cámara. Se conservan celda de 5 kg, HX711,
microswitch, tres paneles LED y el funcionamiento con app/Gemini por Wi-Fi.

La revisión representa **40 componentes y 44 redes**. La comprobación local del
archivo y la revisión visual del PDF no equivalen a ERC oficial ni a pruebas
eléctricas. La conversión/importación del JSON v2 en EasyEDA Pro y las pruebas
con las piezas deben verificarse en el taller.

Para comenzar: llevar placa N16R8, cámara y conexión P1, HX711, celda de carga,
microswitch, fuente, cable USB de programación y material de conexión. Añadir
LED, resistencias y Q1 para probar el encendido desde el microcontrolador.
