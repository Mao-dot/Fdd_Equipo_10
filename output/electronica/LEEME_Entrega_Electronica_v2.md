# FoodScan: electrónica corregida v2

4 de noviembre de 2026. Entrega de esquemático y componentes, sin modificar el modelo 3D.

Extraer el ZIP conservando su estructura de carpetas.

1. Leer `componentes.md` para comprar las piezas y `Proyecto/MóduloElectrónico/BOM.md` para las referencias del esquema.
2. Abrir `Proyecto/MóduloElectrónico/EasyEDA/FoodScan_Esquematico_v2.pdf` para revisar o imprimir la hoja A3.
3. Importar `Proyecto/MóduloElectrónico/EasyEDA/FoodScan_Esquematico_v2.json` en EasyEDA Standard. En Pro usar la importación de Standard y revisar referencias y valores.
4. Revisar `README_v2.md` en el módulo electrónico para fuentes, reproducción y alcance de las comprobaciones.
5. Abrir `Fundamentos de diseño/Entregables/Informe_Entregable_2_Equipo10_Corregido_v2.pdf` para el informe actualizado. El registro de cambios está junto al PDF; el original y `scripts/corregir_informe_v2.py` permiten reproducir la revisión.

La comprobación local pasa con 40 componentes y 44 redes. El esquema no tiene huellas PCB ni Gerber y no acredita pruebas físicas o ERC oficial. El archivo Pro de la entrega anterior no forma parte de esta revisión.

La cámara elegida es Waveshare OV5640 Camera Board (C), SKU 13802. P1 es una cabecera de 18 contactos; P1.18/PWDN queda sin conexión externa. El flash se mantiene apagado y el autofocus requiere firmware. Las conexiones de cámara y sensores son internas; los datos se transmiten por Wi-Fi. La alimentación base es externa, de 5 V / 2.4 A; batería sin seleccionar.
