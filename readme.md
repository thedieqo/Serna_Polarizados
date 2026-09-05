# Serna Polarizados — Sistema de Gestión

Proyecto académico de la asignatura **Electiva CPC: Integración de la IA en el Ciclo de Vida del Software**.

**Estado actual:** planeación, análisis de requisitos y diseño, correspondientes a las sesiones 1 a 4. La implementación está pendiente.

## 1. Descripción

Serna Polarizados es un proyecto de sistema web para organizar la información de clientes, vehículos, trabajos realizados y materiales de las dos sedes de la empresa en Ibagué.

Las dos sedes podrán consultar la misma información de clientes, vehículos e historial de trabajos. Cada sede manejará su propio inventario.

El proyecto se desarrollará durante el semestre con apoyo de inteligencia artificial y revisión de los integrantes del equipo.

## 2. Problemática

Actualmente se utilizan registros manuales y archivos de Excel para administrar información del negocio.

Esto dificulta:

- Consultar los datos de un cliente y sus vehículos.
- Conocer los trabajos que se han realizado a un vehículo.
- Compartir información entre las dos sedes.
- Consultar las existencias de materiales de cada sede.
- Relacionar los materiales utilizados con el trabajo correspondiente.

El proyecto busca organizar esta información en un sistema centralizado.

## 3. Objetivo general

Desarrollar un sistema web para las dos sedes de Serna Polarizados en Ibagué que permita gestionar clientes, vehículos, trabajos realizados e inventario de materiales por sede.

## 4. Objetivos específicos

- Centralizar el registro de clientes y sus vehículos.
- Registrar los trabajos realizados, asociados a un vehículo y una sede.
- Permitir la consulta del historial de trabajos desde ambas sedes.
- Registrar entradas y consumos de materiales en el inventario de cada sede.
- Relacionar el consumo de materiales con los trabajos realizados.
- Documentar y revisar el uso de IA durante las fases del proyecto.

## 5. Alcance de la primera versión

La primera versión, o MVP, es el conjunto de funciones que el equipo se propone construir y demostrar durante el semestre.

### Clientes y vehículos

- Registrar clientes con nombre, documento y contacto.
- Registrar los vehículos de cada cliente, incluyendo su descripción y placa.
- Asociar varios vehículos a un mismo cliente.
- Consultar clientes y vehículos mediante documento o placa.

### Trabajos realizados

- Registrar la fecha, sede, vehículo, descripción del servicio y valor total del trabajo.
- Asociar los materiales consumidos con el trabajo correspondiente.
- Consultar el historial de trabajos de cada vehículo desde cualquiera de las dos sedes.

El registro del valor total del trabajo no incluye la gestión de pagos ni la emisión de facturas.

### Inventario por sede

- Registrar los materiales y su unidad de medida.
- Registrar entradas de materiales.
- Registrar consumos relacionados con los trabajos.
- Consultar las existencias de cada material por sede.
- Conservar el historial de entradas y consumos.

Las unidades y las reglas de medición se detallarán durante el análisis de requisitos.

## 6. Reglas de funcionamiento acordadas

- El alcance inicial comprende únicamente las dos sedes de Ibagué.
- La información de clientes, vehículos e historial de trabajos será compartida entre las dos sedes.
- Cada sede tendrá existencias de materiales independientes.
- Cada trabajo quedará asociado a la sede donde se realizó.
- El consumo de materiales de un trabajo afectará únicamente al inventario de esa sede.
- Un cliente podrá tener varios vehículos.
- Cada trabajo quedará relacionado con el vehículo atendido.

Compartir información entre sedes no significa publicarla para cualquier persona. Los permisos de consulta y modificación se definirán durante el análisis.

## 7. Fuera del alcance inicial

El planteamiento general del negocio contempla otras funciones que no forman parte de esta primera versión:

- Agenda de citas, reprogramaciones y control de no asistencia.
- Registro autónomo de clientes mediante código QR.
- Gestión de pagos, abonos y medios de pago.
- Facturación electrónica e integración con Siigo.
- Gestión de gastos e informes financieros.
- Gestión de proveedores y órdenes de compra.
- Alertas automáticas de inventario.
- Operación en sedes adicionales.

Estas funciones podrán evaluarse después. Su presencia en la visión general del negocio no implica un compromiso de implementación durante este alcance.

## 8. Personas relacionadas con el sistema

Los perfiles identificados en el planteamiento del negocio son:

