# Escenarios de calidad - CampusMarket

Los siguientes escenarios permiten convertir los atributos de calidad del
proyecto en condiciones observables y verificables.

Los valores utilizados como medidas fueron definidos inicialmente por el
equipo y podrán ser ajustados posteriormente mediante pruebas y evidencia
del prototipo.

## Tensiones entre atributos de calidad

CampusMarket presenta tensiones arquitectónicas que deben considerarse al
tomar decisiones sobre la evolución del sistema.

### Mantenibilidad vs rapidez de desarrollo

Una mayor separación entre módulos, responsabilidades y contratos internos
favorece la mantenibilidad porque permite realizar cambios con menor impacto
sobre funcionalidades no relacionadas.

Sin embargo, introducir más abstracciones, validaciones y fronteras internas
requiere mayor esfuerzo inicial de implementación. Por esta razón, existe una
tensión entre mantener una arquitectura modular y avanzar rápidamente en el
desarrollo del prototipo.

En CampusMarket se prioriza conservar fronteras claras entre capacidades del
negocio, aceptando un costo inicial moderado de desarrollo para reducir el
impacto de cambios futuros.

### Rendimiento vs mantenibilidad

Técnicas como índices adicionales, caché o lógica especializada pueden reducir
los tiempos de respuesta de las consultas y favorecer el rendimiento.

Sin embargo, estas optimizaciones también incrementan la complejidad del
código y el esfuerzo necesario para mantenerlo y modificarlo.

En el estado actual de CampusMarket se prioriza una implementación simple y
modular mientras se cumpla el umbral definido en EC-01. Las optimizaciones
adicionales deberán justificarse mediante mediciones antes de incorporarse.

### Disponibilidad vs simplicidad operativa

Agregar infraestructura especializada, mecanismos distribuidos o servicios
adicionales puede aumentar la capacidad de tolerar determinados fallos y
favorecer la disponibilidad.

Sin embargo, estas alternativas también incrementan el costo operativo, la
complejidad de despliegue y el esfuerzo de mantenimiento.

Para el reto arquitectónico de S5, CampusMarket prioriza conservar SQLite y
una única unidad de despliegue, de acuerdo con R-07, y mejorar primero el
comportamiento ante fallos mediante mecanismos internos y medibles antes de
considerar infraestructura adicional.

---

## EC-01 - Consulta de productos

**Atributo de calidad:** Rendimiento.

**Fuente:** Estudiante.

**Estímulo:** El estudiante realiza una búsqueda o aplica un filtro sobre el
catálogo.

**Artefacto:** Funcionalidad de consulta de productos de CampusMarket.

**Entorno:** Operación normal con un catálogo de hasta 1.000 publicaciones.

**Respuesta:** El sistema procesa la consulta y muestra los productos que
coinciden con los criterios seleccionados.

**Medida verificable:** En una prueba de 10 búsquedas consecutivas, por lo
menos 9 deben mostrar los resultados en un tiempo máximo de 2 segundos.

**Prioridad:** Alta.

---

## EC-02 - Protección de publicaciones

**Atributo de calidad:** Seguridad.

**Fuente:** Usuario autenticado.

**Estímulo:** El usuario intenta editar o eliminar una publicación que
pertenece a otro estudiante.

**Artefacto:** Funcionalidad de gestión de publicaciones.

**Entorno:** Operación normal con dos usuarios registrados diferentes.

**Respuesta:** CampusMarket rechaza la operación y mantiene la publicación
sin modificaciones.

**Medida verificable:** En 10 intentos realizados por un usuario que no sea
propietario de la publicación, los 10 intentos deben ser rechazados.

**Prioridad:** Alta.

---

## EC-03 - Modificación del sistema

**Atributo de calidad:** Mantenibilidad.

**Fuente:** Equipo de desarrollo.

**Estímulo:** Se solicita agregar un nuevo estado para los productos, por
ejemplo, `reacondicionado`.

**Artefacto:** Funcionalidad encargada de gestionar los productos.

**Entorno:** Desarrollo normal del sistema.

**Respuesta:** El equipo incorpora la nueva opción sin modificar
funcionalidades no relacionadas con los productos.

**Medida verificable:** El cambio deberá realizarse modificando como máximo
dos módulos principales y sin requerir cambios en las funciones de
autenticación o búsqueda.

**Prioridad:** Alta.

**Decisión arquitectónica relacionada:**  
[ADR-0001 - Adoptar un monolito modular para CampusMarket](../adr/0001-usar-monolito-modular.md)

---

## EC-04 - Recuperación del prototipo

**Atributo de calidad:** Disponibilidad y recuperación.

**Fuente:** Administrador o equipo de desarrollo.

**Estímulo:** La aplicación deja de responder durante una prueba o
demostración.

**Artefacto:** Aplicación CampusMarket.

**Entorno:** Ejecución del prototipo.

**Respuesta:** El equipo reinicia o recupera el servicio y vuelve a permitir
el acceso a CampusMarket sin perder la información almacenada correctamente
antes de la falla.

