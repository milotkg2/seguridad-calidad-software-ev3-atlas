# Guía de estudio — Atlas · defensa EP3

**Integrantes:** Alison Aranda · Macarena Muñoz · Camilo Romero  
**Ramo:** ISY1102 Seguridad y Calidad en el Desarrollo de Software  
**Docente:** Mauricio Velásquez · Sección ISY1102  
**Fecha de la ejecución EP3:** 17 de noviembre de 2026  
**Repo:** https://github.com/milotkg2/seguridad-calidad-software-ev3-atlas

La defensa es **individual** (10 min + 5 de preguntas). El orden del guion es Camilo → Alison → Macarena, pero cualquiera debe poder explicar seguridad, automatización, diagrama, mitigación y mantenimiento.

**Ponderación:** Encargo grupal 11 % + presentación individual 24 % = **35 %**.

---

# 1. Qué se hizo, en una página

1. La EP1 planificó Atlas. La EP2 ejecutó el núcleo (login, RBAC, baja lógica, CT-0012, auditoría) y dejó incidentes abiertos.
2. La EP3 **optimiza** el aseguramiento: re-ejecuta seguridad, agrega automatización UI, mitiga cabeceras y formaliza mantenimiento.
3. Se levantó Atlas con Docker (`codigo/atlas`). API en 3010, pantalla en 8080.
4. El 17-11-2026: `probar.ps1` **15/15**, Playwright OK en **6,1 s**, k6 **0 % error · p95 719 ms**, npm audit, Trivy y ZAP.
5. Mitigación: cabeceras en `nginx.conf` → ZAP WARN **8 → 4**, PASS **60 → 64**.
6. Entregables: `entrega/Informe_EP3_Atlas.docx`, `entrega/Presentacion_EP3_Atlas.pptx`, guion en `docs/05_Guion_Oral_EP3.md`.

**Frase de 25 segundos.** En EP3 re-ejecutamos seguridad con SCA y DAST, automatizamos la API y la pantalla, bajamos los avisos ZAP de 8 a 4 con cabeceras nginx, y dejamos un plan de mantenimiento. El núcleo funcional sigue en verde. El p95, el TLS y los CVE altos de Express siguen abiertos.

---

# 2. Atlas en 60 segundos

| Dato | Valor |
|---|---|
| Qué es | Gestión de clientes, contratos y documentos para pymes |
| Quién lo pide | CreaLab Spa · ERS v1.1 |
| Roles | `jperez` administrador escribe · `editor1` solo lee (RB-4) |
| Contraseña QA | `Clave#Segura2026` (solo local) |
| Datos sembrados | Empresa 1 · cliente Andina 101 · contrato CT-0012 |
| Pantalla | http://localhost:8080 |
| API | http://localhost:3010 · Swagger `/api/docs` |
| Stack | React 19 · Express 4.19 · PostgreSQL 16 · Docker Compose |

**Umbrales del ERS a memorizar**

- CRUD / listado: p95 **&lt; 300 ms** (NFR-PERF-1).
- 200 usuarios concurrentes (NFR-PERF-3).
- Contraseña: 12+ caracteres con mayúscula, minúscula, número y símbolo.
- TLS en comunicaciones (NFR-SEG-1) — en localhost sigue HTTP.

---

# 3. Conceptos (definirlos en voz alta)

