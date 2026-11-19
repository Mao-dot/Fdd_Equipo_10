# Lista de compra vigente de FoodScan

> Lista importada de la rama `rediseño`, commit `d419a1f`. Los enlaces a archivos de CAD y revisiones anteriores apuntan a esa revisión.

[Esquemático recibido v6](EasyEDA/FoodScan_Esquematico_v6.eprj2) · [Organización del Entregable 3](../../Fundamentos%20de%20diseño/Entregables/Entregable_03.md)

Actualizada el **17 de noviembre de 2026** con las compras confirmadas por el equipo y la selección de componentes locales en soles. Las cantidades corresponden a un FoodScan modular con ESP32-S3 N16R8, cuatro tramos LUZPE de 12 V y una primera demostración con comida a temperatura ambiente.

El controlador elegido para los LED es el **módulo MOSFET LR7843 con optoacoplador PC817**. Su compra queda por confirmar. La **fuente principal de 12 V CC / 5 A / 60 W está pendiente de compra**. La referencia Cubull PL-60-12 utilizada previamente queda como antecedente de selección.

## Ya disponible

| Cantidad | Componente | Datos del equipo y comprobaciones de montaje |
| ---: | --- | --- |
| 1 | ESP32-S3 N16R8 | Verificar la revisión física, el puerto USB y las cabeceras de la placa. |
| 1 | Celda de carga | Compra confirmada. Registrar la capacidad y las dimensiones de la unidad recibida. El equipo montará la base, los separadores y la plataforma. |
| 1 | Módulo HX711 | Compra confirmada. Conecta la celda con la ESP32 mediante DOUT y SCK. Comprobar la alimentación y los niveles lógicos de la placa recibida para trabajar a 3,3 V. La tara y la calibración se implementan en el programa. |
| 1 | Pantalla OLED | Compra confirmada. Registrar modelo, controlador, tamaño e interfaz de la unidad recibida antes de definir conexiones, programa y soporte. Comprobar su funcionamiento a 3,3 V. |
| 1 | Portafusible de chasis K3025 | Compra confirmada. Enroscable, un polo y cartucho de 5 × 20 mm. Preparar y aislar las uniones de sus terminales. El cartucho se especifica en la compra pendiente. |
| 1 | Convertidor DC-DC de 12 V a 5 V | Compra confirmada. Registrar el modelo y la corriente nominal de la unidad. Alimentará la ESP32 por la entrada de 5 V apropiada para su placa. Verificar 5,00 V y capacidad de corriente antes de conectarla. |
| 1 rollo | LUZPE COB blanca, modelo 6C1, ref. 2601201 | Etiqueta de la unidad comprada: 12 V CC, 5 m, 55 W, 11 W/m, 320 LED/m e IP20. Declara temperatura de trabajo de −20 a +40 °C. Usar cuatro tramos de aproximadamente 200 mm, cortados en las marcas de la tira. La etiqueta dice blanco y deja sin confirmar la temperatura de color y el CRI. |

## Alimentación y módulos pendientes

