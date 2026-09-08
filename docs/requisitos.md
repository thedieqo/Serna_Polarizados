# Requisitos — Serna Polarizados

## 1. Estado y fuentes

**Fecha de actualización:** 8 de septiembre de 2026.  
**Estado:** versión de trabajo revisada con el administrador participante; revisión conjunta del equipo pendiente.

Este documento reúne el alcance, las reglas confirmadas, los requisitos funcionales y no funcionales, las historias de usuario y sus criterios de aceptación.

### Fuentes

- Entrevista con una asesora de Serna Polarizados.
- Aclaraciones y decisiones del administrador de una sede, integrante del proyecto.
- Borradores y revisión con Gemini.
- Organización y revisión asistida con Codex.

Las respuestas de IA son propuestas revisables. Las decisiones señaladas como confirmadas proceden de las aclaraciones del administrador participante.

La revisión conjunta con Jonathan y la validación posterior con la asesora siguen pendientes.

El documento contiene **13 historias activas**. HU-07 está descartada y conserva su identificador para mantener el registro de esa decisión.

Los criterios describen comprobaciones futuras. **No representan pruebas ejecutadas ni funcionalidades implementadas.**

## 2. Problema y alcance

La información de clientes, vehículos e instalaciones está distribuida entre registros manuales, archivos compartidos y llamadas. Los instaladores tienen dificultades para registrar información desde sus teléfonos. Tampoco existe un registro sistemático de entradas, cortes y sobrantes de material.

### Primera versión

El sistema cubrirá únicamente las dos sedes de Serna Polarizados en Ibagué e incluirá:

- Registro y consulta de clientes y vehículos.
- Registro de trabajos y detalles de instalación.
- Consulta compartida del historial de vehículos.
- Inventario independiente por sede.
- Identificación de rollos y recortes aprovechables.
- Registro del uso de material asociado a trabajos.
- Correcciones de registros de uso con constancia del ajuste.
- Descarte completo de piezas dañadas.

### Exclusiones

- Cálculo de comisiones y remuneraciones.
- Verificación o gestión de pagos.
- Facturación e integración con Siigo.
- Agenda de citas y registro por QR.
- Proveedores y compras.
- Alertas automáticas de inventario.
- Cotización de PPF.
- Módulo completo de garantías.
- Sedes adicionales, incluida Bogotá.
- Cálculo automático de cortes o representación de formas irregulares.

Registrar el valor de un trabajo no indica si fue pagado. El historial permite consultar antecedentes para atender garantías, pero no administra el proceso completo de garantía.

## 3. Perfiles

| Perfil | Responsabilidades confirmadas |
| --- | --- |
| Asesor | Registrar y consultar clientes, vehículos y trabajos. |
| Instalador | Registrar el uso de material y los sobrantes de sus operaciones. |
| Administrador | Registrar y consultar información, corregir registros de uso y registrar descartes de piezas dañadas. |

El cliente proporciona sus datos y los de su vehículo. No tendrá un portal de autoservicio en esta versión.

El mecanismo de identificación de usuarios y la matriz detallada de permisos siguen pendientes. Compartir información entre sedes no significa hacerla pública.

## 4. Reglas confirmadas

1. Un cliente puede tener varios vehículos.
2. No se permiten documentos de clientes ni placas duplicados.
3. Cada trabajo pertenece a un vehículo y a una sede.
4. Clientes, vehículos e historial se comparten entre las dos sedes.
5. Cada pieza de inventario pertenece a una sede.
6. El uso de material se relaciona con un trabajo y con una pieza de origen.
7. La pieza utilizada debe pertenecer a la sede del trabajo.
8. Las dimensiones se registran en centímetros y deben ser positivas.
9. No se puede utilizar más material del disponible.
10. Los sobrantes se representan mediante rectángulos aprovechables medidos por el instalador.
11. El material registrado como sobrante no puede seguir contado dentro de la pieza de origen.
12. Las correcciones del administrador conservan autor, fecha, motivo y datos anteriores y nuevos.
13. Una corrección que implique utilizar más material debe comprobar la disponibilidad.
14. El administrador puede registrar el descarte completo de una pieza dañada.
15. Las operaciones de inventario se guardan completas o no se aplican.
16. Una operación afecta únicamente al inventario de la sede correspondiente.

