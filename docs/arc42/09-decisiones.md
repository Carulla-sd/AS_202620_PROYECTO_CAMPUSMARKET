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

- Pull Request:
  [#5 - Completar esqueleto ejecutable de Evidencia S3](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/5)
- Commit de integración:
  [`4dd857a`](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/4dd857a1e238e50956facd7156b967f03ae30db0)

Este commit constituye la evidencia trazable de la primera materialización
de la decisión arquitectónica adoptada en ADR-0001.

La implementación de S4 y S5 conserva posteriormente las mismas fronteras.

El corte vertical continúa implementándose dentro del módulo
`publicaciones` y no convierte los módulos internos en servicios
distribuidos independientes.

---

## Evidencia de implementación de ADR-0002

ADR-0002 responde a la restricción:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte.**

La condición adversa seleccionada se formalizó mediante:

**EC-05 - Degradación ante bloqueo temporal de persistencia.**

El reto consiste en responder de forma controlada cuando SQLite se encuentra
temporalmente bloqueada durante la creación de una publicación, sin resolver
el problema mediante nueva infraestructura.

### Línea base previa

Antes de aplicar ADR-0002 se realizó una medición reproducible.

| Métrica | Línea base |
|---|---:|
| HTTP durante bloqueo | `500` |
| Tiempo durante bloqueo | `7.323 s` |
| Escritura parcial | `No` |
| HTTP de recuperación | `201` |
| Tiempo de recuperación | `0.007 s` |

La línea base mostró que CampusMarket preservaba la integridad de los datos y
recuperaba la operación normal después de liberar SQLite.

Sin embargo:

- la indisponibilidad temporal se manifestaba como HTTP `500`;
- la solicitud permanecía bloqueada durante `7.323 s`;
- el resultado superaba el umbral máximo de `2 s` definido en EC-05.

---

## Decisión aplicada

La decisión se materializó manteniendo SQLite y conservando el backend como
una única aplicación monolítica modular, sin crear nuevos servicios
desplegables.

Los principales cambios fueron:

- timeout SQLite acotado a `0.5 s`;
- detección específica de `SQLITE_BUSY` y `SQLITE_LOCKED`;
- traducción controlada de la indisponibilidad temporal;
- respuesta HTTP `503 Service Unavailable`;
- mensaje explícito de indisponibilidad temporal para el cliente;
- ausencia de reintentos automáticos;
- preservación de la transacción;
- cierre explícito de conexiones SQLite;
- propagación de la condición controlada hasta Flutter;
- recuperación normal después de liberar el bloqueo.

La solución conserva el recorrido arquitectónico:

**Flutter Web → FastAPI → módulo `publicaciones` → SQLite**

Por lo tanto, ADR-0002 modifica el comportamiento frente a una condición
adversa, pero no cambia la topología del sistema ni introduce nueva
infraestructura.

---

## Correspondencia con la implementación

Los archivos principales afectados son:

```text
backend/app/publicaciones/repository.py
backend/app/publicaciones/service.py
backend/app/publicaciones/router.py
frontend/campusmarket/lib/publicaciones/publicaciones_api.dart
frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart
backend/tests/test_publicaciones_vertical.py
scripts/medir_bloqueo_sqlite.py
