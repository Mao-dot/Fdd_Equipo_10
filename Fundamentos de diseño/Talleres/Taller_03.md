# Taller 03: Revisión de antecedentes científicos y tecnológicos

## 1. Datos generales

- **Equipo:** Equipo 10
- **Curso:** Fundamentos de Diseño
- **Periodo académico:** 2026-2
- **Fecha de elaboración:** 3 de septiembre de 2026
- **ODS principal:** ODS 12 - Producción y consumo responsables
- **Meta seleccionada:** Meta 12.8 - Información y conocimientos para adoptar estilos de vida sostenibles

### Problemática del proyecto

Las personas que desean controlar su alimentación encuentran dificultades para obtener información práctica, inmediata y comprensible sobre la cantidad real y la composición nutricional de los alimentos que consumen. Aunque existen tablas, aplicaciones y bases de datos nutricionales, estas suelen trabajar con porciones estandarizadas y exigen que el usuario identifique el alimento, estime la cantidad servida o introduzca datos manualmente.

El equipo estudia inicialmente esta dificultad en personas físicamente activas que buscan conocer con frecuencia la cantidad de proteínas, carbohidratos y grasas presentes en sus comidas.

> **Pregunta de investigación:** ¿Qué dificultades enfrentan las personas físicamente activas al intentar obtener información práctica y comprensible sobre la cantidad y la composición nutricional de los alimentos que consumen?

---

## 2. Objetivo y alcance del taller

### Objetivo general

Analizar antecedentes científicos, tecnológicos y comerciales vinculados con el reconocimiento de alimentos, la estimación de porciones y la obtención de información nutricional, a fin de identificar enfoques, variables, resultados y limitaciones relevantes para la problemática del Equipo 10.

### Alcance

La revisión comprende doce antecedentes proporcionados por el equipo:

- 3 artículos científicos.
- 3 patentes.
- 3 tesis universitarias.
- 3 productos comerciales.

Los títulos se conservan en su idioma original. La explicación, el análisis y las conclusiones se presentan en español. Las cifras incluidas corresponden únicamente a valores declarados por las fuentes consultadas; cuando una fuente no publica una precisión, capacidad o rango, se indica expresamente como **no especificado**.

---

## 3. Metodología de revisión

Las fuentes entregadas por el equipo fueron verificadas en sus páginas originales o en las fichas institucionales asociadas. Para cada antecedente se analizaron cinco aspectos:

1. El tema o problema que aborda.
2. El método, sistema o propuesta presentada.
3. Su aporte a la problemática del proyecto.
4. Las variables o características estudiadas.
5. Los valores, rangos o resultados cuantitativos disponibles.

Las referencias se presentan al final en formato numérico. Se incluyen autores o inventores, título, año, publicación o institución, páginas o número de artículo cuando corresponde, identificador y enlace. En patentes y productos comerciales se emplean los datos equivalentes aplicables, como titular, número de publicación o fabricante.

---

## 4. Artículos científicos

### 4.1. *A Comparison of Food Portion Size Estimation Using Geometric Models and Depth Images*

Fang et al. comparan dos métodos para estimar el volumen de alimentos: el uso de modelos geométricos predefinidos y el procesamiento de imágenes de profundidad [1]. El primer método asigna formas como esfera, cilindro o prisma según el alimento identificado; el segundo reconstruye el volumen mediante vóxeles obtenidos de un mapa de profundidad.

El estudio evaluó diez objetos con volúmenes reales entre 50 y 450 mL, determinados por desplazamiento de agua. Las imágenes de profundidad tuvieron una resolución de 640 × 480 píxeles. En nueve de los diez objetos, el método basado en profundidad sobreestimó el volumen; en el caso más marcado, el vaso obtuvo una relación promedio de 2,34 entre el volumen estimado y el real. Los modelos geométricos produjeron mejores estimaciones cuando el objeto tenía una forma tridimensional claramente definida [1].