**Medida verificable:** El prototipo deberá volver a estar disponible en un
tiempo máximo de 10 minutos después de detectar la falla.

**Prioridad:** Media.

---

## EC-05 - Degradación ante bloqueo temporal de persistencia

**Atributo de calidad:** Disponibilidad / resiliencia.

**Fuente:** Estudiante que intenta crear una publicación.

**Estímulo:** SQLite se encuentra temporalmente bloqueada cuando el estudiante
intenta crear una nueva publicación.

**Artefacto:** Corte vertical de creación de publicaciones de CampusMarket.

**Entorno:** Aplicación en ejecución normal con persistencia SQLite y un
bloqueo temporal de escritura provocado de forma reproducible.

**Respuesta:** CampusMarket rechaza temporalmente la operación de manera
controlada, sin producir una escritura parcial, informa que la persistencia
se encuentra temporalmente no disponible y recupera la creación normal una
vez liberada la base de datos.

**Medida verificable:** Durante el bloqueo, la solicitud debe finalizar en un
tiempo máximo de **2 segundos** con HTTP `503`, sin crear registros parciales.
Después de liberar SQLite, una nueva solicitud de creación debe responder con
HTTP `201` y persistir correctamente la publicación.

**Prioridad:** Alta.

**Restricción relacionada:**  
[R-07 - Persistencia sin nueva infraestructura durante el primer corte](02-restricciones.md#r-07-persistencia-sin-nueva-infraestructura-durante-el-primer-corte)

**Decisión arquitectónica relacionada:**  
[ADR-0002 - Manejo de bloqueo temporal de SQLite](../adr/0002-manejo-bloqueo-sqlite.md)

### Línea base previa al cambio

La medición realizada el 05/09/2026 antes de modificar la implementación
obtuvo los siguientes resultados:

| Métrica | Línea base |
|---|---:|
| HTTP durante bloqueo | `500` |
| Tiempo durante bloqueo | `7.323 s` |
| Escritura parcial | `No` |
| HTTP después de liberar SQLite | `201` |
| Tiempo de recuperación | `0.007 s` |

La línea base mostró que la implementación preservaba la integridad de los
datos y recuperaba la operación normal después de liberar SQLite.

Sin embargo, no cumplía el comportamiento controlado definido para EC-05,
porque durante el bloqueo respondía con HTTP `500` y tardaba `7.323 s`,
superando el umbral máximo de 2 segundos.

**Evidencia de línea base:**  
[Medición antes del cambio](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)

### Respuesta arquitectónica aplicada

Para responder al escenario se adoptó ADR-0002.

La decisión mantiene SQLite y una única unidad de despliegue, de acuerdo con
R-07, y aplica los siguientes mecanismos:

- espera SQLite acotada mediante timeout de `0.5 s`;
- detección específica de condiciones `SQLITE_BUSY` y `SQLITE_LOCKED`;
- traducción controlada de la indisponibilidad dentro del módulo
  `publicaciones`;
- respuesta HTTP `503 Service Unavailable`;
- ausencia de reintentos automáticos;
- preservación de la transacción para evitar escrituras parciales;
- cierre explícito de conexiones SQLite;
- propagación del mensaje de indisponibilidad hasta la interfaz Flutter;
- recuperación normal después de liberar la base de datos.

La implementación conserva las fronteras arquitectónicas existentes:

**Frontend Flutter → Backend FastAPI → Persistencia SQLite**

No se agregaron bases de datos externas, colas, cachés distribuidas ni nuevos
servicios desplegables.

### Resultado después del cambio

La medición formal realizada el 06/09/2026 produjo:

| Métrica | Línea base | Después del cambio | Umbral |
|---|---:|---:|---:|
| HTTP durante bloqueo | `500` | `503` | `503` |
| Tiempo durante bloqueo | `7.323 s` | `1.283 s` | `≤ 2 s` |
| Escritura parcial | `No` | `No` | `No` |
| HTTP después de liberar SQLite | `201` | `201` | `201` |
| Tiempo de recuperación | `0.007 s` | `0.006 s` | Informativo |

El resultado posterior cumple EC-05:

- la solicitud durante el bloqueo finaliza con HTTP `503`;
- el tiempo de respuesta es inferior al umbral de 2 segundos;
- no se produce una escritura parcial;
- después de liberar SQLite, una nueva creación responde con HTTP `201`;
- la operación normal se recupera sin intervención adicional.

Una ejecución posterior de verificación volvió a confirmar el comportamiento
con los siguientes resultados:

- HTTP durante bloqueo: `503`;
- tiempo durante bloqueo: `1.138 s`;
- escritura parcial: `No`;
- HTTP después de liberar SQLite: `201`;
- tiempo de recuperación: `0.007 s`.

### Verificación automatizada

La prueba correspondiente se encuentra en:

[`backend/tests/test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

La ejecución final del backend produjo:

```text
3 passed, 1 warning in 1.51s
