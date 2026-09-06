# Uso de Inteligencia Artificial - CampusMarket

Este documento registra el uso de herramientas de IA como apoyo al proyecto. Todo resultado se revisa antes de incorporarse y las decisiones finales corresponden al equipo.

## Evidencia S1

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 08/08/2026 | ChatGPT | Apoyo para analizar ideas y estructurar problema, objetivo y alcance inicial. | Se contrastó con el alcance acordado por el equipo. | Se descartaron funcionalidades de pagos y envíos porque excedían el alcance del semestre. |
| 08/08/2026 | ChatGPT | Apoyo para organizar documentación inicial y mantenibilidad. | Se revisó antes de subir al repositorio. | Se descartó ampliar el prototipo con funciones no necesarias para S1. |

## Evidencia S2

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 16/08/2026 | ChatGPT | Apoyo para estructurar arc42 1–3 y restricciones. | Se contrastó con la actividad de S2. | Se rechazaron restricciones que eran requisitos funcionales y no restricciones arquitectónicas. |
| 16/08/2026 | ChatGPT | Apoyo para formular escenarios y árbol de utilidad. | Se verificó que cada escenario tuviera las seis partes y medida numérica. | Se descartaron medidas no verificables o formuladas de manera subjetiva. |
| 16/08/2026 | ChatGPT | Apoyo para C4 Nivel 1 mediante PlantUML. | Se verificaron actores, relaciones, leyenda y alcance. | Se descartaron actores o integraciones que no pertenecían al alcance actual. |

## Evidencia S3

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 17-23/08/2026 | ChatGPT | Comparación de arquitectura en capas, hexagonal y monolito modular. | Se contrastó con EC-01 a EC-04 y las restricciones del proyecto. | Se descartó recomendar microservicios porque no era una alternativa solicitada y añadía complejidad innecesaria. |
| 17-23/08/2026 | ChatGPT | Apoyo para redactar ADR-0001 y tácticas. | El equipo revisó contexto, alternativas, decisión y consecuencias. | Se descartó arquitectura hexagonal como decisión actual por su mayor costo de abstracción para el alcance. |
| 23/08/2026 | ChatGPT | Apoyo para organizar el esqueleto FastAPI, prueba de salud y documentación. | Se comprobó mediante GitHub Actions. | Se descartó implementar lógica de negocio completa porque S3 pedía únicamente el esqueleto ejecutable. |

## Evidencia S4

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 25/08/2026 | ChatGPT | Auditoría de CampusMarket contra la ficha oficial de S4 y el feedback del curso. | Se contrastaron los 10 criterios uno por uno con el repositorio. | Se descartó crear C4 Nivel 3 porque la actividad lo pospone a Semana 6. |
| 25/08/2026 | ChatGPT | Apoyo para diseñar el corte vertical crear publicación: Flutter → FastAPI → SQLite. | Se revisó que atraviese interfaz, lógica y persistencia y que corresponda con ADR-0001. | Se descartó documentar MySQL como persistencia implementada porque todavía no existe en el código. |
| 25/08/2026 | ChatGPT | Apoyo para arc42 5, 6, 9, 12, C4 Nivel 2 y trazabilidad. | Se verificó que la documentación describa únicamente elementos presentes en la propuesta de implementación S4. | Se descartó copiar el contenido del ADR dentro de la sección 9; se mantiene un enlace al ADR. |
| 28/08/2026 | ChatGPT | Revisión de la retroalimentación provisional de S4 y apoyo para ajustar arc42 sección 3, coherencia entre C4 Nivel 1 y Nivel 2, correspondencia con el código y trazabilidad. | El equipo contrastó los ajustes con la ficha S4, el estado real del repositorio y las evidencias existentes antes de incorporarlos. | Se rechazó incluir routers, servicios, repositorios y otros detalles internos dentro del C4 Nivel 2 porque ese nivel de detalle corresponde al C4 Nivel 3 y no era requerido para S4. |
| 29/08/2026 | GitHub Copilot | Generación automática de sugerencias para mensajes y descripciones de commits durante la actualización documental del repositorio. | El equipo revisó las sugerencias antes de confirmar los cambios y mantuvo únicamente las que resultaban coherentes con el cambio realizado. | Se rechazaron mensajes genéricos sugeridos automáticamente y se reemplazaron por mensajes específicos como `Completar README con evidencia verificable de S4`, para mantener mayor trazabilidad en el historial del repositorio. |
| 29/08/2026 | ChatGPT | Auditoría final de la Evidencia S4 y apoyo para completar el README con arranque, corte vertical, pruebas, GitHub Actions, arc42, C4 y trazabilidad. | Se verificó en `master` que el README estuviera completo y que el pipeline ejecutara correctamente las pruebas del backend. | Se rechazó introducir SonarCloud apresuradamente en este cierre y modificar nuevamente el ADR-0001, porque no eran cambios necesarios para resolver los hallazgos principales de la ficha S4 y podían introducir inconsistencias innecesarias. |
| 30/08/2026 | ChatGPT | Revisión de la última retroalimentación automática de S4 y apoyo para hacer explícitas en el README las evidencias que el agente no había podido verificar: glosario de dominio y trazabilidad ASP-05. | El equipo comprobó que `docs/arc42/12-glosario.md` y `docs/aspectos.md` ya contenían la información requerida y expuso esa evidencia en el README sin modificar la arquitectura ni el código. | Se rechazó alterar nuevamente los documentos arquitectónicos solo para satisfacer la extracción del agente; se mantuvo la información original y únicamente se hizo más visible y navegable desde el README. |