En este documento, **pieza** significa un rollo o un recorte identificado. La precisión de las medidas y el procedimiento exacto para registrar cortes y correcciones todavía deben definirse.

## 5. Requisitos funcionales

Los identificadores corresponden a esta versión. Sustituyen la numeración provisional de los borradores de Gemini.

| ID | Requisito | Origen principal |
| --- | --- | --- |
| RF-01 | Registrar clientes con nombre, documento y contacto, sin documentos duplicados. | Alcance y validaciones confirmadas. |
| RF-02 | Registrar vehículos con placa y descripción, asociados a un cliente, sin placas duplicadas. | Alcance y validaciones confirmadas. |
| RF-03 | Consultar clientes por documento y vehículos por placa. | Entrevista y alcance confirmado. |
| RF-04 | Registrar trabajos con vehículo, sede, fecha, servicio y valor total. | Alcance confirmado. |
| RF-05 | Registrar detalles de instalación: tecnología, opacidad, instalador y datos aplicables de retiro de película. | Entrevista y alcance confirmado; estructura detallada pendiente. |
| RF-06 | Consultar el historial del vehículo desde ambas sedes, incluyendo los detalles registrados de cada trabajo. | Entrevista y decisión confirmada. |
| RF-07 | Registrar tipos de material diferenciando tecnología y opacidad. | Entrevista y revisión del inventario. |
| RF-08 | Registrar cada rollo recibido con identificación, sede, tipo de material, ancho y largo en centímetros. | Revisión aprobada del inventario. |
| RF-09 | Registrar el uso de material asociado a un trabajo y una pieza de su misma sede. | Alcance y revisión aprobada. |
| RF-10 | Registrar sobrantes aprovechables con identificación, dimensiones y pieza de origen, evitando duplicar existencias. | Decisión confirmada sobre sobrantes. |
| RF-11 | Consultar rollos y recortes disponibles por sede, material y dimensiones. | Revisión aprobada del inventario. |
| RF-12 | Consultar las piezas y registros de uso asociados a un trabajo. | HU-12 aceptada. |
| RF-13 | Permitir al administrador corregir registros de uso conservando la consistencia del inventario y la constancia del ajuste. | Decisión confirmada; procedimiento y casos dependientes pendientes. |
| RF-14 | Permitir al administrador descartar una pieza completa dañada, indicando el motivo y retirándola de la disponibilidad. | HU-14 aprobada. |
| RF-15 | Mostrar confirmación de guardado únicamente cuando la operación se haya guardado correctamente. | Necesidad de registro fiable y diseño derivado. |
| RF-16 | Validar dimensiones positivas y disponibilidad de material antes de aplicar operaciones. | Validaciones aprobadas; procedimiento de cortes pendiente. |

## 6. Requisitos no funcionales

| ID | Necesidad | Comprobación propuesta | Estado |
| --- | --- | --- | --- |
| RNF-01 | El instalador debe poder completar su registro desde un teléfono. | Ejecutar el recorrido en el teléfono y navegador acordados, comprobando lectura, acceso a campos y ausencia de desplazamiento horizontal innecesario. | Necesidad confirmada; dispositivo y condiciones pendientes. |
| RNF-02 | El flujo debe ser comprensible para instaladores con poca familiaridad tecnológica. | Observar si un instalador identifica el trabajo, registra el material y reconoce el resultado del guardado. | Necesidad derivada de la entrevista; umbral de aceptación pendiente. |
| RNF-03 | Las operaciones de inventario deben conservar la consistencia de los datos. | Simular un fallo y comprobar que no queden registros de uso, sobrantes o cambios de inventario aplicados parcialmente. | Regla confirmada. |
| RNF-04 | Las correcciones deben conservar su trazabilidad. | Consultar una corrección y comprobar autor, fecha, motivo y datos anteriores y nuevos. | Confirmado. |
| RNF-05 | El acceso debe respetar los permisos del usuario. | Intentar una corrección con un perfil sin autorización y comprobar su rechazo. | Corrección exclusiva del administrador confirmada; matriz completa pendiente. |
| RNF-06 | El sistema debe funcionar en los navegadores y dispositivos acordados. | Ejecutar el recorrido principal en cada combinación seleccionada. | Propuesta técnica; combinaciones pendientes. |

