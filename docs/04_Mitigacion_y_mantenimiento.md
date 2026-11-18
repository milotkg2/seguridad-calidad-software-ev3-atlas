# Mitigación de defectos y plan de mantenimiento — Atlas EP3

## 1. Propuestas de mitigación

| ID | Defecto | Criticidad | Mitigación | Estado EP3 |
|---|---|---|---|---|
| INC-02 | p95 del listado sobre 300 ms | Grave | Índice en búsqueda de clientes, paginación, caché de lectura; re-medir con k6 | Abierto. p95 bajó de 1,28 s a 719 ms |
| INC-03 | HTTP en localhost | Moderado | TLS en despliegue (reverse proxy + certificado) | Abierto · plan de despliegue |
| INC-04 | Sin correo de verificación | Moderado | Flujo de verificación post-registro según ERS | Abierto · backlog |
| INC-05 | CVE altos en Express/body-parser/multer | Grave | Plan de parche a Express ≥4.22.3 y multer 2.x; re-correr npm audit y Trivy; justificar cambio vs ERS 4.19.2 | Abierto · priorizado |
| INC-06 | Cabeceras nginx ausentes | Moderado | Cabeceras en `nginx.conf` | **Mitigado en parte**: ZAP WARN 8 → 4 |
| — | Avisos ZAP restantes (caché, COEP, unsafe-inline) | Leve/Moderado | Cache-Control en estáticos; endurecer CSP; COEP si aplica | Abierto menor |

## 2. Plan de mantenimiento (ciclo de vida)

Objetivo: preservar calidad, seguridad y cumplimiento en futuras iteraciones (IE7 / IE8).

| Frecuencia | Actividad | Responsable sugerido | Evidencia |
|---|---|---|---|
| Cada cambio de código | `docker compose up -d --build` + `probar.ps1` | Quien integra | Log 15/15 |
| Cada cambio de UI | `npm run ui` (Playwright) | Frontend | `playwright-ui.txt` |
| Cada release candidato | npm audit + Trivy + ZAP baseline | Seguridad del grupo | Carpeta `evidencias/.../seguridad` |
| Cada release | k6 200 VU · comparar p95 con 300 ms | Rendimiento | `k6-carga.txt` |
| Mensual | Revisar INC abiertos y leyes aplicables | Grupo completo | Acta breve / sección informe |
| Al publicar fuera de localhost | HTTPS obligatorio + rotación JWT_SECRET y DATA_KEY | Despliegue | Checklist TLS |

### Estándares y normas que el plan preserva

- **Ley 19.628 / 21.719:** datos de clientes y banco cifrados; no usar datos reales en QA.
- **Ley 21.663:** control de acceso, registro de acciones, gestión de vulnerabilidades (SCA/DAST).
- **Ley 20.422:** contraste y controles grandes; Lighthouse opcional en releases.
- **OWASP:** cabeceras, RBAC en backend, dependencias actualizadas.
- **ISO 25010 / 29119:** casos trazados al ERS y evidencia regenerable.

### Criterio de salida a producción

No declarar listo mientras INC-02 (p95), INC-03 (TLS) e INC-05 (CVE altos) sigan abiertos sin mitigación aceptada por el docente/cliente.
