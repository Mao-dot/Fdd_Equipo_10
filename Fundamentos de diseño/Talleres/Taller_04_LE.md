# Taller 04 - Lista de exigencias

## Datos generales

- **Proyecto:** Sistema de información nutricional de porciones.
- **Cliente:** DOCENTES.
- **Edición:** 01.
- **Página:** 1 de 1.
- **Fecha:** No consignada en el archivo original.
- **Revisado:** No consignado en el archivo original.
- **Elaborado:** Equipo\_10 - FUNDAMENTOS DE DISEÑO.

## Clasificación

- **E:** Exigencia obligatoria.
- **D:** Característica deseable.

## Lista de exigencias

| Característica | Fecha de cambio | Tipo | Descripción | Responsable |
|---|:---:|:---:|---|:---:|
| Función principal | 10/09/2026 | E | Informar cantidad, energía, proteínas, carbohidratos y grasas de una porción real. | MACP |
| Geometría | 10/09/2026 | D | Componente físico: dimensión mayor ≤ 30 cm. | RJCV |
| Geometría | 10/09/2026 | D | Componente físico: masa total ≤ 1.5 kg. | RJCV |
| Materia | 10/09/2026 | E | Procesar porciones sólidas y semisólidas. | LSTG |
| Materia | 10/09/2026 | D | Incluir bebidas y preparaciones mixtas. | LSTG |
| Energía | 10/09/2026 | D | Módulo propio: alimentación USB de 5 V o autonomía ≥ 4 h. | MACP |
| Señales - Entradas | 10/09/2026 | E | Identidad del alimento y cantidad de la porción. | MACP |
| Señales - Entradas | 10/09/2026 | D | Fotografía, voz o texto como registro alternativo. | MACP |
| Señales - Salidas | 10/09/2026 | E | Cantidad en g y energía en kcal. | MACP |
| Señales - Salidas | 10/09/2026 | E | Proteínas, carbohidratos y grasas en g, con fuente nutricional. | MACP |
| Control | 10/09/2026 | E | Permitir corregir alimento y cantidad antes de confirmar. | MACP |
| Electrónica (hardware) | 10/09/2026 | D | Usar cámara o sensor de masa disponible, según el concepto. | RJCV |
| Software | 10/09/2026 | E | Escalar nutrientes según la cantidad real; error de cálculo ≤ 1 %. | MACP |
| Software | 10/09/2026 | D | Guardar historial por fecha y comida. | MACP |
| Comunicaciones | 10/09/2026 | D | Registrar sin internet y sincronizar al recuperar conexión. | MACP |
| Seguridad | 10/09/2026 | E | Distinguir valores medidos y estimados; no emitir diagnósticos. | LSTG |
| Ergonomía | 10/09/2026 | E | Interfaz en español; registro ≤ 60 s y ≤ 5 acciones. | JM |
| Fabricación | 10/09/2026 | D | Usar componentes disponibles localmente para el prototipo. | RJCV |
| Fabricación | 10/09/2026 | E | Contacto con alimentos: material apto y lavable. | RJCV |
| Control de calidad | 10/09/2026 | E | Validar ≥ 30 porciones: error porcentual medio de cantidad ≤ 20 %. | LSTG |
| Uso | 10/09/2026 | E | Uso doméstico con porciones entre 3 y 5000 g. | JM |
| Mantenimiento | 10/09/2026 | D | Actualizar la base nutricional conservando fuente y versión. | COKJ |
| Costos | 10/09/2026 | D | Costo del prototipo ≤ S/ 500 y sin suscripción obligatoria. | RJCV |
| Plazos | 10/09/2026 | E | Completar el Entregable 2 hasta el 08/10/2026. | COKJ |

## Archivo editable

[Descargar Taller_04_LE.xlsx](../../Recursos/Archivos/Taller_04_LE.xlsx)
