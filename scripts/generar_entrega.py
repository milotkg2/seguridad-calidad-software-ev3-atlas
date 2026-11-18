# -*- coding: utf-8 -*-
"""Genera diagrama, informe Word y presentación PPTX de la EP3 Atlas."""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor as PptRGB
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt as PptPt

BASE = Path(__file__).resolve().parents[1]
ENTREGA = BASE / "entrega"
CAP = BASE / "evidencias" / "atlas" / "capturas"
NAVY = RGBColor(0x18, 0x2B, 0x46)
ORANGE = RGBColor(0xEF, 0x69, 0x24)
GRAY = RGBColor(0x64, 0x6B, 0x73)
PN = PptRGB(0x18, 0x2B, 0x46)
PO = PptRGB(0xEF, 0x69, 0x24)
PW = PptRGB(0xFF, 0xFF, 0xFF)
PG = PptRGB(0x64, 0x6B, 0x73)


def font(size=18):
    for nombre in ("arial.ttf", "segoeui.ttf"):
        ruta = Path(r"C:\Windows\Fonts") / nombre
        if ruta.exists():
            return ImageFont.truetype(str(ruta), size)
    return ImageFont.load_default()


def set_run(run, size=11, bold=False, color=None, name="Arial"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    if color is not None:
        run.font.color.rgb = color


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def para(doc, text, size=11, bold=False, align="justify", color=None, before=0, after=6):
    p = doc.add_paragraph()
    p.alignment = {
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "left": WD_ALIGN_PARAGRAPH.LEFT,
    }[align]
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    run = p.add_run(text)
    set_run(run, size=size, bold=bold, color=color)
    return p


def heading(doc, text):
    return para(doc, text, size=12, bold=True, align="left", color=NAVY, before=12, after=6)


def tabla(doc, rows):
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    for ri, row in enumerate(rows):
        for ci, text in enumerate(row):
            cell = table.rows[ri].cells[ci]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(text)
            set_run(run, size=9, bold=(ri == 0), color=RGBColor(255, 255, 255) if ri == 0 else None)
            if ri == 0:
                shade(cell, "182B46")
    doc.add_paragraph()
    return table


def footer(section):
    p = section.footer.paragraphs[0]
    run = p.add_run("ISY1102  •  Informe EP3 Atlas  |  Página ")
    set_run(run, size=9, color=GRAY)
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.text = " PAGE "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    r = p.add_run()
    r._r.append(fld1)
    r._r.append(instr)
    r._r.append(fld2)
    set_run(r, size=9, color=GRAY)


def diagrama():
    CAP.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1400, 780), "#F4F7FB")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1400, 70), fill="#182B46")
    draw.text((28, 18), "Atlas EP3 · Controles de seguridad automatizados", fill="white", font=font(26))

    def caja(x, y, w, h, titulo, lineas, fill="#FFFFFF", border="#182B46"):
        draw.rectangle((x, y, x + w, y + h), fill=fill, outline=border, width=2)
        draw.rectangle((x, y, x + 10, y + h), fill="#EF6924")
        draw.text((x + 20, y + 12), titulo, fill="#182B46", font=font(18))
        yy = y + 44
        for linea in lineas:
            draw.text((x + 20, yy), linea, fill="#182B46", font=font(15))
            yy += 26

    caja(40, 100, 400, 220, "Código Atlas", ["JWT + bcrypt costo 12", "RBAC exigirEscritura 403", "SQL parametrizado $1,$2", "AES-256-GCM contacto/banco", "Auditoría RF-6"], "#FFFFFF")
    caja(500, 100, 400, 220, "Gates automatizados", ["probar.ps1 · 15 casos", "Playwright UI · 6 s", "npm audit + Trivy", "OWASP ZAP baseline", "k6 200 usuarios"], "#FFFFFF")
    caja(960, 100, 400, 220, "Norma y práctica", ["Ley 19.628 / 21.719", "Ley 21.663", "Ley 20.422 / WCAG", "OWASP cabeceras", "ISO 25010 / 29119"], "#FFFFFF")
    caja(250, 380, 900, 160, "Mitigación EP3 · nginx", ["X-Frame-Options · X-Content-Type-Options · CSP · Permissions-Policy", "ZAP WARN-NEW: 8 → 4   |   PASS: 60 → 64", "INC-06 parcialmente cerrado · 17-11-2026"], "#FFF7F0")
    draw.text((40, 580), "Flujo: código → gates → evidencia regenerable → decisión de mantenimiento / release", fill="#646B73", font=font(16))
    draw.text((40, 620), "Si se omite un gate: vuelve el riesgo que ese control cubre (RBAC, CVE, cabeceras, p95).", fill="#646B73", font=font(16))
    destino = CAP / "diagrama_controles.png"
    img.save(destino)
    return destino


