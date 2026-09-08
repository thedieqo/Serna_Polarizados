# Serna Polarizados — Sistema de Gestión

Proyecto académico de la asignatura **Electiva CPC: Integración de la IA en el Ciclo de Vida del Software**.

**Estado:** análisis de requisitos y diseño inicial. La implementación está pendiente.  
**Última actualización documental:** 8 de septiembre de 2026.

## 1. Descripción

Serna Polarizados es un proyecto de sistema web para organizar clientes, vehículos, trabajos realizados e inventario de las dos sedes de la empresa en Ibagué.

Ambas sedes compartirán clientes, vehículos e historial de trabajos. Cada sede mantendrá su propio inventario de rollos y recortes aprovechables.

El proyecto se desarrolla por dos estudiantes con apoyo de IA y revisión humana.

## 2. Problema identificado

La entrevista con una asesora y las aclaraciones del administrador participante identificaron estas dificultades:

- Información distribuida entre archivos de Excel, formularios y registros manuales.
- Dependencia de llamadas para recuperar antecedentes de instalaciones.
- Dificultades de los instaladores para registrar información desde sus teléfonos.
- Falta de registro sistemático de entradas, cortes y sobrantes.
- Poca claridad sobre las tecnologías y opacidades disponibles.

También se identificaron problemas de pagos y comisiones. Se documentaron como contexto, pero quedaron fuera de la primera versión.

La [síntesis de la entrevista](docs/ia/entrevista-cliente.md) distingue las declaraciones de la asesora de las decisiones posteriores del administrador.

## 3. Objetivo

Desarrollar un sistema web para las dos sedes de Serna Polarizados en Ibagué que centralice la información de clientes, vehículos y trabajos, y permita controlar el inventario de cada sede relacionando las piezas utilizadas con los trabajos realizados.

## 4. Alcance de la primera versión

### Clientes y vehículos

- Registrar clientes con nombre, documento y contacto.
- Registrar vehículos con placa, descripción y cliente asociado.
- Permitir varios vehículos por cliente.
- Consultar clientes por documento y vehículos por placa.
- Evitar documentos y placas duplicados.

### Trabajos e historial

- Registrar vehículo, sede, fecha, servicio y valor total.
- Conservar los detalles registrados de tecnología, opacidad, instalador y retiro de película.
- Consultar el historial del vehículo desde ambas sedes.

La estructura de los detalles de instalación sigue pendiente de precisar.

### Inventario por sede

- Registrar tipos de material diferenciando tecnología y opacidad.
- Identificar rollos recibidos con sede, material, ancho y largo.
- Registrar el uso de material asociado a un trabajo y una pieza de origen.
- Registrar recortes aprovechables sin duplicar existencias.
- Consultar rollos y recortes disponibles por sede.
- Permitir al administrador corregir registros de uso y descartar piezas completas dañadas.

Las dimensiones se registrarán en centímetros. Los recortes se representarán mediante rectángulos aprovechables medidos por el instalador.

El procedimiento exacto de corte, actualización del restante y corrección sigue pendiente de definición.

## 5. Reglas principales

- El sistema cubre únicamente las dos sedes de Ibagué.
- Clientes, vehículos e historial se comparten entre esas sedes.
- Cada trabajo pertenece a un vehículo y a una sede.
- Cada pieza de material pertenece a una sede.
- El material utilizado debe pertenecer a la sede del trabajo.
- No se puede utilizar más material del disponible.
- Un sobrante no puede seguir contado dentro de la pieza de origen.
- Las correcciones conservan autor, fecha, motivo y datos anteriores y nuevos.
- Las operaciones de inventario se guardan completas o no se aplican.
- Compartir información entre sedes no significa hacerla pública.

Las reglas y sus comprobaciones se detallan en [requisitos.md](docs/requisitos.md).

## 6. Fuera del alcance

- Cálculo de comisiones y remuneraciones.
- Gestión o verificación de pagos.
- Facturación e integración con Siigo.
- Agenda de citas y registro por QR.
- Gastos e informes financieros.
- Proveedores y compras.
- Alertas automáticas de inventario.
- Cotización de PPF.
- Gestión completa de garantías.
- Sedes adicionales, incluida Bogotá.
- Cálculo automático de cortes y representación de formas irregulares.

Registrar el valor del trabajo no equivale a gestionar su pago.

El historial podrá apoyar consultas de antecedentes para garantías, sin administrar el proceso completo.

## 7. Personas involucradas

| Persona | Participación prevista |
| --- | --- |
| Administrador | Registrar y consultar información, corregir registros de uso y registrar descartes completos. |
| Asesor | Registrar y consultar clientes, vehículos y trabajos. |
| Instalador | Registrar el uso de material y los sobrantes de sus operaciones. |
| Cliente | Proporcionar sus datos y los de su vehículo, sin portal de autoservicio. |

La identificación de usuarios y los permisos detallados siguen pendientes. La corrección de registros de uso está reservada al administrador.

## 8. Demostración prevista

Con datos ficticios, el equipo buscará demostrar este recorrido:

