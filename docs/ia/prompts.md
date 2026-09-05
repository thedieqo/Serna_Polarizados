# Biblioteca de prompts — Serna Polarizados

Este documento registra instrucciones probadas con IA, sus resultados y las observaciones de revisión.

La sesión 2 solicita al menos cinco prompts probados y comentados. Actualmente se registra una prueba.

## P-01 — Revisar el alcance del proyecto

### Datos de la prueba

- Fecha: 5 de septiembre de 2026.
- Herramienta: Codex.
- Propósito: separar reglas confirmadas de decisiones pendientes.
- Estado: ejecutado; revisión conjunta del equipo pendiente.

### Prompt utilizado

Actúa como analista de requisitos de un proyecto académico pequeño.

CONTEXTO:
Somos dos estudiantes y estamos en la semana 4. Nuestro proyecto es un sistema web para las dos sedes de Serna Polarizados en Ibagué. Ambas sedes comparten información de clientes, vehículos e historial de trabajos, pero cada una tiene su propio inventario.

La primera versión incluye registrar clientes y vehículos, registrar trabajos con fecha, sede, servicio y valor total, consultar el historial y registrar entradas y consumos de materiales por sede. Los consumos deben relacionarse con un trabajo.

TAREA:
Revisa este alcance e identifica cinco reglas de funcionamiento que ya estén confirmadas y tres decisiones que todavía debamos precisar antes de diseñar el sistema.

FORMATO:
Dos listas numeradas: “Reglas confirmadas” y “Decisiones pendientes”. Explica cada punto en una frase sencilla.

RESTRICCIONES:
No generes código. No agregues pagos, facturación, agenda, QR ni nuevas sedes. No presentes propuestas tuyas como decisiones del negocio. No inventes unidades de medida ni permisos de los usuarios.

EJEMPLO:
Regla confirmada: el consumo de un trabajo se descuenta únicamente del inventario de la sede donde se realizó.
Decisión pendiente: definir cómo se corrige un consumo registrado por error.

### Respuesta obtenida

Reglas confirmadas:

1. El sistema cubrirá únicamente las dos sedes de Serna Polarizados en Ibagué.
2. Ambas sedes compartirán la información de clientes, vehículos e historial de trabajos.
3. Cada sede mantendrá su propio inventario de materiales.
4. Cada trabajo estará asociado a un vehículo y registrará fecha, sede, servicio y valor total.
5. Cada consumo estará relacionado con un trabajo y se descontará únicamente del inventario de la sede donde se realizó.

Decisiones pendientes:

1. Definir las unidades de medida de los materiales y cómo registrar cantidades fraccionarias.
2. Determinar qué usuarios podrán consultar, registrar y modificar cada tipo de información.
3. Definir cómo corregir un consumo registrado por error y ajustar las existencias correspondientes.

### Observaciones de revisión asistida

Qué funcionó:

- Entregó cinco reglas y tres decisiones pendientes.
- Utilizó frases sencillas.
- Conservó el alcance de dos sedes.
- Distinguió la información compartida del inventario independiente.
- No generó código ni incorporó módulos excluidos.

Limitaciones:

- El prompt no expresa directamente la relación entre trabajo y vehículo, aunque esa relación sí está acordada en el README y en la conversación.
- Las cantidades fraccionarias se plantean para estudiar; todavía no son una regla aprobada del negocio.

Corrección propuesta para una próxima ejecución:

Agregar al contexto: “Cada trabajo pertenece a un vehículo y a la sede donde se realizó”. Esto permitirá reutilizar el prompt sin depender de la conversación anterior.

Esta mejora todavía no se ha ejecutado como una segunda prueba.

### Revisión humana pendiente

Los dos integrantes deben revisar estas observaciones y registrar si aceptan la respuesta o qué modifican. No se ha registrado todavía la revisión de Jonathan ni la evaluación por otro equipo.


## P-02 — Redactar la visión del proyecto

### Datos de la prueba

- Fecha: 5 de septiembre de 2026.
- Herramienta: Codex.
- Objetivo: obtener una visión breve del proyecto.
- Estado: ejecutado; revisión conjunta del equipo pendiente.