| Concepto | Definición corta | Cómo aparece en EP3 |
|---|---|---|
| Calidad | Grado en que se cumplen requisitos y atributos (ISO 25010) | 15/15 funcionales · p95 medido |
| Seguridad | Confidencialidad, integridad, disponibilidad | RBAC, bcrypt, AES, ZAP, SCA |
| Cumplimiento | Ajuste a leyes y buenas prácticas | 19.628/21.719 · 21.663 · 20.422 · OWASP |
| SCA | Análisis de composición / dependencias | npm audit · Trivy |
| DAST | Prueba dinámica contra app encendida | OWASP ZAP · HTTP de probar.ps1 |
| SAST | Revisión estática de código | Lectura de API (parámetros, bcrypt, AES) |
| Automatización | Ejecutar casos sin pasos manuales repetidos | probar.ps1 · Playwright · k6 |
| Gate | Puerta de calidad: si falla, no se avanza | Scripts + ZAP + audit en cada release |
| Mitigación | Acción que reduce un defecto | Cabeceras nginx (INC-06) |
| Mantenimiento | Actividades periódicas en el ciclo de vida | Plan IE7/IE8 |
| p95 | Tiempo bajo el cual cayó el 95 % de las peticiones | k6: 719 ms |
| CVE | Vulnerabilidad publicada con identificador | Hallazgos npm audit / Trivy |
| RBAC | Acceso según rol | Editor → 403 al escribir |
| Evidencia regenerable | Otro integrante obtiene el mismo resultado con el script | Carpetas `evidencias/atlas/` |

**No confundir**

- SCA ≠ DAST. SCA lee librerías/imagen. DAST llama a la app en marcha.
- Código de salida k6 **99** = umbral de tiempo no cumplido, no “la herramienta se rompió”.
- Código npm audit **1** = hay vulnerabilidades; el informe es válido.
- `Laminas-EFT.pdf` es **otra** evaluación. No aplica a EP3.

---

# 4. Tecnologías del sistema

| Tecnología | Para qué sirve | En Atlas |
|---|---|---|
| React 19 | Pantalla de una sola página | Login, clientes, contratos, auditoría |
| Express 4.19 | API REST | Auth, CRUD, documentos, auditoría |
| PostgreSQL 16 | Datos relacionales | Empresas, usuarios, clientes, contratos |
| nginx | Sirve el build de React y proxy `/api` | Puerto 8080 · cabeceras EP3 |
| JWT | Sesión firmada | Acceso 15 min |
| Refresh token | Renovar acceso sin reescribir clave | 7 días · logout lo revoca |
| bcrypt | Hash de contraseñas | Costo 12 |
| AES-256-GCM | Cifrado en reposo | Contacto y datos bancarios |
| Docker Compose | Ambiente reproducible | Servicios `db`, `api`, `web` |
| Swagger | Documentar y probar la API | `/api/docs` |

---

# 5. Herramientas de prueba: qué son, para qué, cómo

| Herramienta | Qué es | Para qué se usa | Cómo funciona aquí | Resultado EP3 |
|---|---|---|---|---|
| Docker Compose | Orquestador de contenedores | Que cualquiera levante el mismo Atlas | `docker compose up -d --build` | Ambiente OK |
| `probar.ps1` | Script PowerShell + curl | Regresión funcional y RBAC | 15 asserts HTTP | **15/15** |
| Playwright | Automatización de navegador | Flujo real de usuario | login → Andina → CT-0012 → auditoría | **OK · 6,1 s** |
| k6 | Prueba de carga | NFR-PERF 200 VU y p95 | `pruebas/carga.js` | 0 % error · **p95 719 ms** |
| npm audit | SCA de dependencias npm | CVE en `node_modules` de la API | `docker compose exec api npm audit` | **7** (3 altos) |
| Trivy | Escáner de imagen/contenedor | CVE en Alpine y paquetes de la imagen | `trivy image atlas-api` | Alpine 1 media · Node 26 altos · 0 críticos |
| OWASP ZAP | DAST / baseline | Cabeceras y fugas en la pantalla | Baseline a `:8080` | Antes 8 WARN · después **4 WARN** |

### Cómo explicar cada una en 15 segundos

