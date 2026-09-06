# Medición S5 - Degradación controlada ante bloqueo de SQLite

**Fecha:** 06/09/2026  
**Rama:** `S5-restriccion-persistencia`  
**Escenario:** EC-05 - Degradación ante bloqueo temporal de persistencia  
**Restricción:** R-07 - Persistencia sin nueva infraestructura durante el primer corte  
**Decisión:** ADR-0002 - Manejar de forma controlada el bloqueo temporal de SQLite

---

## Objetivo

Verificar el comportamiento de CampusMarket después de implementar
ADR-0002 ante un bloqueo temporal de escritura sobre SQLite.

La medición comprueba:

- respuesta controlada durante el bloqueo;
- cumplimiento del umbral máximo de 2 segundos;
- ausencia de escrituras parciales;
- recuperación de la creación de publicaciones después de liberar SQLite.

---

## Procedimiento reproducible

La medición se ejecutó mediante:

```powershell
python scripts/medir_bloqueo_sqlite.py
