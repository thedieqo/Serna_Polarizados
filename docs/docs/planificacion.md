# Backlog y propuesta de sprints — Serna Polarizados

## 1. Estado

**Fecha:** 8 de septiembre de 2026.  
**Estado:** propuesta de planificación pendiente de revisión con los dos integrantes.

Esta planificación utiliza las historias de [requisitos.md](requisitos.md). No añade funciones ni representa trabajo implementado.

Los sprints no se han iniciado. Sus fechas, duración, estimaciones y responsables se acordarán entre los integrantes antes de comprometer el trabajo.

## 2. Product Backlog

El Product Backlog es la lista ordenada de funcionalidades previstas. El orden siguiente es una propuesta basada en las dependencias de la demostración principal.

Todas las historias están pendientes de implementación.

| Orden | ID | Historia | Prioridad actual | Dependencia o pendiente principal |
| --- | --- | --- | --- | --- |
| 1 | HU-01 | Registrar cliente | Must | Precisar validaciones de los campos. |
| 2 | HU-02 | Consultar cliente | Must | Disponer de clientes registrados para comprobar resultados. |
| 3 | HU-03 | Registrar vehículo | Must | Cliente existente. |
| 4 | HU-04 | Consultar vehículo | Must | Vehículo registrado. |
| 5 | HU-05 | Registrar trabajo y detalles | Must | Vehículo y sede; definir estructura de los detalles de instalación. |
| 6 | HU-06 | Consultar historial | Must | Trabajos registrados para comprobar el historial compartido. |
| 7 | HU-08 | Registrar tipo de material | Must de referencia | Identificación por tecnología y opacidad. |
| 8 | HU-09 | Registrar rollo recibido | Must de referencia | Tipo de material y sede; precisión de medidas pendiente. |
| 9 | HU-11 | Consultar disponibilidad | Must de referencia | Piezas registradas por sede. |
| 10 | HU-10 | Registrar uso y sobrantes | Must de referencia | Trabajo, pieza disponible de su sede y procedimiento de corte definido. |
| 11 | HU-13 | Corregir registro de uso | Must de referencia | Registro de uso; procedimiento de corrección y permisos definidos. |
| 12 | HU-14 | Descartar pieza dañada | Pendiente | Pieza disponible y autorización del administrador. |
| 13 | HU-12 | Consultar material de un trabajo | Should de referencia | Registros de uso asociados al trabajo. |

El orden no cambia automáticamente las prioridades aprobadas.

**Propuesta para HU-14:** asignar Must, porque una pieza dañada no debe seguir disponible para su utilización. Esta prioridad requiere revisión del equipo y no se presenta como aprobada.

HU-12 puede aplazarse. Su aplazamiento no elimina la identificación básica de registros necesaria para corregirlos mediante HU-13.

## 3. Propuesta de sprints

Un sprint es un periodo de trabajo con un objetivo y un resultado que el equipo pueda mostrar y comprobar.

Se propone la siguiente agrupación. La cantidad de historias de cada sprint deberá ajustarse a las estimaciones y al tiempo disponible.

### Sprint 1 — Clientes y vehículos

**Objetivo:** registrar y encontrar un cliente y sus vehículos.

**Historias propuestas:** HU-01, HU-02, HU-03 y HU-04.

**Actividades:**

- Precisar los campos y sus validaciones.
- Construir el registro y consulta de clientes.
- Construir el registro y consulta de vehículos.
- Comprobar documentos y placas duplicados.
- Comprobar varios vehículos por cliente y búsquedas sin resultados.

**Resultado esperado:** demostrar con datos ficticios el registro de un cliente, sus vehículos y la consulta por documento o placa.

### Sprint 2 — Trabajos e inventario inicial

**Objetivo:** conservar trabajos y consultar los materiales disponibles por sede.

**Historias propuestas:** HU-05, HU-06, HU-08, HU-09 y HU-11.

**Condiciones antes de comprometer las historias:**

- Definir los detalles de instalación de HU-05.
- Acordar la precisión de las medidas en centímetros.
- Contar con los clientes y vehículos necesarios.
- Resolver la identificación y los permisos necesarios para las operaciones.

**Actividades:**

- Construir el registro de trabajos y la consulta del historial.
- Construir el registro de tipos de material y rollos.
- Construir la consulta de disponibilidad por sede.
- Comprobar medidas inválidas y separación de inventarios.
- Comprobar la consulta del historial desde ambas sedes.

**Resultado esperado:** registrar un trabajo y un rollo, consultar el historial compartido y distinguir las piezas de cada sede.

Si las estimaciones superan la capacidad disponible, esta agrupación se dividirá antes de iniciar el sprint.

### Sprint 3 — Uso de material y ajustes

**Objetivo:** relacionar el uso de material con los trabajos y mantener consistente el inventario.

**Historias propuestas:** HU-10 y HU-13. HU-14 se incluirá si se confirma su prioridad y existe capacidad.

**Condiciones antes de comprometer las historias:**

- Definir el procedimiento de corte y registro del restante.
- Definir las correcciones cuando existen sobrantes utilizados posteriormente.
- Contar con trabajos y piezas registradas.
- Resolver los permisos de instalador y administrador.

**Actividades:**

- Construir el registro de uso y sobrantes.
- Construir las correcciones con constancia del ajuste.
- Construir el descarte completo si HU-14 se incorpora.
- Comprobar que no se duplique material.
- Comprobar rechazo de piezas de otra sede o no disponibles.
- Comprobar que un fallo no deje cambios parciales.
- Comprobar que únicamente el administrador pueda corregir.
- Recorrer el flujo desde el teléfono acordado.

**Resultado esperado:** demostrar el uso de una pieza, la conservación de sobrantes y la actualización exclusiva del inventario de la sede correspondiente.

HU-12 permanece en el backlog para una planificación posterior según la capacidad disponible.

## 4. Revisión al finalizar cada sprint

Se propone comprobar:

- Que las historias seleccionadas cumplen sus criterios de aceptación.
- Que se revisaron escenarios de éxito y error.
- Que ambos integrantes pueden explicar los cambios.
- Que el trabajo está guardado en GitHub.
- Que las pruebas realmente ejecutadas tienen su resultado registrado.
- Que los errores y pendientes permanecen visibles.
- Que se documentó el apoyo de IA utilizado.

Una historia con criterios esenciales pendientes no se considerará terminada.

## 5. Acuerdos pendientes del equipo

Antes de iniciar el desarrollo, los integrantes deben acordar:

- Fechas y duración de los sprints.
- Tiempo disponible de cada integrante.
- Estimación de las historias.
- Responsables de las tareas.
- Prioridad de HU-14.
- Distribución final de historias según la capacidad.

Esta propuesta no asigna tareas a Jonathan ni supone su aprobación.

## 6. Historia fuera del alcance

**HU-07 — Consultar trabajos por sede y periodo.**

Permanece descartada, con prioridad Won’t para esta versión. No se incluye en ningún sprint.

## 7. Relación con la entrega académica

Esta planificación organiza el desarrollo futuro. No acredita sprints iniciados o completados.

La configuración de Jira y su integración se realizará cuando corresponda a las instrucciones de clase. Por ahora, el backlog y la propuesta de sprints quedan documentados en el repositorio.