- **probar.ps1:** “Repite los casos de la API. Si alguien cambia el RBAC, el 403 falla altiro.”
- **Playwright:** “No basta la API: abre la pantalla y hace el recorrido que haría un usuario.”
- **k6:** “Simula 200 personas pidiendo el listado. Mide errores y el percentil 95.”
- **npm audit:** “Compara las librerías instaladas con avisos públicos. No llama a la API.”
- **Trivy:** “Abre la imagen Docker capa por capa: sistema y Node.”
- **ZAP:** “Con la pantalla encendida revisa respuestas y cabeceras. Por eso vio lo de nginx.”

### Impacto de la automatización (IE5 / IE6)

| Antes (manual) | Ahora |
|---|---|
| Varios minutos por corrida de login + cliente + contrato + auditoría | Playwright **~6 s** |
| Casos API a mano uno por uno | `probar.ps1` en segundos · 15/15 |
| Carga desconocida o solo “impresión” | k6 con número de p95 |

---

# 6. Enfoques de seguridad (IE1 / IE2 · 30 %)

| Enfoque | Función | Herramienta | Ejemplo Atlas |
|---|---|---|---|
| SCA dependencias | Hallar CVE en librerías | npm audit | Express / body-parser altos |
| SCA imagen | Hallar CVE en el contenedor | Trivy | zlib Alpine · paquetes Node |
| DAST | Hallar fallas en runtime | ZAP | Cabeceras ausentes → mitigadas |
| Control de acceso | Probar rol en backend | probar.ps1 | editor 403 |
| Revisión estática | Verificar controles del ERS en código | Lectura `index.js` | bcrypt, AES, SQL `$1` |

**Frase clave.** Cada enfoque cubre un riesgo distinto; **no se sustituyen**. Leer el código no reemplaza a ZAP. npm audit no reemplaza al 403.

---

# 7. Diagrama de controles (IE3 / IE4 · 14 %)

Tres bloques:

1. **Código:** JWT, bcrypt, RBAC, SQL parametrizado, AES-GCM, auditoría.
2. **Gates:** probar.ps1, Playwright, npm audit, Trivy, ZAP, k6.
3. **Norma:** 19.628/21.719, 21.663, 20.422, OWASP.

Figura: `evidencias/atlas/capturas/diagrama_controles.png`.

| Control | Gate | Norma |
|---|---|---|
| JWT + bcrypt | probar.ps1 | 21.663 · NFR-SEG-2/9 |
| RBAC 403 | probar.ps1 | 21.663 · RB-4 |
| AES-GCM | Diseño + código | 19.628 / 21.719 |
| Auditoría | probar + Playwright | 21.663 · RF-6 |
| Cabeceras nginx | ZAP antes/después | OWASP |
| Dependencias | npm audit + Trivy | 21.663 |

---

# 8. Resultados numéricos a memorizar

| Métrica | Valor |
|---|---|
| probar.ps1 | 15 correctas, 0 fallidas |
| Playwright | 4 pasos OK · 6107 ms |
| k6 peticiones / error / p95 | miles · **0 %** · **719 ms** |
| k6 EP2 (comparar) | p95 era **1,28 s** |
| npm audit | 7 (3 high, 1 moderate, 3 low) |
| Trivy Alpine | 1 medium · 0 critical/high OS |
| Trivy Node imagen | 26 high · 15 medium · 0 critical |
| ZAP antes | FAIL 0 · WARN **8** · PASS 60 |
| ZAP después | FAIL 0 · WARN **4** · PASS **64** |

---

# 9. Incidentes

| ID | Nivel | Qué es | Estado EP3 |
|---|---|---|---|
| INC-01 | Moderado | Puerto 3000 ocupado → API en 3010 | Cerrado (heredado) |
| INC-02 | Grave | p95 &gt; 300 ms | Abierto · mejoró 1,28 s → 719 ms |
| INC-03 | Moderado | Sin TLS fuera de localhost | Abierto · plan despliegue |
| INC-04 | Moderado | Sin correo de verificación | Abierto · backlog |
| INC-05 | Grave | CVE altos Express/multer | Abierto · parche priorizado |
| INC-06 | Moderado | Cabeceras nginx | **Mitigado en parte** · WARN 8→4 |

