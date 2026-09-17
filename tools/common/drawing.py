"""Simple paired SVG/PDF drawing surface, with top-left page coordinates."""
from pathlib import Path
from html import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
class Drawing:
    def __init__(self,width,height,pdf_path,svg_path=None,title='Homes concept'):
        self.w,self.h=width,height;self.svg_path=svg_path
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
        self.pdf=canvas.Canvas(str(pdf_path),pagesize=(width*.5,height*.5));self.pdf.scale(.5,.5);self.pdf.setTitle(title)
    def rect(self,x,y,w,h,fill='none',stroke='none',sw=1):
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        if fill!='none':self.pdf.setFillColor(HexColor(fill))
        if stroke!='none':self.pdf.setStrokeColor(HexColor(stroke))
        self.pdf.setLineWidth(sw);self.pdf.rect(x,self.h-y-h,w,h,fill=int(fill!='none'),stroke=int(stroke!='none'))
    def line(self,x1,y1,x2,y2,color='#27352b',sw=1):
        self.svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>');self.pdf.setStrokeColor(HexColor(color));self.pdf.setLineWidth(sw);self.pdf.line(x1,self.h-y1,x2,self.h-y2)
    def text(self,x,y,t,size=16,color='#27352b',anchor='start',bold=False):
        self.svg.append(f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{700 if bold else 400}">{escape(t)}</text>')
        self.pdf.setFillColor(HexColor(color));self.pdf.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
        {'start':self.pdf.drawString,'middle':self.pdf.drawCentredString,'end':self.pdf.drawRightString}[anchor](x,self.h-y,t)
    def circle(self,x,y,r,fill,stroke='none',sw=1):
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>');self.pdf.setFillColor(HexColor(fill))
        if stroke!='none':self.pdf.setStrokeColor(HexColor(stroke))
        self.pdf.setLineWidth(sw);self.pdf.circle(x,self.h-y,r,fill=1,stroke=int(stroke!='none'))
    def image(self,path,x,y,w,h):self.pdf.drawImage(str(path),x,self.h-y-h,width=w,height=h)
    def save(self):
        self.svg.append('</svg>')
        if self.svg_path:Path(self.svg_path).write_text('\n'.join(self.svg))
        self.pdf.save()