No se han aprobado tiempos de respuesta, cifras de concurrencia ni tamaños mínimos de pantalla.

**Distinción:** RF-15 se refiere al mensaje de guardado correcto; RNF-03 exige que todos los cambios de una operación se guarden juntos o no se apliquen.

## 7. Historias de usuario y criterios de aceptación

Las prioridades anteriores se conservan como referencia:

- **Must:** indispensable para la versión prevista.
- **Should:** importante, pero puede aplazarse frente a las funciones indispensables.
- **Could:** opcional; no hay historias asignadas actualmente.
- **Won’t:** fuera de esta versión.

Las historias de inventario cambiaron después de la entrevista. Su esfuerzo y prioridades deben revisarse; HU-14 todavía no tiene prioridad asignada.

Los escenarios de HU-05, HU-10 y HU-13 son parciales porque dependen de decisiones pendientes. No se presentan como historias completamente cerradas.

### HU-01 — Registrar cliente

**Prioridad:** Must.  
**Requisito:** RF-01.

Como asesor, quiero registrar un cliente con nombre, documento y contacto para disponer de sus datos al atenderlo.

**Escenario: registro correcto**

- **Dado** un documento que no está registrado,
- **Cuando** el asesor guarda el nombre, documento y contacto del cliente,
- **Entonces** el cliente queda registrado y disponible para consulta.

**Escenario: documento duplicado**

- **Dado** un documento ya registrado,
- **Cuando** se intenta registrar otro cliente con ese documento,
- **Entonces** se rechaza el nuevo registro, se informa la coincidencia y se conserva el cliente existente.

### HU-02 — Consultar cliente

**Prioridad:** Must.  
**Requisito:** RF-03.

Como asesor, quiero consultar un cliente por su documento para recuperar sus datos y evitar registrarlo nuevamente.

**Escenario: cliente encontrado**

- **Dado** un cliente registrado,
- **Cuando** el asesor consulta su documento,
- **Entonces** aparecen los datos del cliente correspondiente.

**Escenario: cliente no encontrado**

- **Dado** un documento sin coincidencias,
- **Cuando** el asesor lo consulta,
- **Entonces** se informa que no se encontró un cliente con ese documento.

### HU-03 — Registrar vehículo

**Prioridad:** Must.  
**Requisito:** RF-02.

Como asesor, quiero registrar un vehículo y asociarlo a un cliente para identificar a quién pertenece.

**Escenario: registro correcto**

- **Dado** un cliente existente,
- **Cuando** el asesor registra una placa no repetida y la descripción del vehículo,
- **Entonces** el vehículo queda asociado al cliente.

**Escenario: otro vehículo del mismo cliente**

- **Dado** un cliente que ya tiene un vehículo registrado,
- **Cuando** se registra otro vehículo con una placa diferente,
- **Entonces** ambos vehículos permanecen asociados al cliente.

**Escenario: placa duplicada**

- **Dado** un vehículo con una placa registrada,
- **Cuando** se intenta registrar otro con la misma placa,
- **Entonces** se rechaza el nuevo registro y se conserva el vehículo existente.

### HU-04 — Consultar vehículo

**Prioridad:** Must.  
**Requisito:** RF-03.

Como asesor, quiero consultar un vehículo por su placa para identificar al cliente asociado antes de registrar un trabajo.

**Escenario: vehículo encontrado**

- **Dado** un vehículo registrado,
- **Cuando** el asesor busca su placa,
- **Entonces** aparecen el vehículo y su cliente asociado.

**Escenario: vehículo no encontrado**

- **Dada** una placa sin coincidencias,
- **Cuando** el asesor la consulta,
- **Entonces** se informa que no se encontró un vehículo con esa placa.

