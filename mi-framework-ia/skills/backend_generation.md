# Skill: Backend Generation — guía propuesta en F3

> **Guía documental; ejecución no acreditada.** No genera código por sí sola ni forma parte de un motor automático.

## Propósito

Preparar propuestas de backend compatibles con la arquitectura y los contratos actuales.

## Entradas

- Requisito autorizado y criterios de aceptación.
- Routers, schemas, CRUD, modelos y configuración existentes.
- Restricciones de [`project_config.md`](../config/project_config.md).

## Stack de referencia

FastAPI, Pydantic v2, SQLAlchemy 2 y PostgreSQL. La estructura actual usa `api/v1`, `schemas`, `crud`, `models`, `db` y `core`.

## Pasos

1. Leer el requisito y confirmar que no amplía el alcance.
2. Identificar router, schema, CRUD y modelo implicados.
3. Definir la entrada, la salida y los errores HTTP esperados.
4. Mantener la lógica de persistencia en las capas existentes.
5. Señalar impactos sobre datos, compatibilidad y documentación.
6. Entregar el cambio propuesto para revisión humana.

## Salida esperada

Propuesta acotada con contratos, archivos afectados, riesgos y verificaciones pendientes. No se incluyen resultados de pruebas no ejecutadas.

## Límites

- No inventar requisitos ni entidades.
- No introducir dependencias o tecnologías nuevas.
- No presentar inventario, pagos, autenticación o migraciones como implementados.
- No declarar que el código funciona solo porque está escrito.

## Revisión humana

La persona responsable debe comprobar el requisito, la coherencia entre capas, el manejo de errores y la evidencia antes de aceptar la propuesta.
