# Diseño de backend y frontend — Serna Polarizados

## Estado

**Fecha de actualización:** 27 de octubre de 2026 (F2).
**Estado:** diseño actualizado a partir del código existente; implementación parcial.

Este documento describe la estructura y el recorrido de la implementación actual, y conserva como antecedente el diseño previo con Flask, SQLite y HTML/CSS/JavaScript. No presenta como terminadas las funciones que solo están en requisitos o planificación.

El diseño anterior se mantiene en el historial de Git y en [F0_LINEA_BASE_Y_VERIFICACIONES.md](F0_LINEA_BASE_Y_VERIFICACIONES.md). Su stack no corresponde al código actual.

No sustituye a [requisitos.md](requisitos.md) ni a los diagramas `.mmd`, que siguen desactualizados.

## 1. Organización general

La aplicación se organiza como una SPA desacoplada con un backend monolítico por capas:

| Capa | Tecnología actual | Responsabilidad |
| --- | --- | --- |
| Presentación | React 18, TypeScript, Vite y Tailwind CSS | Mostrar formularios, listas y mensajes; enviar solicitudes HTTP al backend. |
| Cliente HTTP | Axios | Centralizar la URL base, el tiempo de espera y el tratamiento de errores. |
| API | FastAPI | Exponer endpoints REST, validar solicitudes y devolver códigos HTTP. |
| Negocio y datos | CRUD con SQLAlchemy 2 | Consultar y guardar entidades; validar existencia de relaciones. |
| Validación | Pydantic v2 | Definir contratos de entrada y salida. |
| Persistencia | PostgreSQL / Supabase | Almacenar clientes, vehículos e instalaciones. |

Las capas del backend forman parte de una misma aplicación. No se usan microservicios ni colas de mensajes. El frontend y el backend se comunican por JSON sobre HTTP.

```text
React (frontend/src)
  páginas → componentes → services → Axios
                                  │
                                  ▼
FastAPI (backend/app/main.py)
  /api/v1/clientes
  /api/v1/vehiculos
  /api/v1/instalaciones
        │
        ▼
  routers → crud → models SQLAlchemy → PostgreSQL
```

Las validaciones del navegador ayudan al usuario, pero no sustituyen las comprobaciones del backend.

## 2. Estructura y pantallas implementadas

### Backend

```text
backend/app/
├── main.py              # FastAPI, CORS y registro de routers
├── core/config.py       # Variables de entorno y configuración
├── db/
│   ├── base.py          # Base declarativa de SQLAlchemy
│   └── session.py       # Engine, SessionLocal y dependencia get_db
├── models/              # Cliente, Vehiculo, Instalacion
├── schemas/             # Contratos Pydantic de entrada y salida
├── crud/                # Consultas y escrituras
└── api/v1/              # Routers de clientes, vehículos e instalaciones
```

### Frontend

```text
frontend/src/
├── App.tsx              # Encabezado, navegación por pestañas y páginas
├── pages/               # ClientesPage, VehiculosPage, InstalacionesPage
├── components/          # Formularios y listado
├── services/            # api.ts, clientes.ts, vehiculos.ts, instalaciones.ts
└── types/               # Interfaces TypeScript de las entidades
```

`App.tsx` usa un estado `activeTab` con `useState`. Aunque `react-router-dom` está instalado, no se usa para navegar.

La navegación visible tiene tres pestañas:

| Pantalla | Contenido actual | Historias relacionadas |
| --- | --- | --- |
| Clientes | Formulario de registro y tabla de clientes. | HU-01, HU-02 |
| Vehículos | Formulario de registro y tabla de vehículos. | HU-03, HU-04 |
| Instalaciones | Formulario de registro y listado de instalaciones. | HU-05, HU-06 |

Estado de la búsqueda: **implementada en backend** mediante `GET /api/v1/clientes/by-documento/{documento}`, `GET /api/v1/vehiculos/by-placa/{placa}` y las funciones CRUD correspondientes; **disponible como servicio frontend** en `clientesService.getByDocumento` y `vehiculosService.getByPlaca`; **no integrada en pantalla**; **no probada funcionalmente**. Los componentes vacíos `ClienteSearch` y `VehiculoSearch`, que nunca fueron importados, se retiraron en F4 sin alterar este estado ni los requisitos RF-03, HU-02 y HU-04.

## 3. Clientes y vehículos

**Historias:** HU-01, HU-02, HU-03 y HU-04.

### Flujo implementado

1. El usuario completa el formulario de cliente.
2. `clientesService.create` envía `POST /api/v1/clientes/`.
3. FastAPI valida con `ClienteCreate`.
4. El router comprueba si el documento ya existe.
5. El CRUD guarda el cliente y devuelve `ClienteRead`.
6. La página recarga la lista y muestra un mensaje de éxito.

Para vehículos:

