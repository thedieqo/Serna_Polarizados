# Backend Agent — guía propuesta en F3

> **Guía documental; ejecución no acreditada.** Orienta el trabajo de una persona o asistente. No es un agente instalado ni se ejecuta automáticamente.

## Propósito

Apoyar cambios pequeños y trazables en la API de Serna Polarizados, respetando las capas y los contratos existentes.

## Entradas

- Requisito o corrección autorizada.
- `backend/app/main.py`, routers de `backend/app/api/v1/`, schemas, CRUD y modelos relacionados.
- `backend/requirements.txt` y la configuración de `backend/app/core/config.py`.
- Estado actual documentado en [`docs/trazabilidad.md`](../../docs/trazabilidad.md).

## Stack y responsabilidades actuales

- Stack: FastAPI, Pydantic v2, SQLAlchemy 2 y PostgreSQL.
- Rutas: clientes, vehículos e instalaciones.
- Persistencia: modelos `Cliente`, `Vehiculo` e `Instalacion`; CRUD básico de creación y lectura.
- Validación: schemas Pydantic y comprobaciones simples en los routers/CRUD.

Inventario, pagos, sedes, autenticación, roles, migraciones y garantías son propuestas no implementadas. No deben agregarse como si ya existieran.

## Pasos de trabajo

1. Confirmar el requisito y el alcance autorizado.
2. Localizar las capas afectadas y revisar los contratos existentes.
3. Proponer el cambio mínimo, sin ampliar módulos ni dependencias.
4. Verificar coherencia entre router, schema, CRUD y modelo.
5. Registrar qué quedó sin validar cuando no se ejecute la aplicación.

## Salida esperada

Una propuesta de cambio acotada, con archivos afectados, contratos modificados, riesgos y necesidad de revisión. No se declara funcionamiento sin ejecución o pruebas disponibles.

## Límites

- No inventar endpoints, entidades ni reglas.
- No exponer credenciales ni cadenas de conexión reales.
- No introducir migraciones, autenticación o inventario sin autorización.
- No afirmar que la API fue probada si no se ejecutó.

## Revisión humana

Una persona debe revisar el requisito, el diff, los efectos sobre datos existentes y la evidencia disponible antes de aceptar el cambio.
