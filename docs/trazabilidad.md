# Trazabilidad — Serna Polarizados

## 1. Propósito y estado

Relacionar las necesidades del negocio con los requisitos, las historias de usuario, el código existente y sus comprobaciones previstas.

**Fecha de actualización:** 27 de octubre de 2026 (F2).
**Documento de referencia:** [Requisitos vigentes](requisitos.md).

Esta matriz utiliza los identificadores de la versión actual: RF-01 a RF-16, RNF-01 a RNF-06 y 13 historias activas. HU-07 permanece descartada. No se añaden requisitos nuevos.

Los estados de implementación se basan en la lectura del código, no en una ejecución de la aplicación. **F2 no ejecutó el sistema ni pruebas automatizadas.** Por tanto, “implementado” significa que existe código que cubre la función descrita; no acredita que haya sido probada.

## 2. Fuentes

- Entrevista con una asesora de Serna Polarizados, documentada en la [síntesis de entrevista](ia/entrevista-cliente.md).
- Aclaraciones y decisiones del administrador de una sede, integrante del proyecto.
- Registro de Excel compartido como ejemplo de la operación actual.
- Borradores de IA y revisión posterior.
- Código actual en `backend/app` y `frontend/src`.

La entrevista aporta necesidades del negocio. Las aclaraciones del administrador delimitan la primera versión y precisan reglas. Las respuestas de IA se conservan como apoyo al análisis, no como decisiones independientes del negocio.

La validación posterior con la asesora y la revisión conjunta con Jonathan siguen pendientes.

## 3. Necesidades identificadas

### N-01 — Organizar clientes y vehículos

Registrar y recuperar los datos de clientes y sus vehículos, evitando documentos y placas duplicados.

**Origen:** registro de Excel, alcance confirmado y solicitud de consulta por documento o placa en la entrevista.

**Evidencia actual:** modelos, CRUD y endpoints de clientes y vehículos; validación de duplicados; formularios y listas en React.

### N-02 — Conservar los trabajos y sus detalles

Relacionar cada trabajo con un vehículo y una sede, conservando fecha, servicio, valor total y detalles registrados de instalación.

**Origen:** alcance confirmado y entrevista sobre la necesidad de conocer tecnología, opacidad, instalador y antecedentes de retiro de película.

**Evidencia actual:** entidad `Instalacion` con vehículo, fecha, tipo de servicio, opacidad, zonas, instaladores, retiro, observaciones y estado. Faltan sede y valor total. No existe una entidad denominada “trabajo”.

La estructura de los detalles de instalación sigue pendiente de precisar.

### N-03 — Compartir el historial entre sedes

Consultar el historial de un vehículo desde cualquiera de las dos sedes de Ibagué.

**Origen:** entrevista sobre la dependencia de llamadas para recuperar información y decisión del administrador de compartirla entre esas dos sedes.

**Evidencia actual:** la API permite filtrar instalaciones por `vehiculo_id`; la interfaz lista instalaciones, pero no ofrece una vista de historial por vehículo. No existe el concepto de sede.

El acceso a información de Bogotá u otras sedes queda fuera de esta versión.

### N-04 — Conocer el inventario de cada sede

Identificar los rollos y recortes disponibles por sede, tecnología, opacidad y dimensiones.

**Origen:** entrevista sobre la falta de visibilidad de materiales y aclaraciones del administrador sobre rollos de distintos anchos y ausencia de registros sistemáticos.

**Evidencia actual:** no implementado.

### N-05 — Relacionar uso de material, trabajos y sobrantes

Registrar qué pieza se utiliza en cada trabajo y qué sobrantes aprovechables quedan, sin duplicar material disponible.

**Origen:** alcance confirmado y aclaraciones del administrador sobre cortes, conservación de sobrantes y posibilidad de medirlos.

**Evidencia actual:** no implementado.

Las dimensiones se registrarán en centímetros. El procedimiento exacto de corte y registro del restante sigue pendiente.

### N-06 — Corregir registros de uso

Permitir que el administrador corrija errores conservando autor, fecha, motivo y datos anteriores y nuevos.

**Origen:** aprobación expresa del administrador.

**Evidencia actual:** no implementado.

El procedimiento para corregir operaciones con sobrantes utilizados posteriormente sigue pendiente.

### N-07 — Retirar piezas dañadas de la disponibilidad

Registrar el descarte completo de una pieza dañada para evitar que siga apareciendo como disponible.

**Origen:** aclaración del administrador sobre sobrantes que se dañan y aprobación de HU-14.

**Evidencia actual:** no implementado.

El tratamiento de daños parciales no está definido.

### N-08 — Facilitar registros fiables desde el teléfono

Permitir que el instalador registre información mediante un flujo comprensible y reconozca si el guardado tuvo éxito.

**Origen:** entrevista sobre dificultades con archivos compartidos, registros desde teléfonos y problemas de guardado.