1. El formulario solicita placa, descripción e identificador del cliente.
2. `vehiculosService.create` envía `POST /api/v1/vehiculos/`.
3. El router comprueba la placa duplicada.
4. El CRUD verifica que el cliente exista.
5. Se guarda el vehículo asociado al cliente.
6. La página recarga la lista.

### Endpoints

| Método | Ruta | Función |
| --- | --- | --- |
| POST | `/api/v1/clientes/` | Crear cliente; rechaza documento duplicado con 409. |
| GET | `/api/v1/clientes/` | Listar clientes con `skip` y `limit`. |
| GET | `/api/v1/clientes/{cliente_id}` | Consultar cliente por ID. |
| GET | `/api/v1/clientes/by-documento/{documento}` | Consultar cliente por documento. |
| POST | `/api/v1/vehiculos/` | Crear vehículo; valida cliente y placa duplicada. |
| GET | `/api/v1/vehiculos/` | Listar vehículos con `skip` y `limit`. |
| GET | `/api/v1/vehiculos/{vehiculo_id}` | Consultar vehículo por ID. |
| GET | `/api/v1/vehiculos/by-placa/{placa}` | Consultar vehículo por placa. |
| GET | `/api/v1/vehiculos/by-cliente/{cliente_id}` | Listar vehículos de un cliente. |

### Modelo y reglas

- `Cliente`: `id`, `nombre`, `documento` único, `contacto`.
- `Vehiculo`: `id`, `placa` única, `descripcion` opcional, `cliente_id`.
- Un cliente puede tener varios vehículos.
- `Cliente.vehiculos` y `Vehiculo.instalaciones` usan `cascade="all, delete-orphan"`.
- No hay endpoints de actualización ni eliminación.
- La búsqueda existe en la API y en los servicios; falta integrarla en la interfaz.

## 4. Instalaciones e historial

**Historias:** HU-05 y HU-06.

### Flujo implementado

1. El formulario carga la lista de vehículos con `GET /api/v1/vehiculos/`.
2. El usuario selecciona vehículo, tipo de servicio, estado, fecha, opacidad global, retiro de material anterior y observaciones.
3. El usuario agrega una o más zonas y una o más asignaciones de instaladores.
4. `instalacionesService.create` envía `POST /api/v1/instalaciones/`.
5. El CRUD verifica que el vehículo exista.
6. La instalación se guarda y la lista se actualiza.

### Endpoints

| Método | Ruta | Función |
| --- | --- | --- |
| POST | `/api/v1/instalaciones/` | Crear instalación; valida que el vehículo exista. |
| GET | `/api/v1/instalaciones/` | Listar instalaciones; acepta `vehiculo_id` para filtrar. |
| GET | `/api/v1/instalaciones/{instalacion_id}` | Consultar instalación por ID. |

### Modelo

`Instalacion` contiene:

- `vehiculo_id`.
- `fecha` con valor por defecto del servidor.
- `tipo_servicio`: `polarizado`, `pelicula_seguridad` o `ambos`.
- `opacidad` opcional.
- `zonas`: lista JSON de objetos; el formulario envía `zona` y `opacidad_aplicada`.
- `asignaciones_instaladores`: lista JSON de objetos; el formulario envía `zona` e `instalador`.
- `retiro_material_anterior`: booleano.
- `observaciones` opcional.
- `estado`: `programado`, `en_proceso`, `finalizado` o `anulado`.
- `created_at` y `updated_at`.

Pydantic exige al menos una zona y una asignación. Los objetos internos de los JSON no tienen un esquema detallado.

### Diferencias con los requisitos

- No existe campo `sede`.
- No existe `valor_total`.
- No hay una entidad separada de trabajo o servicio.
- No se registran materiales, piezas ni sobrantes.
- El listado muestra todas las instalaciones; no hay una vista de historial por vehículo.
- No hay actualización ni anulación mediante endpoint.
- El estado `anulado` existe como valor, pero no hay operación específica de anulación.

## 5. Materiales, rollos y disponibilidad

**Historias:** HU-08, HU-09 y HU-11.

No implementado.

El diseño previo proponía tipos de material, piezas, sede, dimensiones, disponibilidad y descarte. Esas entidades no existen en los modelos actuales. Los requisitos siguen vigentes, pero no deben presentarse como funcionalidades del código.

Cuando se implemente, deberá conservarse la separación entre tipo de material y pieza física, la sede de cada pieza y las dimensiones positivas.

## 6. Registro de uso y sobrantes

**Historia:** HU-10.

No implementado.

No existen modelos de uso, pieza, sobrante ni movimiento de inventario. Tampoco existe una transacción que actualice existencias. El procedimiento de corte y restante sigue pendiente de definición.

El diseño previo de este recorrido se conserva como propuesta en el historial de Git; no describe el código actual.

## 7. Corrección de registros de uso

**Historia:** HU-13.

No implementado.