Este antecedente demuestra que la cantidad de alimento no puede inferirse de manera confiable solo a partir de su apariencia bidimensional. También evidencia que la forma, el ángulo de captura, la segmentación y la referencia espacial influyen directamente en la estimación de una porción. Su principal limitación es que utilizó réplicas de alimentos, etiquetas y máscaras de segmentación conocidas, por lo que sus resultados no representan por sí solos el funcionamiento con comidas reales y mixtas.

### 4.2. *A Novel Approach to Estimate the Weight of Food Items Based on Features Extracted from an Image Using Boosting Algorithms*

Konstantakopoulos, Georga y Fotiadis proponen estimar el peso de un alimento a partir de una sola imagen capturada con un teléfono móvil [2]. El modelo emplea características como el área ocupada por el alimento, el área de un objeto de referencia, la identidad y la categoría del alimento. Estas variables se procesan mediante algoritmos de regresión *boosting*: XGBoost, CatBoost y LightGBM.

La investigación utilizó 23 052 imágenes anotadas de 226 platos mediterráneos y generó 24 996 registros para el entrenamiento. XGBoost obtuvo el mejor desempeño: error absoluto medio del peso de 3,93 g, error porcentual absoluto medio de 3,73 % y raíz del error cuadrático medio de 6,05 g [2].

El aporte principal para el proyecto es mostrar que una sola fotografía puede relacionarse con una estimación cuantitativa del peso cuando existen segmentación, clasificación y una referencia de escala adecuadas. Sin embargo, el modelo fue evaluado con gastronomía mediterránea y depende de que el alimento haya sido correctamente segmentado y clasificado. Por ello, las cifras no deben extrapolarse directamente a platos peruanos, preparaciones mixtas o imágenes tomadas en condiciones distintas.

### 4.3. *Applying Image-Based Food-Recognition Systems on Dietary Assessment: A Systematic Review*

Dalakleidi et al. presentan una revisión sistemática de sistemas de reconocimiento de alimentos basados en imágenes para evaluación dietética [3]. La arquitectura general identificada comprende captura de la fotografía, preprocesamiento, segmentación, extracción de características, clasificación, estimación de volumen y, finalmente, cálculo de energía y nutrientes mediante una base de datos nutricional.

La revisión examinó 159 publicaciones y seleccionó 78 estudios; 45 de ellos, equivalentes al 58 %, utilizaron aprendizaje profundo, especialmente redes neuronales convolucionales. Los autores señalan que el rendimiento de clasificación en el conjunto Food-101 evolucionó de 55,3 % a 90,27 % con el uso de estas redes [3]. También advierten que la iluminación, los objetos ajenos a la comida, la calidad de las bases de datos y el olvido del usuario al fotografiar sus alimentos siguen siendo fuentes de error.

Este trabajo aporta una visión integral del proceso y permite distinguir dos problemas diferentes: reconocer qué alimento aparece en una imagen y determinar cuánto alimento hay. Para el Equipo 10 esta distinción es esencial, porque una clasificación correcta no garantiza una estimación correcta de la porción ni de sus macronutrientes.

---

## 5. Patentes

### 5.1. *Food Recognition Using Visual Analysis and Speech Recognition* (US8439683B2)

La patente de Puri et al., asignada a SRI International, describe un sistema que combina análisis visual con una descripción oral o escrita de la comida [4]. El sistema recibe varias imágenes del plato, extrae una lista de alimentos a partir de la descripción del usuario, clasifica y segmenta los elementos mediante características de color y textura, y estima su volumen para apoyar el cálculo calórico.

La realización preferida utiliza al menos tres imágenes de una misma escena. La patente describe experimentos con 400 conjuntos de imágenes correspondientes a 150 tipos de alimentos, así como una evaluación independiente con 26 tipos. También menciona la Food and Nutrient Database for Dietary Studies (FNDDS), con más de 7000 alimentos, como referencia nutricional [4].

Su aporte consiste en demostrar el valor de combinar modalidades: la imagen aporta evidencia visual y la voz o el texto ayudan a reducir la ambigüedad de reconocimiento. Como limitación para el proyecto, el procedimiento requiere varias imágenes y participación adicional del usuario, lo que puede aumentar el esfuerzo necesario para registrar una comida. La ficha consultada registra la patente como activa.