| Cantidad | Componente | Estado y precio de referencia | Especificación y enlace |
| ---: | --- | --- | --- |
| 1 | Fuente externa regulada de 12 V CC / 5 A / 60 W | Pendiente. Opción MTLAB WQ48, S/27,00, con stock publicado. | Tipo cargador. Confirmar en la unidad entrada de 100–240 V CA, salida de 12 V CC / 5 A y centro positivo. La ficha WQ48 incluye cable de salida y cable alimentador. La marca y el modelo comercial se registrarán al comprar. [Comprar en MTLAB](https://mtlab.pe/producto/adaptador-de-voltaje-ac-dc-12v-5a-fuente-12v-5a-tipo-cargador/) |
| 1 | Regulador XL4015, variante ER22 con borneras | Pendiente. S/17,00, con stock publicado. | Alimentar desde los 12 V y ajustar a 3,30 V para cámara, OLED, HX711 y sensor de puerta, según las fichas de las unidades. Verificar la salida con multímetro antes de conectar los módulos. [Comprar en MTLAB](https://mtlab.pe/producto/step-down-xl4015-reductor-de-voltaje-buck-dc-dc/) |
| 1 | Módulo MOSFET LR7843 con optoacoplador PC817 | Modelo elegido. Compra por confirmar. Electromanía publica S/3,00 y agotado. | Un módulo controla juntos los cuatro tramos LED de 12 V en paralelo, unos 8,8 W y 0,73 A nominales en total. La ficha declara carga de 6–28 V y control de 3,3 V o 5 V. Identificar los bornes de fuente, carga y control del módulo recibido. [Referencia local y disponibilidad en Electromanía](https://www.electromania.pe/producto/modulo-de-fet-tubo-mosfet-mos-de-aislamiento-lr7843/) |
| 1 | Cámara independiente Adafruit 5838, OV5640 | Pendiente de cotización local. Precio y plazo por confirmar. | Sensor de 5 MP, interfaz DVP de 8 bits, lente de 120°, autofoco y placa con pines para conectar a la ESP32 existente. Pedir cabeceras soldadas y configurar XCLK y VM según el montaje previsto. Validar encuadre y enfoque con el plato y habilitar el autofoco en el programa. La búsqueda local del 17/11/2026 dejó pendiente encontrar stock de esta referencia. [Cotizar con MTLAB](https://mtlab.pe/nosotros/) · [Ficha del fabricante](https://www.adafruit.com/product/5838) |
| 1 | Módulo sensor magnético reed SA06 | Pendiente. S/7,00, con stock publicado. | Alimentar a 3,3 V y conectar VCC, GND y DO. La ficha anuncia detección de unos 10 mm, dependiente del imán. Probar la posición y el nivel de salida al cerrar la puerta antes de fijar el sensor. [Comprar en MTLAB](https://mtlab.pe/producto/modulo-interruptor-magnetico-reed-switch-salida-digital/) |
| 1 | Imán de neodimio N35, Ø5 × 3 mm | Pendiente. S/0,50, con stock publicado. | Seleccionar diámetro 5 mm y espesor 3 mm para acompañar al SA06. Ajustar su separación en la prueba de puerta. [Comprar en MTLAB](https://mtlab.pe/producto/imanes-de-neodimio-n35-diametro-4mm-y-5mm/) |

## Entrada, controles, cables y conectores pendientes

| Cantidad | Componente | Precio de referencia | Selección y enlace |
| ---: | --- | ---: | --- |
| 1 | XT60E-M macho de panel AMASS | S/3,00 | Entrada de 12 V del equipo. Ajustar el recorte del panel P09a a esta pieza. [Comprar en Bracsan](https://bracsan.pe/producto/conector-xt60-macho-para-panel-amass-xt60e-m/) |
| 1 juego | XT60 aéreo macho y hembra AMASS | S/4,50 | Usar la hembra del juego en el cable de salida de 12 V de la fuente. La compra total de la entrada es un XT60E-M de panel y un juego aéreo. Identificar polaridad y aislar las soldaduras al adaptar el cable DC. [Comprar en Bracsan](https://bracsan.pe/producto/conector-xt60-macho-hembra-bala-para-bateria-lipo-amass-xt60/) |
| 1 | Interruptor general KAVTO KV-AE R 26 | S/5,50 | ON/OFF, cuatro pines, para 12 V CC. Identificar por continuidad los contactos que cortan el positivo y dimensionar el recorte sobre la unidad recibida. [Comprar en Bracsan](https://bracsan.pe/producto/interruptor-switch-con-luz-uso-automotriz-4-pines-on-off-35a-12vdc-18a-24vdc-kavto-kv-ae-r-26/) |
| 2 | Pulsador momentáneo LA128AY-11D, Ø16 mm | S/15,00 el par | Uno para tara y otro para captura. Usar COM y NO como contactos secos con lógica a 3,3 V, y comprobar que vuelvan al soltar. El indicador integrado es de 24 V y queda fuera del cableado de señales de la ESP32. [Comprar en Bracsan](https://bracsan.pe/producto/pulsador-16mm-250vac-3a-spdt-1no1nc-con-led-24vdc-la128ay-11d/) |
| 1 | Cartucho fusible de 5 × 20 mm | Por definir | Para el K3025 disponible. Elegir corriente y curva después de medir consumo y arranque con la fuente definitiva, considerando el cableado. Confirmar la aptitud del cartucho para 12 V CC. La ficha enlazada ofrece cartuchos rápidos de distintos amperajes. [Ver opciones en Bracsan](https://bracsan.pe/producto/fusible-de-vidrio-europeo-5x20mm-250v-0-1a-0-3a-0-5a-0-8a-1a-1-25a-1-5a-2a-2-5a-3a-3-15a-4a-5a-6a-6-3a-7a-8a-10a-15a/) |
| 6 | Conector rápido 1×4, WC14 | S/13,20 | S/2,20 por unidad. Cinco puntos de conexión comunes por pieza, para distribución. [Comprar en MTLAB](https://mtlab.pe/producto/conector-electrico-empalme-rapido-cables-28awg-a-12awg/) |
| 3 | Conector rápido 1×2, WC12 | S/4,50 | S/1,50 por unidad. Tres puntos de conexión comunes por pieza. [Comprar en MTLAB](https://mtlab.pe/producto/conector-electrico-empalme-rapido-cables-28awg-a-12awg/) |
| 4 | Conector rápido 1×1, WC01 | S/5,60 | S/1,40 por unidad. Empalme de dos extremos de un conductor. [Comprar en MTLAB](https://mtlab.pe/producto/conector-electrico-empalme-rapido-cables-28awg-a-12awg/) |
| 2 | Conector rápido 2×2, WC02 | S/3,20 | S/1,60 por unidad. Dos canales independientes para los dos hilos de cada pulsador. Confirmar continuidad entre sus puntos antes del montaje. [Comprar en MTLAB](https://mtlab.pe/producto/conector-electrico-empalme-rapido-cables-28awg-a-12awg/) |
| 1 m | Cable bipolar Hurricane CC-2X18, dos hilos AWG18 | S/5,20 | Para la entrada de 12 V. Identificar y marcar el positivo en ambos extremos. [Comprar en Bracsan](https://bracsan.pe/producto/cable-de-control-negro-de-2-hilos-18awg-hurricane-cc-2x18/) |
| 2 m por color | Cable flexible siliconado AWG22 rojo y negro | S/8,00 en total | Cuatro metros a S/2,00 por metro. De aquí salen los cuatro pares para las tiras LED, los ramales y los dos chicotes de alimentación de 150 mm para la ESP32. [Comprar en Sawers](https://sawers.com.pe/componentes/cables-y-protoboard/cable-flexible-siliconado-awg-1mts) |
| 1 paquete de cada tipo | Dupont de 15 cm, WU16 hembra–hembra y WU14 macho–hembra | S/12,00 en total | S/6,00 por paquete. Seleccionar ambas variantes para señales y cabeceras de 2,54 mm. Preparar los extremos de los chicotes según las cabeceras reales de la ESP32. [Comprar en MTLAB](https://mtlab.pe/producto/cables-jumper-dupont/) |

Los precios y la disponibilidad publicados se consultaron el 17/11/2026. El subtotal de los artículos de MTLAB con stock de esta lista es **S/90,00**, el de Bracsan **S/33,20** y el de Sawers **S/8,00**, para **S/131,20 antes de envíos**. A ese importe se agregan la cámara, el LR7843 si aún falta, el cartucho y los elementos condicionales siguientes.

| Cantidad | Componente condicional | Criterio y enlace |
| ---: | --- | --- |
| 1 | Cable USB de datos | Comprar si falta un cable compatible con el puerto físico de la ESP32. Para USB-C, MTLAB publica el WD36 por S/10,00. [Comprar en MTLAB](https://mtlab.pe/producto/wd36/) |
| 2 terminales | Faston hembra aislado para el interruptor | Medir las lengüetas del interruptor. Si son de 6,35 mm, el FDD1.25-250 admite AWG22–16. Bracsan ofrece bolsa de 100 por S/10,00, o el taller puede aportar las dos unidades necesarias. El K3025 se prepara con sus uniones soldadas. [Ver referencia en Bracsan](https://bracsan.pe/producto/terminal-tipo-hembra-estandar-aislado-rojo-22-16-100pcs-rf250-fdd1-25-250-1002463/) |

## Alimentación y conexiones previstas

La fuente externa entrega 12 V al XT60 de panel, al fusible y al interruptor general. Desde el bus protegido de 12 V se alimentan el LR7843 y los dos convertidores en paralelo. El convertidor ya adquirido entrega 5 V a la ESP32. El XL4015 ER22 entrega 3,3 V a cámara, OLED, HX711 y SA06, previa comprobación de las placas recibidas. Los retornos de alimentación comparten masa.

El LR7843 recibe la señal de control de 3,3 V de la ESP32 y conmuta el retorno de los cuatro tramos LED conectados en paralelo. Identificar los bornes de la unidad y comprobar su estado al arrancar antes de montar las tiras.

La celda conecta al HX711 y este usa DOUT y SCK hacia la ESP32. El SA06 usa VCC, GND y DO, con un imán en la puerta. Los pulsadores de tara y captura usan contactos COM y NO. La asignación de GPIO y el arnés de la OLED dependen de la revisión física de la ESP32 y de la pantalla adquirida.

La PCB auxiliar, su matriz de arneses y sus comprobaciones eléctricas documentadas corresponden a la revisión A de 5 V. Esta lista refleja el montaje modular de 12 V y los componentes adquiridos por el equipo.

## Carcasa e iluminación mecánica

Las cantidades mecánicas siguientes proceden del CAD. Presentar la celda, la OLED, el LR7843 y los convertidores reales antes de fabricar sus soportes y los recortes del panel de alimentación.

| Cantidad | Componente o servicio | Especificación |
| ---: | --- | --- |
| 1 + 1 + 8 | Perfil, difusor y tapas | 1 m de KLUŚ 45-16 A08504A_1, 1 m de difusor opal HS-11 B17208F_1 y 8 tapas C24206C02. Cortar cuatro tramos de perfil y difusor de 220 mm. Medir el ancho de la LUZPE y probar el cierre del difusor con la tira instalada. [Ficha KLUŚ](https://klusdesign.com/es/producto/45-16-perfil-4166) |
| 1 m | Cinta 3M VHB 4905 | 12,7 mm de ancho y 0,5 mm de espesor. Cortar cuatro tiras de 185 × 6,8 mm para los perfiles y preparar dos recortes para el sensor magnético. [Ficha 3M](https://www.3m.com/3M/en_US/p/d/v000149688/) |
| Según módulos recibidos | Soportes de módulos | Dimensionar la base y los separadores de la celda, además de las fijaciones de la ESP32, OLED, LR7843 y convertidores, sobre las piezas adquiridas. Elegir tornillos y separadores según sus taladros y mantener las conexiones aisladas del soporte. |
| 10 + 10 + 1 m | Sujeción de cables | 10 bridas de nylon de 2,5 × 100 mm, 10 bases para brida de 20 × 20 mm y 1 m de perfil EPDM en U para cantos de 6 mm. |
| 8 + 1 | Paneles de carcasa | Un panel P01 a P08 de contrachapado de abedul de 6 mm, con caras y cantos sellados. Una placa P09a de 74 × 36 × 3 mm en abedul sellado. Ajustar el recorte y comprobar el espacio de P09a con el XT60E-M, el interruptor KAVTO y el K3025 antes de pedir el corte final. [DXF de los paneles](https://github.com/Mao-dot/Fdd_Equipo_10/tree/d419a1fff08f0c810e1d4effd22b1e43ee22a715/Proyecto/M%C3%B3duloMec%C3%A1nico/Redise%C3%B1o/exports/dxf) · [DXF de referencia de P09a](https://github.com/Mao-dot/Fdd_Equipo_10/blob/d419a1fff08f0c810e1d4effd22b1e43ee22a715/Proyecto/M%C3%B3duloMec%C3%A1nico/Redise%C3%B1o/commercial/auxiliary/power/P09a_trial/P09a_panel_alimentacion_prueba.dxf) |
| 1 | Bandeja portante P10 | Disco AISI 304 de Ø240 × 1,5 mm, plano y desbarbado. [DXF P10](https://github.com/Mao-dot/Fdd_Equipo_10/blob/d419a1fff08f0c810e1d4effd22b1e43ee22a715/Proyecto/M%C3%B3duloMec%C3%A1nico/Redise%C3%B1o/exports/dxf/P10.dxf) |
| 1 + 2 + 1 | Junta y herrajes de puerta | Lámina de silicona de celda cerrada de 300 × 280 × 2 mm para G01. Junta de contorno exterior 296 × 271 mm e interior nominal 291,6 × 266,6 mm, con 1,5 mm objetivo al cerrar. 2 pasadores inoxidables Ø4 × 33 mm y 1 casquillo inoxidable Ø6 exterior × Ø3,4 interior × 7,5 mm. |
| 47 | Impresiones PETG | 6 de cada P20A/P20B, 4 de cada P21A/P21B/P29/P34/P35, 2 de cada P22/P23/P31/P32 y 1 de cada P24/P25/P26/P30/P36/P37L/P37R. Medir la ESP32 y la balanza antes de imprimir sus soportes. [STL](https://github.com/Mao-dot/Fdd_Equipo_10/tree/d419a1fff08f0c810e1d4effd22b1e43ee22a715/Proyecto/M%C3%B3duloMec%C3%A1nico/Redise%C3%B1o/exports/stl) |
| 75 + 75 + 6 + 2 | Tornillería de las piezas del CAD | Acero inoxidable A2. 6 tornillos M3 × 12, 54 M3 × 16, 9 M3 × 20 y 6 M3 × 30, todos ISO 4762, y 75 tuercas M3 ISO 4032. Para cámara y OLED, 2 M2,5 × 12 y 4 M2,5 × 5, más 2 tuercas M2,5 para la cámara. Confirmar la profundidad de rosca del OLED. |

En la primera demostración se utiliza la abertura libre de Ø116 mm del divisor P07. Si se amplía a pruebas con comida que suelte vapor, cotizar 1 disco de acrílico transparente Ø130 × 2 mm, 1 junta W02 Ø130 exterior × Ø116 interior × 1 mm, 1 anillo P27, 4 tornillos M3 × 16 y 4 tuercas M3. Validar encuadre, vaho y protección de las tiras IP20 en ese montaje. [Dimensiones del CAD](https://github.com/Mao-dot/Fdd_Equipo_10/blob/d419a1fff08f0c810e1d4effd22b1e43ee22a715/Proyecto/M%C3%B3duloMec%C3%A1nico/Redise%C3%B1o/documentacion/Dimensiones_y_tolerancias.md#óptica-ventilación-y-electrónica)

## Documentos de referencia de revisiones anteriores

- [BOM histórica de la PCB auxiliar Rev. A](https://github.com/Mao-dot/Fdd_Equipo_10/blob/d419a1fff08f0c810e1d4effd22b1e43ee22a715/Proyecto/M%C3%B3duloElectr%C3%B3nico/Redise%C3%B1o_FoodScan/BOM.md) · Inventario asociado al esquema de 5 V publicado en esa revisión.
- [Inventario del ensamblaje CAD original](https://github.com/Mao-dot/Fdd_Equipo_10/blob/d419a1fff08f0c810e1d4effd22b1e43ee22a715/Proyecto/M%C3%B3duloMec%C3%A1nico/Redise%C3%B1o/exports/BOM.md) · Piezas modeladas en esa revisión. Las cantidades para la compra modular figuran arriba.
