"""Exporta SVG v2 a PDF A3 utilizando el mismo pintor vectorial de v1."""
from pathlib import Path

ROOT=Path(__file__).resolve().parent
source=(ROOT/'exportar_pdf.py').read_text(encoding='utf-8')
source=source.replace('FoodScan_Esquematico_v1','FoodScan_Esquematico_v2')
source=source.replace('Interconexion ESP32-CAM, HX711, celda de carga, puerta e iluminacion',
                      'Revision2: ESP32-S3 N16R8, OV5640(C), HX711, puerta y luces por MOSFET')
exec(compile(source,str(ROOT/'exportar_pdf.py'),'exec'))
