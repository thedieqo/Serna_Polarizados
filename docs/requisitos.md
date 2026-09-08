# Requisitos — Serna Polarizados

## 1. Estado y fuentes

Versión consolidada: 8 de septiembre de 2026.

Este documento reúne requisitos funcionales, necesidades de calidad, historias de usuario, prioridades y criterios de aceptación.

Fuentes:

- Entrevista con Helena, asesora de la empresa.
- Aclaraciones y decisiones del administrador de una sede, integrante del proyecto.
- Análisis inicial y revisión con Gemini.
- Organización y revisión asistida con Codex.

Las decisiones del negocio indicadas como confirmadas fueron revisadas con el administrador participante. La revisión conjunta con Jonathan sigue pendiente.

El documento contiene 13 historias activas. HU-07 está descartada.

Los criterios son especificaciones para pruebas futuras; no representan pruebas ejecutadas ni software implementado.

Esta versión sustituye las descripciones y criterios anteriores del documento. El historial de Git conserva las versiones previas.

## 2. Problema y alcance

La información de clientes, vehículos e instalaciones se consulta mediante registros manuales, archivos compartidos y llamadas. Los instaladores tienen dificultades para registrar información desde sus teléfonos. No existe un registro sistemático de entradas, cortes y sobrantes de material.

La primera versión cubrirá las dos sedes de Serna Polarizados en Ibagué e incluirá:

- Clientes y vehículos.
- Registro de trabajos e historial detallado.
- Consulta compartida entre las dos sedes.
- Inventario independiente por sede.
- Identificación de rollos y recortes aprovechables.
- Registro de uso de material, correcciones y descartes.

Fuera de esta versión:

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

El valor del trabajo no indica si fue pagado. El historial permite consultar antecedentes para atender garantías, pero no administra todo ese proceso.

## 3. Perfiles

- Asesor: registra y consulta clientes, vehículos y trabajos.
- Instalador: registra el uso de material y los sobrantes de sus operaciones.
- Administrador: registra y consulta información, corrige registros de uso y registra descartes de piezas dañadas.

La identificación de usuarios y la matriz detallada de permisos siguen pendientes. Compartir información entre sedes no significa acceso público.

## 4. Reglas confirmadas

- Un cliente puede tener varios vehículos.
- No se permiten documentos de clientes ni placas duplicados.
- Cada trabajo pertenece a un vehículo y a una sede.
- Clientes, vehículos e historial se comparten entre las dos sedes.
- El inventario pertenece a una sede específica.
- El uso de material se relaciona con el trabajo y su pieza de origen.
- No se utiliza material de otra sede dentro de ese trabajo.
- Las dimensiones se registran en centímetros y deben ser positivas.
- Los sobrantes se representan mediante rectángulos aprovechables medidos por el instalador.
- El material de un sobrante no puede seguir contado dentro de la pieza de origen.
- El administrador puede corregir registros y debe quedar constancia de autor, fecha, motivo y datos anteriores y nuevos.
- El administrador registra el descarte completo de piezas dañadas.
- Una operación de inventario se guarda completa o no se aplica parcialmente.

## 5. Requisitos funcionales

Los identificadores siguientes corresponden a esta versión consolidada. Sustituyen la numeración provisional de los borradores de Gemini.

