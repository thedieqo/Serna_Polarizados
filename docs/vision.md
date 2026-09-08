# Visión del proyecto — Serna Polarizados

## 1. Visión

Desarrollar un sistema web para las dos sedes de Serna Polarizados en Ibagué que centralice clientes, vehículos e historial de trabajos y permita conocer los rollos y recortes disponibles en el inventario independiente de cada sede.

La propuesta de valor consiste en consultar los antecedentes de un vehículo desde cualquiera de las dos sedes y relacionar los trabajos con las piezas de material utilizadas, los sobrantes aprovechables y los ajustes registrados.

## 2. Situación actual y fuentes

El negocio utiliza registros manuales, archivos de Excel y formularios compartidos para organizar su operación.

La entrevista con una asesora identificó dificultades para consultar antecedentes de instalaciones, conocer la disponibilidad de tecnologías y registrar información desde los teléfonos de los instaladores. Recuperar información de otros puntos de atención puede requerir llamadas.

El administrador participante aclaró que no se registran sistemáticamente las entradas, cortes y sobrantes. Los rollos tienen distintos anchos; algunos sobrantes se conservan para otros trabajos y otros se dañan y se desechan.

La entrevista también identificó problemas relacionados con pagos y comisiones. Estos se conservan como contexto del negocio, pero no se resolverán en la primera versión.

Fuentes:

- [Síntesis de la entrevista y aclaraciones](ia/entrevista-cliente.md).
- Registro de Excel compartido como ejemplo.
- Decisiones del administrador participante, recogidas en [requisitos.md](requisitos.md).

## 3. Personas involucradas

| Persona | Participación prevista |
| --- | --- |
| Administrador | Registrar y consultar información, supervisar el inventario, corregir registros de uso y registrar descartes completos. |
| Asesor | Registrar y consultar clientes, vehículos y trabajos. |
| Instalador | Registrar el uso de material y los sobrantes aprovechables de sus operaciones. |
| Cliente | Proporcionar sus datos y los de su vehículo. |

El cliente no tendrá un portal de autoservicio.

La identificación de usuarios y los permisos detallados siguen pendientes. La corrección de registros de uso está reservada al administrador.

## 4. Necesidades principales

- Encontrar clientes por documento y vehículos por placa.
- Consultar los trabajos anteriores y los detalles registrados de instalación.
- Compartir el historial entre las dos sedes de Ibagué.
- Identificar los rollos y recortes disponibles en cada sede.
- Relacionar cada uso de material con un trabajo y una pieza de origen.
- Registrar sobrantes sin duplicar el material disponible.
- Conservar constancia de las correcciones.
- Retirar de la disponibilidad las piezas descartadas.
- Facilitar el registro desde el teléfono del instalador.

## 5. Alcance de la primera versión

### Clientes y vehículos

- Registrar clientes con nombre, documento y contacto.
- Registrar vehículos con placa, descripción y cliente asociado.
- Permitir varios vehículos por cliente.
- Consultar por documento o placa.
- Evitar documentos y placas duplicados.

### Trabajos e historial

- Registrar vehículo, sede, fecha, servicio y valor total.
- Conservar detalles de tecnología, opacidad, instalador y retiro de película que correspondan.
- Consultar el historial desde ambas sedes.

La estructura de los detalles de instalación todavía debe precisarse.

### Inventario por sede

- Registrar tipos de material diferenciando tecnología y opacidad.
- Identificar cada rollo recibido con su sede, material, ancho y largo.
- Registrar el uso de piezas asociado a trabajos de la misma sede.
- Identificar sobrantes aprovechables y conservar su relación con la pieza de origen.
- Consultar rollos y recortes disponibles por sede.
- Permitir al administrador corregir registros de uso y descartar piezas completas dañadas.

Las dimensiones se registrarán en centímetros. Los recortes se representarán mediante rectángulos aprovechables medidos por el instalador.

La consulta general del material de un trabajo conserva prioridad Should. La prioridad del descarte de piezas está pendiente. Las prioridades y los detalles verificables se mantienen en [requisitos.md](requisitos.md).

## 6. Reglas centrales

- Clientes, vehículos e historial se comparten entre las dos sedes.
- Cada pieza de inventario pertenece a una sede.
- El material utilizado debe pertenecer a la sede del trabajo.
- No se puede utilizar más material del disponible.
- Un sobrante no puede seguir contado dentro de la pieza de origen.
- Las correcciones conservan autor, fecha, motivo y datos anteriores y nuevos.
- Las operaciones de inventario se guardan completas o no se aplican.
- Compartir información entre sedes no significa hacerla pública.

## 7. Límites

La primera versión se limita a las dos sedes de Ibagué.

No incluye:

- Comisiones ni remuneraciones.
- Gestión o verificación de pagos.
- Facturación e integración con Siigo.
- Agenda de citas y registro por QR.
- Gastos e informes financieros.
- Proveedores y compras.
- Alertas automáticas de inventario.
- Cotización de PPF.
- Gestión completa de garantías.
- Sedes adicionales, incluida Bogotá.
- Cálculo automático de cortes o representación de formas irregulares.

Registrar el valor total de un trabajo no equivale a gestionar su pago.

El historial podrá apoyar la consulta de antecedentes para garantías, sin administrar ese proceso completo.

## 8. Resultado esperado

Con datos ficticios, el equipo buscará demostrar que:

1. Se registra un cliente y su vehículo.
2. Se registra un rollo con material, dimensiones y sede.
3. Se registra un trabajo para el vehículo en esa sede.
4. Se relaciona el uso del material con el trabajo y su pieza de origen.
5. Se registran los sobrantes aprovechables sin duplicar existencias.
6. Se actualiza únicamente el inventario de la sede correspondiente.
7. El historial del vehículo puede consultarse desde la otra sede.

El recorrido de inventario se detallará cuando se defina el procedimiento de corte y registro del restante.

Estos resultados ya están vinculados con historias y criterios en [requisitos.md](requisitos.md) y [trazabilidad.md](trazabilidad.md). Todavía no representan funcionalidades implementadas.

## 9. Decisiones técnicas

- Proyecto académico desarrollado por dos integrantes durante el semestre.
- Backend previsto con Python y Flask.
- Frontend previsto con HTML, CSS y JavaScript.
- Base de datos prevista con SQLite.
- Arquitectura de monolito en capas: presentación, negocio y acceso a datos.
- Documentación y control de cambios en GitHub.
- Apoyo de IA con revisión y corrección humana.

El diseño de pantallas y responsabilidades se documenta en [diseno-back-front.md](diseno-back-front.md) y debe mantenerse alineado con los requisitos actuales.

## 10. Estado y pendientes

**Fecha de actualización:** 8 de septiembre de 2026.

El proyecto está en análisis y diseño. La implementación está pendiente.

Falta precisar:

- La estructura y obligatoriedad de los detalles de instalación.
- La precisión de las medidas en centímetros.
- El registro del corte y del material restante.
- Las correcciones cuando existen sobrantes utilizados posteriormente.
- El tratamiento de anulaciones, material equivocado y daños parciales.
- La identificación de usuarios y los permisos detallados.
- La prioridad de HU-14 y la revisión del esfuerzo de inventario.
- Las condiciones de evaluación desde teléfonos y navegadores.

Los casos pendientes no se incorporan automáticamente como nuevas funciones.

La revisión conjunta con Jonathan y la validación posterior con la asesora siguen pendientes. Esta visión expresa el resultado buscado; los requisitos vigentes definen sus reglas y comprobaciones.
