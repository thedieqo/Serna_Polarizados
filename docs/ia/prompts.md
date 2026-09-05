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
