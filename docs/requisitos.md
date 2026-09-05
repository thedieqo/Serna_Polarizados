# Requisitos — Serna Polarizados

## Estado del documento

Borrador de historias de usuario revisado con un integrante del equipo el 5 de septiembre de 2026.

Contiene 12 historias aceptadas. Están pendientes la revisión con Jonathan, la priorización MoSCoW y los criterios de aceptación Gherkin.

## Alcance

Sistema para las dos sedes de Serna Polarizados en Ibagué.

Las sedes comparten información de clientes, vehículos e historial de trabajos. Cada sede mantiene su propio inventario.

La primera versión incluye clientes, vehículos, trabajos y materiales. No incluye pagos, facturación, agenda, QR ni informes financieros.

## Perfiles y decisiones confirmadas

- Asesor y administrador: podrán registrar y consultar la información del alcance acordado.
- Instalador: utilizará la plataforma para registrar los materiales y cantidades consumidos en los trabajos.
- Administrador: podrá corregir consumos registrados por error, dejando constancia del ajuste.

La información compartida entre sedes no será de acceso público.

## Historias de usuario

### HU-01 — Registrar cliente

Como asesor, quiero registrar un cliente con nombre, documento y contacto para disponer de sus datos al atenderlo.

### HU-02 — Consultar cliente

Como asesor, quiero consultar un cliente por su documento para recuperar sus datos y evitar registrarlo nuevamente.

### HU-03 — Registrar vehículo

Como asesor, quiero registrar un vehículo y asociarlo a un cliente para identificar a quién pertenece.

### HU-04 — Consultar vehículo

Como asesor, quiero consultar un vehículo por su placa para identificar al cliente asociado antes de registrar un trabajo.

### HU-05 — Registrar trabajo

Como asesor, quiero registrar un trabajo con vehículo, sede, fecha, servicio y valor total para dejar constancia de la atención realizada.

El valor total representa el importe del trabajo. No incluye registrar pagos ni comprobar si el cliente pagó.

### HU-06 — Consultar historial del vehículo

Como asesor, quiero consultar el historial de trabajos de un vehículo desde cualquiera de las dos sedes para conocer sus atenciones anteriores.

### HU-08 — Registrar material

Como administrador, quiero registrar los materiales indicando su unidad de medida para identificar qué existencias se controlarán.

### HU-09 — Registrar entrada de material

Como administrador, quiero registrar una entrada de material en una sede para actualizar sus existencias.

### HU-10 — Registrar consumo de material

Como instalador, quiero registrar el material y la cantidad consumidos en un trabajo para descontarlos únicamente del inventario de la sede donde se realizó.

### HU-11 — Consultar existencias

Como administrador, quiero consultar las existencias de materiales por sede para conocer cuánto hay disponible en cada una.

### HU-12 — Consultar materiales de un trabajo

Como administrador, quiero consultar los materiales y cantidades consumidos en un trabajo para revisar el uso de inventario asociado a esa atención.

### HU-13 — Corregir consumo de material

Como administrador, quiero corregir un consumo de material registrado por error, dejando constancia del ajuste, para que las existencias de la sede reflejen el consumo real.

## Historia descartada

### HU-07 — Consultar trabajos por sede y periodo

Se propuso consultar los trabajos de una sede durante un periodo.

Fue descartada durante la revisión porque no es necesaria para la primera versión.

Se conserva su identificador en este registro para explicar el cambio. No cuenta entre las 12 historias aceptadas.

## Decisiones pendientes

- Definir las unidades de medida y la precisión de cantidades para cada material, con información del instalador.
- Precisar los campos obligatorios y las validaciones.
- Detallar cómo se registrarán los ajustes de consumos.
- Priorizar las historias mediante MoSCoW.
- Escribir criterios de aceptación Gherkin para todas las historias Must.

## Registro de revisión del resultado de IA

La IA propuso inicialmente 12 historias.

Durante la revisión, un integrante del equipo:

- Aceptó las historias excepto HU-07.
- Descartó la consulta de trabajos por sede y periodo.
- Confirmó la participación del asesor, administrador e instalador.
- Indicó que el instalador aporta los datos del material utilizado.
- Aceptó HU-13 y confirmó que el administrador debe poder corregir consumos.

Resultado: 12 historias aceptadas y una descartada.

La revisión con Jonathan y la evaluación por otro equipo siguen pendientes.