**Escala.** Crítico = cae login o cualquiera borra. Grave = umbral esencial o CVE altos. Moderado = duele y se puede seguir. Leve = cosmético.

---

# 10. Mitigación y mantenimiento (IE7 / IE8 · 20 %)

**Mitigación aplicada.** En `nginx.conf`: `server_tokens off`, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, CSP.

**Plan de mantenimiento**

| Cuándo | Qué |
|---|---|
| Cada cambio | `probar.ps1` |
| Cada cambio UI | `npm run ui` (Playwright) |
| Cada release | npm audit + Trivy + ZAP + k6 |
| Al publicar | HTTPS + rotar JWT_SECRET y DATA_KEY |
| Mensual | Revisar INC abiertos |

**Criterio de producción.** No declarar listo con INC-02, INC-03 e INC-05 abiertos sin mitigación aceptada.

---

# 11. Leyes y ética

| Norma | Vínculo con Atlas |
|---|---|
| Ley 19.628 / 21.719 | Datos personales y bancarios · cifrado AES-GCM · solo datos de prueba |
| Ley 21.663 | Acceso, auditoría, gestión de vulnerabilidades (SCA/DAST) |
| Ley 20.422 | Contraste y botones grandes · sin prueba formal con adultos mayores |
| OWASP | Cabeceras, RBAC en backend, dependencias |
| ISO 25010 / 29119 | Calidad y proceso de pruebas con evidencia |

**Ética.** Veracidad: se dice el p95 real y los CVE. Escaneos solo en Docker local. No atacar otros sistemas. Contraseña QA solo vale aquí.

---

# 12. Rúbrica: qué pesa (para priorizar el estudio)

| Peso | Encargo | Defensa |
|---|---|---|
| **30 %** | IE1 enfoques/herramientas seguridad | IE2 exponerlos |
| **24 %** | IE5 automatización | IE6 evidencias e impacto |
| **20 %** | IE7 plan de mantenimiento | IE8 comunicar el plan |
| **14 %** | IE3 diagramas | IE4 explicar diagramas |
| **12 %** | IE9 documentación | IE10 recursos visuales |

---

# 13. Quién habla (10 minutos)

| Minuto | Quién | Diapos | Foco |
|---|---|---|---|
| 0:00–3:20 | Camilo | 1–4 | Caso, ajustes, enfoques seguridad |
| 3:20–6:40 | Alison | 5–9 | Automatización, k6, diagrama, evidencia |
| 6:40–10:00 | Macarena | 10–13 | Mitigación, mantenimiento, veredicto |

Texto completo: `docs/05_Guion_Oral_EP3.md`.

---

# 14. Preguntas posibles y respuestas cortas

**1. ¿Qué cambió entre EP2 y EP3?**  
Re-escaneo de seguridad, Playwright, mitigación nginx (WARN 8→4), plan de mantenimiento y remedición k6 (p95 719 ms).

**2. ¿Por qué usaron ZAP y también npm audit?**  
ZAP es DAST (runtime). npm audit es SCA (dependencias). Detectan cosas distintas.

**3. ¿Trivy no es lo mismo que npm audit?**  
No. npm audit mira las libs de la app. Trivy mira la imagen: Alpine + lo que quedó instalado, incluidas herramientas de Node.

**4. ¿Cumplen los 200 usuarios?**  
Concurrentes sí, con 0 % de error. El tiempo p95 es 719 ms y el ERS pide menos de 300 ms. INC-02 abierto.

**5. ¿Por qué el código 99 de k6?**  
Porque cruzó el umbral de duración. La prueba sí terminó; el tiempo no cumple.

**6. ¿Qué mitigaron de verdad en código?**  
Cabeceras de seguridad en nginx. Evidencia: ZAP antes/después.

