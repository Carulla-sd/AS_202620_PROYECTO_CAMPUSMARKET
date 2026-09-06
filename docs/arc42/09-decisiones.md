# 9. Decisiones arquitectónicas

Las decisiones arquitectónicas de CampusMarket se mantienen en registros ADR
independientes. Esta sección no repite todo su contenido; funciona como índice
trazable entre las decisiones, escenarios de calidad e implementación.

| ADR | Estado | Decisión | Escenario principal |
|---|---|---|---|
| [ADR-0001](../adr/0001-usar-monolito-modular.md) | Aceptado | Adoptar un monolito modular como estrategia arquitectónica inicial. | EC-03 - Modificación del sistema |
| [ADR-0002](../adr/0002-manejo-bloqueo-sqlite.md) | Aceptado | Aplicar espera acotada y degradación controlada ante bloqueo temporal de SQLite. | EC-05 - Degradación ante bloqueo temporal de persistencia |

---

## Evidencia de implementación de ADR-0001

La decisión definida en ADR-0001 se materializó inicialmente durante la
construcción del esqueleto ejecutable de la Evidencia S3.

La implementación introdujo una única aplicación backend en FastAPI
organizada mediante módulos asociados con capacidades del negocio:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

La incorporación del esqueleto ejecutable fue consolidada mediante:

- Pull Request: [#5 - Completar esqueleto ejecutable de Evidencia S3](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/5)
- Commit de integración: [`4dd857a`](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/4dd857a1e238e50956facd7156b967f03ae30db0)

Este commit constituye la evidencia trazable de la primera materialización
de la decisión arquitectónica adoptada en ADR-0001.

La implementación de S4 y S5 conserva posteriormente las mismas fronteras.
El corte vertical continúa implementándose dentro del módulo
`publicaciones` y no convierte los módulos en servicios distribuidos.

---

## Evidencia de implementación de ADR-0002

ADR-0002 responde a la restricción:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte.**

La condición adversa se formalizó mediante:

**EC-05 - Degradación ante bloqueo temporal de persistencia.**

La línea base previa mostró:

| Métrica | Línea base |
|---|---:|
| HTTP durante bloqueo | `500` |
| Tiempo durante bloqueo | `7.323 s` |
| Escritura parcial | `No` |
| HTTP de recuperación | `201` |

La decisión se materializó manteniendo SQLite y la única unidad de
despliegue existente.

Los principales cambios fueron:

- timeout SQLite acotado a `0.5 s`;
- detección específica de `SQLITE_BUSY` y `SQLITE_LOCKED`;
- traducción de la indisponibilidad temporal dentro del módulo;
- respuesta HTTP `503 Service Unavailable`;
- mensaje explícito de indisponibilidad temporal para el cliente;
- preservación de la transacción;
- cierre explícito de conexiones SQLite;
- recuperación normal después de liberar el bloqueo.

Los archivos principales afectados son:

```text
backend/app/publicaciones/repository.py
backend/app/publicaciones/service.py
backend/app/publicaciones/router.py
frontend/campusmarket/lib/publicaciones/publicaciones_api.dart
frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart
backend/tests/test_publicaciones_vertical.py
scripts/medir_bloqueo_sqlite.py
