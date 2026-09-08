# Pruebas de requisitos con Gemini

## 1. Datos del proceso

- Fecha de ejecución: 8 de septiembre de 2026.
- Herramienta: Gemini.
- Modelo específico: no registrado.
- Idioma de las instrucciones: inglés.
- Idioma solicitado para las respuestas: español.
- Propósito: obtener requisitos funcionales y no funcionales basados en la entrevista y el alcance acordado.

Los prompts fueron preparados con apoyo de Codex y ejecutados por el integrante del proyecto en Gemini.

Este documento conserva las instrucciones y resúmenes de los resultados. Los resúmenes no sustituyen las respuestas completas de Gemini, cuya incorporación al repositorio sigue pendiente.

## 2. Primera ejecución — Obtener requisitos

### Prompt utilizado

Act as a requirements analyst assisting two students with a small academic software project. Respond in Spanish.

CONTEXT:
The project is Serna Polarizados, a web management system for two branches in Ibagué, Colombia.

An advisor described these operational problems:
- Customer, vehicle and installation information is spread across spreadsheets and shared forms.
- Staff must call other branches to retrieve installation details.
- Installers use phones and struggle with complex spreadsheets; they sometimes cannot confirm whether their entries were saved.
- Staff lack reliable visibility of available window-film technologies and opacity variants.
- Payment verification and commission calculations are slow, but those functions are outside the first release.

CONFIRMED FIRST-RELEASE SCOPE:
- Register customers with name, identification document and contact information.
- Associate multiple vehicles with a customer and search by plate or customer identification.
- Record jobs with vehicle, branch, date, service and total value.
- Include installed technology, opacity, installer information and relevant film-removal information in the vehicle history. The exact structure of these details still requires clarification.
- Share customer, vehicle and job history between the two Ibagué branches.
- Maintain separate material inventory for each branch.
- Record material receipts and job-related consumption.
- Deduct consumption only from the job's branch.
- Allow administrators to correct consumption quantities with an audit record.
- Provide a simple mobile-friendly workflow for installers.

CONFIRMED VALIDATIONS:
- No duplicate customer identification documents or vehicle plates.
- Receipt and consumption quantities must be positive.
- Consumption cannot exceed available stock.
- Increasing a consumption through a correction requires sufficient remaining stock.
- Corrections must preserve author, date, reason, previous quantity and new quantity.

TASK:
Extract functional and non-functional requirements from this context. Distinguish confirmed needs from proposed technical criteria and unresolved questions. Do not simulate additional statements from the advisor.

OUTPUT:
1. A functional-requirements table with ID, requirement, source and verification method.
2. A non-functional-requirements table with ID, quality need, proposed measurable acceptance criterion and validation status.
3. A list of unresolved questions.
4. A short list of excluded functions.

Use RF-01 onward and RNF-01 onward. Keep requirements distinct without forcing a specific count.

CONSTRAINTS:
Do not generate code, diagrams or user stories yet.
Do not include commission calculations, payment verification, invoicing, appointment scheduling, supplier management, automatic stock alerts or PPF quotation.
Do not include Bogotá or additional branches in the first release.
Recording job value does not mean recording payment.
History supports warranty enquiries; a complete warranty-management module is not approved.
Do not invent measurement units, opacity values, user permissions or performance targets.
Any suggested numeric quality target must be clearly marked as a proposal awaiting validation.
Exclude confidential incidents and personal data from the output.

EXAMPLE:
RF: The system must allow staff to retrieve a vehicle's installation history by its plate.
Verification: Search for a registered plate and confirm that the corresponding jobs and installation details appear.

### Resumen del resultado

Gemini produjo:

- 16 requisitos funcionales.
- 4 requisitos no funcionales.
- Preguntas pendientes.
- Una lista de funciones excluidas.

La respuesta cubrió clientes, vehículos, trabajos, historial compartido, inventario y correcciones.

### Revisión de la primera respuesta

Se identificaron estos problemas:

- Presentó la imposibilidad de editar o eliminar auditorías como una regla confirmada, aunque no se había aprobado.
- Mezcló la adaptación móvil con funciones del sistema.
- No expresó claramente el registro de vehículos y materiales.
- No detalló suficientemente cómo ajustar el inventario al corregir consumos.
- Era necesario aclarar que la confirmación de guardado depende del éxito real de la operación.
- Faltaba explicitar la integridad conjunta del consumo y el inventario.
- Preguntó qué perfiles existían, aunque ya estaban identificados.