**7. ¿Por qué no parchearon Express ya?**  
El fix fuerza 4.22.3, fuera de la 4.19.2 del ERS. Quedó como INC-05 priorizado con justificación en el plan.

**8. ¿Para qué sirve Playwright si ya tienen probar.ps1?**  
probar.ps1 cubre API. Playwright cubre el recorrido de pantalla del usuario.

**9. Expliquen el diagrama en 30 segundos.**  
Controles en código, gates automáticos y norma. Si se omite un gate, vuelve el riesgo que cubría.

**10. ¿Qué es un plan de mantenimiento aquí?**  
Actividades periódicas: scripts en cada cambio, SCA/DAST/k6 en cada release, HTTPS al publicar.

**11. ¿Qué ley aplica al RUT y la cuenta bancaria?**  
19.628 actualizada por 21.719. En Atlas van cifrados con AES-GCM.

**12. ¿Qué aporta la 21.663?**  
Ciberseguridad: acceso, registro de acciones y gestión de vulnerabilidades.

**13. ¿Por qué no declaran listo para producción?**  
Por veracidad: p95, TLS y CVE altos siguen abiertos.

**14. ¿Dónde está la evidencia?**  
`evidencias/atlas/seguridad`, `automatizacion`, `capturas` y `RESULTADOS_EP3.md`. Fecha 17-11-2026.

**15. ¿Cómo lo corre otra persona?**  
Clonar el repo, `cd codigo/atlas`, `docker compose up -d --build`, `probar.ps1`. Para UI: `cd pruebas`, `npm install`, `npm run ui`.

**16. ¿SonarQube?**  
No instalado. No se declara. La revisión estática fue lectura de código + SCA.

**17. ¿La guía del profesor tenía errores?**  
Sí: la plantilla de 6 secciones no reemplaza los 5 apartados del encargo; la EFT es otra evaluación; Cypress no es obligatorio. Fuente de verdad: PDFs oficiales del encargo y la presentación.

**18. Den una recomendación completa.**  
Hallazgo: p95 719 ms. Evidencia: k6-carga.txt. Impacto: no se acredita NFR-PERF-1. Acción: optimizar listado y re-medir. Prioridad alta. Norma: NFR-PERF.

**19. ¿Qué visuales llevan a la defensa?**  
Diagrama de controles, tabla ZAP antes/después, capturas Playwright, números de k6.

**20. ¿El orden de exposición es fijo?**  
El guion sí; el docente puede llamar al azar. Cada uno debe dominar todo.

---

# 15. Comandos rápidos

```powershell
cd codigo\atlas
docker compose up -d --build
powershell -ExecutionPolicy Bypass -File .\probar.ps1

cd pruebas
npm install
npm run ui

docker compose exec api npm audit --audit-level=low
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity CRITICAL,HIGH,MEDIUM --no-progress atlas-api:latest
docker run --rm -v "${PWD}\pruebas:/scripts" grafana/k6 run /scripts/carga.js
```

ZAP (desde la raíz del repo, con Atlas arriba):

```powershell
docker run --rm -v "${PWD}\evidencias\atlas\seguridad:/zap/wrk:rw" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:8080 -I -r zap-pantalla.html
```

---

# 16. Checklist antes de entrar

- [ ] Explico SCA vs DAST vs RBAC en 40 segundos.
- [ ] Digo de memoria: 15/15 · Playwright 6 s · p95 719 ms · ZAP 8→4.
- [ ] Señalo el diagrama y una norma por control.
- [ ] Explico la mitigación nginx con evidencia.
- [ ] Recito el plan de mantenimiento (cambio / release / publicar).
- [ ] Cito 19.628/21.719 y 21.663 con un dato de Atlas.
- [ ] Digo INC-02, INC-05 e INC-03 abiertos sin maquillar.
- [ ] Sé levantar Docker y correr `probar.ps1` / Playwright.
- [ ] Leí `docs/00_Revision_guia_y_trampas.md`.