## Evidencia S5

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 04/09/2026 | ChatGPT | **Revisión y saneamiento del primer corte.** Se analizó la retroalimentación acumulada de S1-S4 para estructurar `correcciones.md`; se revisó la trazabilidad entre ADR-0001 y su primera materialización en código; se formularon las tensiones de calidad pendientes de S1; se verificó el procedimiento de arranque mediante un solo comando; y se realizó una primera configuración de SonarQube Cloud mientras todavía no se encontraba disponible el proyecto oficial del curso. | El equipo contrastó `correcciones.md` con la retroalimentación oficial y el estado real del repositorio. Se confirmó que el PR #5 y el commit `4dd857a` materializaron inicialmente el monolito modular. También se ejecutó `scripts/run_s4.ps1`, verificando FastAPI, Flutter Web y `/health`, y se almacenaron evidencias en `docs/evidencias/`. La primera integración de SonarQube Cloud fue comprobada mediante el Run #29. | No se marcaron inicialmente todas las semanas como saneadas mientras existían pendientes verificables. Se descartaron tensiones de calidad genéricas y se conservaron únicamente las relacionadas con CampusMarket. No se reescribió ADR-0001 para agregar el commit de implementación, porque habría alterado el historial de una decisión aceptada. Tampoco se consideró suficiente documentar el arranque sin ejecutarlo realmente. |
| 05/09/2026 | ChatGPT | **Auditoría técnica, SonarQube Cloud y definición del reto S5.** Se revisó la integración oficial de CampusMarket en SonarQube Cloud, se diagnosticó la superposición entre rutas de fuentes y pruebas, se retiró la configuración temporal asociada al proyecto personal y se revisó la coherencia de `README.md`, `correcciones.md` y `docs/ia.md`. También se analizaron las instrucciones de Semana 5 para distinguir correctamente una restricción arquitectónica de un escenario de calidad y delimitar el reto del primer corte. | El equipo comprobó el proyecto oficial `ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET`, corrigió `.sonarcloud.properties` definiendo `backend/app,frontend/campusmarket/lib` como fuentes y `backend/tests` como pruebas, y verificó posteriormente `Quality Gate passed`. Se eliminaron `sonar-project.properties` y el análisis manual mediante `SONAR_TOKEN`. Para S5 se midió el comportamiento inicial del corte vertical ante un bloqueo de SQLite: HTTP `500`, `7.323 s`, sin escritura parcial y recuperación HTTP `201`. A partir de esa evidencia se definió R-07 y se formuló EC-05. | Se descartó continuar usando el proyecto personal de SonarCloud una vez disponible el proyecto oficial. No se eliminaron pruebas para resolver la superposición de rutas, porque el problema estaba en la configuración del análisis. Se rechazó utilizar el monolito modular como nueva restricción porque ya correspondía a ADR-0001. También se descartó introducir PostgreSQL, colas, cachés distribuidas o nuevos servicios antes de medir y justificar el problema arquitectónico. |
| 06/09/2026 | ChatGPT | **Diseño, implementación, depuración y verificación de ADR-0002.** Se compararon alternativas para responder al bloqueo temporal de SQLite y se materializó una solución con timeout de `0.5 s`, identificación específica de `SQLITE_BUSY` y `SQLITE_LOCKED`, traducción de la indisponibilidad entre repository, service y router, respuesta HTTP `503` y ausencia de reintento automático. Posteriormente se diagnosticó un problema de cierre de conexiones en Windows, se corrigió el ciclo de vida de SQLite y se propagó el mensaje de degradación controlada hasta la interfaz Flutter. Finalmente se revisaron ADR-0002, C4 Nivel 2, EC-05, `docs/aspectos.md` y las evidencias de medición para cerrar la trazabilidad del reto. | El equipo ejecutó `python -m pytest backend/tests -q` con resultado `3 passed`, y `flutter analyze` con resultado `No issues found!`. La medición formal posterior obtuvo HTTP `503` en `1.283 s`, sin escritura parcial, con recuperación HTTP `201` en `0.006 s`. Una ejecución posterior volvió a confirmar el escenario con HTTP `503` en `1.138 s` y recuperación HTTP `201`. Se comprobó además la cadena `SQLite → repository → service → router → HTTP 503 → API Flutter → formulario`, conservando las fronteras `Flutter → FastAPI → SQLite`. | Se rechazó migrar a otra base de datos o añadir infraestructura externa porque R-07 exige mantener SQLite y una única unidad de despliegue. Se descartó el reintento automático porque podía aumentar la latencia y comprometer el umbral de `≤ 2 s`. También se evitó tratar cualquier `OperationalError` como bloqueo para no ocultar fallos distintos. La primera medición que terminaba con `PermissionError` no se utilizó como evidencia final aunque sus métricas fueran favorables; primero se corrigió el cierre de conexiones y se repitió la ejecución sin traceback. Finalmente, se rechazó conservar únicamente el mensaje genérico de error en Flutter porque no comunicaba adecuadamente la indisponibilidad temporal definida en EC-05. |

## Criterio de uso

La IA se utiliza como apoyo para análisis, documentación, organización, comparación de alternativas y revisión técnica.

El equipo mantiene la responsabilidad de:

- revisar cada propuesta antes de incorporarla;
- ejecutar directamente las pruebas y mediciones;
- contrastar las recomendaciones con el estado real del repositorio;
- aceptar, corregir o rechazar las propuestas de IA con justificación técnica;
- tomar y defender las decisiones arquitectónicas finales.

Las propuestas generadas por IA no se consideran evidencia por sí mismas. La evidencia utilizada por el proyecto corresponde a resultados verificables del repositorio, pruebas ejecutadas, mediciones, documentación trazable y decisiones revisadas por el equipo.
