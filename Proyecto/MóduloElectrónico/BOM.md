# FoodScan · Lista de componentes del rediseño

FoodScan pesa y fotografía el plato en la misma operación. La pantalla muestra
el peso neto y el estado de la captura. La aplicación usa la foto y el peso
para estimar los nutrientes.

## Electrónica

| Cantidad | Componente | Función y estado |
|---:|---|---|
| 1 | ESP32-S3-DevKitC-1 N16R8 | Placa disponible en el equipo. Coordina pesaje, iluminación, captura y comunicación por Wi-Fi. |
| 1 | **Adafruit OV5640 Camera Breakout 5838, 5 MP, lente de 120° con autofoco** | Cámara superior seleccionada para compra. Reemplaza la Waveshare OV5640 (C) de las revisiones anteriores. [Ficha de Adafruit](https://www.adafruit.com/product/5838). |
| 1 | Celda de carga de barra de 5 kg | Mide la carga sobre la plataforma de pesaje. |
| 1 | Módulo HX711 | Convierte la señal de la celda en una lectura de peso. |
| 1 | Microswitch de puerta | Detecta el cierre de la puerta antes de la captura. |
| 4 | Tiras LED COB blancas de 5 V, 4000 K, 200 mm por tira | Iluminan el plato desde las esquinas. Los difusores ayudan a reducir reflejos y sombras. |
| 1 | Pantalla frontal | Muestra los gramos netos y mensajes como «Cierra la puerta», «Peso estable» y «Capturando». Modelo por definir. |
| 1 conjunto | Fuente externa regulada de 5 V, interruptor general y protección | Alimenta y protege el equipo. La fuente de referencia de la entrega anterior es de 4,8 A. Confirmar la capacidad con la carga del rediseño. |
| 1 conjunto | Etapa de control de luces y material de montaje electrónico | Permite encender las tiras durante la captura y fijar los módulos dentro de la caja. |

## Piezas mecánicas principales

| Cantidad | Pieza | Función y estado |
|---:|---|---|
| 1 conjunto | Carcasa, puerta y plataforma de pesaje | Sostienen el plato y los módulos. El diseño de la plataforma debe dejarla libre de contacto con la carcasa durante el pesaje. |
| 1 | Soporte ajustable de cámara | Permite centrar la cámara sobre el plato y ajustar la altura durante las pruebas. |
| 4 | Perfiles de esquina con difusor opal | Sostienen y difunden las tiras COB. |
| 1 | Ventana transparente lavable para la cámara | Aísla la cámara del vapor y las salpicaduras. Se monta sellada al marco y accesible para limpieza. |
| 1 | Salida alta de vapor con deflector opaco | Dirige el vapor hacia la parte posterior y limita la entrada de luz ambiente. |
| Opcional | Calentador suave para el borde de la ventana | Se evaluará si la ventana se empaña en las pruebas con comida caliente. |

Probar el encuadre y el enfoque con un plato de referencia de 22 cm a unos
29 cm de la lente, con las luces y la ventana instaladas. Repetir la captura
con comida caliente para revisar condensación, reflejos y nitidez antes de
fijar la altura del soporte.

El esquema eléctrico y el modelo 3D del rediseño están pendientes. El
[esquema v4](README_v4.md) y la [BOM v2](BOM_v2.md) documentan montajes
anteriores con la cámara Waveshare.
