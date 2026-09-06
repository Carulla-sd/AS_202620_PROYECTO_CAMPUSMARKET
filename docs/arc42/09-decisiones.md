# 9. Decisiones arquitectónicas

Las decisiones arquitectónicas de CampusMarket se mantienen en registros ADR
independientes. Esta sección no repite todo su contenido; funciona como índice
trazable entre las decisiones, los escenarios de calidad y su materialización
en el repositorio.

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

Evidencia:

[Línea base de bloqueo SQLite](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)

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
```

La responsabilidad principal de cada elemento es:

- `repository.py`: configura la espera SQLite de `0.5 s`, identifica
  `SQLITE_BUSY` y `SQLITE_LOCKED`, preserva la transacción y traduce el
  bloqueo a una indisponibilidad temporal de persistencia.
- `service.py`: mantiene la traducción de la indisponibilidad dentro de la
  frontera funcional del módulo `publicaciones`.
- `router.py`: expone la condición controlada mediante HTTP
  `503 Service Unavailable`.
- `publicaciones_api.dart`: identifica específicamente HTTP `503` y conserva
  el mensaje proporcionado por el backend.
- `publicacion_form_page.dart`: informa al usuario sobre la indisponibilidad
  temporal mediante un mensaje específico.
- `test_publicaciones_vertical.py`: verifica el bloqueo, el HTTP `503`, el
  umbral temporal, la integridad y la recuperación.
- `medir_bloqueo_sqlite.py`: reproduce la condición adversa y genera las
  métricas utilizadas como evidencia.

---

## Resultado posterior a ADR-0002

Después de aplicar la decisión se repitió el escenario de forma reproducible.

| Métrica | Línea base | Después de ADR-0002 | Umbral EC-05 |
|---|---:|---:|---:|
| HTTP durante bloqueo | `500` | `503` | `503` |
| Tiempo durante bloqueo | `7.323 s` | `1.283 s` | `≤ 2 s` |
| Escritura parcial | `No` | `No` | `No` |
| HTTP de recuperación | `201` | `201` | `201` |
| Tiempo de recuperación | `0.007 s` | `0.006 s` | Informativo |

La solicitud bloqueada pasó de:

**HTTP `500` en `7.323 s`**

a:

**HTTP `503` en `1.283 s`**

sin producir escrituras parciales.

Después de liberar SQLite, una nueva creación respondió HTTP `201` y persistió
correctamente la publicación.

Por lo tanto, el resultado satisface EC-05.

Una ejecución posterior volvió a confirmar el comportamiento con:

- HTTP `503`;
- tiempo durante bloqueo de `1.138 s`;
- ninguna escritura parcial;
- recuperación HTTP `201`.

La medición formal utilizada como evidencia continúa siendo la ejecución de
`1.283 s`.

Evidencia:

[Medición posterior a ADR-0002](../evidencias/medicion-bloqueo-sqlite-2026-09-06.md)

---

## Verificación automatizada

La prueba relevante se encuentra en:

[`backend/tests/test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

La prueba verifica:

- bloqueo exclusivo de SQLite;
- respuesta HTTP `503`;
- tiempo máximo de `2 s`;
- ausencia de escritura parcial;
- mensaje explícito de indisponibilidad;
- liberación del bloqueo;
- recuperación mediante HTTP `201`;
- persistencia correcta después de la recuperación.

La ejecución final del backend produjo:

```text
3 passed
```

El frontend fue verificado mediante:

```bash
cd frontend/campusmarket
flutter analyze
```

con resultado:

```text
No issues found!
```

El escenario adverso puede reproducirse mediante:

```bash
python scripts/medir_bloqueo_sqlite.py
```

---

## Trazabilidad de implementación de ADR-0002

La respuesta arquitectónica completa de S5 fue consolidada inicialmente en
`master` mediante:

- Pull Request:
  [#28 - Completar reto arquitectónico S5 del primer corte](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/28)
- Commit de integración:
  [`ff68cf2`](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/ff68cf255b90340634e0760f056870f9a19e9abd)

Ese commit reúne la implementación, las pruebas, las mediciones y la
documentación principal utilizadas para verificar ADR-0002.

La documentación de cierre y trazabilidad del ADR fue refinada
posteriormente sin modificar la decisión arquitectónica ni el comportamiento
implementado.

La cadena principal es:

**ASP-06 → R-07 / EC-05 → C4 Nivel 2 → ADR-0002 → código → prueba → medición → evidencia**

Elementos relacionados:

- [R-07 - Restricción arquitectónica](02-restricciones.md#r-07-persistencia-sin-nueva-infraestructura-durante-el-primer-corte)
- [EC-05 - Escenario de calidad](10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia)
- [ADR-0002](../adr/0002-manejo-bloqueo-sqlite.md)
- [C4 Nivel 2](../c4/02-contenedores.md)
- [Aspectos y trazabilidad](../aspectos.md)
- [Registro de IA](../ia.md)
- [Línea base](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
- [Medición posterior](../evidencias/medicion-bloqueo-sqlite-2026-09-06.md)
- [Prueba automatizada](../../backend/tests/test_publicaciones_vertical.py)
- [Script de medición](../../scripts/medir_bloqueo_sqlite.py)

Con estas evidencias, ADR-0002 queda asociado explícitamente con:

**restricción → escenario de calidad → decisión → implementación → prueba → medición → evidencia**

y conserva la trazabilidad requerida para el primer corte.
