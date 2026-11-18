# -*- coding: utf-8 -*-
"""Presentación EP3 con el diseño Duoc de la guía rediseñada."""
from __future__ import annotations

import shutil
from pathlib import Path

from pptx import Presentation

BASE = Path(__file__).resolve().parents[1]
GUIA = Path(r"C:\Users\Razon\Downloads\Presentacion_EP4_API_Alumnos_rediseño (1).pptx")
DESTINO = BASE / "entrega" / "Presentacion_EP3_Atlas.pptx"


def poner(shape, nuevo: str):
    lineas = nuevo.split("\n")
    tf = shape.text_frame
    parrafos = list(tf.paragraphs)
    for i, linea in enumerate(lineas):
        if i < len(parrafos):
            p = parrafos[i]
            if p.runs:
                p.runs[0].text = linea
                for run in p.runs[1:]:
                    run.text = ""
            else:
                p.text = linea
        else:
            tf.add_paragraph().text = linea
    for p in parrafos[len(lineas):]:
        for run in p.runs:
            run.text = ""


def poner_celda(cell, texto: str):
    p = cell.text_frame.paragraphs[0]
    if p.runs:
        p.runs[0].text = texto
        for run in p.runs[1:]:
            run.text = ""
    else:
        p.text = texto


def main():
    if not GUIA.exists():
        raise SystemExit(f"No está la guía: {GUIA}")
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(GUIA, DESTINO)
    prs = Presentation(DESTINO)

    # Reemplazos globales (texto exacto de la plantilla → Atlas EP3)
    cambios = {
        "ISY1102 · EP4": "ISY1102 · EP3",
        "API de Alumnos\nLaboratorio 15-all": "Atlas\nClientes, contratos y documentos",
        "Verificando la calidad, seguridad y cumplimiento normativo":
            "Optimizando calidad, seguridad y automatización",
        "Seguridad y Calidad en el Desarrollo de Software\nAlison Aranda · Macarena Muñoz · Camilo Romero\nDocente: Mauricio Velásquez · 16 de octubre de 2026":
            "Seguridad y Calidad en el Desarrollo de Software\nAlison Aranda · Macarena Muñoz · Camilo Romero\nDocente: Mauricio Velásquez · 17 de noviembre de 2026",
        "Recorrido de la defensa": "Recorrido de la defensa EP3",
        "El sistema bajo prueba": "Ajustes desde EP2",
        "SUT": "INC abiertos",
        "De EP01 a EP3": "Seguridad",
        "Plan → ejecución": "Enfoques",
        "Estrategia y tipos": "Resultados SCA/DAST",
        "Origen e impacto": "npm · Trivy · ZAP",
        "Herramientas": "Automatización",
        "Pipeline 01–14": "probar · Playwright · k6",
        "Pruebas, Docker, Trivy": "Evidencia e impacto",
        "Resultados reales": "Diagrama y mitigación",
        "403, baja lógica, auditoría": "Cabeceras · WARN 8→4",
        "Incidentes y cierre": "Mantenimiento y veredicto",
        "Ética, normas, veredicto": "Plan · normas · cierre",
        "El sistema: API de Alumnos": "Ajustes EP2 → EP3",
        "Microservicio Spring Boot 3": "Incidentes heredados",
        "Maven + SQLite · CRUD en /api/v1/alumnos": "INC-02 p95 · INC-05 CVE · INC-06 cabeceras",
        "Documentada con OpenAPI": "EP3 re-ejecuta seguridad",
        "Swagger y Redoc incluidos": "Agrega Playwright UI",
        "Laboratorio 15-all": "Mitiga nginx",
        "Todas las tools · módulos con-error y sin-error": "Formaliza mantenimiento",
        "Datos personales de alumnos": "Datos de clientes pyme",
        "RUT, nombre, email · Ley 19.628 / 21.719": "Contacto y banco · Ley 19.628 / 21.719",
        "Infraestructura · SQLite, REST, OpenAPI": "React 19 · Express 4.19 · PostgreSQL 16",
        "Aplicación · casos de uso": "JWT · RBAC · AES-GCM",
        "Alumno · reglas de negocio": "Auditoría RF-6",
        "De EP01 a EP3: del plan a la evidencia": "Enfoques de seguridad",
        "Ejecución en el laboratorio 15-all": "Ejecución sobre Atlas en Docker",
        "EP01": "SCA",
        "Plan de pruebas (caso Atlas)": "npm audit + Trivy",
        "Estrategia y tipos de prueba": "CVE en librerías e imagen",
        "Criterios, trazabilidad y ética": "Función: hallar dependencias vulnerables",
        "EP3": "DAST",
        "Ejecución sobre Atlas en Docker": "OWASP ZAP + probar.ps1",
        "Login, 403, baja lógica y documento": "Cabeceras y RBAC 403",
        "Evidencia HTTP del 17-10-2026": "Función: runtime y acceso",
        "Meta: detectar, clasificar y remediar, sin “maquillar” resultados":
            "Meta: cada enfoque cubre un riesgo distinto; no se sustituyen",
        "Estrategia: enfoque mixto con prioridades": "Resultados de seguridad · 17-11-2026",
        "Automatizado con Maven y CI, más revisión manual de reportes":
            "SCA y DAST con evidencia anexada",
        "Prioridad 1": "npm audit",
        "Estáticos": "7 hallazgos",
        "Prioridad 2": "Trivy",
        "Unitarias y cobertura": "0 críticos Alpine",
        "Prioridad 3": "ZAP antes",
        "SCA y contenedor": "0 FAIL · 8 WARN",
        "Prioridad 4": "ZAP después",
        "DAST": "0 FAIL · 4 WARN",
        "Prioridad 5": "RBAC",
        "Carga": "editor 403",
        "JDK 21 · Docker · proyecto 15-all": "Docker Atlas · jperez / editor1",
        "verify OK · ZAP FAIL=0 · métricas bajo SLA · evidencia anexada":
            "PASS 64 · WARN 4 · evidencia anexada",
        "Tipos de prueba: origen e impacto": "Automatización: origen e impacto",
        "Indicador IE4 · 38 % de la pauta": "Indicador IE5/IE6 · 24 % de la pauta",
        "Herramientas: pipeline 01–14": "Herramientas de automatización",
        "01–04": "API",
        "Calidad de código": "probar.ps1",
        "Spotless · Checkstyle · PMD · SpotBugs": "15/15 en segundos",
        "05–07 · 10": "UI",
        "Pruebas y cobertura": "Playwright",
        "JUnit · PIT · JaCoCo · Cucumber": "login → Andina → CT-0012",
        "08–09": "Carga",
        "Gate y dependencias": "k6 200 VU",
        "SonarQube · Snyk": "p95 = 719 ms",
        "11": "Repo",
        "Contenedor": "Evidencias",
        "Docker · Trivy": "logs + capturas",
        "12": "Fecha",
        "Seguridad dinámica": "17-11-2026",
        "OWASP ZAP": "regenerable",
        "13–14": "Impacto",
        "Carga y rendimiento": "menos tiempo",
        "Gatling · JMeter": "misma cobertura",
        "Cada herramienta cubre un riesgo distinto · integración continua con GitHub Actions":
            "Automatizar ahorra minutos y deja evidencia repetible",
        "Ejecución real: resultados": "Ejecución real: automatización",
        "46": "15",
        "tests, 0 fallos": "casos API OK",
        "mvn clean verify · BUILD SUCCESS": "probar.ps1 · 15/15",
        "94 %": "6 s",
        "mutaciones eliminadas": "flujo UI Playwright",
        "PIT 16/17 · umbral 80 %": "Andina · CT-0012 · auditoría",
        "12 ms": "0 %",
        "media de respuesta": "error en k6",
        "Gatling y JMeter · 0 errores": "200 usuarios · 20 s",
        "0": "719",
        "alertas ZAP (FAIL)": "ms de p95",
        "58 PASS · cabeceras OK": "ERS pide < 300 ms",
        "Prueba funcional del CRUD": "Códigos y métricas",
        "POST crear alumno": "login 200",
        "RUT duplicado": "editor 403",
        "DELETE eliminar": "Playwright OK",
        "GET tras eliminar": "k6 0 % error",
        "Docker + Trivy: imagen verificada": "Diagrama de controles",
        "Imagen alumnos-api:1.0.0": "Código: JWT · RBAC · AES · auditoría",
        "Base eclipse-temurin:21-jre-alpine": "Gates: scripts · ZAP · audit · Trivy · k6",
        "Usuario no-root (app)": "Norma: 19.628 · 21.663 · 20.422 · OWASP",
        "Superficie mínima con Alpine": "nginx: cabeceras de seguridad",
        "trabajo-grupo/evidencias/docker/": "evidencias/atlas/capturas/diagrama_controles.png",
        "vulnerabilidades CRITICAL / HIGH en el SO (Trivy)": "ZAP WARN 8 → 4 tras mitigar",
        "smoke test GET /api/v1/alumnos": "PASS 60 → 64",
        "Origen: asegurar el empaquetado    Impacto si se omite: CVE en runtime o ejecución como root":
            "Origen: integrar controles. Impacto si se omite: no se demuestra norma ni gate.",
        "Incidentes: origen e impacto": "Mitigación: origen e impacto",
        "INC-01": "INC-06",
        "MODERADO": "MITIGADO",
        "Spotless falla por CRLF": "Cabeceras nginx",
        "Finales de línea CRLF en Windows": "ZAP marcó clickjacking y CSP",
        "El gate de formato corta el build": "Pantalla sin X-Frame / nosniff",
        "spotless:apply": "Headers en nginx.conf",
        "Java 24 rompe Mockito": "INC-02 / INC-05",
        "Entorno distinto al JDK 21 que exige el lab": "p95 719 ms · CVE Express",
        "16 errores: no se podía demostrar el Quality Gate": "Aún sobre 300 ms · parche pendiente",
        "Temurin 21 instalado, suite en verde": "Quedan abiertos priorizados",
        "Contraste didáctico: módulos con-error (Snyk, ZAP, Trivy) frente a 15-all ya remediado":
            "INC-03 TLS y INC-04 correo quedan en el plan de mantenimiento.",
        "Ética y normativa": "Plan de mantenimiento",
        "Confidencialidad": "Cada cambio",
        "Solo datos de prueba": "probar.ps1 (+ Playwright)",
        "Veracidad": "Cada release",
        "Se reportó Spotless y Java 24": "audit · Trivy · ZAP · k6",
        "No maleficencia": "Al publicar",
        "Escaneos solo en QA local": "HTTPS + rotar secretos",
        "Mejora continua": "Mensual",
        "Remediación priorizada": "revisar INC abiertos",
        "Ley 19.628 / 21.719": "Ley 19.628 / 21.719",
        "Protección de datos personales: RUT, nombre, email": "Clientes, contacto y banco cifrados",
        "Ley 21.663": "Ley 21.663",
        "Marco de ciberseguridad: SCA, DAST, imagen, cabeceras": "Acceso, auditoría y gestión de CVE",
        "OWASP · ISO 25010 / 27001 / 29119": "OWASP · ISO 25010 / 29119",
        "Calidad, seguridad y proceso con evidencia": "Calidad sostenible con evidencia",
        "Recomendaciones": "Recomendaciones EP3",
        "1": "1",
        "Fijar JDK 21 en el equipo y en CI": "Bajar p95 bajo 300 ms",
        "Entorno": "Rendimiento",
        "2": "2",
        ".gitattributes con eol=lf + Spotless en pre-commit": "Parchear Express y multer",
        "Calidad": "SCA",
        "3": "3",
        "Completar SonarQube y Snyk con los tokens del grupo": "Publicar solo con HTTPS",
        "Gates": "TLS",
        "4": "4",
        "Agregar autenticación (JWT / API key) si la API se expone": "Correo de verificación ERS",
        "Seguridad": "Funcional",
        "5": "5",
        "Actualizar Spring Boot ante CVE transitivas (.snyk)": "Mantener gates en cada release",
        "Mantención": "Ciclo de vida",
        "Veredicto y cierre": "Veredicto y cierre",
        "VEREDICTO": "VEREDICTO",
        "Con JDK 21, la API 15-all cumple calidad, seguridad dinámica y rendimiento":
            "Atlas cumple núcleo funcional, RBAC y automatización EP3",
        "De diseñar en EP01 a ejecutar con evidencia auditable":
            "p95, TLS y CVE altos siguen abiertos",
        "Riesgos residuales": "Riesgos residuales",
        "API sin autenticación\nCVE transitivas aceptadas en .snyk":
            "Pendiente: NFR-PERF 300 ms · TLS · Express",
        "¿Preguntas?": "¿Preguntas?",
        "Gracias · Alison Aranda · Camilo Romero · Macarena Muñoz":
            "Gracias · Alison Aranda · Camilo Romero · Macarena Muñoz",
    }

    for numero, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if shape.has_text_frame:
                actual = shape.text_frame.text
                # Evitar colisiones con números de página / métricas pequeñas
                if actual in ("0", "11", "12") and numero not in (8, 12):
                    if actual == "0" and numero == 8:
                        poner(shape, "719")
                    continue
                if numero == 8 and actual == "0":
                    poner(shape, "719")
                elif numero == 9 and actual == "0":
                    poner(shape, "8→4")
                elif numero == 9 and actual == "200":
                    poner(shape, "64")
                elif actual in cambios:
                    poner(shape, cambios[actual])
            if shape.has_table:
                filas = [
                    ["Tipo", "Herramienta", "Origen", "Impacto si se omite"],
                    ["API", "probar.ps1", "RF/RB ERS", "No hay regresión repetible"],
                    ["UI", "Playwright", "NFR-USAB", "Solo se prueba a mano"],
                    ["Carga", "k6", "NFR-PERF", "No se conoce el p95"],
                    ["SCA", "npm audit", "21.663", "CVE ocultas en dependencias"],
                    ["Imagen", "Trivy", "21.663", "CVE en el contenedor"],
                    ["DAST", "OWASP ZAP", "OWASP", "Cabeceras y fugas en runtime"],
                    ["Acceso", "RBAC HTTP", "RB-4", "El editor escribe por API"],
                ]
                for ri, row in enumerate(shape.table.rows):
                    for ci, cell in enumerate(row.cells):
                        poner_celda(cell, filas[ri][ci])

    prs.save(DESTINO)
    print(DESTINO)


if __name__ == "__main__":
    main()