- **Administrador:** supervisa la operación y el inventario.
- **Asesor:** registra y consulta información de clientes, vehículos y trabajos.
- **Instalador:** realiza los trabajos y aporta información sobre los materiales utilizados.
- **Cliente:** proporciona sus datos y los de su vehículo.

La distribución de funciones y los permisos de acceso se precisarán en las historias de usuario. No se incluye un portal de autoservicio para clientes en la primera versión.

## 9. Flujo principal previsto

1. Buscar al cliente y su vehículo.
2. Registrar sus datos si todavía no existen.
3. Registrar el trabajo y la sede donde se realiza.
4. Registrar los materiales consumidos en ese trabajo.
5. Descontar el consumo del inventario de la sede correspondiente.
6. Consultar el trabajo en el historial del vehículo desde cualquiera de las dos sedes.

## 10. Demostración prevista del MVP

Con datos ficticios, el equipo buscará demostrar este recorrido:

1. Registrar un cliente y su vehículo.
2. Registrar existencias de un material en una sede.
3. Registrar un trabajo para el vehículo en esa sede.
4. Asociar el consumo del material al trabajo.
5. Comprobar la disminución de existencias en esa sede.
6. Consultar el historial del vehículo desde la otra sede y comprobar que su inventario no cambió.

Este recorrido servirá para mantener el alcance concreto y preparar una demostración breve del proyecto.

## 11. Tecnologías elegidas

- **Lenguaje del backend:** Python.
- **Framework del backend:** Flask.
- **Frontend:** HTML, CSS y JavaScript.
- **Base de datos:** SQLite.
- **Control de versiones:** Git.
- **Repositorio compartido:** GitHub.
- **Diagramas:** Mermaid.

### Justificación

El equipo ha utilizado Flask y SQLite en actividades académicas y tiene mayor familiaridad con HTML, CSS y JavaScript.

Flask y SQLite aparecen como ejemplo en la sesión 2. La elección del frontend corresponde a los conocimientos previos del equipo y al alcance sencillo del proyecto.

## 12. Arquitectura prevista

Se utilizará un **monolito en capas**, la arquitectura recomendada por defecto en la sesión 4.

La aplicación se organizará en:

- **Presentación:** pantallas, formularios y respuestas que recibe el usuario.
- **Negocio:** reglas para gestionar clientes, vehículos, trabajos y materiales.
- **Datos:** operaciones para guardar y consultar información en SQLite.

Por ejemplo, al registrar un consumo, la pantalla recibirá los datos, la capa de negocio comprobará las reglas y la capa de datos guardará el movimiento.

Las capas formarán parte de una misma aplicación. Los componentes y diagramas detallados se elaborarán a partir de las historias de usuario.

## 13. Equipo de trabajo

- [Tu nombre completo]
- Jonathan [completar apellidos]

La asignación de los roles de producto, backend y frontend/pruebas está pendiente de acuerdo entre los integrantes.

Ambos participaremos en:

- Revisión del alcance y los requisitos.
- Validación del diseño.
- Revisión y comprensión del código.
- Pruebas del sistema.
- Documentación del uso de IA.
- Preparación de la sustentación.

## 14. Uso de inteligencia artificial

La IA se utilizará para apoyar la planeación, el análisis, el diseño y, posteriormente, la implementación, las pruebas, el despliegue y el mantenimiento.

El equipo revisará y corregirá las propuestas antes de incorporarlas al proyecto. Se registrarán los prompts utilizados, los resultados relevantes y las correcciones realizadas.

La matriz de uso previsto se encuentra en:

[Consultar matriz de uso de IA](docs/ia/matriz-ia.md)

## 15. Estado de la documentación

Actualmente el repositorio contiene:

- Este README con la descripción, el alcance y las decisiones iniciales.
- La matriz de uso previsto de IA.

El trabajo pendiente de las sesiones 1 a 4 incluye:

- Acordar los roles del equipo.
- Completar la visión y el análisis competitivo.
- Construir la biblioteca de al menos cinco prompts probados y comentados.
- Definir entre 12 y 15 historias de usuario y priorizarlas.
- Escribir criterios de aceptación para todas las historias Must.
- Relacionar las historias con las necesidades que les dieron origen.
- Elaborar y revisar los diagramas de componentes por capas, clases, casos de uso y secuencia.
- Mantener actualizada la bitácora de IA.

Este README presenta el proyecto y su alcance; no sustituye los entregables de requisitos y diseño.
