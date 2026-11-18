# EP3 — Atlas · Evaluación Parcial N.º 3 (ISY1102)

Aseguramiento de calidad y seguridad sobre **Atlas** (CreaLab Spa): pruebas de seguridad, automatización, diagrama de controles, mitigación y plan de mantenimiento.

**Alison Aranda · Macarena Muñoz · Camilo Romero** · Sección ISY1102 · Docente: Mauricio Velásquez

## Qué hay en este repositorio

| Ruta | Contenido |
|---|---|
| `codigo/atlas/` | Software local (React, Express, PostgreSQL) + `probar.ps1` y `pruebas/carga.js` |
| `docs/ERS_Atlas_EP1.pdf` | ERS del caso |
| `docs/oficial/` | Encargo, presentación y guía del docente |
| `docs/00_Revision_guia_y_trampas.md` | Errores y trampas de la guía (leer antes) |
| `docs/01_Plan_de_pasos_EP3.md` | Plan de trabajo ordenado por la rúbrica |
| `entrega/` | Informe y presentación (se agregan al avanzar) |
| `evidencias/` | Logs y capturas de la EP3 |

## Arranque

```powershell
cd codigo\atlas
docker compose up -d --build
powershell -ExecutionPolicy Bypass -File .\probar.ps1
```

| Recurso | URL |
|---|---|
| Pantalla | http://localhost:8080 |
| API | http://localhost:3010 |
| Swagger | http://localhost:3010/api/docs |

Usuarios de prueba, contraseña `Clave#Segura2026`: `jperez` (administrador) y `editor1` (solo lectura).

## Antes de escribir el informe

1. Leer `docs/00_Revision_guia_y_trampas.md`.
2. Seguir `docs/01_Plan_de_pasos_EP3.md`.
3. Donde la guía choque con el encargo oficial, manda el encargo.
