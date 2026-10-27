# Skill: Database Design — guía propuesta en F3

> **Guía documental; ejecución no acreditada.** No crea tablas, migraciones ni conexiones. Solo ayuda a analizar el modelo.

## Propósito

Revisar la coherencia entre requisitos, modelos SQLAlchemy y persistencia PostgreSQL.

## Entradas

- Requisitos y reglas de negocio vigentes.
- `backend/app/models/cliente.py`, `vehiculo.py` e `instalacion.py`.
- `backend/app/db/session.py` y la configuración de conexión.
- Decisiones de alcance documentadas.

## Estado actual

Tecnología: PostgreSQL mediante SQLAlchemy. No hay migraciones versionadas ni creación automatizada de esquema.

| Tabla | Atributos observados |
|---|---|
| `clientes` | `id`, `nombre`, `documento`, `contacto` |
| `vehiculos` | `id`, `placa`, `descripcion`, `cliente_id` |
| `instalaciones` | `id`, `vehiculo_id`, `fecha`, `tipo_servicio`, `opacidad`, `zonas`, `asignaciones_instaladores`, `retiro_material_anterior`, `observaciones`, `estado`, `created_at`, `updated_at` |

Relaciones: un cliente tiene muchos vehículos; un vehículo tiene muchas instalaciones. El código usa `cascade="all, delete-orphan"`, lo que no coincide con una política de conservación de historial y sigue pendiente de decisión.

## Propuestas no implementadas

Usuario, sede, cita, servicio, instalador, inventario, consumo de material, pago y garantía son entidades propuestas. No existen como tablas ni modelos actuales y no deben mostrarse como implementadas.

## Pasos

1. Contrastar cada entidad propuesta con los modelos reales.
2. Revisar claves primarias, claves foráneas y cardinalidades.
3. Identificar duplicación o atributos sin respaldo en requisitos.
4. Señalar decisiones pendientes, como la conservación del historial.
5. Entregar observaciones sin modificar la base de datos.

## Salida esperada

Lista de coincidencias, divergencias y decisiones pendientes, con referencias a archivos. No se afirma que el esquema exista en una base real.

## Límites

- No ejecutar SQL, migraciones ni conexiones.
- No inventar tablas o columnas.
- No cambiar modelos para que coincidan con un diagrama histórico.

## Revisión humana

La persona responsable valida el modelo contra requisitos y decide cualquier cambio de persistencia.