1. Registrar un cliente y su vehículo.
2. Registrar un tipo de material y un rollo recibido en una sede.
3. Registrar un trabajo para el vehículo en esa sede.
4. Asociar el uso de material al trabajo y a su pieza de origen.
5. Registrar los sobrantes aprovechables sin duplicar material.
6. Comprobar que únicamente cambia el inventario de esa sede.
7. Consultar el historial del vehículo desde la otra sede.

El recorrido de inventario se completará cuando se defina el procedimiento de corte y registro del restante.

Esta demostración está prevista; todavía no se ha ejecutado.

## 9. Tecnologías y arquitectura

| Elemento | Elección prevista |
| --- | --- |
| Backend | Python y Flask |
| Frontend | HTML, CSS y JavaScript |
| Base de datos | SQLite |
| Control de versiones | Git y GitHub |
| Arquitectura | Monolito en capas |

La aplicación se organizará en tres capas:

- **Presentación:** formularios, información y mensajes.
- **Negocio:** comprobación de permisos y reglas.
- **Acceso a datos:** almacenamiento y consulta en SQLite.

Las capas forman parte de una misma aplicación.

El [diseño inicial de backend y frontend](docs/diseno-back-front.md) describe las responsabilidades y pantallas propuestas. Los diagramas están pendientes de actualización y revisión.

## 10. Documentación

| Documento | Contenido |
| --- | --- |
| [Visión](docs/vision.md) | Problema, propuesta de valor y límites del proyecto. |
| [Requisitos](docs/requisitos.md) | Reglas, requisitos funcionales y no funcionales, historias y criterios de aceptación. |
| [Trazabilidad](docs/trazabilidad.md) | Relación entre necesidades, requisitos, historias y comprobaciones. |
| [Diseño de backend y frontend](docs/diseno-back-front.md) | Propuesta de pantallas, responsabilidades y relaciones de datos. |
| [Análisis competitivo](docs/analisis-competitivo.md) | Comparación documental de soluciones existentes. |
| [Diagrama de arquitectura](docs/diagramas/arquitectura.mmd) | Representación inicial de las capas; pendiente de revisión. |
| [Entrevista y aclaraciones](docs/ia/entrevista-cliente.md) | Síntesis de la entrevista y decisiones posteriores. |
| [Matriz de uso de IA](docs/ia/matriz-ia.md) | Apoyo previsto de IA y revisión del equipo. |
| [Biblioteca de prompts](docs/ia/prompts.md) | Instrucciones utilizadas, resultados y observaciones. |
| [Pruebas con Gemini](docs/ia/pruebas-gemini.md) | Prompts de análisis y resúmenes de resultados. |
| [Revisión de historias con Gemini](docs/ia/revision-historias-gemini.md) | Archivo destinado a la revisión y sus correcciones; pendiente de ajustar. |

La existencia de un archivo no significa que su revisión esté terminada.

## 11. Uso de inteligencia artificial

Se ha utilizado IA para apoyar la delimitación del alcance, el análisis de requisitos, la redacción de historias y la propuesta de diseño.

- **Gemini:** generación y revisión de borradores de requisitos.
- **Codex:** apoyo en organización, revisión y redacción de documentación.

Los registros distinguen instrucciones, respuestas, correcciones y decisiones confirmadas. Los prompts originales se conservan como evidencia histórica; las traducciones o mejoras no se presentan como ejecutadas sin haberlas probado.

La revisión de IA no sustituye la validación del negocio ni la revisión de los integrantes.

La implementación y las pruebas del software son actividades futuras.

## 12. Estado y próximos pasos

### Documentado

- Entrevista y aclaraciones del administrador.
- Alcance y exclusiones.
- 16 requisitos funcionales y 6 no funcionales.
- 13 historias activas, con HU-07 descartada.
- Criterios de aceptación, algunos todavía parciales.
- Trazabilidad y diseño inicial.
- Registros de uso de IA.

### Pendiente

- Precisar los detalles de instalación de HU-05.
- Definir el procedimiento de corte y restante de HU-10.
- Definir las correcciones de HU-13, incluidos los casos con sobrantes utilizados.
- Acordar la precisión de las medidas.
- Completar la identificación de usuarios y los permisos.
- Asignar prioridad a HU-14 y revisar el esfuerzo de inventario.
- Acordar condiciones de evaluación de los requisitos no funcionales.
- Completar la revisión de evidencias de IA y documentos restantes.
- Actualizar y revisar los diagramas.
- Organizar el backlog y la propuesta de sprints con las dependencias actuales.
- Revisar con Jonathan y validar los resultados derivados con la asesora.
- Preparar la sustentación del trabajo realizado.

Los sprints todavía no se presentan como iniciados ni completados. Las decisiones pendientes no se consideran resueltas por aparecer en un documento.

## 13. Equipo

Proyecto desarrollado por dos estudiantes:

- Integrante que administra una sede de Serna Polarizados: nombre completo pendiente de registrar.
- Jonathan: apellidos pendientes de registrar.

La distribución de tareas se acordará entre ambos y se reflejará en la planificación.

## 14. Alcance de esta entrega

Este repositorio documenta el análisis y el diseño inicial del proyecto.

No contiene todavía una aplicación implementada ni evidencia de pruebas de funcionamiento. Los criterios escritos describen cómo se comprobarán las funciones durante el desarrollo.
