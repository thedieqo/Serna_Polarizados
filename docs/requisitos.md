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

- ## Actualización de revisión — 5 de septiembre de 2026

Un integrante del equipo aprobó las seis validaciones propuestas:

1. No permitir documentos de clientes duplicados.
2. No permitir placas de vehículos duplicadas.
3. Exigir cantidades mayores que cero en entradas y consumos.
4. Impedir consumos superiores a las existencias de la sede.
5. Comprobar existencias suficientes cuando una corrección aumenta el consumo.
6. Registrar quién realizó cada ajuste, cuándo, el motivo y las cantidades anterior y nueva.

Esta aprobación sustituye el estado pendiente de esas seis validaciones en las secciones anteriores.

### Escenarios adicionales de las validaciones aprobadas

#### HU-01 — Documento duplicado

Dado que existe un cliente con un documento registrado,
Cuando el asesor intenta registrar otro cliente con ese mismo documento,
Entonces el sistema informa que el documento ya existe,
Y no crea un segundo cliente.

#### HU-03 — Placa duplicada

Dado que existe un vehículo con una placa registrada,
Cuando el asesor intenta registrar otro vehículo con esa misma placa,
Entonces el sistema informa que la placa ya existe,
Y no crea un segundo vehículo.

#### HU-09 — Cantidad de entrada inválida

Dado que el administrador está registrando una entrada,
Cuando introduce una cantidad igual o menor que cero,
Entonces el sistema rechaza la entrada,
Y las existencias permanecen sin cambios.

#### HU-10 — Cantidad de consumo inválida

Dado que el instalador está registrando un consumo,
Cuando introduce una cantidad igual o menor que cero,
Entonces el sistema rechaza el consumo,
Y las existencias permanecen sin cambios.

#### HU-13 — Corrección sin existencias suficientes

Dado que un consumo debe aumentarse,
Y la diferencia supera las existencias disponibles en la sede del trabajo,
Cuando el administrador intenta confirmar la corrección,
Entonces el sistema rechaza el ajuste,
Y conserva el consumo y las existencias anteriores.

#### HU-13 — Constancia de la corrección

Dado que el administrador realiza una corrección válida e indica su motivo,
Cuando confirma el ajuste,
Entonces quedan registrados el consumo afectado, el administrador, la fecha y hora, el motivo y las cantidades anterior y nueva.

### Pendientes que continúan abiertos

- Revisar los documentos con Jonathan.
- Definir las unidades y precisión de cantidades con el instalador.
- Precisar cómo corregir un material equivocado o anular completamente un consumo.
- Detallar el mecanismo de identificación de los usuarios para aplicar permisos y registrar quién realiza los ajustes.

- ## Actualización del inventario — 8 de septiembre de 2026

### Situación actual confirmada

Según el administrador de una sede:

- Actualmente no se registran de forma sistemática las entradas, los cortes ni los sobrantes.
- Los rollos pueden tener distintos anchos.
- Los sobrantes normalmente se guardan para otros trabajos.
- Algunos sobrantes se dañan y deben desecharse.
- Los instaladores pueden medir y registrar los sobrantes aprovechables.
- El ancho y el largo se registrarán en centímetros.

### Ajustes propuestos al sistema

- Identificar cada rollo recibido por sede, tecnología, opacidad y dimensiones.
- Identificar la pieza de material utilizada en cada trabajo.
- Registrar los recortes aprovechables y sus dimensiones.
- Relacionar cada recorte con el material del que proviene.
- Registrar el descarte de material dañado y su motivo.
- Mostrar las dimensiones de las piezas disponibles, sin reducir la disponibilidad a una cantidad total de metros.

Estas funciones son una propuesta de diseño para responder a los hallazgos. El flujo exacto de cortes, recortes y descartes debe validarse antes de implementarlo.

### Regla de consistencia propuesta

El material debe contabilizarse una sola vez.

Al registrar un corte, se debe actualizar la pieza de origen y registrar lo utilizado, los sobrantes aprovechables y el desperdicio correspondiente, sin duplicar existencias.

### Pendientes de diseño

- Definir la precisión de las medidas en centímetros.
- Acordar cómo medir recortes irregulares.
- Definir quién puede registrar y autorizar descartes.
- Adaptar las correcciones de consumo para conservar también la consistencia de las piezas y sus dimensiones.
- Revisar las historias y criterios anteriores que trataban el inventario únicamente como cantidades acumuladas.

- ## Revisión propuesta de historias de inventario

Fecha: 8 de septiembre de 2026.

Esta propuesta utiliza las aclaraciones del administrador: los rollos tienen anchos diferentes, se conservan sobrantes y los instaladores pueden medirlos en centímetros.

Las siguientes versiones están pendientes de aprobación. Cuando se aprueben, sustituirán las versiones anteriores de estas historias.

### HU-08 — Registrar tipo de material

Como administrador, quiero registrar los tipos de material distinguiendo tecnología y opacidad para identificar correctamente los rollos y recortes disponibles.

### HU-09 — Registrar rollo recibido

Como administrador, quiero registrar cada rollo recibido con su sede, tipo de material, ancho y largo en centímetros para conocer el material que ingresa a esa sede.

### HU-10 — Registrar uso de material y sobrantes

Como instalador, quiero identificar la pieza utilizada en un trabajo y registrar el material utilizado y los sobrantes aprovechables para mantener actualizado el inventario de la sede del trabajo sin contar material dos veces.

Una pieza puede ser un rollo o un recorte disponible.

El mecanismo exacto para registrar cortes y calcular el material restante está pendiente de diseño.

### HU-11 — Consultar material disponible

Como administrador, quiero consultar los rollos y recortes disponibles por sede, tecnología, opacidad y dimensiones para conocer las piezas que pueden utilizarse.

