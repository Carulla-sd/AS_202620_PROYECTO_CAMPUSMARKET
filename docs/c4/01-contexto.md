# C4 Nivel 1 - Contexto de CampusMarket

El diagrama de contexto vigente de CampusMarket se mantiene como
**diagrama como código** en:

[`01-contexto.puml`](./01-contexto.puml)

## Propósito

El C4 Nivel 1 representa a **CampusMarket como un único sistema** e identifica
únicamente a las personas y elementos externos que interactúan con él.

En este nivel no se muestran contenedores, módulos, componentes, clases ni
detalles internos de implementación.

Su objetivo es responder principalmente:

- quién utiliza CampusMarket;
- para qué interactúa con el sistema;
- cuál es el límite del sistema bajo diseño.

## Actores externos

### Estudiante

Miembro de la comunidad universitaria que utiliza CampusMarket para:

- publicar productos;
- consultar productos;
- buscar productos disponibles.

### Administrador

Usuario responsable de supervisar las publicaciones y apoyar la gestión del
contenido disponible en CampusMarket.

## Sistema bajo diseño

**CampusMarket** es un marketplace universitario orientado a centralizar la
publicación, consulta y búsqueda de productos dentro de la comunidad
universitaria.

En el C4 Nivel 1 se representa como una única caja, sin exponer su estructura
interna.

## Relaciones principales

- **Estudiante → CampusMarket:** publica, consulta y busca productos mediante
  un navegador web.
- **Administrador → CampusMarket:** supervisa publicaciones y contenido
  mediante un navegador web.

Durante el desarrollo local del prototipo se utiliza comunicación mediante
**HTTP**.

El uso de **HTTPS** corresponde a un despliegue externo futuro y no se
documenta como si ya estuviera implementado en el entorno local actual.

## Alcance

En la línea base S4 y durante el primer corte se mantienen fuera del alcance
actual:

- pagos electrónicos;
- procesamiento bancario;
- envíos y logística;
- servicios externos de transporte.

Actualmente no se representan sistemas externos adicionales porque esas
integraciones no forman parte del prototipo implementado.

Esta decisión mantiene el diagrama consistente con el estado real del sistema
y evita representar integraciones todavía inexistentes.

## Relación con el C4 Nivel 2

El **C4 Nivel 1** representa CampusMarket como un único sistema.

El **C4 Nivel 2** realiza un acercamiento al interior de esa caja y muestra los
contenedores actualmente implementados:

- **Frontend Web** - Flutter / Dart;
- **Backend API** - FastAPI / Python;
- **Persistencia local** - SQLite.

Los actores externos definidos en el Nivel 1 se mantienen coherentes con el
Nivel 2.

La restricción **R-07 - Persistencia sin nueva infraestructura durante el
primer corte** no modifica los actores externos ni el límite de CampusMarket,
por lo que la topología del C4 Nivel 1 se conserva durante S5.

La respuesta arquitectónica de S5 afecta el comportamiento interno ante la
indisponibilidad temporal de SQLite, detalle que se documenta en el
[C4 Nivel 2](./02-contenedores.md) y en
[ADR-0002](../adr/0002-manejo-bloqueo-sqlite.md).

## Fuente canónica

El archivo [`01-contexto.puml`](./01-contexto.puml) es la fuente versionada y
vigente del C4 Nivel 1.

Cualquier modificación del diagrama debe realizarse sobre ese archivo para
evitar mantener versiones contradictorias de la arquitectura.

La documentación textual de este archivo complementa el diagrama, pero no
reemplaza su fuente PlantUML.
