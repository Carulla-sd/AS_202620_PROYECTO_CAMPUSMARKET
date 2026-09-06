# Aspectos del proyecto - CampusMarket

Este documento mantiene la trazabilidad de los aspectos de CampusMarket desde los requisitos y decisiones arquitectónicas hasta su implementación y evidencia verificable.

La cadena de trazabilidad utilizada es:

**Aspecto → Requisito → C4 → ADR → Código → Pruebas → Evidencia**

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
| ASP-01 | Consulta y búsqueda de productos | [EC-01 - Consulta de productos](./arc42/10-escenarios-de-calidad.md#ec-01---consulta-de-productos) | [C4 Nivel 2](./c4/02-contenedores.md) | Sin ADR específico: escenario aún no materializado | No materializado en el corte vertical actual | Sin prueba específica de EC-01 todavía | Escenario definido en S2; sin evidencia de implementación todavía |
| ASP-02 | Gestión segura de publicaciones | [EC-02 - Protección de publicaciones](./arc42/10-escenarios-de-calidad.md#ec-02---protección-de-publicaciones) | [C4 Nivel 1](./c4/01-contexto.md) | Sin ADR específico: escenario aún no materializado | No materializado en el corte vertical actual | Sin prueba específica de EC-02 todavía | Escenario definido en S2; sin evidencia de implementación todavía |
| ASP-03 | Evolución de la gestión de productos | [EC-03 - Modificación del sistema](./arc42/10-escenarios-de-calidad.md#ec-03---modificación-del-sistema) | [C4 Nivel 2](./c4/02-contenedores.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`backend/app/publicaciones/`](../backend/app/publicaciones/), [`publicacion_form_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Evidencia S3/S4 |
| ASP-04 | Recuperación del prototipo | [EC-04 - Recuperación del prototipo](./arc42/10-escenarios-de-calidad.md#ec-04---recuperación-del-prototipo) | [C4 Nivel 1](./c4/01-contexto.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`scripts/run_s4.ps1`](../scripts/run_s4.ps1) | [`test_health.py`](../backend/tests/test_health.py) | [Evidencia de arranque con un comando](./evidencias/arranque-un-comando-2026-09-04.md) |
| ASP-05 | Creación de publicaciones | [Alcance funcional - Gestión de publicaciones](./arc42/ARC42.md#32-alcance-funcional) | [C4 Nivel 2](./c4/02-contenedores.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`publicacion_form_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart), [`publicaciones_api.dart`](../frontend/campusmarket/lib/publicaciones/publicaciones_api.dart), [`router.py`](../backend/app/publicaciones/router.py), [`service.py`](../backend/app/publicaciones/service.py), [`repository.py`](../backend/app/publicaciones/repository.py) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Evidencia funcional S4 del corte vertical |
| ASP-06 | Degradación controlada ante bloqueo de persistencia | [R-07 - Persistencia sin nueva infraestructura](./arc42/02-restricciones.md#r-07-persistencia-sin-nueva-infraestructura-durante-el-primer-corte) / [EC-05 - Degradación ante bloqueo temporal](./arc42/10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia) | [C4 Nivel 2](./c4/02-contenedores.md) | [ADR-0002 - Manejo de bloqueo SQLite](./adr/0002-manejo-bloqueo-sqlite.md) | [`repository.py`](../backend/app/publicaciones/repository.py), [`service.py`](../backend/app/publicaciones/service.py), [`router.py`](../backend/app/publicaciones/router.py), [`publicaciones_api.dart`](../frontend/campusmarket/lib/publicaciones/publicaciones_api.dart), [`publicacion_form_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | [Línea base](./evidencias/linea-base-bloqueo-sqlite-2026-09-05.md) / [Medición posterior](./evidencias/medicion-bloqueo-sqlite-2026-09-06.md) |

## Alcance de materialización de los aspectos

Los aspectos **ASP-01** y **ASP-02** corresponden a escenarios de calidad
definidos durante la construcción de la línea base arquitectónica en S2.

En el primer corte estos escenarios permanecen especificados y trazados hacia
sus requisitos y vistas C4 correspondientes, pero todavía no forman parte del
corte vertical implementado.

Por esta razón, las columnas asociadas con ADR, código, pruebas y evidencia
indican explícitamente que todavía no existe una materialización verificable,
en lugar de asociar artificialmente elementos que no comprueban realmente
EC-01 o EC-02.

En particular:

- **ASP-01 / EC-01** define el comportamiento esperado para consulta y
  búsqueda de productos, incluida su medida de rendimiento, pero el corte
  vertical actual no implementa todavía la búsqueda y filtrado necesarios
  para verificar ese escenario completo.

- **ASP-02 / EC-02** define la protección de publicaciones frente a
  modificaciones realizadas por usuarios no propietarios, pero el corte
  actual todavía no incorpora el mecanismo completo de autenticación,
  propiedad y autorización necesario para verificar ese escenario.

Estos escenarios permanecen como parte de la arquitectura prevista y podrán
materializarse en la evolución posterior del sistema.

La materialización funcional acumulada hasta S4 se concentra principalmente
en **ASP-03, ASP-04 y ASP-05**, asociados con la evolución modular,
recuperación del prototipo y creación de publicaciones.

Para S5 se incorpora **ASP-06**, que corresponde al aspecto afectado por la
restricción R-07 y cuya trazabilidad se completa de extremo a extremo:

**ASP-06 → R-07 / EC-05 → C4 Nivel 2 → ADR-0002 → código → pruebas → evidencia**

De esta manera, `docs/aspectos.md` diferencia explícitamente entre escenarios
arquitectónicos definidos para evolución posterior y aspectos que ya cuentan
con implementación y evidencia verificable.

## Estado de trazabilidad S4

La fila **ASP-05 - Creación de publicaciones** representa el corte vertical
implementado durante S4.

La trazabilidad del corte vertical corresponde al recorrido:

**Interfaz Flutter → API FastAPI → lógica del módulo `publicaciones` → persistencia SQLite.**

Durante la verificación local se creó una publicación desde la interfaz
Flutter y se comprobó posteriormente su almacenamiento en SQLite, por lo que
las rutas indicadas corresponden al comportamiento real del prototipo.

La recuperación del prototipo también quedó evidenciada mediante
**ASP-04**, utilizando el script de arranque con un solo comando, la prueba de
salud y las capturas almacenadas en `docs/evidencias/`.

## Verificación de EC-03 en S4

Durante el ajuste final de la Evidencia S4 se incorporó el estado de producto
`reacondicionado`, utilizado como caso concreto para verificar el escenario
**EC-03 - Modificación del sistema**.

El cambio se mantuvo dentro de la capacidad funcional de `publicaciones` y
requirió ajustes únicamente en los elementos directamente relacionados con
la creación, validación y persistencia de publicaciones.

No fue necesario modificar los módulos de autenticación ni búsqueda,
manteniendo las fronteras definidas por el
**ADR-0001 - Monolito modular**.

La prueba automatizada
[`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py)
crea una publicación con estado `reacondicionado`, verifica su persistencia
en SQLite y posteriormente recupera el registro para comprobar que el nuevo
estado se conserva correctamente.

De esta forma queda trazada la relación:

**EC-03 → ADR-0001 → módulo `publicaciones` → código → prueba automatizada.**

## Trazabilidad S5

Para la evaluación arquitectónica de S5 se incorporó el aspecto:

**ASP-06 - Degradación controlada ante bloqueo de persistencia.**

La cadena completa es:

**ASP-06 → R-07 / EC-05 → C4 Nivel 2 → ADR-0002 → código → prueba automatizada → evidencia antes/después**

La restricción **R-07** mantiene SQLite y una única unidad de despliegue,
sin incorporar una base de datos externa, colas, cachés distribuidas ni
nuevos servicios desplegables.

El escenario **EC-05** verifica la respuesta del corte vertical ante un
bloqueo temporal de persistencia.

La línea base previa al cambio registró:

- HTTP durante bloqueo: `500`;
- tiempo durante bloqueo: `7.323 s`;
- escritura parcial: `No`;
- recuperación posterior: HTTP `201`.

ADR-0002 materializa la respuesta arquitectónica mediante:

- espera SQLite acotada a `0.5 s`;
- detección específica de `SQLITE_BUSY` y `SQLITE_LOCKED`;
- traducción controlada de la indisponibilidad;
- respuesta HTTP `503`;
- ausencia de escritura parcial;
- mensaje explícito al usuario;
- recuperación normal después de liberar SQLite.

Después de aplicar la decisión, la medición formal registró:

- HTTP durante bloqueo: `503`;
- tiempo durante bloqueo: `1.283 s`;
- escritura parcial: `No`;
- recuperación posterior: HTTP `201`;
- tiempo de recuperación: `0.006 s`.

El resultado cumple el umbral establecido por EC-05 de responder en un tiempo
máximo de **2 segundos** durante el bloqueo.

Una ejecución posterior de verificación volvió a confirmar el comportamiento,
obteniendo HTTP `503` en `1.138 s`, sin escritura parcial y con recuperación
HTTP `201`.

La implementación conserva las fronteras del sistema:

**Frontend Flutter → Backend FastAPI → Persistencia SQLite**

y no introduce infraestructura adicional.

De esta forma ASP-06 queda trazado desde la restricción arquitectónica hasta
una evidencia reproducible y contrastada con su umbral.