### Prompt utilizado

Actúa como analista de software que ayuda a dos estudiantes a redactar la visión de un proyecto académico pequeño.

CONTEXTO:
El proyecto es un sistema web para las dos sedes de Serna Polarizados en Ibagué. Actualmente el negocio utiliza registros manuales y archivos de Excel.

La primera versión incluye clientes, vehículos, trabajos realizados e inventario. Ambas sedes comparten la información de clientes, vehículos e historial de trabajos, pero cada una maneja su propio inventario.

Un cliente puede tener varios vehículos. Cada trabajo pertenece a un vehículo y a la sede donde se realizó, y registra fecha, servicio y valor total. Cada consumo de materiales se relaciona con un trabajo y se descuenta únicamente del inventario de esa sede.

Las personas involucradas son administrador, asesor, instalador y cliente. Los permisos todavía no están definidos y el cliente no tendrá un portal de autoservicio.

TAREA:
Redacta un borrador breve de la visión del proyecto que explique el problema, las personas involucradas, la propuesta de valor y el alcance de la primera versión.

FORMATO:
Utiliza cinco apartados: Problema, Personas involucradas, Propuesta de valor, Alcance del MVP y Exclusiones. Máximo 300 palabras en total.

RESTRICCIONES:
No generes código ni historias de usuario. No inventes estadísticas, beneficios medidos ni permisos. No incluyas pagos, facturación, Siigo, agenda, QR, proveedores, alertas automáticas ni sedes adicionales dentro del MVP. Distingue el registro del valor de un trabajo de la gestión de su pago.

EJEMPLO:
Propuesta de valor: consultar el historial de un vehículo desde cualquiera de las dos sedes y mantener separado el inventario de cada una.

### Respuesta obtenida

#### Problema

Serna Polarizados utiliza registros manuales y archivos de Excel. El proyecto busca organizar la información de clientes, vehículos, trabajos y materiales para facilitar su consulta entre las dos sedes de Ibagué.

#### Personas involucradas

Administrador, asesor, instalador y cliente. Sus permisos y responsabilidades dentro del sistema están pendientes de definición. El cliente proporciona información, pero no tendrá un portal de autoservicio en la primera versión.

#### Propuesta de valor

Centralizar la información de clientes, vehículos e historial de trabajos para consultarla desde ambas sedes, manteniendo un inventario independiente por sede y relacionando los materiales consumidos con cada trabajo.

#### Alcance del MVP

- Registrar clientes y asociar varios vehículos a un mismo cliente.
- Registrar trabajos vinculados a un vehículo y una sede, indicando fecha, servicio y valor total.
- Consultar el historial de trabajos desde ambas sedes.
- Registrar materiales, entradas, consumos y existencias por sede.
- Asociar cada consumo con un trabajo y descontarlo únicamente del inventario de la sede donde se realizó.

El valor total describe el importe del trabajo; registrarlo no incluye gestionar ni comprobar su pago.

#### Exclusiones

La primera versión no incluye gestión de pagos, facturación, integración con Siigo, agenda de citas, registro mediante QR, gestión de proveedores, alertas automáticas ni sedes adicionales.

Las unidades de medida de los materiales y los permisos de los usuarios se precisarán durante el análisis de requisitos.

### Comentarios de revisión asistida

- La respuesta incluyó los cinco apartados solicitados y no superó las 300 palabras.
- Conservó el alcance de dos sedes con inventarios separados.
- Distinguió registrar el valor del trabajo de gestionar su pago.
- No inventó permisos ni resultados medidos.
- Incluyó entradas y existencias, acordadas anteriormente pero no detalladas en este prompt.

### Mejora propuesta

Añadir al contexto: “El inventario incluye registrar materiales, entradas, consumos y consultar existencias”.

Esta mejora haría el prompt más preciso. Todavía no se ha probado esa nueva versión.

### Revisión humana pendiente

Los dos integrantes deben leer el resultado y registrar sus observaciones. Los comentarios anteriores fueron preparados con apoyo de IA y no equivalen a la revisión de Jonathan.