## 3. Segunda ejecución — Corregir el análisis

### Prompt utilizado

Revise your previous requirements analysis using the review below. Respond in Spanish.

Keep the approved scope: two branches in Ibagué; customers, vehicles, detailed job history and separate inventory per branch.

Apply these corrections:

1. RNF-04 incorrectly labels audit-record immutability as a confirmed business rule. Preserving the adjustment author, date, reason, previous quantity and new quantity is confirmed. Preventing every role from editing or deleting audit records is a technical proposal awaiting validation.

2. Separate mobile usability from functional requirements. Installers are confirmed to record material consumption; do not assume they can create complete job records.

3. Explicitly include vehicle registration with plate, description and associated customer.

4. Explicitly include material registration. The inventory must distinguish window-film technologies and opacity variants, but the exact catalogue structure, measurement units and precision remain unresolved. Do not invent their values.

5. Clarify consumption corrections: adjust inventory by the difference between the old and new quantities, affect only the job's branch and preserve an audit record. Increasing consumption requires sufficient remaining stock.

6. Add transactional integrity: saving a consumption or correction and updating inventory must succeed together or leave both unchanged. This is a previously agreed system rule.

7. Show a successful-save message only after persistence succeeds. The two-second target, 360-pixel width and proposed browser list are not approved requirements; label them as proposals with test conditions still to be agreed.

8. The known profiles are administrator, advisor and installer. Ask about unresolved permissions rather than asking which profiles exist.

9. Remove the unqualified word “immediately” from cross-branch verification. Verify that a successfully saved record can be retrieved from the other branch without inventing a response-time target.

OUTPUT:
- A revised functional-requirements table.
- A revised non-functional-requirements table.
- Unresolved questions.
- Excluded functions.
- A short change log explaining what you corrected.

Preserve existing IDs where possible. Mark moved or replaced requirements explicitly and assign new IDs to additions.

Distinguish interview evidence, decisions confirmed by the project representative and technical proposals. Do not claim that the revised output has been approved or tested.

Do not generate code, diagrams or user stories. Do not add commissions, payments, invoicing, appointments, QR registration, suppliers, automatic stock alerts, PPF quotation or additional branches.

### Resumen del resultado

Gemini produjo una segunda versión con:

- 20 requisitos funcionales.
- 4 requisitos no funcionales.
- Preguntas pendientes.
- Exclusiones.
- Un registro de cambios.

Corrigió la clasificación de la auditoría, explicitó el registro de vehículos y materiales, precisó las correcciones de consumo e incorporó el guardado conjunto de operaciones.

### Limitaciones detectadas en la segunda respuesta

- Cambió varios identificadores pese a la instrucción de conservarlos cuando fuera posible.
- No expresó por separado la consulta de existencias por sede.
- Debía distinguir la necesidad confirmada de uso móvil de los criterios técnicos todavía propuestos.
- La prueba de fallo debía comprobar que todos los datos afectados permanecieran sin cambios.

Por tanto, la segunda respuesta tampoco se aceptó automáticamente como versión definitiva.

## 4. Aclaraciones posteriores del representante del negocio

Después de las ejecuciones de Gemini, el administrador explicó que:

- No se registraban sistemáticamente entradas, cortes y sobrantes.
- Los rollos tenían diferentes anchos.
- Los sobrantes se guardaban y algunos se dañaban.
- Los instaladores podían medirlos y registrarlos.

Posteriormente se acordó utilizar centímetros y representar los sobrantes mediante rectángulos aprovechables.

Estas aclaraciones obligaron a revisar el inventario basado únicamente en cantidades y sustituirlo por identificación de rollos y recortes.

Los prompts anteriores se conservan como evidencia histórica. No describen por sí solos todo el diseño de inventario actualmente acordado.

## 5. Resultado consolidado y pendientes

Los requisitos e historias vigentes se encuentran en:

[Consultar requisitos](../requisitos.md)

La síntesis anonimizada de la entrevista y las aclaraciones está en:

[Consultar entrevista](entrevista-cliente.md)

Pendientes:

- Incorporar las respuestas completas de Gemini como evidencia.
- Revisar los resultados con Jonathan.
- Validar los requisitos derivados con la asesora.
- Resolver los pendientes técnicos identificados en requisitos.md.
- Actualizar la trazabilidad, el backlog y la planificación de sprints.

Este registro documenta pruebas de prompts, no pruebas de funcionamiento del software.
