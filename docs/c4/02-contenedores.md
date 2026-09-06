# C4 Nivel 2 - Contenedores de CampusMarket

El diagrama de contenedores vigente de CampusMarket se mantiene como
**diagrama como código** en:

[`02-contenedores.puml`](./02-contenedores.puml)

## Propósito

El C4 Nivel 2 representa los contenedores principales que conforman
CampusMarket, indicando su responsabilidad general, la tecnología utilizada
y las relaciones entre ellos.

Este nivel responde principalmente a:

- qué partes principales forman el sistema;
- qué responsabilidad tiene cada contenedor;
- qué tecnología utiliza cada uno;
- cómo se comunican entre sí.

Los actores externos se mantienen coherentes con el C4 Nivel 1:

- **Estudiante:** utiliza CampusMarket para publicar, consultar y buscar
  productos.
- **Administrador:** accede al sistema para funciones de supervisión.

## Contenedores

| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| Frontend Web | Flutter / Dart | Proporcionar la interfaz web mediante la cual los usuarios interactúan con CampusMarket. |
| Backend API | FastAPI / Python | Recibir solicitudes HTTP, validar datos y coordinar la lógica de aplicación. |
| Persistencia local | SQLite | Almacenar y recuperar los datos utilizados por el corte vertical implementado. |

La topología actual puede resumirse como:

**Frontend Web → Backend API → Persistencia local SQLite**

## Correspondencia con el código

| Contenedor C4 | Evidencia en el repositorio |
|---|---|
| Frontend Web | `frontend/campusmarket/lib/` |
| Backend API | `backend/app/` |
| Persistencia local | `backend/app/publicaciones/repository.py`, que utiliza `sqlite3` para almacenar y recuperar publicaciones. |

La base SQLite utilizada durante la ejecución se genera dinámicamente.

Por esta razón, la evidencia versionada de la persistencia se encuentra en el
código responsable del acceso a SQLite y no en un archivo de base de datos
almacenado en Git.

Esta correspondencia permite verificar que los límites representados en el
C4 Nivel 2 tienen una materialización observable en la estructura real del
repositorio.

## Relaciones entre contenedores

Las relaciones principales son:

- **Estudiante → Frontend Web:** publica y consulta productos mediante un
  navegador web.
- **Administrador → Frontend Web:** accede mediante navegador web para
  supervisar contenido.
- **Frontend Web → Backend API:** crea y consulta publicaciones mediante
  **HTTP/JSON REST**.
- **Backend API → Persistencia local:** guarda y recupera publicaciones
  mediante **SQL utilizando `sqlite3`**.

El frontend no accede directamente a SQLite.

La persistencia es utilizada exclusivamente a través del backend, conservando
la separación entre interfaz, lógica de aplicación y almacenamiento.

## Corte vertical implementado

El corte vertical actualmente verificable recorre:

**Flutter Web → FastAPI → módulo `publicaciones` → SQLite**

Su materialización principal se encuentra en:

- `frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart`
- `frontend/campusmarket/lib/publicaciones/publicaciones_api.dart`
- `backend/app/publicaciones/router.py`
- `backend/app/publicaciones/service.py`
- `backend/app/publicaciones/repository.py`

La prueba automatizada asociada se encuentra en:

[`backend/tests/test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

## Impacto arquitectónico de S5

La restricción:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte**

mantiene SQLite como mecanismo de persistencia y conserva una única unidad de
despliegue.

Por esta razón, la respuesta arquitectónica de S5 **no modifica la topología
del C4 Nivel 2**.

CampusMarket continúa compuesto por:

**Frontend Web → Backend API → Persistencia local SQLite**

No se incorporaron:

- bases de datos externas;
- colas;
- cachés distribuidas;
- nuevos servicios desplegables.

### Impacto en Backend API → Persistencia local

El principal impacto de S5 se concentra en la relación:

**Backend API → Persistencia local**

Ante un bloqueo temporal de SQLite, el Backend API aplica la decisión
registrada en ADR-0002:

- utiliza una espera acotada de `0.5 s`;
- identifica específicamente las condiciones `SQLITE_BUSY` y
  `SQLITE_LOCKED`;
- traduce la indisponibilidad temporal de forma controlada;
- evita producir escrituras parciales;
- responde con HTTP `503 Service Unavailable` cuando SQLite continúa
  bloqueada;
- recupera la creación normal después de liberar la base de datos.

### Impacto en Frontend Web → Backend API

La relación:

**Frontend Web → Backend API**

mantiene su comunicación mediante **HTTP/JSON REST**.

Cuando el backend responde HTTP `503`, el cliente Flutter identifica la
indisponibilidad temporal y muestra al usuario un mensaje específico en lugar
de presentar únicamente un error genérico.

Por lo tanto, S5 modifica el **comportamiento observable de las relaciones**
entre contenedores, pero no agrega contenedores ni cambia las fronteras del
sistema.

## Conservación de las fronteras arquitectónicas

La decisión de S5 conserva:

- la topología definida en el C4 Nivel 2;
- SQLite como persistencia;
- la separación entre frontend, backend y almacenamiento;
- las fronteras establecidas mediante
  [ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md).

La respuesta específica al bloqueo se encuentra registrada en:

[ADR-0002 - Manejo de bloqueo temporal de SQLite](../adr/0002-manejo-bloqueo-sqlite.md)

## Evidencia del cambio S5

La línea base previa al cambio registró:

- HTTP durante bloqueo: `500`;
- tiempo durante bloqueo: `7.323 s`;
- escritura parcial: `No`;
- recuperación posterior: HTTP `201`.

Después de aplicar ADR-0002 se obtuvo formalmente:

- HTTP durante bloqueo: `503`;
- tiempo durante bloqueo: `1.283 s`;
- escritura parcial: `No`;
- recuperación posterior: HTTP `201`;
- tiempo de recuperación: `0.006 s`.

El resultado cumple el umbral de EC-05 de responder durante el bloqueo en un
máximo de **2 segundos**.

Evidencias:

- [Línea base](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
- [Medición posterior](../evidencias/medicion-bloqueo-sqlite-2026-09-06.md)
- [EC-05](../arc42/10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia)
- [ADR-0002](../adr/0002-manejo-bloqueo-sqlite.md)

## Alcance del Nivel 2

Este diagrama representa únicamente:

- contenedores principales;
- responsabilidades generales;
- tecnologías principales;
- relaciones entre contenedores.

No representa:

- módulos internos;
- componentes;
- clases;
- routers;
- services;
- repositories;
- manejo interno de excepciones.

Ese nivel de detalle corresponde al **C4 Nivel 3** y no se representa en el
primer corte.

Los detalles internos mencionados en la documentación de S5 se utilizan como
evidencia de implementación, pero no se incorporan como elementos gráficos
del C4 Nivel 2.

## Relación con el C4 Nivel 1

El [C4 Nivel 1](./01-contexto.md) representa CampusMarket como un único
sistema frente a Estudiante y Administrador.

El C4 Nivel 2 realiza un acercamiento al interior de esa caja y muestra cómo
el sistema se materializa actualmente mediante Frontend Web, Backend API y
SQLite.

Los actores y límites permanecen coherentes entre ambos niveles.

## Fuente canónica

El archivo [`02-contenedores.puml`](./02-contenedores.puml) es la fuente
versionada y vigente del C4 Nivel 2.

Cualquier modificación gráfica debe realizarse sobre ese archivo para evitar
versiones contradictorias de la arquitectura.

La documentación textual de este archivo complementa el diagrama, pero no
reemplaza su fuente PlantUML.
