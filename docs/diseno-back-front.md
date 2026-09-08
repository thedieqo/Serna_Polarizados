# Diseño inicial de backend y frontend — Serna Polarizados

## Estado

**Fecha de actualización:** 8 de septiembre de 2026.  
**Estado:** propuesta de diseño; implementación pendiente.

Este documento propone pantallas, responsabilidades y relaciones de datos para el alcance definido en [requisitos.md](requisitos.md).

Las reglas confirmadas proceden de ese documento. La agrupación de pantallas y la organización técnica son propuestas para su programación posterior.

No representa funcionalidades implementadas ni sustituye los diagramas de diseño.

## 1. Organización general

Se propone una aplicación organizada como monolito en capas:

| Capa | Tecnología prevista | Responsabilidad |
| --- | --- | --- |
| Presentación | HTML, CSS y JavaScript | Mostrar formularios, información y mensajes; enviar las acciones del usuario al backend. |
| Negocio | Python y Flask | Comprobar permisos y reglas, coordinar registros y decidir si una operación puede realizarse. |
| Acceso a datos | Acceso a SQLite desde Python | Guardar y consultar información, conservando las relaciones entre registros. |

Las capas forman parte de una misma aplicación.

Las validaciones del navegador ayudan al usuario, pero no sustituyen las comprobaciones del backend.

## 2. Pantallas propuestas

Se propone agrupar las operaciones en tres pantallas principales. Los formularios de corrección y descarte se abrirían dentro del contexto correspondiente.

| Pantalla | Información y campos principales | Acciones | Historias |
| --- | --- | --- | --- |
| Clientes y vehículos | Nombre, documento y contacto del cliente; placa, descripción y cliente asociado al vehículo. | Buscar cliente, registrar cliente, consultar sus vehículos, registrar vehículo y buscar por placa. | HU-01 a HU-04 |
| Trabajos e historial | Vehículo, sede, fecha, servicio, valor total y detalles registrados de instalación; pieza utilizada y sobrantes vinculados al trabajo. | Consultar historial, registrar trabajo, registrar uso y sobrantes, identificar un registro para corregirlo. Consulta general de material aplazable. | HU-05, HU-06, HU-10, HU-12 y HU-13 |
| Materiales e inventario | Tecnología, opacidad, identificación de pieza, sede, ancho y largo en centímetros, disponibilidad y motivo de descarte. | Registrar tipo de material, registrar rollo recibido, consultar disponibilidad y descartar una pieza completa. | HU-08, HU-09, HU-11 y HU-14 |

La distribución definitiva debe revisarse con el equipo. Los campos que describen cortes, correcciones y múltiples detalles de instalación siguen pendientes.

### Uso desde teléfonos

Se propone:

- Mostrar formularios con etiquetas claras.
- Mantener visibles el vehículo, el trabajo y la sede durante el registro de material.
- Mostrar mensajes comprensibles cuando una operación falle.
- Confirmar el guardado solamente después de la respuesta correcta del backend.

La facilidad de uso deberá evaluarse con un instalador. Todavía no se han acordado dispositivos ni condiciones completas de prueba.

## 3. Clientes y vehículos

**Historias:** HU-01, HU-02, HU-03 y HU-04.

### Frontend

- Formulario de cliente con nombre, documento y contacto.
- Búsqueda de cliente por documento.
- Formulario de vehículo con descripción, placa y cliente asociado.
- Búsqueda de vehículo por placa.
- Presentación de los vehículos asociados a un cliente.
- Mensajes de coincidencia, ausencia de resultados o duplicación.

### Backend

- Registrar y consultar clientes.
- Impedir documentos duplicados.
- Registrar vehículos vinculados a clientes existentes.
- Impedir placas duplicadas.
- Conservar varios vehículos asociados a un mismo cliente.
- Devolver resultados correspondientes al documento o placa consultados.

## 4. Trabajos e historial

**Historias:** HU-05 y HU-06.

### Frontend

- Formulario con vehículo, sede, fecha, servicio y valor total.
- Presentación de los detalles registrados de tecnología, opacidad, instalador y retiro de película.
- Historial del vehículo con identificación de la sede de cada trabajo.
- Mensaje cuando el vehículo no tenga trabajos registrados.

### Backend

- Comprobar que el vehículo y la sede existan.
- Guardar la relación entre trabajo, vehículo y sede.
- Conservar los detalles de instalación registrados.
- Permitir consultar el historial desde ambas sedes de Ibagué.
- Mantener el valor del trabajo separado de cualquier gestión de pagos.