def build_docx(fig_diagrama: Path):
    ENTREGA.mkdir(parents=True, exist_ok=True)
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(1.9)
    sec.bottom_margin = Cm(1.8)
    sec.left_margin = Cm(2.2)
    sec.right_margin = Cm(2.2)
    footer(sec)

    para(doc, "Duoc UC  |  INSTITUTO PROFESIONAL", size=16, bold=True, align="center", color=ORANGE, after=8)
    para(doc, "INFORME EP3 — SEGURIDAD Y CALIDAD", size=18, bold=True, align="center", color=NAVY, after=2)
    para(doc, "Optimizando el aseguramiento de la calidad y seguridad del software", size=12, bold=True, align="center", after=8)
    para(doc, "Atlas — clientes, contratos y documentos (CreaLab Spa)", size=12, align="center", after=8)
    para(doc, "ISY1102 · Sección ISY1102", size=11, align="center")
    para(doc, "Integrantes: Alison Aranda · Macarena Muñoz · Camilo Romero", size=11, align="center")
    para(doc, "Docente: Mauricio Velásquez · Fecha: 17 de noviembre de 2026", size=11, align="center", after=12)

    heading(doc, "Índice")
    for item in (
        "1. Introducción y ajustes respecto de EP1 y EP2",
        "2. Enfoques y herramientas de pruebas de seguridad",
        "3. Diagrama de controles de seguridad automatizados",
        "4. Resultados de pruebas de seguridad",
        "5. Resultados de pruebas automatizadas",
        "6. Propuestas de mitigación de defectos",
        "7. Plan de mantenimiento y preservación normativa",
        "8. Conclusiones",
        "9. Anexos",
    ):
        para(doc, item, size=12, bold=True, align="left", color=NAVY, after=2)

    heading(doc, "1. Introducción y ajustes respecto de EP1 y EP2")
    para(doc, "Atlas es la plataforma de CreaLab Spa para gestionar clientes, contratos y documentos. La EP1 definió el plan; la EP2 ejecutó el núcleo funcional y de seguridad (login, RBAC, baja lógica, documento CT-0012 y auditoría) sobre Docker. Esta EP3 optimiza el aseguramiento: re-ejecuta pruebas de seguridad, incorpora automatización UI, mitiga cabeceras de la pantalla y formaliza un plan de mantenimiento.")
    para(doc, "Ajustes a partir de los incidentes abiertos de la EP2 (no hay PDF de feedback adicional en el repositorio; se usan los hallazgos documentados):")
    tabla(doc, [
        ["Incidente EP2", "Hallazgo", "Ajuste en EP3"],
        ["INC-02", "p95 = 1,28 s con 200 usuarios", "Remedición k6: p95 = 719 ms. Sigue sobre 300 ms"],
        ["INC-03", "HTTP en localhost", "Plan de despliegue con HTTPS"],
        ["INC-04", "Correo de verificación ausente", "Backlog de mantenimiento"],
        ["INC-05", "CVE altos en Express y paquetes", "Re-ejecución npm audit y Trivy; plan de parche"],
        ["INC-06", "8 avisos ZAP en nginx", "Cabeceras aplicadas; ZAP WARN 8 → 4"],
    ])

    heading(doc, "2. Enfoques y herramientas de pruebas de seguridad")
    para(doc, "Se identifican enfoques según su función en la detección de vulnerabilidades (IE1):")
    tabla(doc, [
        ["Enfoque", "Herramienta", "Función", "Qué detecta en Atlas"],
        ["SCA dependencias", "npm audit", "CVE en librerías instaladas", "Express, body-parser, path-to-regexp, qs, send"],
        ["SCA imagen", "Trivy", "CVE en SO y paquetes de la imagen", "zlib en Alpine; 26 altos en Node de la imagen"],
        ["DAST", "OWASP ZAP baseline", "Fallos en runtime de la pantalla", "Cabeceras ausentes / fugas Server"],
        ["Acceso (dinámico)", "probar.ps1", "Control de rol en API encendida", "Editor POST/DELETE → 403"],
        ["Revisión estática", "Código API", "Controles exigidos por el ERS", "bcrypt, AES-GCM, SQL parametrizado"],
    ])
    para(doc, "SAST de producto (SonarQube) no está instalado en el equipo y no se declara como resultado. La distinción importa: npm audit y Trivy no sustituyen a ZAP, y el 403 no se deduce solo del código.")

    heading(doc, "3. Diagrama de controles de seguridad automatizados")
    para(doc, "El siguiente diagrama integra controles del código, gates automatizados y criterios normativos (IE3). Cada gate deja evidencia regenerable en evidencias/atlas.")
    if fig_diagrama.exists():
        doc.add_picture(str(fig_diagrama), width=Cm(16))
        para(doc, "Figura 1. Controles de seguridad automatizados de Atlas y vínculo normativo.", size=10, align="center", color=GRAY)
    tabla(doc, [
        ["Control", "Gate", "Norma"],
        ["JWT + bcrypt", "probar.ps1", "21.663 · NFR-SEG-2/9"],
        ["RBAC 403", "probar.ps1", "21.663 · RB-4"],
        ["AES-GCM", "Revisión + diseño", "19.628 / 21.719"],
        ["Auditoría", "probar.ps1 + Playwright", "21.663 · RF-6"],
        ["Cabeceras nginx", "ZAP antes/después", "OWASP"],
        ["Dependencias / imagen", "npm audit + Trivy", "21.663"],
    ])

    heading(doc, "4. Resultados de pruebas de seguridad")
    tabla(doc, [
        ["Prueba", "Resultado 17-11-2026", "Evidencia"],
        ["npm audit", "7 hallazgos: 3 altos, 1 moderado, 3 bajos", "seguridad/npm-audit-api.txt"],
        ["Trivy atlas-api", "Alpine 1 media; Node 26 altos, 15 medios, 0 críticos", "seguridad/trivy-api.txt"],
        ["ZAP baseline (antes)", "FAIL 0 · WARN 8 · PASS 60", "seguridad/zap-consola.txt"],
        ["ZAP baseline (después)", "FAIL 0 · WARN 4 · PASS 64", "seguridad/zap-consola-post.txt"],
        ["CP-SEG-01 editor", "403 en POST y DELETE", "automatizacion/probar-ps1.txt"],
    ])
    para(doc, "Interpretación: no hubo fallos ZAP de categoría FAIL. Los avisos de cabeceras se redujeron tras la mitigación en nginx. Los CVE altos de Express y multer permanecen abiertos (INC-05) porque el parche fuerza versiones fuera del rango fijado en el ERS (Express 4.19.2); el plan de mantenimiento prioriza esa actualización con justificación.")

    heading(doc, "5. Resultados de pruebas automatizadas")
    para(doc, "La automatización busca eficiencia y aseguramiento de calidad (IE5). Se midió el impacto en tiempo y repetición:")
    tabla(doc, [
        ["Herramienta", "Qué automatiza", "Resultado", "Impacto"],
        ["probar.ps1", "15 casos API (login, RBAC, baja, documento)", "15/15 OK", "Segundos frente a minutos manuales"],
        ["Playwright", "Login → Andina → CT-0012 → auditoría", "OK en 6,1 s", "Recorrido UI regenerable"],
        ["k6", "200 usuarios · listado clientes", "0 % error · p95 719 ms", "NFR-PERF medido; umbral 300 ms no cumple"],
    ])
    for nombre, pie in (
        ("ui_01_login_clientes.png", "Figura 2. Playwright: listado tras login de jperez."),
        ("ui_02_cliente_contratos.png", "Figura 3. Playwright: contratos del cliente Andina (CT-0012)."),
        ("ui_03_auditoria.png", "Figura 4. Playwright: vista de auditoría."),
    ):
        ruta = CAP / nombre
        if ruta.exists():
            doc.add_picture(str(ruta), width=Cm(14))
            para(doc, pie, size=10, align="center", color=GRAY)
    para(doc, "Comparación de carga: en EP2 el p95 fue 1,28 s; en EP3 es 719 ms. Hay mejora, pero INC-02 permanece abierto respecto del ERS.")

    heading(doc, "6. Propuestas de mitigación de defectos")
    tabla(doc, [
        ["ID", "Acción", "Estado"],
        ["INC-06", "Cabeceras de seguridad en nginx.conf", "Aplicado · WARN 8→4"],
        ["INC-02", "Índices/paginación en listado y re-medir k6", "Propuesto · p95 aún >300 ms"],
        ["INC-05", "Parche Express/multer + re-scan SCA", "Propuesto · priorizado"],
        ["INC-03", "HTTPS en despliegue real", "Propuesto"],
        ["INC-04", "Correo de verificación del ERS", "Propuesto · backlog"],
    ])

    heading(doc, "7. Plan de mantenimiento y preservación normativa")
    para(doc, "El plan preserva calidad, seguridad y cumplimiento a lo largo del ciclo de vida (IE7):")
    tabla(doc, [
        ["Frecuencia", "Actividad", "Norma que preserva"],
        ["Cada cambio", "probar.ps1", "Funcionalidad y RBAC (21.663)"],
        ["Cada cambio UI", "Playwright ui-flujo", "Usabilidad / regresión"],
        ["Cada release", "npm audit + Trivy + ZAP", "21.663 · OWASP"],
        ["Cada release", "k6 200 VU", "NFR-PERF"],
        ["Al publicar", "HTTPS + rotar secretos", "NFR-SEG-1 · 21.663"],
        ["Mensual", "Revisión de INC abiertos", "Mejora continua"],
    ])
    para(doc, "Criterio de salida a producción: no declarar listo mientras INC-02, INC-03 e INC-05 sigan sin mitigación aceptada.")

    heading(doc, "8. Conclusiones")
    para(doc, "Atlas en EP3 mantiene el núcleo funcional automatizado (15/15) y agrega automatización UI. Las pruebas de seguridad se ejecutaron con SCA y DAST; la mitigación de cabeceras redujo avisos ZAP de 8 a 4. El rendimiento mejoró (p95 719 ms) sin alcanzar aún los 300 ms del ERS.")
    para(doc, "El veredicto es de avance con riesgo controlado en ambiente de prueba. La calidad sostenible queda apoyada en el plan de mantenimiento y en evidencia regenerable bajo evidencias/atlas.")

    heading(doc, "9. Anexos")
    para(doc, "A. ERS: docs/ERS_Atlas_EP1.pdf")
    para(doc, "B. Ajustes: docs/02_Ajustes_EP1_EP2.md")
    para(doc, "C. Diagrama: docs/03_Diagrama_controles.md")
    para(doc, "D. Mitigación y mantenimiento: docs/04_Mitigacion_y_mantenimiento.md")
    para(doc, "E. Evidencias: evidencias/atlas/RESULTADOS_EP3.md")
    para(doc, "F. Código: codigo/atlas · https://github.com/milotkg2/seguridad-calidad-software-ev3-atlas")

    destino = ENTREGA / "Informe_EP3_Atlas.docx"
    doc.save(destino)
    print(destino)
    return destino


