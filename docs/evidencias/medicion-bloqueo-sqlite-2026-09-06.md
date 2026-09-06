# Medición S5 - Degradación controlada ante bloqueo de SQLite

**Fecha:** 06/09/2026  
**Rama:** `S5-restriccion-persistencia`  
**Escenario:** EC-05 - Degradación ante bloqueo temporal de persistencia  
**Restricción:** R-07 - Persistencia sin nueva infraestructura durante el primer corte  
**Decisión:** ADR-0002 - Manejar de forma controlada el bloqueo temporal de SQLite  

---

## Objetivo

Verificar el comportamiento de CampusMarket después de implementar ADR-0002
ante un bloqueo temporal de escritura sobre SQLite.

La medición comprueba:

- respuesta controlada durante el bloqueo;
- cumplimiento del umbral máximo de 2 segundos;
- ausencia de escrituras parciales;
- recuperación de la creación de publicaciones después de liberar SQLite.

---

## Procedimiento reproducible

La medición se ejecutó con:

`python scripts/medir_bloqueo_sqlite.py`

El script realiza el siguiente procedimiento:

1. crea una base SQLite temporal;
2. inicializa la tabla de publicaciones;
3. toma un bloqueo exclusivo sobre SQLite;
4. ejecuta `POST /publicaciones`;
5. mide el tiempo de respuesta;
6. verifica el número de registros antes y después del intento;
7. libera el bloqueo;
8. ejecuta nuevamente `POST /publicaciones`;
9. comprueba la recuperación y persistencia de la publicación.

---

## Verificación automatizada

Antes de realizar la medición se ejecutó:

`python -m pytest backend/tests -q`

Resultado observado:

`3 passed, 1 warning in 1.59s`

Las tres pruebas finalizaron correctamente.

El warning corresponde a una advertencia de deprecación de
`Starlette TestClient/httpx` y no afecta el resultado funcional de EC-05.

---

## Resultado con SQLite bloqueada

| Métrica | Resultado |
|---|---:|
| HTTP durante bloqueo | `503` |
| Tiempo durante bloqueo | `1.283 s` |
| Registros antes | `0` |
| Registros después del intento | `0` |
| Escritura parcial | `No` |

Mensaje devuelto al cliente:

`La persistencia está temporalmente no disponible. Intenta nuevamente.`

---

## Recuperación después de liberar SQLite

| Métrica | Resultado |
|---|---:|
| HTTP de recuperación | `201` |
| Tiempo de recuperación | `0.006 s` |
| Registros finales | `1` |

La nueva publicación fue persistida correctamente después de liberar SQLite.

---

## Comparación con la línea base

| Métrica | Línea base | Después de ADR-0002 | Umbral EC-05 | Resultado |
|---|---:|---:|---:|---|
| HTTP durante bloqueo | `500` | `503` | `503` | Cumple |
| Tiempo durante bloqueo | `7.323 s` | `1.283 s` | `≤ 2 s` | Cumple |
| Escritura parcial | `No` | `No` | `No` | Cumple |
| HTTP después de liberar SQLite | `201` | `201` | `201` | Cumple |
| Tiempo de recuperación | `0.007 s` | `0.006 s` | Informativo | Correcto |
| Publicación posterior persistida | `Sí` | `Sí` | `Sí` | Cumple |

---

## Interpretación

La línea base mostró que CampusMarket preservaba la integridad de los datos,
pero trataba el bloqueo temporal de SQLite como un error interno HTTP `500`
y mantenía la solicitud esperando `7.323 s`.

Después de implementar ADR-0002, la misma condición adversa produce HTTP
`503` en `1.283 s`, dentro del umbral máximo de 2 segundos definido en EC-05.

No se produjo ninguna escritura parcial y, después de liberar SQLite, una
nueva solicitud respondió HTTP `201` y persistió correctamente la publicación.

---

## Conclusión

La implementación satisface EC-05.

Ante un bloqueo temporal de SQLite, CampusMarket:

- responde mediante HTTP `503`;
- finaliza la solicitud en `1.283 s`;
- cumple el umbral de `≤ 2 s`;
- no genera escrituras parciales;
- informa de manera explícita la indisponibilidad temporal;
- recupera la operación normal después de liberar SQLite;
- crea y persiste posteriormente la publicación con HTTP `201`.

La solución mantiene SQLite, conserva una única unidad de despliegue y no
incorpora bases externas, colas, cachés distribuidas ni nuevos servicios.

Por lo tanto, también se mantiene el cumplimiento de R-07.

---

## Trazabilidad

La cadena verificable para S5 es:

**R-07 → EC-05 → ADR-0002 → código → prueba automatizada → medición**

### Restricción

[R-07 - Persistencia sin nueva infraestructura](../arc42/02-restricciones.md#r-07-persistencia-sin-nueva-infraestructura-durante-el-primer-corte)

### Escenario de calidad

[EC-05 - Degradación ante bloqueo temporal de persistencia](../arc42/10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia)

### Decisión arquitectónica

[ADR-0002 - Manejo de bloqueo SQLite](../adr/0002-manejo-bloqueo-sqlite.md)

### Código

- `backend/app/publicaciones/repository.py`
- `backend/app/publicaciones/service.py`
- `backend/app/publicaciones/router.py`

### Prueba automatizada

- `backend/tests/test_publicaciones_vertical.py`

### Script reproducible

- `scripts/medir_bloqueo_sqlite.py`

### Evidencia previa

[Línea base antes del cambio](linea-base-bloqueo-sqlite-2026-09-05.md)