### HU-05 — Registrar trabajo y detalles

**Prioridad:** Must.  
**Requisitos:** RF-04 y RF-05.

Como asesor, quiero registrar el trabajo y sus detalles de instalación para dejar constancia de lo realizado al vehículo.

**Escenario: registro del trabajo**

- **Dado** un vehículo existente y una de las dos sedes,
- **Cuando** el asesor registra fecha, servicio y valor total,
- **Entonces** el trabajo queda asociado al vehículo y a esa sede con los datos registrados.

**Escenario: conservación de los detalles**

- **Dado** un trabajo con detalles de instalación registrados,
- **Cuando** se consulta su historial,
- **Entonces** se muestran los datos guardados de tecnología, opacidad, instalador y retiro de película que correspondan.

**Pendiente:** concretar cómo representar varias tecnologías, opacidades o instaladores dentro de un trabajo y qué detalles son obligatorios según el servicio. Los escenarios se completarán después de esa definición.

El valor total del trabajo no representa un registro de pago.

### HU-06 — Consultar historial

**Prioridad:** Must.  
**Requisito:** RF-06.

Como asesor, quiero consultar el historial de un vehículo desde ambas sedes para conocer sus atenciones anteriores.

**Escenario: consulta desde la otra sede**

- **Dado** un trabajo registrado en una de las sedes de Ibagué,
- **Cuando** el asesor consulta el historial del vehículo desde la otra sede,
- **Entonces** aparece el trabajo con su sede, fecha, servicio, valor total y detalles de instalación registrados.

**Escenario: historial vacío**

- **Dado** un vehículo registrado sin trabajos,
- **Cuando** el asesor consulta su historial,
- **Entonces** se informa que todavía no tiene trabajos registrados.

### HU-08 — Registrar tipo de material

**Prioridad de referencia:** Must.  
**Requisito:** RF-07.

Como administrador, quiero registrar tipos de material distinguiendo tecnología y opacidad para identificar los rollos y recortes.

**Escenario: registro del tipo de material**

- **Dado** un tipo de material que se desea registrar,
- **Cuando** el administrador guarda su tecnología y opacidad,
- **Entonces** queda disponible para identificar las piezas correspondientes.

### HU-09 — Registrar rollo recibido

**Prioridad de referencia:** Must.  
**Requisitos:** RF-08 y RF-16.

Como administrador, quiero registrar cada rollo recibido con sede, material y dimensiones para conocer lo que ingresa.

**Escenario: ingreso correcto**

- **Dado** un tipo de material registrado,
- **Cuando** el administrador guarda un rollo con identificación, sede y dimensiones positivas en centímetros,
- **Entonces** el rollo queda disponible en esa sede y no cambia el inventario de la otra.

**Escenario: dimensiones inválidas**

- **Dado** un ancho o largo igual o menor que cero,
- **Cuando** se intenta guardar el rollo,
- **Entonces** se rechaza el registro sin modificar el inventario.

**Pendiente:** definir la precisión admitida en las medidas.

### HU-10 — Registrar uso y sobrantes

**Prioridad de referencia:** Must.  
**Requisitos:** RF-09, RF-10, RF-15 y RF-16.  
**Requisito de calidad relacionado:** RNF-03.

Como instalador, quiero registrar la pieza utilizada y los sobrantes aprovechables de un trabajo para mantener el inventario sin duplicar material.

**Escenario general: registro del uso**

- **Dado** un trabajo y una pieza disponible de su misma sede,
- **Cuando** el instalador registra una operación de uso válida,
- **Entonces** se conserva la relación entre trabajo y pieza de origen y se actualiza únicamente el inventario de esa sede.

**Escenario general: sobrantes aprovechables**

- **Dada** una operación de uso que produce sobrantes aprovechables,
- **Cuando** el instalador registra sus dimensiones,
- **Entonces** cada sobrante queda identificado con material, sede y pieza de origen, sin seguir contado dentro del material disponible de origen.

**Escenario: pieza de otra sede**

