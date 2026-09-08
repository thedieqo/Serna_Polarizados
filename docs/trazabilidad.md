# Trazabilidad — Serna Polarizados

## 1. Propósito y estado

Relacionar las necesidades del negocio con los requisitos, las historias de usuario y sus comprobaciones previstas.

**Fecha de actualización:** 8 de septiembre de 2026.  
**Documento de referencia:** [Requisitos vigentes](requisitos.md).

Esta matriz utiliza los identificadores de la versión actual: RF-01 a RF-16, RNF-01 a RNF-06 y 13 historias activas. HU-07 permanece descartada.

Las comprobaciones son criterios para pruebas futuras. No se ha implementado ni probado el sistema.

## 2. Fuentes

- Entrevista con una asesora de Serna Polarizados, documentada en la [síntesis de entrevista](ia/entrevista-cliente.md).
- Aclaraciones y decisiones del administrador de una sede, integrante del proyecto.
- Registro de Excel compartido como ejemplo de la operación actual.
- Borradores de IA y revisión posterior.

La entrevista aporta necesidades del negocio. Las aclaraciones del administrador delimitan la primera versión y precisan reglas. Las respuestas de IA se conservan como apoyo al análisis, no como decisiones independientes del negocio.

La validación posterior con la asesora y la revisión conjunta con Jonathan siguen pendientes.

## 3. Necesidades identificadas

### N-01 — Organizar clientes y vehículos

Registrar y recuperar los datos de clientes y sus vehículos, evitando documentos y placas duplicados.

**Origen:** registro de Excel, alcance confirmado y solicitud de consulta por documento o placa en la entrevista.

### N-02 — Conservar los trabajos y sus detalles

Relacionar cada trabajo con un vehículo y una sede, conservando fecha, servicio, valor total y detalles registrados de instalación.

**Origen:** alcance confirmado y entrevista sobre la necesidad de conocer tecnología, opacidad, instalador y antecedentes de retiro de película.

La estructura de los detalles de instalación sigue pendiente de precisar.

### N-03 — Compartir el historial entre sedes

Consultar el historial de un vehículo desde cualquiera de las dos sedes de Ibagué.

**Origen:** entrevista sobre la dependencia de llamadas para recuperar información y decisión del administrador de compartirla entre esas dos sedes.

El acceso a información de Bogotá u otras sedes queda fuera de esta versión.

### N-04 — Conocer el inventario de cada sede

Identificar los rollos y recortes disponibles por sede, tecnología, opacidad y dimensiones.

**Origen:** entrevista sobre la falta de visibilidad de materiales y aclaraciones del administrador sobre rollos de distintos anchos y ausencia de registros sistemáticos.

### N-05 — Relacionar uso de material, trabajos y sobrantes

Registrar qué pieza se utiliza en cada trabajo y qué sobrantes aprovechables quedan, sin duplicar material disponible.

**Origen:** alcance confirmado y aclaraciones del administrador sobre cortes, conservación de sobrantes y posibilidad de medirlos.

Las dimensiones se registrarán en centímetros. El procedimiento exacto de corte y registro del restante sigue pendiente.

### N-06 — Corregir registros de uso

Permitir que el administrador corrija errores conservando autor, fecha, motivo y datos anteriores y nuevos.

**Origen:** aprobación expresa del administrador.

El procedimiento para corregir operaciones con sobrantes utilizados posteriormente sigue pendiente.

### N-07 — Retirar piezas dañadas de la disponibilidad

Registrar el descarte completo de una pieza dañada para evitar que siga apareciendo como disponible.

**Origen:** aclaración del administrador sobre sobrantes que se dañan y aprobación de HU-14.

El tratamiento de daños parciales no está definido.

### N-08 — Facilitar registros fiables desde el teléfono

Permitir que el instalador registre información mediante un flujo comprensible y reconozca si el guardado tuvo éxito.

**Origen:** entrevista sobre dificultades con archivos compartidos, registros desde teléfonos y problemas de guardado.

Los dispositivos y las condiciones concretas de evaluación siguen pendientes.

## 4. Relación entre necesidades, requisitos e historias

Las prioridades de inventario se conservan como referencia y requieren revisión del esfuerzo. HU-14 tiene prioridad pendiente.

| Historia | Necesidades | Requisitos funcionales | Prioridad |
| --- | --- | --- | --- |
| HU-01 — Registrar cliente | N-01 | RF-01 | Must |
| HU-02 — Consultar cliente | N-01 | RF-03 | Must |
| HU-03 — Registrar vehículo | N-01 | RF-02 | Must |
| HU-04 — Consultar vehículo | N-01 | RF-03 | Must |
| HU-05 — Registrar trabajo y detalles | N-02 | RF-04, RF-05 | Must |
| HU-06 — Consultar historial | N-02, N-03 | RF-06 | Must |
| HU-08 — Registrar tipo de material | N-04 | RF-07 | Must de referencia |
| HU-09 — Registrar rollo recibido | N-04 | RF-08, RF-16 | Must de referencia |
| HU-10 — Registrar uso y sobrantes | N-04, N-05, N-08 | RF-09, RF-10, RF-15, RF-16 | Must de referencia |
| HU-11 — Consultar disponibilidad | N-04, N-07 | RF-11 | Must de referencia |
| HU-12 — Consultar material de un trabajo | N-05 | RF-12 | Should de referencia |
| HU-13 — Corregir registro de uso | N-04, N-06 | RF-13 | Must de referencia |
| HU-14 — Descartar pieza dañada | N-04, N-07 | RF-14 | Pendiente |

