# FoodScan: revisión de componentes y funcionamiento

Fecha: 4 de noviembre de 2026. Estado: planificación para revisar el prototipo existente; no acredita compras, montaje ni pruebas físicas.

## Base revisada

- El informe y el [esquema anterior v1](MóduloElectrónico/EasyEDA/FoodScan_Esquematico_v1.json) utilizaban ESP32-CAM AI-Thinker, OV2640, celda de 5 kg, HX711, microswitch y tres paneles de cuatro LED. La lista vigente es [Componentes_v2.md](MóduloElectrónico/Componentes_v2.md); la copia de la raíz `componentes.md` ya fue actualizada.
- La [verificación de conexiones anterior](MóduloElectrónico/EasyEDA/Verificacion_conexiones.json) corresponde a iluminación conectada a la alimentación general. La [BOM vigente](MóduloElectrónico/BOM.md) y el esquema v2 incorporan Q1 para controlarla desde el microcontrolador.
- [Especificación del Taller 11](Especificacion_S11.md) y [documentación mecánica](MóduloMecánico/README.md): plataforma de 220 × 220 mm, plato de referencia de 200 mm y cámara a una distancia nominal de 270 mm del plano del plato. El soporte CAD actual es fijo.
- [Guion del avance de FoodScan](../output/guiones/Guion_FoodScan_Avance_Prototipo_5_minutos.md): documenta Gemini 3.8 Flash, fotografía, peso total y descripción, con 924 entradas de las Tablas Peruanas de Composición de Alimentos del INS, décima edición de 2017. El programa calcula los nutrientes a partir de la tabla; el usuario puede corregir alimentos y porciones. Describe ingreso manual del peso y la integración automática pendiente.

La app real está en `../FoodScan/`, una carpeta excluida por el `.gitignore` del repositorio del curso y que contiene su propio proyecto Next.js/PWA. Se revisaron `lib/gemini.ts`, `lib/nutrition.ts` y `app/api/analyze/route.ts`: existe un backend de Gemini y el cálculo con catálogo. El módulo `MóduloSoftware/Código fuente/` del curso solo contiene un README; el firmware y el enlace automático con ESP32 siguen pendientes. La copia del curso coincide con el HEAD de `main` remoto al efectuar esta revisión.

## Decisiones expresadas por el usuario

1. Se utilizará una sola ESP32-S3 N16R8, comprada sin cámara incluida. La cámara se comprará por separado.
2. Cámara, pesaje, detector de puerta, luces y electrónica se montarán dentro de la máquina.
3. Durante el uso no habrá un cable de datos hacia una laptop. Las órdenes y los datos se comunicarán por Wi-Fi.
4. La IA es Gemini mediante API. La referencia anterior a SigLIP ejecutado en una laptop no corresponde a la solución indicada por el usuario.
5. Se conserva la app FoodScan y su cálculo con tabla nutricional. La mejora busca automatizar la entrada de fotografía y peso y controlar el ciclo físico.
6. Los S/ 150 entre cinco integrantes son la reserva para cámara y ESP32; los demás materiales se presupuestan aparte.
7. La webcam USB propuesta durante la conversación no se considera una selección cerrada para este diseño. Su conexión directa por USB a la laptop no satisface el funcionamiento requerido.

## Secuencia solicitada

1. El plato vacío está dentro cuando se prepara o inicia el prototipo. Se establece la tara y se muestra 0 g.
2. Se retira ese plato, se sirve la comida y se vuelve a introducir.
3. Se cierra la puerta y se pulsa Registrar en la app.
4. El equipo comprueba que la tara es válida, la puerta está cerrada y el peso es estable y está dentro del rango admitido.
5. Se enciende la iluminación; se permite estabilizar la imagen y realizar el enfoque con la cámara seleccionada.
6. Se obtienen fotografía y masa neta de la misma medición y se envían por Wi-Fi al flujo de análisis de la app con Gemini.
7. La app muestra el estado de carga y posteriormente los resultados. El cálculo nutricional conserva la fuente de la tabla y la revisión del usuario.
8. Al terminar se apagan las luces, se detiene la captura y se retira el plato.

La tara se conserva mientras se retira y vuelve a colocar el mismo plato. No se debe volver a tarar automáticamente al detectar una lectura negativa ni cuando entra el plato con comida. Una nueva tara requiere el recipiente vacío; la calibración con una masa conocida es una operación distinta.

### Propuesta de espera al terminar

Para admitir otra orden desde la app sin un encendido manual adicional, se propone que la ESP32 permanezca encendida y conectada, con las luces apagadas y la captura detenida. Este modo de espera no equivale a cortar toda la alimentación. El interruptor general conserva el apagado completo. No se considera confirmado un mecanismo de apagado y encendido remoto de la alimentación.

## Cambios sobre los componentes existentes

