# ADR-0002 - Manejar de forma controlada el bloqueo temporal de SQLite

**Estado:** Aceptado  
**Fecha:** 2026-09-05  
**Decisión:** Aplicar espera acotada y degradación controlada ante bloqueo temporal de SQLite  
**Escenario principal:** EC-05 - Degradación ante bloqueo temporal de persistencia  
**Restricción principal:** R-07 - Persistencia sin nueva infraestructura durante el primer corte  
**Aspecto relacionado:** Creación de publicaciones  

---

## 1. Contexto

CampusMarket implementa actualmente el corte vertical de creación de
publicaciones mediante:

`Flutter Web → FastAPI → módulo publicaciones → SQLite`

La persistencia se encuentra implementada dentro del módulo
`publicaciones`, conservando las fronteras definidas por ADR-0001 y una
única unidad de despliegue.

Para la evaluación arquitectónica de S5, el equipo definió la restricción:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte.**

Esta restricción establece que CampusMarket debe mantener SQLite como
mecanismo de persistencia y conservar una única unidad de despliegue. No se
incorporarán bases de datos externas, colas, cachés distribuidas ni nuevos
servicios desplegables como respuesta al reto.

La condición adversa seleccionada para evaluar la arquitectura es un bloqueo
temporal de escritura sobre SQLite durante la creación de una publicación.

El escenario relacionado es:

**EC-05 - Degradación ante bloqueo temporal de persistencia.**

EC-05 establece que, mientras SQLite se encuentra bloqueada, CampusMarket
debe:

- rechazar temporalmente la creación de forma controlada;
- responder en un tiempo máximo de 2 segundos;
- utilizar HTTP `503`;
- no producir escrituras parciales;
- informar que la persistencia se encuentra temporalmente no disponible;
- recuperar la creación normal después de liberar SQLite.

### Línea base previa a la decisión

Antes de modificar la implementación se realizó una medición reproducible
bloqueando SQLite deliberadamente.

Los resultados fueron:

| Métrica | Línea base |
|---|---:|
| HTTP durante bloqueo | `500` |
| Tiempo durante bloqueo | `7.323 s` |
| Escritura parcial | `No` |
| HTTP después de liberar SQLite | `201` |
| Tiempo de recuperación | `0.007 s` |

La evidencia se encuentra en:

[`../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md`](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)

La línea base demuestra que la implementación conservaba la integridad
de los datos y se recuperaba después de liberar SQLite, pero presentaba dos
problemas relevantes:

1. devolvía HTTP `500`, tratando una indisponibilidad temporal de
   persistencia como un error interno genérico;
2. mantenía la solicitud esperando `7.323 s`, superando ampliamente el
   umbral de 2 segundos definido en EC-05.

Por lo tanto, se necesitaba una decisión que mejorara el comportamiento ante
el bloqueo sin violar R-07.

---

## 2. Fuerzas arquitectónicas

La decisión está condicionada por las siguientes fuerzas:

- **Disponibilidad / resiliencia:** el bloqueo temporal debe producir una
  degradación controlada y observable.
- **Tiempo de respuesta:** EC-05 establece un máximo de 2 segundos durante
  la condición adversa.
- **Integridad:** un intento fallido no debe dejar registros parciales.
- **Simplicidad operativa:** R-07 impide agregar nueva infraestructura.
- **Mantenibilidad:** la solución debe respetar las fronteras del módulo
  `publicaciones`.
- **Trazabilidad:** la respuesta debe poder verificarse mediante una prueba
  automatizada y una medición reproducible.
- **Reversibilidad:** la solución no debe impedir sustituir SQLite en una
  evolución futura del sistema.

---

## 3. Alternativas evaluadas

### 3.1 Alternativa A - Mantener el comportamiento actual

Consiste en conservar la conexión SQLite y el manejo de errores existentes,
sin introducir un límite específico para el tiempo de espera ni traducir el
bloqueo a una respuesta controlada.

**Ventajas:**

- no requiere cambios de implementación;
- mantiene el código actual;
- no introduce lógica adicional.

**Desventajas:**

- la línea base devuelve HTTP `500`;
- el intento bloqueado tarda `7.323 s`;
- no diferencia una indisponibilidad temporal de un error interno;
- no cumple el umbral de 2 segundos de EC-05;
- ofrece poca información al cliente sobre la condición ocurrida.

**Decisión sobre la alternativa:**

Se descarta porque existe evidencia reproducible de que no cumple EC-05.

---

### 3.2 Alternativa B - Espera acotada y respuesta HTTP 503