### 5.2. *Connected Food Scale System and Method* (US20140063180A1)

Sharma propone una balanza digital conectada con uno o varios dispositivos móviles [5]. El sistema integra un sensor de carga, conversión analógica-digital, memoria, pantalla, interfaz de comunicación y registros alimentarios diferenciados por usuario. La balanza puede sincronizar los datos con una aplicación móvil y asociar una fotografía del alimento con la entrada registrada.

La patente contempla conexiones físicas o inalámbricas, incluidas Wi-Fi y Bluetooth, y un soporte para colocar el teléfono y fotografiar el alimento. También describe la posibilidad de mantener registros para seis a ocho usuarios. No publica una capacidad de pesaje ni una precisión metrológica concreta [5].

Este antecedente aporta una arquitectura que vincula una medición objetiva del peso con una interfaz digital y un historial personal. No obstante, la identificación del alimento y la calidad de la información nutricional continúan dependiendo de la base de datos y de la interacción implementada. La fuente registra esta solicitud como abandonada; dicho estado no elimina su utilidad como antecedente técnico, pero debe diferenciarse de una patente concedida y vigente.

### 5.3. *一种自动识别食物卡路里的电子秤及方法* (CN108871530A)

La patente de 公文静 describe una balanza electrónica que busca reconocer automáticamente el alimento y calcular sus calorías sin que el usuario introduzca manualmente su nombre [6]. El sistema contiene un módulo de identificación, un módulo de pesaje, una base de datos, un módulo de análisis y un módulo de visualización.

El cálculo propuesto relaciona el peso medido, expresado en gramos, con el valor energético registrado para 100 g del alimento mediante la expresión `cal = m / 100 × C`. La descripción incluye ejemplos de referencia: arroz, 125 kcal/100 g; panecillo al vapor, 225 kcal/100 g; y manzana, 60 kcal/100 g [6]. Estos valores son ejemplos contenidos en la patente y no una tabla nutricional adoptada por el proyecto.

El aporte principal es integrar en un mismo equipo la identificación, el pesaje y la presentación de la información calórica. La patente no especifica el rango o la precisión de la balanza ni el desempeño del reconocimiento automático. La ficha consultada la registra como solicitud pendiente.

---

## 6. Tesis

### 6.1. *Single View Reconstruction for Food Portion Estimation*

La tesis doctoral de Fang desarrolla métodos para estimar porciones a partir de una sola imagen, con el propósito de reducir la carga que supone tomar varias fotografías de una comida [7]. La investigación reúne tres líneas complementarias: modelos geométricos y mapas de profundidad para estimar volumen, patrones de coocurrencia para incorporar contexto alimentario y redes generativas adversarias para estimar directamente la energía de una imagen.

El trabajo define la porción como la cantidad de alimento expresable mediante volumen, peso, energía o nutrientes. En uno de los métodos basados en modelos geométricos se reporta un error inferior al 6 % en la estimación energética de una imagen, bajo el supuesto de contar con segmentación e identificación correctas [7]. Esta condición es importante: el resultado corresponde al subsistema de estimación y no a un proceso completamente automático evaluado de extremo a extremo.

Para el Equipo 10, la tesis aporta una explicación profunda de la relación entre imagen, escala, volumen, peso y energía. También demuestra que el contexto de una comida puede mejorar la estimación, aunque no sustituye la necesidad de validar el sistema con alimentos y porciones representativos del público objetivo.

### 6.2. *Modelo ProLab: Checkifood, aplicación móvil que ayuda al régimen alimenticio con machine learning*

Romero De Chorié et al. presentan una propuesta peruana de aplicación móvil orientada a personas de 18 a 45 años que desean mejorar sus hábitos alimentarios [8]. Checkifood plantea utilizar *machine learning* para detectar y analizar platos mediante fotografías, simplificando el registro frente a aplicaciones que requieren el ingreso manual de alimentos.