def add_title(slide, text, top=0.4, size=28, color=PN):
    box = slide.shapes.add_textbox(Inches(0.5), Inches(top), Inches(9), Inches(0.7))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = PptPt(size)
    p.font.bold = True
    p.font.color.rgb = color
    p.font.name = "Arial"
    return box


def add_bullets(slide, lines, top=1.3, size=16):
    box = slide.shapes.add_textbox(Inches(0.6), Inches(top), Inches(8.8), Inches(5))
    tf = box.text_frame
    tf.word_wrap = True
    for i, linea in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = linea
        p.level = 0
        p.font.size = PptPt(size)
        p.font.name = "Arial"
        p.font.color.rgb = PN
        p.space_after = PptPt(8)
    return box


def build_pptx():
    ENTREGA.mkdir(parents=True, exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    blank = prs.slide_layouts[6]

    # 1 portada
    s = prs.slides.add_slide(blank)
    shape = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(5.625))
    shape.fill.solid()
    shape.fill.fore_color.rgb = PN
    shape.line.fill.background()
    t = s.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(8.5), Inches(2.5))
    tf = t.text_frame
    p = tf.paragraphs[0]
    p.text = "Atlas · EP3"
    p.font.size = PptPt(40)
    p.font.bold = True
    p.font.color.rgb = PW
    p.font.name = "Arial"
    p2 = tf.add_paragraph()
    p2.text = "Optimizando calidad y seguridad del software"
    p2.font.size = PptPt(20)
    p2.font.color.rgb = PO
    p2.font.name = "Arial"
    p3 = tf.add_paragraph()
    p3.text = "Alison Aranda · Macarena Muñoz · Camilo Romero\nISY1102 · 17 de noviembre de 2026"
    p3.font.size = PptPt(14)
    p3.font.color.rgb = PW
    p3.font.name = "Arial"

    slides_content = [
        ("De EP2 a EP3", [
            "EP2: login, RBAC 403, baja lógica, CT-0012, auditoría",
            "Abiertos: p95, TLS, CVE Express, cabeceras nginx",
            "EP3: re-escaneo seguridad · Playwright · mitigación nginx · plan de mantenimiento",
        ]),
        ("Enfoques de seguridad (IE2)", [
            "SCA: npm audit y Trivy → CVE en librerías e imagen",
            "DAST: OWASP ZAP → cabeceras y fugas en runtime",
            "Acceso: probar.ps1 → editor recibe 403",
            "Cada enfoque cubre un riesgo distinto; no se sustituyen",
        ]),
        ("Resultados de seguridad", [
            "npm audit: 7 hallazgos (3 altos)",
            "Trivy: 0 críticos Alpine · 26 altos en paquetes Node",
            "ZAP antes: 0 FAIL · 8 WARN · 60 PASS",
            "ZAP después: 0 FAIL · 4 WARN · 64 PASS",
        ]),
        ("Automatización (IE6)", [
            "probar.ps1: 15/15 en segundos",
            "Playwright: login → Andina → CT-0012 → auditoría en 6,1 s",
            "Impacto: menos tiempo manual, evidencia regenerable",
        ]),
        ("Carga k6 · NFR-PERF", [
            "200 usuarios · 20 s · 0 % de error",
            "p95 = 719 ms (EP2: 1,28 s)",
            "ERS pide < 300 ms → INC-02 sigue abierto",
        ]),
        ("Diagrama de controles (IE4)", [
            "Código: JWT, RBAC, bcrypt, AES-GCM, auditoría",
            "Gates: scripts, ZAP, npm audit, Trivy, k6",
            "Norma: 19.628/21.719 · 21.663 · 20.422 · OWASP",
            "Ver figura diagrama_controles.png en evidencias",
        ]),
        ("Evidencia e impacto", [
            "Logs en evidencias/atlas/seguridad y automatizacion",
            "Capturas UI Playwright ui_01 a ui_03",
            "Misma prueba, otro integrante, mismo resultado",
        ]),
        ("Mitigación aplicada", [
            "nginx: X-Frame-Options, nosniff, CSP, Permissions-Policy",
            "server_tokens off",
            "ZAP WARN 8 → 4 · PASS 60 → 64",
            "INC-06 parcialmente cerrado",
        ]),
        ("Plan de mantenimiento (IE8)", [
            "Cada cambio: probar.ps1 (+ Playwright si toca UI)",
            "Cada release: npm audit + Trivy + ZAP + k6",
            "Al publicar: HTTPS y rotación de secretos",
            "Preserva 21.663 y calidad sostenible",
        ]),
        ("Reflexión normativa", [
            "19.628/21.719: contacto y banco cifrados",
            "21.663: acceso, auditoría, gestión de CVE",
            "20.422: contraste y controles grandes",
            "No se declara producción con INC-02/03/05 abiertos",
        ]),
        ("Veredicto", [
            "Cumple núcleo funcional y RBAC con automatización",
            "Seguridad ejecutada con SCA + DAST y mitigación parcial",
            "Pendiente: p95 < 300 ms, TLS, parche Express",
            "Avance con riesgo controlado en ambiente de prueba",
        ]),
        ("Cierre", [
            "Gracias",
            "Alison Aranda · Camilo Romero · Macarena Muñoz",
            "¿Preguntas? (5 minutos)",
            "Repo: seguridad-calidad-software-ev3-atlas",
        ]),
    ]

    for titulo, bullets in slides_content:
        s = prs.slides.add_slide(blank)
        bar = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.15), Inches(5.625))
        bar.fill.solid()
        bar.fill.fore_color.rgb = PO
        bar.line.fill.background()
        add_title(s, titulo)
        add_bullets(s, bullets)

    destino = ENTREGA / "Presentacion_EP3_Atlas.pptx"
    prs.save(destino)
    print(destino)
    return destino


if __name__ == "__main__":
    fig = diagrama()
    print(fig)
    build_docx(fig)
    build_pptx()
