"""Construye el informe de evidencia a partir de archivos medidos, no de valores inventados."""
from pathlib import Path
import json
from html import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

RAIZ=Path(__file__).resolve().parents[1]
SALIDA=RAIZ/"entrega"
SALIDA.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont("ArialLab",r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialLabBold",r"C:\Windows\Fonts\arialbd.ttf"))
estilos=getSampleStyleSheet()
for name in ("Normal","BodyText","Title","Heading1","Heading2"):
    estilos[name].fontName="ArialLabBold" if name in ("Title","Heading1","Heading2") else "ArialLab"
    estilos[name].textColor=colors.black
estilos["Normal"].fontSize=10.2
estilos["Normal"].leading=14
estilos["Normal"].spaceAfter=8
estilos["Title"].fontSize=23
estilos["Title"].leading=29
estilos["Title"].spaceAfter=17
estilos["Heading1"].fontSize=16
estilos["Heading1"].leading=20
estilos["Heading1"].spaceAfter=13
estilos["Heading2"].fontSize=12
estilos["Heading2"].leading=16
estilos["Heading2"].spaceBefore=10
estilos["Heading2"].spaceAfter=8
estilos.add(ParagraphStyle(name="SmallLab",fontName="ArialLab",fontSize=8.4,leading=11,spaceAfter=5))
estilos.add(ParagraphStyle(name="CodeLab",fontName="Courier",fontSize=8.2,leading=11,spaceAfter=10))
historia=[]
md=[]
def titulo(t):
    historia.append(Paragraph(escape(t),estilos["Title"]));md.append("# "+t)
def h(t):
    historia.append(Paragraph(escape(t),estilos["Heading1"]));md.append("## "+t)
def h2(t):
    historia.append(Paragraph(escape(t),estilos["Heading2"]));md.append("### "+t)
def par(t,small=False):
    historia.append(Paragraph(escape(t),estilos["SmallLab" if small else "Normal"]));md.append(t)
def tabla(headers,rows,widths):
    datos=[[Paragraph(escape(str(c)),estilos["SmallLab"]) for c in headers]]
    datos += [[Paragraph(escape(str(c)),estilos["SmallLab"]) for c in r] for r in rows]
    t=Table(datos,colWidths=widths,repeatRows=1,hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e5ebf2")),
        ("GRID",(0,0),(-1,-1),.5,colors.HexColor("#d9d9d9")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f7f9fb")])]))
    historia.extend([t,Spacer(1,10)])
    md.append("| "+" | ".join(headers)+" |\n|"+"|".join("---" for _ in headers)+"|")
    md.extend("| "+" | ".join(str(c) for c in r)+" |" for r in rows)
def code(t):
    historia.append(Preformatted(t,estilos["CodeLab"]));md.append("~~~powershell\n"+t+"\n~~~")
def pagina(): historia.append(PageBreak())
def leer(p): return json.loads((RAIZ/p).read_text(encoding="utf8"))
