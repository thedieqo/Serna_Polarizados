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


## Priorización MoSCoW revisada

Un integrante del equipo aprobó la siguiente clasificación el 5 de septiembre de 2026. La revisión con Jonathan sigue pendiente.

### Must — Indispensables

- HU-01: registrar cliente.
- HU-02: consultar cliente por documento.
- HU-03: registrar vehículo asociado a un cliente.
- HU-04: consultar vehículo por placa.
- HU-05: registrar trabajo.
- HU-06: consultar historial del vehículo desde ambas sedes.
- HU-08: registrar material y unidad de medida.
- HU-09: registrar entrada de material por sede.
- HU-10: registrar consumo y descontarlo de la sede correspondiente.
- HU-11: consultar existencias por sede.
- HU-13: corregir consumos erróneos dejando constancia del ajuste.

Estas funciones permiten registrar y recuperar la información, completar el flujo principal, comprobar las existencias y corregir errores de consumo.

### Should — Importante, después de las indispensables

- HU-12: consultar materiales y cantidades consumidos en un trabajo.

Puede aplazarse esta consulta detallada. La relación entre el consumo y el trabajo debe guardarse desde el principio mediante HU-10.

### Could — Opcionales

No se asignaron historias a esta categoría.

### Won’t — Fuera de esta versión

- HU-07: consultar trabajos por sede y periodo.

Esta historia permanece descartada.

### Cambios frente a la propuesta inicial de IA

HU-02, HU-04 y HU-13 pasaron de Should a Must, con aprobación del usuario.

Esta clasificación sustituye la propuesta inicial de P-05. El registro de esa prueba se conserva como evidencia del proceso.

### Siguiente actividad

Escribir criterios de aceptación en formato Dado–Cuando–Entonces para las once historias Must.


## Criterios de aceptación — Borrador para revisión

Estos escenarios cubren las once historias Must.

Los comportamientos ya acordados se traducen en resultados comprobables. Las validaciones adicionales indicadas al final son propuestas pendientes de aprobación del equipo.

Los ejemplos usarán datos ficticios.

### HU-01 — Registrar cliente

Escenario: registrar un cliente

Dado que el asesor dispone del nombre, documento y contacto de un cliente que no está registrado,
Cuando guarda esos datos,
Entonces el cliente queda registrado y disponible para consulta.

### HU-02 — Consultar cliente por documento

Escenario: encontrar un cliente registrado

Dado que existe un cliente registrado con un documento,
Cuando el asesor consulta ese documento,
Entonces el sistema muestra los datos del cliente correspondiente.

Escenario: consultar un documento sin coincidencias

Dado que no existe un cliente con el documento consultado,
Cuando el asesor realiza la búsqueda,
Entonces el sistema informa que no se encontró un cliente.

### HU-03 — Registrar vehículo

Escenario: asociar un vehículo a un cliente

Dado que existe un cliente registrado,
Cuando el asesor registra la descripción y placa de un vehículo y lo asocia al cliente,
Entonces el vehículo queda registrado con esa asociación.

Escenario: registrar otro vehículo del mismo cliente

Dado que un cliente ya tiene un vehículo registrado,
Cuando el asesor registra otro vehículo para ese cliente,
Entonces ambos vehículos permanecen asociados al cliente.

### HU-04 — Consultar vehículo por placa

Escenario: encontrar un vehículo

Dado que existe un vehículo registrado con una placa,
Cuando el asesor busca esa placa,
Entonces el sistema muestra el vehículo y el cliente asociado.

Escenario: consultar una placa sin coincidencias

Dado que no existe un vehículo con la placa consultada,
Cuando el asesor realiza la búsqueda,
Entonces el sistema informa que no se encontró el vehículo.

### HU-05 — Registrar trabajo

Escenario: guardar un trabajo

Dado que existe un vehículo registrado,
Cuando el asesor registra para ese vehículo la sede, fecha, servicio y valor total de un trabajo,
Entonces el trabajo queda asociado al vehículo y a la sede seleccionada,
Y queda disponible en el historial del vehículo.