| ID | Requisito | Origen principal |
| --- | --- | --- |
| RF-01 | Registrar clientes con nombre, documento y contacto, sin documentos duplicados. | Alcance y validaciones confirmadas |
| RF-02 | Registrar vehículos con placa y descripción, asociados a un cliente, sin placas duplicadas. | Alcance y validaciones confirmadas |
| RF-03 | Consultar clientes por documento y vehículos por placa. | Entrevista y alcance confirmado |
| RF-04 | Registrar trabajos con vehículo, sede, fecha, servicio y valor total. | Alcance confirmado |
| RF-05 | Registrar detalles de instalación: tecnología, opacidad, instalador y datos aplicables de retiro de película. | Entrevista y alcance confirmado; estructura detallada pendiente |
| RF-06 | Consultar el historial del vehículo desde ambas sedes, incluyendo los detalles registrados de cada trabajo. | Entrevista y decisión confirmada |
| RF-07 | Registrar tipos de material diferenciando tecnología y opacidad. | Entrevista y revisión del inventario |
| RF-08 | Registrar cada rollo recibido con identificación, sede, tipo de material, ancho y largo en centímetros. | Revisión aprobada del inventario |
| RF-09 | Registrar el uso de material asociado a un trabajo y una pieza de su misma sede. | Alcance y revisión aprobada |
| RF-10 | Registrar sobrantes aprovechables con identificación, dimensiones y pieza de origen, evitando duplicar existencias. | Decisión confirmada sobre sobrantes |
| RF-11 | Consultar rollos y recortes disponibles por sede, material y dimensiones. | Revisión aprobada del inventario |
| RF-12 | Consultar las piezas y registros de uso asociados a un trabajo. | HU-12 aceptada |
| RF-13 | Permitir al administrador corregir registros de uso conservando consistencia y constancia del ajuste. | Decisión confirmada; casos dependientes pendientes |
| RF-14 | Permitir al administrador descartar una pieza completa dañada, indicando el motivo y retirándola de la disponibilidad. | HU-14 aprobada |
| RF-15 | Mostrar confirmación de guardado únicamente cuando la operación se haya guardado correctamente. | Necesidad de registro fiable y diseño derivado |
| RF-16 | Validar dimensiones positivas y disponibilidad de la pieza antes de aplicar operaciones. | Validaciones aprobadas, adaptadas al inventario por piezas |

## 6. Requisitos no funcionales

| ID | Necesidad | Comprobación propuesta | Estado |
| --- | --- | --- | --- |
| RNF-01 | El instalador debe poder completar su registro desde un teléfono. | Ejecutar el recorrido en el teléfono y navegador acordados, comprobando lectura, acceso a campos y ausencia de desplazamiento horizontal innecesario. | Necesidad confirmada; dispositivo y condiciones pendientes |
| RNF-02 | El flujo debe ser comprensible para instaladores con poca familiaridad tecnológica. | Realizar una prueba con un instalador y observar si identifica el trabajo, registra material y reconoce el resultado del guardado. | Necesidad derivada de entrevista; umbral de aceptación pendiente |
| RNF-03 | Las operaciones de inventario deben ser consistentes. | Provocar un fallo durante un registro y comprobar que no queden consumos, sobrantes o cambios de origen aplicados parcialmente. | Regla del sistema confirmada |
| RNF-04 | Los ajustes deben conservar su trazabilidad. | Consultar una corrección y comprobar autor, momento, motivo y datos anteriores y nuevos. | Confirmado |
| RNF-05 | El acceso debe respetar los permisos del usuario. | Intentar una corrección con un perfil sin autorización y comprobar su rechazo. | Corrección exclusiva del administrador confirmada; matriz completa pendiente |
| RNF-06 | El sistema debe funcionar en los navegadores y dispositivos acordados. | Ejecutar el recorrido principal en cada combinación seleccionada. | Propuesta técnica; combinaciones pendientes |

No se han aprobado tiempos de respuesta, cifras de concurrencia ni tamaños mínimos de pantalla.

## 7. Historias de usuario y criterios

Las prioridades previas se conservan como referencia. La revisión del esfuerzo de las historias de inventario y la prioridad de HU-14 quedan pendientes.

### HU-01 — Registrar cliente
Prioridad: Must.
Requisito: RF-01.

Como asesor, quiero registrar un cliente con nombre, documento y contacto para disponer de sus datos al atenderlo.

Escenario: registro correcto
- Dado un cliente que no está registrado,
- Cuando el asesor guarda sus datos válidos,
- Entonces el cliente queda disponible para consulta.

Escenario: documento duplicado
- Dado un documento ya registrado,
- Cuando se intenta registrar otro cliente con ese documento,
- Entonces se rechaza el registro y se informa la coincidencia.

### HU-02 — Consultar cliente
Prioridad: Must.
Requisito: RF-03.

Como asesor, quiero consultar un cliente por su documento para recuperar sus datos y evitar registrarlo nuevamente.