**Pendiente:** definir qué detalles son obligatorios y cómo representar varias tecnologías, opacidades o instaladores dentro de un trabajo.

## 5. Materiales, rollos y disponibilidad

**Historias:** HU-08, HU-09 y HU-11.

### Frontend

- Formulario de tipo de material con tecnología y opacidad.
- Formulario de rollo recibido con identificación, sede, material, ancho y largo.
- Medidas expresadas en centímetros.
- Consulta de rollos y recortes disponibles por sede, material y dimensiones.
- Mensajes para dimensiones inválidas o consultas sin resultados.

### Backend

- Registrar tipos de material.
- Identificar cada rollo recibido y asociarlo a una sede.
- Validar dimensiones positivas.
- Consultar piezas disponibles sin mezclar inventarios de sedes.
- Excluir de la disponibilidad las piezas descartadas.
- Conservar la diferencia entre tipo de material y pieza física.

Un tipo de material puede corresponder a varios rollos y recortes con dimensiones diferentes.

La unidad acordada es el centímetro. La precisión admitida sigue pendiente.

## 6. Registro de uso y sobrantes

**Historia:** HU-10.

### Frontend

- Abrir el registro de uso dentro del trabajo correspondiente.
- Mostrar la sede del trabajo sin permitir elegir otra para el uso.
- Permitir identificar la pieza de origen.
- Permitir registrar las dimensiones de los sobrantes aprovechables.
- Mostrar el resultado del guardado.

Los campos exactos del corte y del restante se definirán antes de implementar esta operación.

### Backend: recorrido previsto

1. Identificar al usuario y comprobar su autorización.
2. Recuperar el trabajo y obtener su sede.
3. Comprobar que la pieza de origen exista, esté disponible y pertenezca a esa sede.
4. Validar dimensiones positivas y disponibilidad conforme al procedimiento de corte que se acuerde.
5. Preparar el registro de uso, los sobrantes y la actualización del origen.
6. Guardar todos los cambios juntos, sin duplicar material.
7. Confirmar el éxito únicamente si toda la operación se guardó.

Si falla un cambio, no debe aplicarse ninguno.

### Límites del diseño actual

- No se ha definido cómo registrar exactamente el corte y el restante del rollo.
- Comparar únicamente áreas no permite comprobar que un recorte cabe en una pieza.
- No se implementará optimización automática de cortes.
- Los sobrantes se representarán mediante rectángulos aprovechables medidos por el instalador.

Por estos pendientes, todavía no se define una fórmula definitiva de actualización del inventario.

## 7. Corrección de registros de uso

**Historia:** HU-13.

### Frontend

- Permitir identificar el registro que se va a corregir.
- Mostrar los datos originales.
- Solicitar los datos corregidos y el motivo.
- Mostrar el resultado de la operación.

La identificación básica del registro es necesaria aunque se aplace la consulta general de HU-12.

### Backend: recorrido previsto

1. Comprobar que el usuario sea administrador.
2. Recuperar el registro de uso y las piezas relacionadas.
3. Validar el motivo y los cambios solicitados.
4. Comprobar si la corrección puede aplicarse según las reglas que se acuerden.
5. Verificar disponibilidad si la corrección implica utilizar más material.
6. Guardar el ajuste y sus efectos en inventario como una sola operación.
7. Conservar autor, fecha, motivo y datos anteriores y nuevos.

La corrección afecta únicamente al inventario de la sede correspondiente.

**Pendiente:** definir el tratamiento de sobrantes utilizados posteriormente, anulaciones y material equivocado.

El diseño anterior basado únicamente en restar dos cantidades no basta para resolver correcciones de rollos y recortes relacionados.

## 8. Descarte de piezas dañadas

**Historia:** HU-14.  
**Prioridad:** pendiente de asignación.

### Frontend

- Seleccionar una pieza disponible.
- Mostrar su identificación, material, sede y dimensiones.
- Solicitar el motivo del descarte.
- Confirmar el resultado.

### Backend

- Comprobar que el usuario sea administrador.
- Validar la pieza y el motivo.
- Registrar el descarte completo.
- Retirar la pieza de la disponibilidad conservando su identificación y el registro del descarte.
- Guardar la operación completa sin afectar al inventario de la otra sede.

El tratamiento de daños parciales sigue pendiente y no se incorpora automáticamente como una función adicional.