### HU-06 — Consultar historial desde ambas sedes

Escenario: consultar un trabajo realizado en la otra sede

Dado que un vehículo tiene un trabajo registrado en la sede A,
Cuando el asesor consulta el historial de ese vehículo desde la sede B,
Entonces puede consultar ese trabajo e identificar que fue realizado en la sede A.

Escenario: consultar un vehículo sin trabajos

Dado que un vehículo está registrado pero no tiene trabajos,
Cuando el asesor consulta su historial,
Entonces el sistema indica que no hay trabajos registrados para ese vehículo.

### HU-08 — Registrar material

Escenario: registrar un material con su unidad

Dado que el administrador conoce el nombre y la unidad de medida acordada para un material,
Cuando registra el material,
Entonces queda disponible para registrar entradas y consumos,
Y su unidad de medida puede consultarse.

Las unidades específicas están pendientes de definición con el instalador.

### HU-09 — Registrar entrada por sede

Escenario: aumentar existencias en una sola sede

Dado que un material está registrado y tiene existencias conocidas en ambas sedes,
Cuando el administrador registra una entrada de cantidad positiva en la sede A,
Entonces las existencias de la sede A aumentan en esa cantidad,
Y las existencias de la sede B no cambian,
Y queda registrado el movimiento de entrada.

### HU-10 — Registrar consumo por trabajo

Escenario: descontar material de la sede del trabajo

Dado que existe un trabajo de la sede A y hay material suficiente en esa sede,
Cuando el instalador registra el material y la cantidad consumida en el trabajo,
Entonces el consumo queda asociado al trabajo,
Y las existencias de la sede A disminuyen en esa cantidad,
Y las existencias de la sede B no cambian.

Escenario propuesto: impedir un consumo superior a las existencias

Dado que la cantidad solicitada supera las existencias del material en la sede del trabajo,
Cuando el instalador intenta registrar el consumo,
Entonces el sistema informa que no hay existencias suficientes,
Y no registra el consumo ni modifica el inventario.

### HU-11 — Consultar existencias por sede

Escenario: distinguir existencias de ambas sedes

Dado que un material tiene cantidades diferentes en las dos sedes,
Cuando el administrador consulta sus existencias por sede,
Entonces el sistema muestra la cantidad correspondiente a cada sede y su unidad de medida.

### HU-13 — Corregir consumo

Escenario: disminuir una cantidad consumida por error

Dado que un consumo registrado para un trabajo de la sede A tiene una cantidad incorrecta,
Cuando el administrador corrige esa cantidad por una menor,
Entonces las existencias de la sede A aumentan por la diferencia,
Y las existencias de la sede B no cambian,
Y queda constancia del ajuste relacionado con el consumo.

Escenario: aumentar una cantidad consumida por error

Dado que un consumo registrado para un trabajo de la sede A debe corregirse por una cantidad mayor,
Y hay existencias suficientes para cubrir la diferencia,
Cuando el administrador confirma la corrección,
Entonces las existencias de la sede A disminuyen por la diferencia,
Y las existencias de la sede B no cambian,
Y queda constancia del ajuste relacionado con el consumo.

### Validaciones propuestas pendientes de aprobación

Estas reglas todavía deben ser revisadas por el equipo:

- No permitir documentos de clientes duplicados.
- No permitir placas de vehículos duplicadas.
- Exigir cantidades positivas en entradas y consumos.
- Impedir consumos que superen las existencias de la sede.
- Aplicar el mismo control de existencias al aumentar un consumo mediante una corrección.
- Guardar en cada ajuste quién lo realizó, cuándo, el motivo y las cantidades anterior y nueva.

### Pendientes de estos criterios

- Confirmar las validaciones propuestas.
- Definir las unidades y precisión de cantidades con el instalador.
- Precisar cómo tratar correcciones de material equivocado o anulación completa de un consumo.
- Revisar los escenarios con Jonathan.
- Actualizar el estado inicial del documento después de aprobar esta revisión.