- Dado un cliente registrado,
- Cuando se consulta su documento,
- Entonces aparecen sus datos.
- Si no hay coincidencia, se informa que no se encontró el cliente.

### HU-03 — Registrar vehículo
Prioridad: Must.
Requisito: RF-02.

Como asesor, quiero registrar un vehículo y asociarlo a un cliente para identificar a quién pertenece.

- Dado un cliente existente,
- Cuando se registra una placa no repetida y la descripción del vehículo,
- Entonces el vehículo queda asociado a ese cliente sin eliminar sus otros vehículos.

Escenario: placa duplicada
- Dado un vehículo con una placa registrada,
- Cuando se intenta registrar otro con la misma placa,
- Entonces se rechaza el nuevo registro.

### HU-04 — Consultar vehículo
Prioridad: Must.
Requisito: RF-03.

Como asesor, quiero consultar un vehículo por su placa para identificar al cliente asociado antes de registrar un trabajo.

- Dado un vehículo registrado,
- Cuando se busca su placa,
- Entonces aparecen el vehículo y su cliente.
- Si no hay coincidencia, se informa que no se encontró el vehículo.

### HU-05 — Registrar trabajo y detalles
Prioridad: Must.
Requisitos: RF-04 y RF-05.

Como asesor, quiero registrar el trabajo y sus detalles de instalación para dejar constancia de lo realizado al vehículo.

- Dado un vehículo existente,
- Cuando se registra el trabajo con sede, fecha, servicio y valor total,
- Entonces queda asociado al vehículo y a esa sede.
- Los detalles de tecnología, opacidad, instalador y retiro que se registren deben conservarse y aparecer en el historial.

Pendiente: concretar cómo representar varias tecnologías, opacidades o instaladores dentro de un trabajo y qué detalles son obligatorios.

### HU-06 — Consultar historial
Prioridad: Must.
Requisito: RF-06.

Como asesor, quiero consultar el historial de un vehículo desde ambas sedes para conocer sus atenciones anteriores.

- Dado un trabajo registrado en la sede A,
- Cuando se consulta el vehículo desde la sede B,
- Entonces aparece el trabajo con su sede, fecha, servicio y detalles de instalación registrados.
- Si el vehículo no tiene trabajos, se indica que su historial está vacío.

### HU-08 — Registrar tipo de material
Prioridad de referencia: Must.
Requisito: RF-07.

Como administrador, quiero registrar tipos de material distinguiendo tecnología y opacidad para identificar los rollos y recortes.

- Dado un tipo de material que se desea registrar,
- Cuando el administrador guarda su tecnología y opacidad,
- Entonces queda disponible para identificar las piezas correspondientes.

### HU-09 — Registrar rollo recibido
Prioridad de referencia: Must.
Requisitos: RF-08 y RF-16.

Como administrador, quiero registrar cada rollo recibido con sede, material y dimensiones para conocer lo que ingresa.

- Dado un tipo de material registrado,
- Cuando se guarda un rollo con sede y dimensiones positivas en centímetros,
- Entonces queda identificado en esa sede y no cambia el inventario de la otra.

Escenario: dimensiones inválidas
- Dado un ancho o largo igual o menor que cero,
- Cuando se intenta guardar el rollo,
- Entonces se rechaza el registro sin modificar el inventario.

### HU-10 — Registrar uso y sobrantes
Prioridad de referencia: Must.
Requisitos: RF-09, RF-10, RF-15 y RF-16.

Como instalador, quiero registrar la pieza utilizada y los sobrantes aprovechables de un trabajo para mantener el inventario sin duplicar material.

- Dado un trabajo y una pieza disponible de la misma sede,
- Cuando se registra una operación válida de uso y sus sobrantes,
- Entonces se conserva la relación con el trabajo y la pieza de origen.
- Cada sobrante queda identificado con material, sede y dimensiones aprovechables.
- La pieza de origen se actualiza sin contar dos veces el material.

Escenario: pieza de otra sede
- Dada una pieza de una sede distinta de la del trabajo,
- Cuando se intenta utilizar,
- Entonces se rechaza la operación sin modificar existencias.