El principal aporte es contextual: confirma la pertinencia de una experiencia móvil con identificación visual para usuarios peruanos y aborda la facilidad de registro como parte central de la propuesta de valor. La tesis desarrolla ampliamente la viabilidad económica y social del modelo; sin embargo, la ficha institucional consultada no publica métricas técnicas de precisión del reconocimiento, error en gramos ni exactitud nutricional [8]. Por ello, no corresponde utilizar sus resultados financieros como evidencia de desempeño tecnológico.

### 6.3. *Evaluación del aporte nutricional del menú del servicio de alimentación para deportistas albergados del IPD y su relación con sus requerimientos nutricionales*

López Aliaga Pantigoso evalúa el menú y la ingesta efectiva de deportistas de alto rendimiento alojados en la Villa Deportiva Nacional (VIDENA) [9]. Durante una semana de agosto de 2018 se empleó pesaje directo para analizar el desayuno, almuerzo, cena y fraccionamientos consumidos por 30 deportistas, y se comparó el aporte con sus requerimientos de energía y macronutrientes.

Aunque esta tesis no desarrolla un sistema de reconocimiento de imágenes, aporta un referente para definir qué debe medirse y cómo obtener valores de comparación: peso servido, peso consumido, energía, proteínas, carbohidratos y grasas. También evidencia que la información nutricional para personas físicamente activas debe relacionarse con la porción efectivamente consumida y no únicamente con una porción genérica [9].

La ficha pública consultada no presenta todos los valores individuales o rangos nutricionales del estudio. En consecuencia, únicamente se consideran el tamaño de la muestra, la duración y las variables confirmadas, sin completar resultados no disponibles en la fuente resumida.

---

## 7. Productos comerciales

### 7.1. *ESN00 Smart Nutrition Scale*

La Etekcity ESN00 es una balanza nutricional conectada a la aplicación VeSync [10]. Mide el peso del alimento y permite consultar hasta 19 nutrientes mediante una base de datos de aproximadamente un millón de registros alimentarios proporcionada por Nutritionix. También ofrece función de tara, personalización de alimentos y sincronización con Apple Health y Fitbit.

El equipo utiliza cuatro sensores y mide entre 3 y 5000 g, con incrementos de 1 g. Admite gramos, mililitros, onzas y libras/onzas [10]. Su aporte para el proyecto es demostrar la precisión y claridad que puede obtenerse cuando la porción se mide físicamente. Su principal limitación de uso es que la identificación del alimento y la selección correcta de la entrada nutricional continúan dependiendo del usuario y de la base de datos.

### 7.2. *Fitia - Contador de Calorías y Dietas con IA*

Fitia es una aplicación de seguimiento nutricional que permite registrar alimentos mediante fotografía, voz, texto o código de barras [11]. Calcula una ingesta objetivo de calorías y macronutrientes con base en datos como actividad, composición corporal y objetivo personal. La empresa indica que su base de alimentos es revisada mediante un algoritmo interno y por profesionales en nutrición.

El producto aporta una referencia de experiencia de usuario: ofrece varios mecanismos de entrada y convierte la información en metas y gráficos comprensibles. También confirma que las personas pueden preferir distintos modos de registrar una misma comida. La página comercial no publica un rango de error para la estimación mediante fotografía ni una precisión absoluta en gramos, por lo que no es posible comparar técnicamente esa función con los artículos científicos revisados.

### 7.3. *SnapCalorie - AI Calorie Tracking Made Simple*

SnapCalorie permite fotografiar una comida para que un sistema de inteligencia artificial identifique los alimentos y calcule su información nutricional [12]. El flujo comercial se resume en tres pasos: tomar la fotografía, analizarla y revisar el registro. La aplicación presenta calorías y macronutrientes, e incorpora notas de voz, seguimiento de tendencias y planificación de comidas.

La página del producto afirma que el registro es cinco veces más rápido que el ingreso manual y que su tecnología alcanza el doble de precisión que nutricionistas [12]. Estas son afirmaciones comerciales: la misma página no proporciona la métrica, el conjunto de prueba, el tamaño de muestra ni un error absoluto que permitan verificarlas o compararlas con un estudio científico. Por ello, el aporte considerado es su flujo de interacción y no esas cifras como evidencia experimental.