**Evidencia actual:** la interfaz usa Tailwind con clases responsive y muestra mensajes de éxito y error. No se ha evaluado en un teléfono ni con un instalador.

Los dispositivos y las condiciones concretas de evaluación siguen pendientes.

## 4. Relación entre necesidades, requisitos e historias

Las prioridades de inventario se conservan como referencia y requieren revisión del esfuerzo. HU-14 tiene prioridad pendiente.

Estados usados en esta tabla:

- **Implementado:** existe código que cubre el flujo descrito; no implica prueba ejecutada.
- **Parcial:** existe una parte del flujo o falta integración en la interfaz.
- **No implementado:** no existe código para la función.
- **Pendiente de verificación:** existe código, pero no se ejecutó ni se comprobó en F2.

| Historia | Necesidades | Requisitos funcionales | Prioridad | Estado observado |
| --- | --- | --- | --- | --- |
| HU-01 — Registrar cliente | N-01 | RF-01 | Must | Implementado en código. |
| HU-02 — Consultar cliente | N-01 | RF-03 | Must | Parcial: endpoint y servicio; falta integrar búsqueda en la interfaz. |
| HU-03 — Registrar vehículo | N-01 | RF-02 | Must | Implementado en código. |
| HU-04 — Consultar vehículo | N-01 | RF-03 | Must | Parcial: endpoint y servicio; falta integrar búsqueda en la interfaz. |
| HU-05 — Registrar trabajo y detalles | N-02 | RF-04, RF-05 | Must | Parcial: hay instalación con vehículo, fecha, servicio, zonas e instaladores; faltan sede y valor total. |
| HU-06 — Consultar historial | N-02, N-03 | RF-06 | Must | Parcial: filtro por vehículo en la API; falta vista de historial y sede. |
| HU-08 — Registrar tipo de material | N-04 | RF-07 | Must de referencia | No implementado. |
| HU-09 — Registrar rollo recibido | N-04 | RF-08, RF-16 | Must de referencia | No implementado. |
| HU-10 — Registrar uso y sobrantes | N-04, N-05, N-08 | RF-09, RF-10, RF-15, RF-16 | Must de referencia | No implementado. |
| HU-11 — Consultar disponibilidad | N-04, N-07 | RF-11 | Must de referencia | No implementado. |
| HU-12 — Consultar material de un trabajo | N-05 | RF-12 | Should de referencia | No implementado. |
| HU-13 — Corregir registro de uso | N-04, N-06 | RF-13 | Must de referencia | No implementado. |
| HU-14 — Descartar pieza dañada | N-04, N-07 | RF-14 | Pendiente | No implementado. |

RF-15 y RF-16 son validaciones compartidas: su aparición en una historia no limita su aplicación a esa historia. RF-15 se aplica a las confirmaciones de guardado y RF-16 a las operaciones que requieren dimensiones y disponibilidad.

### Requisitos funcionales sin historia exclusiva

| Requisito | Estado observado | Evidencia o límite |
| --- | --- | --- |
| RF-01 — Registrar clientes sin documento duplicado | Implementado en código. | `POST /clientes/`, validación en router y restricción única. |
| RF-02 — Registrar vehículos sin placa duplicada | Implementado en código. | `POST /vehiculos/`, validación de placa y cliente. |
| RF-03 — Consultar clientes y vehículos | Parcial. | Endpoints `by-documento` y `by-placa`; servicios del frontend; búsqueda no integrada en pantallas. |
| RF-04 — Registrar trabajos con sede y valor | Parcial. | Instalación registra vehículo, fecha, servicio y estado; no sede ni valor. |
| RF-05 — Registrar detalles de instalación | Parcial. | Zonas y asignaciones JSON; estructura interna y obligatoriedad pendientes. |
| RF-06 — Consultar historial del vehículo | Parcial. | Filtro `vehiculo_id`; no hay vista de historial ni sede. |
| RF-07 a RF-14 — Inventario, correcciones y descarte | No implementado. | Sin modelos ni endpoints. |
| RF-15 — Confirmar solo tras guardado correcto | Parcial. | Los formularios muestran éxito después de la respuesta; no hay operaciones de inventario. |
| RF-16 — Validar dimensiones y disponibilidad | No implementado. | No existen dimensiones ni inventario. |

## 5. Comprobaciones previstas y evidencia actual

Los escenarios detallados y sus pendientes se encuentran en [requisitos.md](requisitos.md).