Consiste en mantener SQLite y establecer un tiempo máximo corto de espera
para adquirir el bloqueo de persistencia.

Si SQLite continúa bloqueada después de ese intervalo, el repositorio
identifica la condición de indisponibilidad temporal y la aplicación la
traduce a una respuesta HTTP `503 Service Unavailable`.

Para esta etapa se utiliza un tiempo de espera de **0.5 segundos** para las
conexiones SQLite involucradas en el corte vertical.

No se incorporan reintentos automáticos adicionales durante esta etapa.

**Ventajas:**

- permite cumplir el umbral máximo de 2 segundos;
- diferencia una indisponibilidad temporal de un error interno;
- conserva SQLite;
- conserva una única unidad de despliegue;
- no agrega infraestructura;
- mantiene la integridad transaccional existente;
- permite una prueba reproducible del comportamiento adverso;
- conserva las fronteras del módulo `publicaciones`.

**Desventajas y costos:**

- una operación puede ser rechazada aunque el bloqueo fuese a liberarse
  poco después de los 0.5 segundos;
- el cliente deberá volver a intentar la operación posteriormente;
- se agrega lógica explícita para clasificar la indisponibilidad temporal;
- el valor de 0.5 segundos deberá revisarse si cambian las características
  de carga del sistema.

**Decisión sobre la alternativa:**

Se acepta para el primer corte.

---

### 3.3 Alternativa C - Migrar la persistencia a PostgreSQL u otra base externa

Consiste en sustituir SQLite por un motor de base de datos externo con
mayores capacidades de concurrencia.

**Ventajas:**

- mayor capacidad para manejar concurrencia;
- mejores mecanismos para escenarios con múltiples escritores;
- facilita una evolución hacia cargas mayores.

**Desventajas:**

- introduce nueva infraestructura;
- aumenta la complejidad de despliegue y configuración;
- requiere migración y configuración adicional;
- aumenta el costo operativo del prototipo;
- cambia más elementos de la arquitectura de los necesarios para responder
  al escenario actual;
- viola directamente R-07 durante el primer corte.

**Decisión sobre la alternativa:**

Se descarta para S5 porque incumple la restricción arquitectónica establecida.

No se descarta como posible evolución futura de CampusMarket.

---

## 4. Decisión

**CampusMarket adopta la Alternativa B: espera acotada y degradación
controlada mediante HTTP `503`.**

La implementación:

1. mantiene SQLite como persistencia;
2. mantiene una única unidad de despliegue;
3. configura un tiempo de espera SQLite de `0.5 s`;
4. detecta específicamente la condición de base temporalmente bloqueada;
5. evita exponer directamente errores internos de SQLite al cliente;
6. traduce la indisponibilidad temporal a HTTP `503 Service Unavailable`;
7. devuelve un mensaje comprensible para el cliente;
8. conserva la ausencia de escrituras parciales;
9. permite la creación normal después de liberar la base;
10. verifica el comportamiento mediante una prueba automatizada y una
    medición reproducible.

No se implementaron reintentos automáticos en esta decisión.

El cliente puede volver a intentar posteriormente la operación cuando la
persistencia vuelva a estar disponible.

---

## 5. Justificación

La alternativa seleccionada proporciona el mejor equilibrio entre
disponibilidad, simplicidad operativa, mantenibilidad y cumplimiento de la
restricción R-07.

La línea base demostró que CampusMarket ya conservaba la integridad y se
recuperaba una vez liberada SQLite. El principal problema no requería
sustituir el mecanismo de persistencia, sino controlar cuánto tiempo esperaba
la aplicación y cómo comunicaba el fallo temporal.

Se configuró una espera SQLite de `0.5 s`, manteniendo margen frente al
umbral máximo de 2 segundos establecido por EC-05.

La medición posterior confirmó que la solicitud completa bajo bloqueo
respondió en `1.283 s`, cumpliendo el umbral arquitectónico.

La respuesta HTTP `503` representa explícitamente una indisponibilidad
temporal del servicio necesario para completar la operación, en lugar de
presentarla como un HTTP `500` genérico.

La solución tampoco modifica la estrategia definida por ADR-0001: el cambio
permanece dentro del módulo `publicaciones` y no introduce servicios
distribuidos.

---

## 6. Tácticas arquitectónicas

Las tácticas utilizadas son:

### Tiempo de espera acotado

Limitar cuánto tiempo la operación espera por la disponibilidad de SQLite.

**Objetivo:** evitar una espera prolongada como los `7.323 s` observados en
la línea base.

