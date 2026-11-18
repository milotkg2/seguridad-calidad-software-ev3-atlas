# Resultados de ejecución EP3 — 17 de noviembre de 2026

Ambiente: Docker local · API http://localhost:3010 · pantalla http://localhost:8080

## Automatización funcional

| Prueba | Resultado | Evidencia |
|---|---|---|
| `probar.ps1` | 15 correctas, 0 fallidas | `automatizacion/probar-ps1.txt` |
| Playwright UI (login → Andina → CT-0012 → auditoría) | OK en 6,1 s | `automatizacion/playwright-ui.txt` + capturas `ui_01`…`ui_03` |
| k6 200 VU / 20 s | 0 % error · p95 = **719 ms** (umbral 300 ms no cumple) | `automatizacion/k6-carga.txt` |

Comparación de carga con EP2 (17-10-2026): p95 bajó de 1,28 s a 719 ms. Sigue abierto INC-02.

## Seguridad

| Enfoque | Herramienta | Función | Resultado |
|---|---|---|---|
| SCA dependencias | npm audit | CVE en librerías de la API | 7 hallazgos (3 high, 1 moderate, 3 low) |
| SCA imagen | Trivy | CVE en Alpine + paquetes Node de la imagen | Alpine: 1 medium · Node: 26 high, 15 medium, 0 critical |
| DAST pantalla | OWASP ZAP baseline | Cabeceras y fugas en runtime | FAIL-NEW 0 · WARN-NEW 8 · PASS 60 (antes de mitigar nginx) |
| Acceso | probar.ps1 CP-SEG-01 | RBAC en backend | editor POST/DELETE → 403 |

Logs: `seguridad/npm-audit-api.txt`, `seguridad/trivy-api.txt`, `seguridad/zap-consola.txt`, `seguridad/zap-pantalla.html`.

## Mitigación aplicada en código

- `codigo/atlas/web/nginx.conf`: `server_tokens off`, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy y CSP.

### ZAP antes / después de las cabeceras

| Corrida | FAIL-NEW | WARN-NEW | PASS | Informe |
|---|---|---|---|---|
| Antes | 0 | 8 | 60 | `zap-pantalla.html` / `zap-consola.txt` |
| Después | 0 | **4** | **64** | `zap-pantalla-post.html` / `zap-consola-post.txt` |

Avisos que bajaron tras la mitigación: clickjacking, X-Content-Type-Options, Server version leak, CSP ausente y Permissions-Policy. Quedan 4 avisos menores (caché, style-src unsafe-inline, Modern Web App, COEP).