| Historia | Comprobaciones previstas | Evidencia actual |
| --- | --- | --- |
| HU-01 | Registro correcto y rechazo de documento duplicado sin alterar el cliente existente. | Código de creación y validación; no se ejecutó la prueba. |
| HU-02 | Consulta con coincidencia y mensaje cuando no existe el cliente. | Endpoint y servicio; falta interfaz de búsqueda. |
| HU-03 | Asociación con un cliente, conservación de varios vehículos por cliente y rechazo de placa duplicada. | Código de creación, validación y relación uno a muchos; no se ejecutó la prueba. |
| HU-04 | Consulta con coincidencia y mensaje cuando no existe el vehículo. | Endpoint y servicio; falta interfaz de búsqueda. |
| HU-05 | Conservación de vehículo, sede, fecha, servicio, valor total y detalles registrados. | Vehículo, fecha, servicio y detalles parciales; faltan sede y valor. |
| HU-06 | Consulta del historial desde la otra sede y mensaje de historial vacío. | Filtro por vehículo; faltan sede, vista de historial y mensaje específico. |
| HU-08 | Registro del tipo de material con tecnología y opacidad. | No implementado. |
| HU-09 | Registro del rollo en su sede y rechazo de dimensiones no positivas. | No implementado. |
| HU-10 | Asociación con trabajo y origen, registro de sobrantes sin duplicación, rechazo de otra sede, pieza no disponible o dimensiones inválidas, y ausencia de cambios parciales ante un fallo. | No implementado. |
| HU-11 | Disponibilidad diferenciada por sede, exclusión de piezas descartadas y consulta sin resultados. | No implementado. |
| HU-12 | Identificación de piezas y registros de uso del trabajo, o mensaje cuando no existen. | No implementado. |
| HU-13 | Constancia de la corrección, rechazo de usuario no autorizado o falta de motivo y ausencia de cambios parciales ante un fallo. | No implementado. |
| HU-14 | Descarte completo con motivo, conservación del registro y ausencia de cambios en la otra sede; rechazo si falta el motivo. | No implementado. |

La consulta general de HU-12 puede aplazarse sin eliminar la identificación básica del registro que debe corregirse mediante HU-13.

## 6. Relación con los requisitos no funcionales

| Requisito | Necesidades relacionadas | Aplicación principal | Comprobación prevista | Estado observado |
| --- | --- | --- | --- | --- |
| RNF-01 — Uso desde teléfono | N-08 | HU-10 | Completar el registro desde el teléfono y navegador acordados. | Parcial: interfaz responsive; sin evaluación en dispositivo. |
| RNF-02 — Flujo comprensible | N-08 | HU-10 | Observar si un instalador identifica el trabajo, registra material y reconoce el resultado. | Pendiente: no evaluado con usuarios. |
| RNF-03 — Consistencia de las operaciones | N-04, N-05, N-06, N-07 | Operaciones de inventario, especialmente HU-09, HU-10, HU-13 y HU-14 | Simular un fallo y comprobar que no se apliquen cambios parciales. | No verificable: el inventario no existe. |
| RNF-04 — Trazabilidad de correcciones | N-06 | HU-13 | Comprobar autor, fecha, motivo y datos anteriores y nuevos. | No implementado. |
| RNF-05 — Respeto de permisos | N-06 y control de acceso transversal | HU-13 y operaciones sujetas a permisos | Rechazar una corrección realizada por un usuario que no sea administrador. | No implementado: la API no tiene autenticación. |
| RNF-06 — Compatibilidad acordada | N-08 y acceso transversal | Recorrido principal del sistema | Ejecutar el recorrido en los dispositivos y navegadores que se acuerden. | Pendiente: no se ejecutó la aplicación. |

La confirmación de éxito corresponde a **RF-15**. El guardado completo de una operación, sin cambios parciales, corresponde a **RNF-03**.

RNF-06 es una propuesta técnica pendiente de concretar. Las condiciones de evaluación de RNF-01 y RNF-02 tampoco están completamente definidas.

## 7. Historia descartada

**HU-07 — Consultar trabajos por sede y periodo.**

La IA la propuso y el administrador participante la descartó por no ser necesaria para esta versión.

**Prioridad:** Won’t.

No forma parte de las 13 historias activas ni debe asignarse a un sprint de esta versión.

## 8. Estado de revisión y pendientes

- La matriz está alineada documentalmente con los requisitos del 8 de septiembre de 2026 y con el código observado en F2.
- Se conservan las decisiones confirmadas por el administrador participante.
- HU-05 requiere incorporar sede y valor, además de precisar los detalles de instalación.
- HU-06 requiere una vista de historial y el concepto de sede.
- HU-10 requiere definir el procedimiento de corte y registro del restante.
- HU-13 requiere definir el procedimiento de corrección y los casos con sobrantes utilizados posteriormente.
- HU-14 requiere asignación de prioridad.
- Las historias de inventario requieren revisión de esfuerzo y prioridades.
- La revisión conjunta con Jonathan y la validación posterior con la asesora siguen pendientes.
- El diseño, los diagramas y la planificación deben utilizar estos mismos identificadores.
- No se ejecutaron pruebas; la cobertura descrita es estática y debe verificarse en una fase posterior.

Esta matriz permite seguir el origen y la comprobación prevista de cada historia. No acredita que las funcionalidades estén implementadas por completo, probadas o totalmente definidas.
