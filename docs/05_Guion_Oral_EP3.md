# Guion oral EP3 — 10 minutos + 5 de preguntas

**Orden:** Camilo → Alison → Macarena · ~3 min 20 s cada uno.  
Defensa individual: cualquiera debe poder explicar todo el proyecto.

| Quién | Tiempo | Diapositivas | Foco |
|---|---|---|---|
| Camilo | 0:00–3:20 | 1–4 | Caso, ajustes EP2, enfoques de seguridad |
| Alison | 3:20–6:40 | 5–9 | Automatización, evidencias, diagrama |
| Macarena | 6:40–10:00 | 10–13 | Mitigación, mantenimiento, veredicto |

---

## Camilo (0:00–3:20)

**Diapo 1.** Somos Alison, Macarena y Camilo. EP3 sobre Atlas: optimizar aseguramiento de calidad y seguridad. Encargo grupal 11 %, defensa 24 %.

**Diapo 2.** En EP2 dejamos abiertos el p95, TLS, CVE de Express y cabeceras. En EP3 re-ejecutamos seguridad, agregamos Playwright y mitigamos nginx.

**Diapo 3 — enfoques.** SCA con npm audit y Trivy: miran dependencias e imagen. DAST con ZAP: mira la pantalla encendida. Acceso con probar.ps1: el editor recibe 403. Cada enfoque detecta un tipo distinto de vulnerabilidad.

**Diapo 4.** npm audit: 7 hallazgos, 3 altos. Trivy: 0 críticos en Alpine, 26 altos en paquetes Node. ZAP: 0 fallos; avisos de cabeceras. Paso a Alison.

## Alison (3:20–6:40)

**Diapo 5.** Automatización: `probar.ps1` deja 15/15 en segundos. Playwright recorre login, Andina, CT-0012 y auditoría en unos 6 segundos. Manualmente ese flujo toma varios minutos.

**Diapo 6.** k6 con 200 usuarios: 0 % de error. p95 = 719 ms. Mejoró respecto de 1,28 s de EP2, pero el ERS pide 300 ms. INC-02 sigue abierto.

**Diapo 7 — diagrama.** Controles en código (JWT, RBAC, bcrypt, AES, auditoría) y gates (scripts, ZAP, audit, Trivy, k6). Cada uno apunta a 19.628, 21.663, 20.422 u OWASP.

**Diapo 8.** Evidencias en el repo: logs y capturas con fecha 17-11-2026. La automatización reduce tiempo y hace repetible la prueba.

**Diapo 9.** Impacto: menos tiempo manual, misma cobertura funcional, más cobertura de seguridad. Paso a Macarena.

## Macarena (6:40–10:00)

**Diapo 10.** Mitigación: pusimos cabeceras en nginx. ZAP bajó de 8 a 4 avisos. Quedan CVE de Express y el p95.

**Diapo 11 — mantenimiento.** Cada cambio: probar.ps1. Cada release: audit, Trivy, ZAP, k6. Al publicar: HTTPS. Eso preserva 21.663 y calidad en el tiempo.

**Diapo 12.** Reflexión: Atlas cumple el núcleo funcional y el RBAC. No está listo para producción con INC-02, INC-03 e INC-05 abiertos. La EP3 muestra detección, mitigación parcial y plan.

**Diapo 13.** Veredicto y gracias. Preguntas.

---

## Preguntas típicas (5 min)

- ¿Por qué ZAP y no solo leer el código? Porque DAST ve lo que el servidor envía en runtime.
- ¿Por qué Playwright además de probar.ps1? La API no cubre el recorrido de pantalla del usuario.
- ¿Cumplen los 200 usuarios? Concurrentes sí, con 0 % error; el tiempo p95 no.
- ¿Qué ley aplica al RUT/banco? 19.628 / 21.719; cifrado AES-GCM.
- ¿Qué mantiene la calidad después? El plan de mantenimiento del diapo 11.
