# Plan de pasos — EP3 Atlas

**Grupo:** Alison Aranda, Macarena Muñoz, Camilo Romero  
**Caso:** Atlas (CreaLab Spa) · ISY1102  
**Ponderación:** Encargo grupal 11% + defensa individual 24% = 35%

Este plan se basa en el encargo y la presentación oficiales. La guía del profesor se usa solo como apoyo; ver `00_Revision_guia_y_trampas.md`.

---

## Objetivo de la EP3

Sobre el mismo Atlas de la EP2:

1. Ejecutar y documentar **pruebas de seguridad** (enfoques + función + evidencia).
2. Incorporar **automatización** funcional y no funcional, con ahorro de tiempo/recursos demostrable.
3. Elaborar un **diagrama** de controles de seguridad automatizados ligados a norma/ley.
4. Proponer **mitigación** de defectos y un **plan de mantenimiento** para iteraciones futuras.
5. Ajustar lo hecho en EP1/EP2 según feedback e incidentes abiertos.

---

## Herencia de la EP2 (punto de partida)

Ya existe y se reutiliza como base (no se inventa otro sistema):

| Pieza | Estado EP2 | Qué pide la EP3 |
|---|---|---|
| Login, RBAC 403, baja lógica, CT-0012, auditoría | Ejecutado | Mantener + automatizar |
| k6 200 VU, p95 1,28 s | No cumple 300 ms (INC-02) | Remedir o mitigar y documentar |
| npm audit / Trivy | Hallazgos altos (INC-05) | Seguridad + plan de parche |
| ZAP baseline pantalla | 0 FAIL, 8 WARN (INC-06) | Seguridad + mitigación cabeceras |
| TLS / correo verificación | INC-03 / INC-04 abiertos | Mantenimiento / backlog |

---

## Orden de trabajo (no saltar)

### Paso 0 — Ambiente (día 1)

1. Clonar este repositorio.
2. `cd codigo/atlas` → `docker compose up -d --build`.
3. Verificar http://localhost:8080 y http://localhost:3010/api/salud.
4. Correr `powershell -ExecutionPolicy Bypass -File .\probar.ps1` (debe dar 15 correctas).

### Paso 1 — Ajustes EP1/EP2 (encargo, apartado 1)

1. Listar feedback del docente (si hay escrito) + incidentes INC-01…INC-06.
2. Decidir por cada uno: cerrado / mitigado / aceptado con plan.
3. Redactar sección “Ajustes respecto de EP1 y EP2” con evidencia.

### Paso 2 — Pruebas de seguridad (IE1 30%)

Ejecutar y guardar en `evidencias/atlas/seguridad/`:

1. **DAST:** OWASP ZAP contra pantalla (y, si es posible, API documentada).
2. **SCA:** `npm audit` en el contenedor API.
3. **Imagen:** Trivy sobre `atlas-api`.
4. **Acceso:** reconfirmar RBAC (editor 403) y política de contraseña/JWT.
5. **Entradas:** al menos un caso negativo (inyección / tipo de archivo / campo vacío) con resultado esperado.

En el informe: tabla enfoque → herramienta → función → hallazgo → criticidad.

### Paso 3 — Automatización (IE5 24%)

Dejar scripts regenerables en el repo:

1. Mantener `probar.ps1` (API funcional/seguridad).
2. Mantener `pruebas/carga.js` (k6, NFR carga).
3. **Agregar** una de estas (mínimo una nueva respecto de EP2):
   - Playwright: login + listado + contrato CT-0012, o
   - Postman/Newman: colección de endpoints críticos.
4. Opcional: Lighthouse sobre http://localhost:8080 (rendimiento/accesibilidad).
5. Medir y escribir: “antes X minutos manual / ahora Y segundos con script”.

Evidencia en `evidencias/atlas/automatizacion/`.

### Paso 4 — Diagrama de controles (IE3 14%)

1. Dibujar pipeline Atlas: commit/build → contenedor → API (JWT, RBAC, bcrypt, AES-GCM, SQL parametrizado, auditoría) → pantalla → gates (npm audit, Trivy, ZAP, pruebas auto).
2. Anotar al lado: Ley 19.628/21.719, 21.663, 20.422 / OWASP.
3. Insertar figura en el informe y ensayar su explicación oral (IE4).

### Paso 5 — Mitigación y mantenimiento (IE7 20%)

1. Propuestas concretas por defecto (cabeceras nginx, Express, p95, HTTPS, correo).
2. Plan de mantenimiento: frecuencia (ej. cada sprint), responsables del grupo, qué se re-ejecuta, qué se monitorea, qué norma se preserva.
3. No inventar CI de GitHub Actions si el token no tiene scope `workflow`; documentar scripts locales como puerta de calidad.

### Paso 6 — Informe grupal (IE9 12%)

Apartados mínimos del encargo (obligatorios):

1. Ajustes EP1/EP2.
2. Resultados de pruebas de seguridad.
3. Resultados de pruebas automatizadas.
4. Propuestas de mitigación.
5. Propuestas para preservar calidad, seguridad y cumplimiento.

Formato: Arial 12/11, interlineado 1,5, justificado, portada completa, capturas legibles.  
Salida: `entrega/Informe_EP3_Atlas.docx` (o PDF).

### Paso 7 — Presentación y guion (defensa 24%)

Contenido oral obligatorio:

1. Ejecución de pruebas de seguridad.
2. Resultados de seguridad.
3. Resultados de automatización (con evidencia visual).
4. Reflexiones calidad / seguridad / norma / legal.
5. Plan de mantenimiento.

Tiempo: 10 min + 5 preguntas. Orden al azar. Guion equitativo Camilo → Alison → Macarena.  
Salida: `entrega/Presentacion_EP4_Atlas.pptx` y `docs/02_Guion_Oral.md`.

### Paso 8 — Entrega AVA

1. Subir informe + material de apoyo el día de la evaluación.
2. Ensayo completo del grupo (cada uno domina todo el proyecto).

---

## Prioridad según rúbrica

1. Seguridad con ejemplos (30%).
2. Automatización con evidencia de impacto (24%).
3. Plan de mantenimiento ligado a norma (20%).
4. Diagrama de controles (14%).
5. Documentación y visuales (12%).

---

## Qué no hacer

- No usar la estructura ni el formato de `Laminas-EFT.pdf`.
- No copiar Cuidarte+ ni el laboratorio Alumnos.
- No declarar cerrado un INC sin evidencia nueva.
- No afirmar SonarQube/JMeter si no se ejecutaron.
- No apagar Docker antes de ZAP/k6/Playwright.
