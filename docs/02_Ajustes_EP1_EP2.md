# Ajustes respecto de EP1 y EP2 — base de la EP3

Fecha de referencia del ambiente: 17 de noviembre de 2026.  
Caso: Atlas. Fuente: encargo EP3 (apartado obligatorio de puntos previos ajustados).

## Qué se hereda de la EP2

| Área | Resultado EP2 | Decisión en EP3 |
|---|---|---|
| Login, RBAC 403, baja lógica, CT-0012, auditoría | 15/15 en `probar.ps1` | Se mantiene como regresión automatizada |
| Puerto API 3010 (INC-01) | Cerrado en README | Sin cambio; documentado |
| Carga k6 200 VU, p95 1,28 s (INC-02) | Grave, abierto | Remedir + plan de mitigación de rendimiento |
| TLS solo HTTP en localhost (INC-03) | Moderado, abierto | Plan de mantenimiento / despliegue HTTPS |
| Correo de verificación (INC-04) | Moderado, abierto | Backlog de mantenimiento |
| npm audit / Trivy (INC-05) | Grave, abierto | Re-ejecutar SCA e imagen; plan de parche Express |
| ZAP baseline, 8 avisos nginx (INC-06) | Moderado, abierto | Re-ejecutar DAST; mitigar cabeceras en web |

## Feedback aplicado (sin inventar notas del docente)

No hay un PDF de feedback escrito en el repositorio. Los ajustes se toman de los **incidentes abiertos** de la EP2 y de lo que el encargo exige cerrar o planificar:

1. No declarar NFR de carga cumplido sin nueva medición.
2. Separar prueba estática (npm audit, Trivy) de dinámica (ZAP, HTTP, UI).
3. Agregar automatización regenerable más allá de capturas manuales.
4. Incluir plan de mantenimiento y diagrama de controles ligados a norma.

## Qué cambia en esta iteración (EP3)

1. Repositorio propio `seguridad-calidad-software-ev3-atlas`.
2. Carpetas de evidencia `seguridad/` y `automatizacion/`.
3. Automatización UI nueva (Playwright) sobre login → cliente → contrato.
4. Re-ejecución de ZAP, npm audit, Trivy y k6 con fecha EP3.
5. Informe orientado a los cinco apartados del encargo (no a la plantilla genérica de la guía).