| Referencia actual | Elemento existente | Revisión propuesta |
|---|---|---|
| E01 / U1 | ESP32-CAM AI-Thinker, OV2640 y base MB | Sustituir el controlador por la ESP32-S3 N16R8 acordada. La cámara será independiente. Rehacer la asignación de pines según la placa y la cámara concretas. Si la nueva placa incorpora programación USB, la base MB anterior deja de formar parte de ese montaje. |
| Cámara incluida en E01 | OV2640 de 2 MP | Recomendación concreta para esta revisión: **Waveshare OV5640 Camera Board (C), SKU 13802**, de 5 MP, con autofocus e interfaz DVP de 8 bits, alimentación de 3.3 V. Se conectará internamente a la ESP32-S3, que transmitirá la fotografía por Wi-Fi. Falta verificar la conexión a la placa física seleccionada, el montaje y la cotización local; no es una compra confirmada. |
| E02 / LC1 | Celda de carga de 5 kg y cuatro hilos | Mantener inicialmente. Verificar el error, la repetibilidad y el comportamiento al quitar y recolocar el plato. La capacidad incluye plataforma, recipiente y comida, aunque se aplique tara. |
| E03 / U2 | HX711 compatible con alimentación de 3.3 V | Mantener. Ubicar cerca de la celda y comprobar estabilidad durante la conmutación de luces y la transmisión Wi-Fi. |
| E04 / SW2 | Microswitch KW11 con palanca y rueda | Mantener en el marco. Habilita el pesaje/captura cuando la puerta está cerrada; no identifica alimentos. |
| E05–E06 / D1–D12, R1–R12 | Tres paneles de cuatro LED, con resistencia por LED | Conservar como primera configuración de prueba, junto con los difusores existentes. Probar uniformidad, sombras y reflejos antes de sustituirlos por barras o tiras LED. |
| Nuevo | Control de iluminación | Añadir una etapa MOSFET compatible con la señal de 3.3 V de la ESP32, con estado apagado definido al arrancar. Su dimensionado depende del consumo final de las luces. La alimentación de las luces no se toma directamente de un GPIO. |
| E08 | Adaptador externo de 5 V / 2.4 A | Calcular de nuevo el consumo al cerrar cámara e iluminación. No se establece todavía que deba reemplazarse por una fuente de mayor corriente. |
| E09–E14 | Jack, interruptor, condensadores, fusible y portafusible | Conservar sus funciones y revisar valores/conexiones con la nueva alimentación y carga. |
| E15–E18 | Placas de montaje, jumpers, cableado y USB | Adaptar a la nueva placa y a la cámara independiente. El USB puede utilizarse para programación; no será el enlace de datos durante el uso normal. |
| Montaje mecánico | Base y plataforma reforzadas, separadores, topes y difusores | Conservar el principio de plataforma aislada de paredes y puerta. Revisar fijaciones y holguras reales. Incorporar centrado repetible del plato y soporte ajustable de cámara; reservar espacio para adaptador, cableado y disipación. |

No se justifica añadir una segunda ESP32, pantalla o sensores adicionales para cumplir la secuencia descrita. La celda, la cámara y el detector de puerta ya cubren las entradas necesarias del ciclo.

## Cambios de software e integración

- Automatizar la recepción de la foto y el peso en el registro de la app existente, conservando su revisión y cálculo nutricional.
- Añadir estados de preparación/tara, plato retirado, listo, captura, análisis, resultado y error.
- Mantener la misma tara durante la retirada y reposición del recipiente.
- Asociar foto y gramos mediante un identificador de medición; cancelar o repetir si la puerta se abre o el peso cambia durante la captura.
- Apagar las luces al terminar, cancelar o agotar el tiempo de espera, incluso si falla la consulta a Gemini.
- Usar una conexión Wi-Fi con acceso a Internet para la consulta a Gemini. La red local sin Internet descrita en la versión anterior no basta para esa consulta.
- Conservar la autenticación de Gemini en el backend Next.js existente. Lo pendiente es implementar la recepción automática de mediciones y el control del ciclo físico; no se requiere un servidor nuevo ni una laptop encendida.
- Conservar la distinción de la app: el peso total se mide; la identificación y el reparto de un plato mixto propuestos por Gemini son estimaciones revisables; los nutrientes se calculan con la tabla.

## Pendientes que condicionan el esquema y el CAD

1. Modelo físico de placa ESP32-S3 N16R8 y conexión a la cámara recomendada, Waveshare OV5640 Camera Board (C). Verificar cotización y disponibilidad antes de considerarla dentro del presupuesto conjunto de S/ 150.
2. Alimentación: está decidido que los datos sean inalámbricos; falta confirmar si se admite cable de alimentación o se requiere batería.
3. Ensayo de las luces y difusores existentes para decidir si se mantienen o sustituyen.
4. Implementar posteriormente el enlace con el backend existente de `FoodScan/`: `POST /api/analyze` recibe JSON `image` (Data URL), `totalGrams` y `description` opcional. El código de la app ya se pudo revisar; el control de estados de la máquina y la integración ESP32 continúan pendientes y no forman parte de esta corrección electrónica.

La lista y el esquema corregidos se entregan en `MóduloElectrónico/BOM.md` y `MóduloElectrónico/EasyEDA/FoodScan_Esquematico_v2.json`, con su PDF. Esta revisión no acredita compras ni pruebas físicas. El CAD permanece en la versión previa y fuera del alcance solicitado.

Referencia de la cámara recomendada: [Waveshare OV5640 Camera Board (C), SKU 13802](https://www.waveshare.com/catalog/product/view/id/3494/s/ov5640-camera-board-c/category/37/). La ficha del fabricante especifica autofocus, DVP de 8 bits, SCCB, 3.3 V y resolución máxima del sensor de 2592 × 1944. Precio publicado al consultar el 4 de noviembre de 2026: US$ 26.99, sin calcular entrega a Perú. El enfoque, la resolución de captura utilizada y el comportamiento térmico se verifican con el montaje real.
