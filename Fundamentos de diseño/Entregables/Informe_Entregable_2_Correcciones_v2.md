# Correcciones del informe técnico FoodScan

**Equipo 10 · Revisión electrónica 2 · 4 de noviembre de 2026**

Se corrigió el [informe del Entregable 2](Informe_Entregable_2_Equipo10_Corregido_v2.pdf), conservando las 40 páginas, el índice, la investigación, las alternativas A/B y la numeración de tablas y figuras. El PDF original de octubre se conserva sin modificar. Existe una copia idéntica de la revisión en `Presentaciones de Proyecto` y en `output/pdf`.

| Páginas | Corrección |
|---|---|
| 1 | Fecha e identificación de la revisión electrónica. |
| 14, 18 | Energía base de 5 V por jack; batería no seleccionada. Wi-Fi previsto, integración pendiente. |
| 20–22 | Tara con plato vacío, conservación al retirarlo, orden Registrar, puerta y peso estable, iluminación, enfoque, captura, transmisión, análisis, apagado de luces y espera. Calibración separada de tara. |
| 24–25, 27 | Placa ESP32-S3-DevKitC-1 N16R8 y cámara independiente Waveshare OV5640 Camera Board (C), 5 MP AF; sustitución de compatibilidad y mapa GPIO antiguos. |
| 30–31 | Leyenda de componentes, Q1 AO3400A y resistencias de control, desacoplo, alimentación y asignación resumida de GPIO. |
| 31–34 | Vistas mecánicas identificadas como bocetos previos; no se modifica el modelo 3D. |
| 38 | Justificación del concepto C actualizada. S/ 150 corresponde solo a placa y cámara; total por cotizar. Puntajes de Pugh conservados como comparación conceptual. |
| 40 | Fuentes de Espressif, Waveshare y AO3400A; documentación electrónica v2. |

La referencia para esta corrección es [Componentes_v2.md](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/Componentes_v2.md), junto con la [BOM v2](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/BOM_v2.md) y el [esquemático v2](https://github.com/Mao-dot/Fdd_Equipo_10/blob/de536443a028184165824cff16a31466040ab7d6/Proyecto/M%C3%B3duloElectr%C3%B3nico/EasyEDA/FoodScan_Esquematico_v2.pdf).

La revisión distingue el diseño propuesto de las pruebas realizadas: quedan pendientes montaje, calibración, captura/autofocus, consumo y temperatura, firmware e integración automática con la app. Gemini y el cálculo con TPCA se conservan en el backend existente.

## Reproducción y revisión

El script [corregir_informe_v2.py](../../scripts/corregir_informe_v2.py) genera el PDF a partir del original y conserva los bocetos existentes. Requiere Python con ReportLab, PyMuPDF y las fuentes Times New Roman de Windows. El manifiesto [Informe_Corregido_v2_verificacion.json](../../output/pdf/Informe_Corregido_v2_verificacion.json) registra el original, su SHA-256, las páginas intervenidas y las copias generadas.

Se comprobaron el texto y las conexiones contra la lista v2 y se revisó la representación visual del PDF. Estas comprobaciones documentales no equivalen a validación física del prototipo.