---

## 8. Síntesis integrada de los antecedentes

### 8.1. Reconocimiento y estimación de cantidad son etapas diferentes

Los antecedentes distinguen con claridad entre identificar el alimento y determinar su cantidad. La clasificación puede reconocer que un plato contiene arroz, pollo o verduras, pero el cálculo nutricional requiere además estimar el peso o volumen de cada elemento. Los errores de segmentación o identificación se trasladan a las etapas posteriores y afectan el resultado final.

### 8.2. La estimación visual necesita referencias y validación

Los artículos y tesis muestran que una imagen puede utilizarse para estimar porciones, pero su desempeño depende de la escala, la forma tridimensional, el ángulo, la iluminación, la superposición entre alimentos y la diversidad del conjunto de entrenamiento. Los mejores resultados revisados se obtienen bajo condiciones específicas y no deben asumirse como universales.

### 8.3. El pesaje aporta una referencia objetiva

La balanza comercial y las patentes relacionadas demuestran que el peso puede medirse directamente con una incertidumbre menor que una estimación puramente visual. Sin embargo, pesar no resuelve automáticamente la identificación del alimento ni garantiza que la entrada elegida en la base nutricional sea correcta. La revisión sugiere que medición, identificación y consulta nutricional deben evaluarse como componentes separados.

### 8.4. La facilidad de registro influye en el uso sostenido

Las aplicaciones comerciales reducen pasos mediante fotografías, voz, códigos de barras y sincronización. Esto responde directamente a la problemática del proyecto, pues una herramienta técnicamente precisa puede resultar poco útil si obliga al usuario a realizar demasiadas búsquedas o estimaciones manuales. No obstante, la rapidez declarada por un producto no sustituye la validación de la exactitud de sus resultados.

### 8.5. La información debe ser comprensible y trazable

Para apoyar decisiones informadas, los valores nutricionales deben indicar con claridad a qué alimento y cantidad corresponden. También conviene diferenciar entre una medición, una estimación algorítmica y un valor tomado de una base de datos. Esta trazabilidad permitiría al usuario interpretar proteínas, carbohidratos, grasas y energía sin asumir una precisión que el sistema no haya demostrado.

### 8.6. Implicancias para las siguientes etapas del proyecto

Sin definir todavía una solución final, los antecedentes permiten proponer criterios para continuar la investigación:

- Analizar por separado la identificación del alimento, la estimación de la porción y el cálculo de nutrientes.
- Considerar condiciones reales de uso y alimentos representativos del contexto peruano.
- Evaluar el esfuerzo requerido al usuario y no únicamente la precisión técnica.
- Comparar cualquier estimación con una referencia objetiva, como el pesaje directo.
- Mostrar unidades, fuente nutricional y nivel de certeza de forma comprensible.
- Evitar presentar información nutricional como diagnóstico o recomendación médica personalizada.

---

## 9. Conclusiones

1. La literatura científica confirma que es posible estimar el peso, volumen o energía de alimentos mediante imágenes; sin embargo, la precisión depende de condiciones de captura, segmentación, clasificación, referencias de escala y representatividad de los datos.

2. Las patentes muestran tres arquitecturas complementarias: reconocimiento multimodal con imágenes y voz, conexión entre balanza y aplicación, e integración de identificación, pesaje y cálculo calórico en un solo equipo. También evidencian que la existencia de una propuesta técnica no implica que su precisión haya sido validada públicamente.

3. Las tesis aportan métodos de reconstrucción, un antecedente peruano de registro fotográfico y variables nutricionales relevantes para personas físicamente activas. En especial, el estudio con deportistas destaca la importancia de relacionar los nutrientes con la cantidad realmente consumida.

4. Los productos comerciales demuestran que existe interés por reducir el ingreso manual de información. La balanza ofrece valores metrológicos verificables, mientras que las aplicaciones basadas en imágenes priorizan la rapidez y facilidad de uso, aunque sus páginas comerciales no siempre publican métricas suficientes para evaluar la precisión.