- **Dada** una pieza de una sede distinta de la del trabajo,
- **Cuando** se intenta utilizar,
- **Entonces** se rechaza la operación sin modificar existencias.

**Escenario: pieza no disponible**

- **Dada** una pieza que ya no está disponible,
- **Cuando** se intenta registrar su uso,
- **Entonces** se rechaza la operación y se conserva el inventario sin cambios.

**Escenario: dimensiones inválidas**

- **Dado** un registro de dimensiones iguales o menores que cero,
- **Cuando** se intenta guardar la operación,
- **Entonces** se rechaza sin aplicar cambios en el inventario.

**Escenario: fallo de guardado**

- **Dada** una operación que modifica la pieza de origen y registra sobrantes,
- **Cuando** falla el guardado de uno de sus cambios,
- **Entonces** no se aplica ninguno de los cambios y no se muestra confirmación de éxito.

**Pendiente:** definir qué datos describen el corte y cómo se registra el material restante del rollo. También falta concretar la comprobación de que el material solicitado cabe en la pieza disponible; comparar únicamente áreas no es suficiente.

Los escenarios generales deberán detallarse cuando se acuerde ese procedimiento.

### HU-11 — Consultar disponibilidad

**Prioridad de referencia:** Must.  
**Requisito:** RF-11.

Como administrador, quiero consultar rollos y recortes por sede, material y dimensiones para identificar lo disponible.

**Escenario: disponibilidad por sede**

- **Dadas** piezas disponibles en ambas sedes,
- **Cuando** el administrador consulta una sede,
- **Entonces** aparecen únicamente sus piezas disponibles con identificación, tecnología, opacidad, ancho y largo.

**Escenario: pieza descartada**

- **Dada** una pieza cuyo descarte fue registrado,
- **Cuando** se consulta la disponibilidad,
- **Entonces** esa pieza no aparece como disponible.

**Escenario: sin disponibilidad**

- **Dada** una consulta sin piezas disponibles que coincidan,
- **Cuando** el administrador consulta la disponibilidad,
- **Entonces** se informa que no hay piezas disponibles para esa consulta.

### HU-12 — Consultar material de un trabajo

**Prioridad de referencia:** Should.  
**Requisito:** RF-12.

Como administrador, quiero consultar las piezas y registros de uso de un trabajo para revisar su relación con el inventario.

**Escenario: trabajo con material registrado**

- **Dado** un trabajo con material utilizado,
- **Cuando** el administrador consulta su detalle,
- **Entonces** se identifican las piezas de origen y los registros de uso asociados.

**Escenario: trabajo sin material registrado**

- **Dado** un trabajo sin registros de uso,
- **Cuando** el administrador consulta su detalle,
- **Entonces** se informa que no tiene uso de material registrado.

Aplazar esta consulta general no elimina la identificación básica del registro que el administrador necesita corregir mediante HU-13.

### HU-13 — Corregir registro de uso

**Prioridad de referencia:** Must.  
**Requisito:** RF-13.  
**Requisitos de calidad relacionados:** RNF-03, RNF-04 y RNF-05.

Como administrador, quiero corregir un registro de uso dejando constancia del cambio para mantener un inventario consistente.

**Escenario general: corrección válida**

- **Dado** un registro que admite corrección conforme al procedimiento que se acuerde,
- **Cuando** el administrador registra una corrección válida e indica el motivo,
- **Entonces** se conservan autor, fecha, motivo y datos anteriores y nuevos, y se actualiza el inventario de la sede correspondiente sin duplicaciones.

**Escenario: usuario sin autorización**

- **Dado** un usuario que no es administrador,
- **Cuando** intenta corregir un registro de uso,
- **Entonces** se rechaza la operación sin modificar el registro ni el inventario.

**Escenario: falta de motivo**

- **Dada** una corrección sin motivo,
- **Cuando** el administrador intenta guardarla,
- **Entonces** se solicita el motivo y no se aplica la corrección.

**Escenario: fallo de guardado**

- **Dada** una corrección que afecta al registro de uso y al inventario,
- **Cuando** falla el guardado de uno de los cambios,
- **Entonces** no se aplica ninguno y se conservan los datos anteriores.