## 9. Consulta de material de un trabajo

**Historia:** HU-12.  
**Prioridad de referencia:** Should.

Se propone mostrar las piezas de origen y los registros de uso asociados al trabajo.

Esta consulta general puede aplazarse frente a las funciones indispensables. Las relaciones entre trabajo, uso y pieza se conservarán desde el registro inicial.

Si no existe uso de material registrado, se mostrará un mensaje indicando esa situación.

## 10. Datos principales y relaciones propuestas

Esta lista orienta el diseño; no define todavía las tablas definitivas de la base de datos.

| Información | Datos y relaciones principales |
| --- | --- |
| Cliente | Nombre, documento y contacto. Puede tener varios vehículos. |
| Vehículo | Placa, descripción y cliente asociado. Puede tener varios trabajos. |
| Sede | Identifica una de las dos sedes de Ibagué. Se relaciona con trabajos y piezas de inventario. |
| Trabajo | Vehículo, sede, fecha, servicio, valor total y detalles de instalación. |
| Tipo de material | Tecnología y opacidad. Se relaciona con rollos y recortes. |
| Pieza | Identificación, tipo de material, sede, ancho, largo y disponibilidad. Puede ser un rollo o un recorte. |
| Registro de uso | Relaciona un trabajo con la pieza utilizada. Los datos exactos del corte están pendientes. |
| Sobrante | Pieza aprovechable vinculada a su origen y a la operación que la produjo. |
| Corrección | Registro afectado, autor, fecha, motivo y datos anteriores y nuevos. |
| Descarte | Pieza descartada y motivo, conservando el registro de la operación. |

La identidad del usuario deberá permitir comprobar permisos y registrar al autor de las correcciones. Su mecanismo todavía no está definido.

Los detalles de instalación y las relaciones entre usos, sobrantes y correcciones requieren revisión antes de cerrar el modelo de datos.

## 11. Información compartida y separada

### Compartida entre las dos sedes

- Clientes.
- Vehículos.
- Historial y detalles registrados de trabajos.

### Identificada por sede

- Trabajos realizados.
- Rollos y recortes.
- Entradas y registros de uso.
- Correcciones y descartes.

Compartir el historial de un trabajo no cambia la sede a la que pertenece su inventario.

## 12. Mensajes necesarios

- El documento ya está registrado.
- La placa ya está registrada.
- No se encontró el cliente o vehículo.
- El vehículo todavía no tiene trabajos registrados.
- Las dimensiones deben ser mayores que cero.
- La pieza no está disponible.
- La pieza pertenece a otra sede.
- No hay material suficiente para la operación.
- Debe indicar el motivo.
- No tiene permiso para realizar esta operación.
- No se pudo guardar la operación.
- La operación se guardó correctamente.

Los mensajes son propuestas de redacción. El backend debe comprobar la condición correspondiente antes de devolver el resultado.

## 13. Pendientes antes de implementar

- Precisar los detalles de instalación y sus campos obligatorios.
- Definir la precisión de las dimensiones en centímetros.
- Definir el registro del corte y del restante.
- Definir correcciones con sobrantes utilizados posteriormente.
- Resolver el tratamiento de anulaciones, material equivocado y daños parciales.
- Completar la identificación de usuarios y los permisos.
- Revisar la prioridad de HU-14 y el esfuerzo de las historias de inventario.
- Acordar dispositivos y condiciones de evaluación de uso.
- Revisar el diseño con Jonathan.
- Actualizar los diagramas conforme a los requisitos vigentes.

## 14. Dependencias para la planificación posterior

- Registrar un vehículo requiere un cliente.
- Registrar un trabajo requiere un vehículo y una sede.
- Registrar un rollo requiere un tipo de material y una sede.
- Registrar uso requiere un trabajo y una pieza disponible de esa sede.
- Corregir requiere un registro de uso y un procedimiento de corrección definido.
- Descartar requiere una pieza disponible.
- Las operaciones restringidas requieren identificar al usuario y comprobar sus permisos.

Estas dependencias servirán para organizar el backlog y los sprints. No constituyen una asignación de fechas, responsables ni tareas realizadas.

## 15. Referencias

- [Requisitos](requisitos.md).
- [Trazabilidad](trazabilidad.md).
- [Visión del proyecto](vision.md).
- [Síntesis de entrevista y aclaraciones](ia/entrevista-cliente.md).