5. En conjunto, los antecedentes respaldan la pertinencia de estudiar cómo brindar información nutricional de una porción cotidiana de forma práctica y comprensible. También indican que cualquier propuesta futura deberá equilibrar exactitud, facilidad de uso, transparencia de los datos y adecuación al contexto del público objetivo.

---

## 10. Referencias

1. Fang S, Zhu F, Jiang C, Zhang S, Boushey CJ, Delp EJ. [*A Comparison of Food Portion Size Estimation Using Geometric Models and Depth Images*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6226035/). En: *2016 IEEE International Conference on Image Processing (ICIP)*. IEEE; 2016. p. 26-30. doi: [10.1109/ICIP.2016.7532312](https://doi.org/10.1109/ICIP.2016.7532312).

2. Konstantakopoulos FS, Georga EI, Fotiadis DI. [*A Novel Approach to Estimate the Weight of Food Items Based on Features Extracted from an Image Using Boosting Algorithms*](https://www.nature.com/articles/s41598-023-47885-0). *Scientific Reports*. 2023;13:21040. doi: [10.1038/s41598-023-47885-0](https://doi.org/10.1038/s41598-023-47885-0).

3. Dalakleidi KV, Papadelli M, Kapolos I, Papadimitriou K. [*Applying Image-Based Food-Recognition Systems on Dietary Assessment: A Systematic Review*](https://pmc.ncbi.nlm.nih.gov/articles/PMC9776640/). *Advances in Nutrition*. 2022;13(6):2590-2619. doi: [10.1093/advances/nmac078](https://doi.org/10.1093/advances/nmac078).

4. Puri M, Zhu Z, Lubin J, Pschar T, Divakaran A, Sawhney HS. [*Food Recognition Using Visual Analysis and Speech Recognition*](https://patents.google.com/patent/US8439683B2/en). Patente estadounidense US8439683B2. SRI International Inc.; publicada el 14 de mayo de 2013.

5. Sharma A. [*Connected Food Scale System and Method*](https://patents.google.com/patent/US20140063180/en). Solicitud de patente estadounidense US20140063180A1. BBY Solutions Inc.; publicada el 6 de marzo de 2014.

6. 公文静. [*一种自动识别食物卡路里的电子秤及方法*](https://patents.google.com/patent/CN108871530A/en). Solicitud de patente china CN108871530A. Sichuan Feixun Information Technology Co. Ltd.; publicada el 23 de noviembre de 2018.

7. Fang S. [*Single View Reconstruction for Food Portion Estimation*](https://hammer.purdue.edu/articles/thesis/SINGLE_VIEW_RECONSTRUCTION_FOR_FOOD_PORTION_ESTIMATION/7767125/1) [tesis doctoral]. West Lafayette: Purdue University; 2019.

8. Romero De Chorié GE, Tineo Ramón ME, Benavides Santur JD, Guerrero Reyes FA, Rosas Arbildo G. [*Modelo ProLab: Checkifood, aplicación móvil que ayuda al régimen alimenticio con machine learning*](http://hdl.handle.net/20.500.12404/28095) [tesis de maestría]. Lima: Pontificia Universidad Católica del Perú; 2024.

9. López Aliaga Pantigoso SC. [*Evaluación del aporte nutricional del menú del servicio de alimentación para deportistas albergados del IPD y su relación con sus requerimientos nutricionales*](http://hdl.handle.net/10757/625118) [tesis de licenciatura]. Lima: Universidad Peruana de Ciencias Aplicadas; 2019.

10. Etekcity. [*ESN00 Smart Nutrition Scale*](https://etekcity.com/products/smart-nutrition-scale-esn00) [Internet]. Consultado el 3 de septiembre de 2026.

11. Fitia. [*Contador de Calorías y Dietas con IA*](https://fitia.app/es/) [Internet]. Consultado el 3 de septiembre de 2026.

12. PerceptionLabs Inc. [*SnapCalorie - AI Calorie Tracking Made Simple*](https://www.snapcalorie.com/) [Internet]. Consultado el 3 de septiembre de 2026.