**Pendiente:** definir el procedimiento de corrección de piezas y el tratamiento de sobrantes utilizados posteriormente. La comprobación de disponibilidad cuando aumenta el uso deberá concretarse con ese procedimiento.

El escenario general no cierra toda la historia.

### HU-14 — Descartar pieza dañada

**Prioridad:** pendiente de asignación.  
**Requisito:** RF-14.

Como administrador, quiero registrar el descarte completo de una pieza dañada indicando el motivo para retirarla de la disponibilidad.

**Escenario: descarte completo**

- **Dada** una pieza disponible,
- **Cuando** el administrador confirma su descarte con un motivo,
- **Entonces** deja de estar disponible, se conserva el registro del descarte y no cambia el inventario de la otra sede.

**Escenario: falta de motivo**

- **Dado** un descarte sin motivo,
- **Cuando** el administrador intenta guardarlo,
- **Entonces** se solicita el motivo y no se aplica el descarte.

El tratamiento de daños parciales no está definido ni se incorpora automáticamente al alcance.

## 8. Historia descartada

### HU-07 — Consultar trabajos por sede y periodo

**Prioridad:** Won’t para esta versión.

Fue propuesta por la IA y descartada expresamente por el administrador participante.

No forma parte de las 13 historias activas y no debe reincorporarse al backlog de esta versión.

## 9. Pendientes de definición y revisión

| Pendiente | A qué afecta |
| --- | --- |
| Revisar el documento con Jonathan y validar los resultados derivados con la asesora. | Revisión del equipo y contraste con la fuente del negocio. |
| Precisar los detalles obligatorios de instalación y cómo representar varios materiales o instaladores. | RF-05 y HU-05. |
| Definir la precisión de las medidas en centímetros. | Registro de rollos, cortes y recortes. |
| Definir el registro del corte y del material restante. | RF-09, RF-10, RF-16 y HU-10. |
| Definir correcciones cuando hay sobrantes utilizados posteriormente. | RF-13 y HU-13. |
| Decidir el tratamiento de anulaciones, material equivocado y daños parciales. | Límites del procedimiento de inventario; no son funciones adicionales aprobadas. |
| Completar el mecanismo de identificación y la matriz de permisos. | Acceso a las operaciones según el perfil. |
| Asignar prioridad a HU-14 y revisar esfuerzo y prioridades del inventario. | Priorización y planificación posterior. |
| Acordar condiciones de comprobación de los requisitos no funcionales. | Dispositivos, navegadores y evaluación de facilidad de uso. |
| Actualizar trazabilidad, diseño y planificación con estos identificadores. | Coherencia entre documentos. |

Estas decisiones pendientes deben mantenerse visibles. No se presentan como resueltas por la IA.

## 10. Documentación relacionada

- [Síntesis de la entrevista y aclaraciones](ia/entrevista-cliente.md).
- [Biblioteca de prompts](ia/prompts.md).
- [Pruebas de prompts con Gemini](ia/pruebas-gemini.md).
- [Revisión de historias con Gemini](ia/revision-historias-gemini.md).
- [Trazabilidad](trazabilidad.md).
- [Diseño inicial de backend y frontend](diseno-back-front.md).

Los prompts y las respuestas anteriores se conservan como evidencia del proceso. No sustituyen los requisitos vigentes de este documento.

## 11. Resumen de esta revisión

- Se conservaron los 16 requisitos funcionales, los 6 no funcionales y las 13 historias activas.
- Se mantuvo HU-07 fuera del alcance.
- Se separaron los escenarios de consulta con y sin resultados.
- Se explicitó el registro de varios vehículos por cliente.
- Se relacionó la consistencia de las operaciones con RNF-03.
- Se organizaron los escenarios de validación, guardado y corrección.
- Se mantuvieron visibles los aspectos incompletos de HU-05, HU-10 y HU-13.
- Se conservó la prioridad pendiente de HU-14.
- No se incorporaron pagos, comisiones ni nuevas sedes.
- No se presenta la documentación como software implementado o probado.