**Resultado observado:** la solicitud completa durante el bloqueo respondió
en `1.283 s`.

### Detección explícita de fallo temporal

Distinguir el bloqueo temporal de SQLite de otros errores inesperados de
persistencia.

La detección se realiza específicamente sobre las condiciones
`SQLITE_BUSY`, `SQLITE_LOCKED` y los mensajes asociados al bloqueo de la
base.

**Objetivo:** no convertir todos los errores de base de datos en HTTP `503`.

### Degradación controlada

Traducir específicamente la indisponibilidad temporal a HTTP `503`.

**Objetivo:** proporcionar al cliente una respuesta semánticamente adecuada
y permitir un reintento posterior.

El mensaje retornado durante la medición fue:

`La persistencia está temporalmente no disponible. Intenta nuevamente.`

### Preservación de la transacción

No confirmar escrituras cuando la operación no logra completarse.

**Objetivo:** conservar la propiedad ya observada en la línea base de cero
escrituras parciales.

**Resultado observado:** los registros permanecieron en `0` antes y después
del intento bloqueado.

### Recuperación después de liberar el recurso

No mantener un estado de fallo permanente dentro de la aplicación.

**Objetivo:** permitir que una nueva solicitud funcione normalmente cuando
SQLite deje de estar bloqueada.

**Resultado observado:** después de liberar SQLite, la nueva creación
respondió HTTP `201` en `0.006 s` y dejó `1` registro persistido.

---

## 7. Consecuencias

### Consecuencias positivas

- la solicitud bloqueada deja de esperar varios segundos;
- el cliente puede distinguir una indisponibilidad temporal;
- se conserva SQLite;
- no se incorpora infraestructura adicional;
- se mantiene una sola unidad de despliegue;
- se conservan las fronteras del monolito modular;
- el escenario adverso puede verificarse automáticamente;
- se mantiene la posibilidad de sustituir SQLite posteriormente;
- la conexión SQLite se cierra explícitamente después de cada operación,
  evitando mantener recursos abiertos innecesariamente.

### Consecuencias negativas

- un bloqueo superior al tiempo tolerado provoca el rechazo temporal de la
  operación;
- el usuario puede necesitar volver a intentar la creación;
- se introduce lógica adicional de manejo de errores;
- el valor del timeout constituye una política que deberá revisarse si
  cambia la carga del sistema.

### Riesgos aceptados

El equipo acepta que una operación pueda ser rechazada temporalmente en lugar
de esperar indefinidamente.

Para el prototipo actual se prioriza una respuesta rápida y controlada sobre
mantener una solicitud bloqueada durante varios segundos.

---

## 8. Criterio de reconsideración

Esta decisión deberá reconsiderarse si aparece evidencia de que SQLite deja
de ser suficiente para la carga real del sistema.

En particular, se revisará ADR-0002 si ocurre cualquiera de las siguientes
condiciones:

- más del **5 % de 100 intentos de creación** bajo una carga representativa
  terminan en indisponibilidad por contención de escritura;
- CampusMarket necesita ejecutar múltiples instancias del backend escribiendo
  concurrentemente sobre la misma persistencia;
- los requisitos futuros exigen una concurrencia de escritura que no pueda
  satisfacerse manteniendo EC-05;
- una nueva restricción elimina la obligación de mantener SQLite.

En ese caso se volverá a evaluar una base de datos con mayor capacidad de
concurrencia, como PostgreSQL.

---

## 9. Costo de reversión aceptado

El costo de reversión se considera **moderado**.

La decisión introduce una política específica para SQLite, pero la lógica
queda localizada dentro del módulo `publicaciones` y no modifica las
fronteras generales definidas por ADR-0001.

Una futura sustitución de SQLite requeriría principalmente:

- reemplazar o adaptar el mecanismo de persistencia;
- retirar la detección específica de bloqueo SQLite;
- conservar o redefinir la excepción de indisponibilidad de persistencia;
- ejecutar nuevamente las pruebas del corte vertical;
- volver a medir EC-05 con la nueva tecnología.

El equipo acepta este costo porque evita introducir infraestructura adicional
antes de que exista evidencia que la justifique.

---

## 10. Impacto sobre la implementación

La decisión fue materializada principalmente dentro del corte vertical de
`publicaciones`.

Los cambios se localizaron en:

```text
backend/app/publicaciones/repository.py
backend/app/publicaciones/service.py
backend/app/publicaciones/router.py
backend/tests/test_publicaciones_vertical.py
scripts/medir_bloqueo_sqlite.py