No hay entidad de corrección, auditoría, autor, motivo ni conservación de datos anteriores y nuevos. Tampoco hay autenticación que permita comprobar el perfil del administrador.

## 8. Descarte de piezas dañadas

**Historia:** HU-14.  
**Prioridad:** pendiente de asignación.

No implementado. No existen piezas ni registro de descarte.

El tratamiento de daños parciales sigue pendiente y no se incorpora automáticamente como una función adicional.

## 9. Consulta de material de un trabajo

**Historia:** HU-12.  
**Prioridad de referencia:** Should.

No implementado. No existe relación entre instalación, uso de material y piezas.

## 10. Datos principales y relaciones implementadas

| Entidad | Datos actuales | Relaciones |
| --- | --- | --- |
| Cliente | `id`, `nombre`, `documento`, `contacto` | Uno a muchos con vehículos. |
| Vehículo | `id`, `placa`, `descripcion`, `cliente_id` | Pertenece a un cliente; uno a muchos con instalaciones. |
| Instalación | `id`, `vehiculo_id`, `fecha`, `tipo_servicio`, `opacidad`, `zonas`, `asignaciones_instaladores`, `retiro_material_anterior`, `observaciones`, `estado`, `created_at`, `updated_at` | Pertenece a un vehículo. |

Relaciones:

```text
Cliente 1 ─── N Vehiculo 1 ─── N Instalacion
```

Restricciones observadas:

- `clientes.documento` es único.
- `vehiculos.placa` es única.
- `vehiculos.cliente_id` es obligatorio.
- `instalaciones.vehiculo_id` es obligatorio.
- Las relaciones usan eliminación en cascada desde el ORM. Esto difiere de la conservación de historial propuesta en los requisitos y requiere una decisión antes de implementar borrados.

No hay migraciones Alembic ni creación automática de tablas documentada. La base de datos debe prepararse fuera de este código o mediante un mecanismo que todavía no forma parte del repositorio.

## 11. Información compartida y separada

### Compartida en el modelo actual

- Clientes.
- Vehículos.
- Instalaciones.

### Separada por sede

No implementada. El modelo actual no tiene `sede_id` en instalaciones, piezas ni movimientos. Por tanto, el sistema todavía no puede distinguir inventario por sede ni aplicar la regla de que el material pertenece a la sede del trabajo.

## 12. Mensajes y errores

### Backend

- `409` si el documento del cliente ya existe.
- `409` si la placa del vehículo ya existe.
- `400` si el cliente de un vehículo no existe.
- `400` si el vehículo de una instalación no existe.
- `404` si no se encuentra un cliente, vehículo o instalación.
- `422` para errores de validación de Pydantic.

### Frontend

- Mensajes de éxito después de una respuesta correcta.
- Mensajes de error provenientes de `error.response.data.detail`.
- Mensaje de error de conexión generado por el interceptor de Axios.
- Estados de carga y listas vacías en clientes, vehículos e instalaciones.

Los mensajes de inventario, permisos y correcciones descritos en el diseño anterior no están implementados.

## 13. Pendientes antes de completar la implementación

- Incorporar sede y valor total a la instalación, o decidir el modelo que los represente.
- Precisar los detalles de instalación y sus campos obligatorios.
- Integrar búsquedas por documento y placa en la interfaz.
- Implementar un historial por vehículo.
- Definir la precisión de las dimensiones en centímetros.
- Definir el registro del corte, el restante y los sobrantes.
- Definir correcciones con sobrantes utilizados posteriormente.
- Resolver anulaciones, material equivocado y daños parciales.
- Implementar autenticación, roles y permisos.
- Agregar migraciones de base de datos.
- Agregar pruebas automatizadas y registrar pruebas ejecutadas.
- Actualizar los diagramas `.mmd` conforme al código actual.
- Revisar con Jonathan y validar los requisitos con la asesora.

## 14. Dependencias para la implementación posterior

- Registrar un vehículo requiere un cliente existente.
- Registrar una instalación requiere un vehículo existente.
- Registrar un trabajo con sede requiere definir el modelo de sede.
- Registrar un rollo requiere tipo de material, sede y dimensiones.
- Registrar uso requiere trabajo, pieza disponible y reglas de corte.
- Corregir requiere registro de uso, autor, motivo y procedimiento definido.
- Descartar requiere una pieza disponible y un registro de descarte.
- Aplicar permisos requiere autenticación y roles.

Estas dependencias sirven para organizar el trabajo futuro. No constituyen una asignación de fechas, responsables ni tareas realizadas.

## 15. Referencias

- [Requisitos](requisitos.md).
- [Trazabilidad](trazabilidad.md).
- [Visión del proyecto](vision.md).
- [Planificación](planificacion.md).
- [Síntesis de entrevista y aclaraciones](ia/entrevista-cliente.md).
- [Línea base y verificaciones F0](F0_LINEA_BASE_Y_VERIFICACIONES.md).
