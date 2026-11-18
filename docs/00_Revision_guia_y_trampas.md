# Revisión de la Guía paso a paso EP3 — trampas y errores

**Fuente de verdad:** `docs/oficial/EP3_Encargo.pdf` y `docs/oficial/EP3_Presentacion.pdf`.  
**Documento revisado:** `docs/oficial/Guia_Paso_a_Paso_EP3.pdf`.  
**No usar como fuente de verdad:** `Laminas-EFT.pdf` (es la Evaluación Final Transversal, otra evaluación).

La guía ayuda a ordenar el trabajo, pero el profesor avisó que puede tener errores o trampas. Abajo está lo que hay que corregir o no seguir al pie de la letra.

---

## 1. Conflicto: estructura del informe

| Qué dice la guía (diapositiva 7) | Qué exige el encargo oficial |
|---|---|
| Plantilla de 6 secciones: 1 Introducción, 2 Criterios, 3 Plan, 4 Casos, 5 Ejecución, 6 Mejora | Cinco contenidos obligatorios: ajustes de EP1/EP2, resultados de seguridad, resultados de automatización, mitigación de defectos, preservación de calidad/norma/legal |

**Trampa:** armar el informe solo con la “plantilla oficial” de 6 puntos y omitir los cinco contenidos del encargo.  
**Qué hacer:** se puede mantener una estructura larga (como en EP2), pero **cada apartado obligatorio del encargo debe aparecer con título propio y evidencia**. El índice de la guía no reemplaza al encargo.

---

## 2. Conflicto: qué debe llevar la defensa

| Guía (diapositiva 11) | Presentación oficial |
|---|---|
| Estrategia, herramientas, evidencia, defectos, reflexiones | Ejecución de pruebas de seguridad; resultados de seguridad; resultados de automatización; reflexiones calidad/seguridad/norma/legal; **plan de mantenimiento** |

**Trampa:** preparar 10 minutos sin plan de mantenimiento. En la rúbrica oral, el plan de mantenimiento es **IE8 = 20%**.  
**Qué hacer:** el cierre oral debe incluir mantenimiento (quién, cuándo, qué se re-ejecuta, qué norma se preserva).

---

## 3. Conflicto: feedback que hay que usar

| Guía | Encargo | Presentación |
|---|---|---|
| Feedback EP1 y EP2 | Feedback EP1 y EP2 | Solo menciona feedback EP1 |

**Trampa:** ignorar la EP2 porque la lámina de presentación solo cita EP1.  
**Qué hacer:** el informe debe abrir con **ajustes explícitos** según feedback de EP1 y EP2 (INC abiertos de Atlas: p95, TLS, CVE de Express, cabeceras nginx, correo de verificación).

---

## 4. Confusión con Laminas-EFT.pdf

Ese PDF está en la carpeta EV3, pero es de la **EFT** (otra evaluación): 9 apartados, nombre `ET_SECCION_GRUPO_X.pdf`, Arial 14, ponderación 8%+32%.

**Trampa:** copiar formato, nombre de archivo o estructura de 9 apartados de la EFT en la EP3.  
**Qué hacer para EP3:** Word/PDF con Arial **12** títulos / **11** cuerpo, interlineado 1,5, justificado. Encargo 11% + defensa 24% = 35%.

---

## 5. Herramientas sugeridas ≠ herramientas obligatorias

La guía recomienda Cypress/Playwright, Postman y Lighthouse. No son las únicas válidas.

**Trampa 1:** decir que “hay que usar Cypress” aunque Atlas ya tenga script HTTP, k6, ZAP, npm audit y Trivy.  
**Trampa 2:** reutilizar solo capturas de EP2 y llamarlas “automatización EP3” sin **nueva ejecución** ni evidencia de ahorro de tiempo/recursos (IE5/IE6 = 24%).  
**Qué hacer:**

- Seguridad (IE1/IE2 30%): ZAP (idealmente más profundo que solo baseline), npm audit, Trivy, y prueba de entradas/RBAC.
- Automatización (IE5/IE6 24%): dejar `probar.ps1` y k6, y **agregar** al menos un flujo UI automatizado (Playwright) o colección Postman/Newman, con log regenerable.
- No funcionales: k6 (carga) y, si cabe, Lighthouse (rendimiento/accesibilidad de la pantalla).

---

## 6. Diagrama de controles (IE3/IE4 = 14%)

La guía muestra un esquema genérico (código → gate → build).

**Trampa:** pegar un diagrama bonito sin vínculo a Atlas ni a leyes 19.628/21.719, 21.663 y 20.422.  
**Qué hacer:** un diagrama **del pipeline de Atlas** (login/JWT, RBAC, bcrypt, AES-GCM, auditoría, ZAP/npm/Trivy en CI o script) y, al lado, el criterio normativo que cubre cada control.

---

## 7. Pesos: priorizar lo que más vale

Coincide guía y rúbrica:

| Peso | Encargo | Defensa |
|---|---|---|
| 30% | IE1 enfoques/herramientas seguridad | IE2 exponerlos |
| 24% | IE5 automatización | IE6 evidencias de impacto |
| 20% | IE7 plan de mantenimiento | IE8 comunicar el plan |
| 14% | IE3 diagramas | IE4 explicar diagramas |
| 12% | IE9 documentación | IE10 recursos visuales |

**Trampa:** llenar el informe de narrativa y dejar flaca la automatización o el mantenimiento.  
**Qué hacer:** primero seguridad + automatización con evidencia, luego mantenimiento y diagrama, luego formato.

---

## 8. Otros detalles a no confundir

- Tiempo oral: **10 + 5** minutos. Defensa **individual** aunque el informe sea grupal. Orden al azar.
- “Imágenes Docker del caso” = contenedores de Atlas en ejecución, no inventar otro SUT.
- Caso del grupo: **Atlas** (no Cuidarte+). No copiar trabajos de otros grupos.
- ZAP “exploración” en la guía no obliga a un ataque activo destructivo; sí exige evidencia de seguridad con función clara (DAST). Baseline + hallazgos documentados sirve si se explica el límite.
- Código de salida de herramientas (k6=99, npm audit=1) **no** es fallo de ejecución: es umbral o hallazgos.

---

## Veredicto de la revisión

La guía es un **mapa**, no el encargo. Donde choque con `EP3_Encargo.pdf` / `EP3_Presentacion.pdf`, manda el PDF oficial. Ignorar `Laminas-EFT.pdf` para esta entrega. Partir de Atlas EP2, cerrar o documentar incidentes abiertos, y **demostrar automatización nueva** con evidencia regenerable.
