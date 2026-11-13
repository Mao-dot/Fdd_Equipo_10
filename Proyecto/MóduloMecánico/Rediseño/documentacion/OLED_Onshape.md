# Waveshare 25742 en Onshape

Onshape marcó la instancia E03 al importar `FoodScan_cerrado.step`. La comprobación exacta de OpenCascade detectó problemas de curvas sobre superficies en 55 de los 165 sólidos del STEP OEM. Incluyen cuatro separadores roscados, el seguro del conector flexible, el conector lateral y 49 microrrelieves. Reparar la parametrización de las curvas en memoria dio resultados que se perdían al volver a exportar e importar el STEP.

La variante de intercambio conserva 110 sólidos OEM intactos, entre ellos el PCB, el módulo de pantalla y las cabeceras. Dos recortes localizados en los conectores quitan menos de 0,001 mm³ por componente. Los cuatro separadores conservan la cara de apoyo, el hombro y los centros de montaje del original. La hélice interna se representa mediante un taladro nominal Ø2,5 con bocas Ø2,8. Los 49 microrrelieves se omiten. El original del fabricante permanece archivado con su SHA-256.

Importar el [STEP cerrado para Onshape](../exports/step/FoodScan_cerrado_Onshape.step) como un único documento. Para ver la puerta abierta, usar la [variante abierta](../exports/step/FoodScan_abierto_Onshape.step). El [STEP de E03 por separado](../exports/step/E03_Waveshare_25742_mecanico.step) usa las coordenadas del ensamblaje. El generador es `python -m cad_model.oled_onshape`. [Datos de verificación](../exports/validacion/OLED_Onshape.json)

Las comprobaciones de topología y montaje son locales en OpenCascade. La aceptación del archivo por el traductor de Onshape se confirma al importarlo allí.