Escenario: fallo de guardado
- Dada una operación que modifica origen y sobrantes,
- Cuando falla uno de sus cambios,
- Entonces no se aplica ninguno y no se muestra confirmación de éxito.

Pendiente: definir el registro exacto del corte y del material restante en el rollo. No basta comparar áreas para comprobar que una pieza cabe en otra.

### HU-11 — Consultar disponibilidad
Prioridad de referencia: Must.
Requisito: RF-11.

Como administrador, quiero consultar rollos y recortes por sede, material y dimensiones para identificar lo disponible.

- Dadas piezas disponibles en ambas sedes,
- Cuando se consulta una sede,
- Entonces aparecen sus piezas con identificación, tecnología, opacidad, ancho y largo.
- Las piezas descartadas no aparecen como disponibles.

### HU-12 — Consultar material de un trabajo
Prioridad de referencia: Should.
Requisito: RF-12.

Como administrador, quiero consultar las piezas y registros de uso de un trabajo para revisar su relación con el inventario.

- Dado un trabajo con material utilizado,
- Cuando se consulta su detalle,
- Entonces se identifican las piezas de origen y registros de uso asociados.

Aplazar esta consulta general no elimina la selección básica de registros necesaria para corregirlos mediante HU-13.

### HU-13 — Corregir registro de uso
Prioridad de referencia: Must.
Requisito: RF-13.

Como administrador, quiero corregir un registro de uso dejando constancia del cambio para mantener un inventario consistente.

- Dado un registro que admite corrección según las reglas definidas,
- Cuando el administrador realiza una corrección válida e indica el motivo,
- Entonces se conservan autor, momento, motivo y datos anteriores y nuevos.
- El inventario afectado se actualiza sin duplicaciones.
- La operación se guarda completa o no se aplica.

Escenario: usuario sin autorización
- Dado un usuario que no es administrador,
- Cuando intenta corregir un registro,
- Entonces el sistema rechaza la operación.

Pendiente: reglas concretas para corregir piezas y para tratar sobrantes ya utilizados. Este escenario no cierra todavía toda la historia.

### HU-14 — Descartar pieza dañada
Prioridad: pendiente de asignación.
Requisito: RF-14.

Como administrador, quiero registrar el descarte completo de una pieza dañada indicando el motivo para retirarla de la disponibilidad.

- Dada una pieza disponible,
- Cuando el administrador confirma su descarte con un motivo,
- Entonces deja de aparecer como disponible.
- Se conserva el registro del descarte y la identificación de la pieza.
- El inventario de la otra sede permanece sin cambios.

El tratamiento de daños parciales no está definido.

## 8. Historia descartada

HU-07 — Consultar trabajos por sede y periodo.

Descartada expresamente por el administrador participante. Prioridad Won’t. No cuenta entre las 13 historias activas.

## 9. Pendientes reales

- Revisar el documento con Jonathan y validar los resultados derivados de la entrevista con Helena.
- Precisar campos y estructura del detalle de instalación.
- Definir la precisión de las medidas en centímetros.
- Definir el registro del corte y del restante del rollo.
- Definir correcciones cuando existen sobrantes utilizados posteriormente.
- Resolver anulaciones, material equivocado y daños parciales.
- Completar la identificación de usuarios y matriz de permisos.
- Asignar prioridad a HU-14 y revisar el esfuerzo del inventario por piezas.
- Acordar condiciones de prueba de los requisitos no funcionales.
- Actualizar trazabilidad y diseño con esta versión.

## 10. Resumen de cambios

- Se incorporó la entrevista de la asesora como fuente.
- Se amplió el detalle del historial para incluir información de instalación.
- Se sustituyó el inventario basado solo en cantidades por identificación de rollos y recortes.
- Se aprobaron medidas en centímetros y rectángulos aprovechables.
- Se añadió HU-14 para descartes completos.
- Se conservaron las exclusiones de pagos, comisiones y sedes adicionales.
- Se separaron decisiones confirmadas de propuestas técnicas y pendientes.

Las pruebas de prompts y sus resultados se conservan en docs/ia/prompts.md. La respuesta inicial de IA no se presenta como una decisión del negocio ni como software probado.