### HU-12 — Consultar material utilizado en un trabajo

Como administrador, quiero consultar las piezas de origen y el material utilizado en un trabajo para revisar su relación con los movimientos de inventario.

### HU-13 — Corregir un registro de uso

Como administrador, quiero corregir un registro de uso de material dejando constancia del motivo y de los datos anteriores y nuevos para mantener un inventario consistente.

Si el sobrante afectado ya se utilizó en otro trabajo, la forma de corregirlo debe definirse antes de implementar esta función.

### HU-14 — Registrar material dañado

Como administrador, quiero registrar el descarte de una pieza dañada indicando el motivo para que deje de aparecer como disponible.

Esta historia propone que el administrador registre el descarte. Ese permiso está pendiente de aprobación.

La gestión de daños parciales dentro de una pieza queda pendiente de definición.

## Efecto sobre las versiones anteriores

- Las reglas de documentos y placas únicos permanecen vigentes.
- La información de clientes, vehículos e historial sigue compartida entre las dos sedes.
- El inventario sigue separado por sede.
- Las medidas de ancho y largo se expresan en centímetros.
- Las correcciones deben conservar su autor, fecha, motivo y datos anteriores y nuevos.
- El registro de uso y su efecto en inventario deben guardarse juntos o no aplicarse.

Los criterios anteriores que calculaban todo el inventario mediante una única cantidad ya no son suficientes. Deberán revisarse para contemplar piezas, dimensiones y sobrantes.

No se asignan todavía prioridades definitivas a esta revisión.

## Estado

Borrador de ajuste pendiente de aprobación y de revisión con Jonathan.

Con HU-14, el conjunto tendría 13 historias activas. HU-07 continúa descartada.


## Aprobación del ajuste de inventario — 8 de septiembre de 2026

El administrador de una sede, participante en el proyecto, aprobó las versiones revisadas de HU-08 a HU-13 y la nueva HU-14.

Estas versiones sustituyen las descripciones anteriores de esas historias.

Se confirmó que el administrador registrará el descarte de piezas dañadas.

La revisión con Jonathan sigue pendiente. Esta aprobación no implica que las funciones estén implementadas o probadas.

## Criterios de aceptación revisados — Inventario

Estado: borrador para revisión.

### HU-08 — Registrar tipo de material

Dado que el administrador dispone de la tecnología y opacidad de un material,
Cuando registra ese tipo de material,
Entonces queda disponible para identificar los rollos y recortes correspondientes.

### HU-09 — Registrar rollo recibido

Dado que existe un tipo de material registrado,
Cuando el administrador registra un rollo indicando sede, material, ancho y largo positivos en centímetros,
Entonces el rollo queda identificado y disponible en esa sede,
Y no se incrementa el inventario de la otra sede.

Escenario: dimensiones inválidas

Dado que el administrador está registrando un rollo,
Cuando introduce un ancho o largo igual o menor que cero,
Entonces el sistema rechaza el registro,
Y no modifica las existencias.

### HU-10 — Registrar uso de material y sobrantes

Dado que existe un trabajo y una pieza disponible en la misma sede,
Cuando el instalador registra el uso de material y los sobrantes aprovechables conforme a las reglas de corte que se definan,
Entonces el uso queda relacionado con el trabajo y la pieza de origen,
Y los sobrantes quedan identificados con su material, sede y dimensiones,
Y la disponibilidad de la pieza de origen se actualiza sin duplicar el material,
Y el inventario de la otra sede no cambia.

Escenario: pieza de otra sede

Dado que una pieza pertenece a una sede diferente de la del trabajo,
Cuando se intenta utilizarla en ese trabajo,
Entonces el sistema rechaza la operación,
Y no modifica ninguna de las dos existencias.

Escenario: fallo al guardar

Dado que se está registrando el uso de una pieza,
Cuando falla el guardado de alguno de los cambios asociados,
Entonces no queda aplicado parcialmente el consumo, la actualización de origen ni el registro de sobrantes.

Los casos de corte y validación de dimensiones requieren definir primero cómo se registrarán las piezas rectangulares y los recortes irregulares. Este criterio todavía no es suficiente para implementar toda la función.

### HU-11 — Consultar material disponible

Dado que existen rollos y recortes disponibles en las dos sedes,
Cuando el administrador consulta el material de una sede,
Entonces puede distinguir cada pieza por su identificación, tecnología, opacidad, ancho y largo,
Y las piezas descartadas no aparecen como disponibles.

### HU-12 — Consultar material utilizado en un trabajo

Dado que un trabajo tiene usos de material registrados,
Cuando el administrador consulta su detalle,
Entonces puede identificar las piezas de origen y los registros de uso asociados a ese trabajo.

### HU-13 — Corregir registro de uso

Dado que el administrador selecciona un registro de uso que puede corregirse conforme a las reglas acordadas,
Cuando confirma una corrección válida e indica el motivo,
Entonces quedan conservados el autor, la fecha, el motivo y los datos anteriores y nuevos,
Y se actualiza el inventario afectado sin duplicar material,
Y los cambios se guardan juntos o no se aplica ninguno.

La corrección de un registro cuyo sobrante ya fue utilizado en otro trabajo sigue pendiente de diseño. No se considera resuelta por este escenario.

### HU-14 — Descartar pieza dañada

Dado que existe una pieza disponible en una sede,
Cuando el administrador registra su descarte e indica el motivo,
Entonces la pieza deja de aparecer como disponible,
Y se conserva la relación del descarte con esa pieza,
Y no cambia el inventario de la otra sede.

Este escenario cubre el descarte completo de una pieza. El tratamiento de daños parciales sigue pendiente.
