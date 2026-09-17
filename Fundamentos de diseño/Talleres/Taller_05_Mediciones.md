# Taller 05 - Mediciones y errores

## Configuraciones evaluadas

| Configuración | Lecturas | Valor de referencia (V) | Promedio medido (V) | Error absoluto medio (V) | Error relativo medio | Error porcentual medio |
|---|---:|---:|---:|---:|---:|---:|
| 5 V / 1 A | 10 | 5.000 | 4.998 | 0.002 | 0.000400 | 0.0400 % |
| 3.3 V / 1 A | 10 | 3.300 | 3.305 | 0.005 | 0.001515 | 0.1515 % |
| 12 V / 1 A | 10 | 12.000 | 11.970 | 0.030 | 0.002500 | 0.2500 % |

## Cálculo

El error absoluto se calcula mediante:

\[
E_a = \left|V_{medido} - V_{referencia}\right|
\]

El error relativo se calcula mediante:

\[
E_r = \frac{E_a}{V_{referencia}}
\]

El error porcentual corresponde a \(E_r \times 100\).

## Archivo de trabajo

[Descargar Taller_05_Mediciones.xlsx](../../Recursos/Archivos/Taller_05_Mediciones.xlsx)

## Resultados y conclusiones

- Se registraron 30 lecturas: 10 para cada configuración.
- Las lecturas repetidas se conservaron sin introducir variaciones artificiales.
- La configuración de 5 V presentó el menor error relativo medio: 0.000400, equivalente a 0.0400 %.
- La configuración de 12 V presentó el mayor error relativo medio: 0.002500, equivalente a 0.2500 %.
- En las tres configuraciones, las diez lecturas coinciden dentro de la precisión registrada en el archivo original.
