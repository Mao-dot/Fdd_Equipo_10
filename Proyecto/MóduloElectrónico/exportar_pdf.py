"""Copia PDF vectorial A3 de la vista SVG del mismo esquema editable."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.colors import toColor

ROOT=Path(__file__).resolve().parent
src=ROOT/'EasyEDA'/'FoodScan_Esquematico_v1.svg'
out=ROOT/'EasyEDA'/'FoodScan_Esquematico_v1.pdf'
c=canvas.Canvas(str(out),pagesize=landscape(A3))
c.setTitle('FoodScan - Esquema electrico del prototipo')
c.setAuthor('Equipo 10 - Fundamentos de Diseno - UPCH')
c.setSubject('Interconexion ESP32-CAM, HX711, celda de carga, puerta e iluminacion')
pw,ph=landscape(A3)
scale=min(pw/1620,ph/1145)
c.translate((pw-1620*scale)/2,(ph+1145*scale)/2)
c.scale(scale,-scale)

def paint(e):
    stroke=e.get('stroke','none'); fill=e.get('fill','none')
    if stroke!='none': c.setStrokeColor(toColor(stroke))
    if fill!='none': c.setFillColor(toColor(fill))
    c.setLineWidth(float(e.get('stroke-width',1)))
    return int(stroke!='none'),int(fill!='none')

for e in ET.parse(src).getroot():
    tag=e.tag.split('}')[-1]
    stroke,fill=paint(e)
    if tag=='rect':
        c.rect(*[float(e.get(k,0)) for k in ('x','y','width','height')],stroke=stroke,fill=fill)
    elif tag=='circle':
        c.circle(*[float(e.get(k)) for k in ('cx','cy','r')],stroke=stroke,fill=fill)
    elif tag in ('polyline','polygon'):
        nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',e.get('points'))))
        p=c.beginPath(); p.moveTo(nums[0],nums[1])
        for i in range(2,len(nums),2): p.lineTo(nums[i],nums[i+1])
        if tag=='polygon': p.close()
        c.drawPath(p,stroke=stroke,fill=fill)
    elif tag=='path':
        tokens=re.findall(r'[MLml]|-?\d+(?:\.\d+)?',e.get('d'))
        p=c.beginPath(); x=y=0; i=0; command='M'
        while i<len(tokens):
            if tokens[i] in ('M','L','m','l'): command=tokens[i]; i+=1
            a,b=map(float,tokens[i:i+2]); i+=2
            if command.islower(): a+=x; b+=y
            x,y=a,b
            if command.upper()=='M': p.moveTo(x,y); command='L'
            else: p.lineTo(x,y)
        c.drawPath(p,stroke=stroke,fill=fill)
    elif tag=='text':
        x=float(e.get('x')); y=float(e.get('y')); size=float(e.get('font-size','10pt').replace('pt',''))*96/72
        c.saveState(); c.translate(x,y); c.scale(1,-1)
        c.setFont('Helvetica-Bold' if e.get('font-weight')=='bold' else 'Helvetica',size)
        value=e.text or ''; anchor=e.get('text-anchor','start')
        {'start':c.drawString,'end':c.drawRightString,'middle':c.drawCentredString}[anchor](0,0,value)
        c.restoreState()
    else:
        raise ValueError(tag)
c.showPage(); c.save()
print(out)
