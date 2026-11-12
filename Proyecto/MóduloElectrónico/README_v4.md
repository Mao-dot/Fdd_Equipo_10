# FoodScan: esquema v4 con iluminación COB

**Equipo 10 · 12 de noviembre de 2026**

Esta hoja documenta la entrega anterior con tiras COB y cámara Waveshare OV5640 (C).
La [lista del rediseño](BOM.md) incorpora la cámara Adafruit 5838 y la pantalla frontal.

- [Esquemático editable exportado desde EasyEDA Standard](EasyEDA/FoodScan_Esquematico_EasyEDA_Standard_v4_COB.json).
- [Hoja PDF A3](../../output/pdf/FoodScan_Conexiones_v4_COB.pdf).
- [Vista del esquema en PNG](EasyEDA/FoodScan_Conexiones_v4_COB.png) y [SVG](EasyEDA/FoodScan_Conexiones_v4_COB.svg).
- [Lista de redes verificada](EasyEDA/Verificacion_conexiones_v4.json).

## Iluminación y alimentación

LED1 a LED4 son tiras COB monocolor de dos hilos, 5 V, 4000 K y 200 mm
por esquina. Sustituyen a D1-D12 y a sus resistencias R1-R12. Los positivos
van a +5 V y los negativos a `LED-`, el retorno conmutado por el drenador
de Q1. El GPIO42 controla Q1 a través de R14 y R15 mantiene la compuerta
a GND mientras el GPIO está en alta impedancia.

La entrada es el adaptador WODE WA-24-5 de 5 V CC y 4,8 A especificado en
el modelo. El positivo pasa por J1, el fusible retardado F1 de 3,15 A y
SW1 hasta X1. La placa ESP32 entrega los 3,3 V para la cámara y el HX711.

| Bornera | Polos en el orden del plano |
|---|---|
| X1 | 1 +5 V, 2 GND |
| X2A | 1 LED1+, 2 LED1-, 3 LED3+, 4 LED3- |
| X2B | 1 LED2+, 2 LED2-, 3 LED4+, 4 LED4- |
| X3 | 1 3,3 V, 2 GND, 3 DT (GPIO4), 4 SCK (GPIO2) |
| X4 | 1 DOOR_N (GPIO1 a NO), 2 GND (a COM) |
| X5 | 1 E+, 2 E-, 3 A-, 4 A+ |

La numeración identifica los polos del plano. Verificar el orden físico de
las borneras y la polaridad de cada tira al preparar el cableado. El commit
no especifica la potencia por metro de las tiras. Medir la corriente conjunta
con las cuatro encendidas y comprobar la temperatura de Q1 y la capacidad
del jack, el interruptor, los cables, las borneras y el fusible con esa carga.
[Ficha de Q1 AO3400A](https://www.aosmd.com/res/data_sheets/AO3400A.pdf).

## Abrir y verificar

En EasyEDA Standard, ir a **Archivo → Abrir → EasyEDA…** y elegir el JSON
exportado. Se abrió la hoja en el editor y se verificó que la exportación
conserva las referencias y valores de los 26 componentes, los 106 terminales
y la geometría de las conexiones. Se comprobaron 30 redes conectadas y dos
terminales intencionalmente libres. La comprobación se hizo sobre el archivo.

El [generador](generar_conexiones_v4.py) regenera la hoja, la vista vectorial,
el PDF y la lista de redes con Python y ReportLab.