RF-15 y RF-16 son validaciones compartidas: su aparición en una historia no limita su aplicación a esa historia. RF-15 se aplica a las confirmaciones de guardado y RF-16 a las operaciones que requieren dimensiones y disponibilidad.

## 5. Comprobaciones previstas por historia

Los escenarios detallados y sus pendientes se encuentran en [requisitos.md](requisitos.md).

| Historia | Comprobaciones previstas |
| --- | --- |
| HU-01 | Registro correcto y rechazo de documento duplicado sin alterar el cliente existente. |
| HU-02 | Consulta con coincidencia y mensaje cuando no existe el cliente. |
| HU-03 | Asociación con un cliente, conservación de varios vehículos por cliente y rechazo de placa duplicada. |
| HU-04 | Consulta con coincidencia y mensaje cuando no existe el vehículo. |
| HU-05 | Conservación de vehículo, sede, fecha, servicio, valor total y detalles registrados. Criterios parciales hasta precisar la estructura de instalación. |
| HU-06 | Consulta del historial desde la otra sede y mensaje de historial vacío. |
| HU-08 | Registro del tipo de material con tecnología y opacidad. |
| HU-09 | Registro del rollo en su sede y rechazo de dimensiones no positivas. |
| HU-10 | Asociación con trabajo y origen, registro de sobrantes sin duplicación, rechazo de otra sede, pieza no disponible o dimensiones inválidas, y ausencia de cambios parciales ante un fallo. Procedimiento de corte pendiente. |
| HU-11 | Disponibilidad diferenciada por sede, exclusión de piezas descartadas y consulta sin resultados. |
| HU-12 | Identificación de piezas y registros de uso del trabajo, o mensaje cuando no existen. |
| HU-13 | Constancia de la corrección, rechazo de usuario no autorizado o falta de motivo y ausencia de cambios parciales ante un fallo. Procedimiento de corrección pendiente. |
| HU-14 | Descarte completo con motivo, conservación del registro y ausencia de cambios en la otra sede; rechazo si falta el motivo. |

La consulta general de HU-12 puede aplazarse sin eliminar la identificación básica del registro que debe corregirse mediante HU-13.

## 6. Relación con los requisitos no funcionales

| Requisito | Necesidades relacionadas | Aplicación principal | Comprobación prevista |
| --- | --- | --- | --- |
| RNF-01 — Uso desde teléfono | N-08 | HU-10 | Completar el registro desde el teléfono y navegador acordados. |
| RNF-02 — Flujo comprensible | N-08 | HU-10 | Observar si un instalador identifica el trabajo, registra material y reconoce el resultado. |
| RNF-03 — Consistencia de las operaciones | N-04, N-05, N-06, N-07 | Operaciones de inventario, especialmente HU-09, HU-10, HU-13 y HU-14 | Simular un fallo y comprobar que no se apliquen cambios parciales. |
| RNF-04 — Trazabilidad de correcciones | N-06 | HU-13 | Comprobar autor, fecha, motivo y datos anteriores y nuevos. |
| RNF-05 — Respeto de permisos | N-06 y control de acceso transversal | HU-13 y operaciones sujetas a permisos | Rechazar una corrección realizada por un usuario que no sea administrador. Los demás permisos deben precisarse. |
| RNF-06 — Compatibilidad acordada | N-08 y acceso transversal | Recorrido principal del sistema | Ejecutar el recorrido en los dispositivos y navegadores que se acuerden. |

La confirmación de éxito corresponde a **RF-15**. El guardado completo de una operación, sin cambios parciales, corresponde a **RNF-03**.

RNF-06 es una propuesta técnica pendiente de concretar. Las condiciones de evaluación de RNF-01 y RNF-02 tampoco están completamente definidas.

## 7. Historia descartada

**HU-07 — Consultar trabajos por sede y periodo.**

La IA la propuso y el administrador participante la descartó por no ser necesaria para esta versión.

**Prioridad:** Won’t.

No forma parte de las 13 historias activas ni debe asignarse a un sprint de esta versión.

## 8. Estado de revisión y pendientes

- La matriz está alineada documentalmente con los requisitos del 8 de septiembre de 2026.
- Se conservan las decisiones confirmadas por el administrador participante.
- HU-05 requiere precisar los detalles de instalación.
- HU-10 requiere definir el procedimiento de corte y registro del restante.
- HU-13 requiere definir el procedimiento de corrección y los casos con sobrantes utilizados posteriormente.
- HU-14 requiere asignación de prioridad.
- Las historias de inventario requieren revisión de esfuerzo y prioridades.
- La revisión conjunta con Jonathan y la validación posterior con la asesora siguen pendientes.
- El diseño, los diagramas y la planificación deben utilizar estos mismos identificadores.

Esta matriz permite seguir el origen y la comprobación prevista de cada historia. No acredita que las funcionalidades estén implementadas, probadas o totalmente definidas.
