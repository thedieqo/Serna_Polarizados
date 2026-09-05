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
## P-03 — Comparar soluciones existentes

### Datos de la prueba

- Fecha: 5 de septiembre de 2026.
- Herramienta: Codex con búsqueda web.
- Objetivo: comparar tres sistemas mediante fuentes oficiales.
- Estado: ejecutado; revisión conjunta del equipo pendiente.

### Prompt utilizado

Actúa como analista de software para un proyecto académico pequeño.

CONTEXTO:
Estamos desarrollando Serna Polarizados para dos sedes de Ibagué. El alcance incluye clientes, vehículos, trabajos realizados e inventario independiente por sede. Ambas sedes comparten el historial de trabajos. Cada consumo de material debe relacionarse con un trabajo y descontarse de la sede correspondiente.

TAREA:
Consulta fuentes oficiales de Shopmonkey, AutoLeap y Odoo y compara sus funciones relevantes para este proyecto. Al final, indica tres aprendizajes que podamos aplicar sin ampliar nuestro alcance.

FORMATO:
Una tabla con tres filas y estas columnas: Sistema, Funciones verificadas, Utilidad para Serna y Aspectos pendientes de verificar. Después, una lista de tres aprendizajes. Incluye enlaces a las fuentes utilizadas.

RESTRICCIONES:
No inventes funciones, precios ni pruebas realizadas. Distingue los datos publicados de tus interpretaciones. Si no puedes verificar algo, escribe “No verificado”. No afirmes que nuestro proyecto es superior. No añadas pagos, facturación, agenda, QR ni otras funciones al MVP.

EJEMPLO:
Aspecto pendiente de verificar: comprobar si el sistema permite registrar consumos fraccionarios de material de polarizado en metros.

### Resumen de la respuesta obtenida

Se consultaron fuentes oficiales. No se realizaron pruebas de funcionamiento de los sistemas.

- Shopmonkey: documenta registro de clientes, asociación de vehículos, historial de servicios y herramientas de inventario relacionadas con trabajos.
- AutoLeap: documenta seguimiento de piezas por trabajo, existencias por ubicación y gestión de inventario de varias sedes.
- Odoo: documenta registro de contactos y organización de existencias mediante almacenes y ubicaciones.
- Quedaron sin verificar aspectos específicos como consumos fraccionarios de película de polarizado y la configuración necesaria para reproducir todo el flujo de Serna.

Los tres aprendizajes propuestos fueron:

1. Relacionar cada trabajo con un vehículo y cada vehículo con su cliente.
2. Identificar la sede afectada por cada entrada o consumo.
3. Conservar el material y la cantidad utilizados por trabajo, definiendo antes las unidades de medida.

### Fuentes consultadas

- Shopmonkey, clientes y vehículos:
  https://support.shopmonkey.io/hc/en-us/articles/38744260861204-Lists-Page
- Shopmonkey, inventario:
  https://www.shopmonkey.io/demo-inventory-management
- AutoLeap, inventario:
  https://autoleap.com/features/inventory/
- Odoo 19, contactos:
  https://www.odoo.com/documentation/19.0/applications/essentials/contacts.html
- Odoo 19, organización del inventario:
  https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management.html

### Comentarios de revisión asistida

Qué funcionó:

- Entregó una tabla con tres sistemas y cuatro columnas.
- Incluyó tres aprendizajes relacionados con el alcance.
- Utilizó fuentes oficiales y separó funciones documentadas de interpretaciones.
- Indicó lo que no pudo verificar.
- No comparó precios ni afirmó que Serna fuera superior.

Limitaciones:

- La revisión fue documental; no demuestra el funcionamiento práctico.
- No confirmó todos los aspectos importantes para Serna, como el consumo fraccionario de materiales.
- Las fuentes de Odoo corresponden a la versión 19; el análisis competitivo anterior citaba documentación de versiones 17 y 18.

Correcciones y seguimiento:

No se modificó la respuesta durante esta prueba. Queda pendiente revisar si conviene actualizar las referencias del análisis competitivo para utilizar una misma versión de Odoo.

No se realizó una segunda ejecución del prompt.

### Revisión humana pendiente

Los integrantes deben abrir las fuentes, revisar las afirmaciones y registrar sus observaciones. La revisión asistida no sustituye la revisión del equipo.


## P-04 — Proponer historias de usuario

### Datos de la prueba

- Fecha: 5 de septiembre de 2026.
- Herramienta: Codex.
- Objetivo: proponer historias de usuario para el alcance acordado.
- Estado: ejecutado y revisado con un integrante; revisión con Jonathan pendiente.

### Prompt utilizado

Actúa como analista de requisitos para un proyecto académico pequeño.

CONTEXTO:
Serna Polarizados necesita un sistema para sus dos sedes de Ibagué. Ambas comparten clientes, vehículos e historial de trabajos, pero cada sede tiene inventario independiente.

El alcance incluye:

- Registrar y consultar clientes con nombre, documento y contacto.
- Registrar vehículos asociados a clientes y consultarlos por placa.
- Registrar trabajos asociados a un vehículo y una sede, con fecha, servicio y valor total.
- Consultar el historial de trabajos desde ambas sedes.
- Registrar materiales, entradas y consumos, y consultar existencias por sede.
- Relacionar cada consumo con un trabajo y descontarlo del inventario de esa sede.

Los perfiles identificados son administrador, asesor e instalador. Sus permisos específicos todavía están pendientes de definición.

TAREA:
Propón 12 historias de usuario para este alcance. Cada historia debe expresar una necesidad concreta y poder revisarse por separado.

FORMATO:
Lista numerada de HU-01 a HU-12. Usa en cada una:
“Como [perfil], quiero [acción] para [beneficio]”.
Después, incluye hasta tres dudas relevantes para revisar las historias.

RESTRICCIONES:
No generes código. No agregues pagos, facturación, agenda, QR, proveedores, alertas automáticas ni nuevas sedes. Registrar el valor de un trabajo no significa gestionar su pago. No inventes unidades de medida. La asignación de perfiles es una propuesta para validar, no una decisión confirmada de permisos. No dividas artificialmente una misma necesidad para completar las 12 historias.

EJEMPLO:
Como asesor, quiero consultar el historial de un vehículo por su placa para conocer los trabajos anteriores antes de atenderlo.

### Resumen de la respuesta inicial

La IA propuso estas 12 historias:

- HU-01: registrar cliente.
- HU-02: consultar cliente.
- HU-03: registrar vehículo.
- HU-04: consultar vehículo.
- HU-05: registrar trabajo.
- HU-06: consultar historial del vehículo.
- HU-07: consultar trabajos por sede y periodo.
- HU-08: registrar material.
- HU-09: registrar entrada de material.
- HU-10: registrar consumo de material.
- HU-11: consultar existencias.
- HU-12: consultar materiales de un trabajo.

También preguntó por los permisos, las unidades de medida y la necesidad de HU-07.

### Qué funcionó

- Entregó 12 historias con perfil, acción y beneficio.
- Conservó la separación de inventarios por sede.
- Relacionó los consumos con los trabajos.
- Presentó los perfiles como propuestas para revisar.
- Formuló dudas que permitieron obtener decisiones del usuario.

### Qué no funcionó

La consulta por sede y periodo de HU-07 no era necesaria para la primera versión. La propuesta de IA necesitó una corrección de alcance.

### Revisión humana y correcciones

Un integrante del equipo revisó las historias y:

1. Aceptó las historias excepto HU-07.
2. Descartó HU-07 por no ser necesaria.
3. Confirmó que asesor y administrador podrán registrar y consultar la información mencionada.
4. Confirmó que el instalador utiliza la plataforma y aporta los datos de los materiales consumidos.

Después, la IA propuso:

HU-13: Como administrador, quiero corregir un consumo de material registrado por error, dejando constancia del ajuste, para que las existencias de la sede reflejen el consumo real.

El usuario confirmó expresamente que el administrador debe poder hacer esa corrección.

### Resultado final

Quedaron 12 historias aceptadas: HU-01 a HU-06 y HU-08 a HU-13.

HU-07 se conserva como descartada para mantener el registro del cambio.

Las historias completas y revisadas están en:

[Consultar requisitos](../requisitos.md)

### Pendientes

- Precisar las unidades de medida y la precisión de las cantidades: identificar al instalador como fuente no resuelve todavía esta decisión.
- Revisar las historias con Jonathan.
- Asignar prioridades MoSCoW.
- Escribir criterios de aceptación Gherkin para las historias Must.

## P-05 — Priorizar historias con MoSCoW

### Datos de la prueba

- Fecha: 5 de septiembre de 2026.
- Herramienta: Codex.
- Objetivo: proponer prioridades según la demostración principal.
- Estado: ejecutado; priorización pendiente de revisión del equipo.

### Prompt utilizado

Actúa como analista de requisitos para un proyecto académico pequeño.

CONTEXTO:
Somos dos estudiantes y desarrollaremos un sistema para las dos sedes de Serna Polarizados en Ibagué. Ambas comparten clientes, vehículos e historial de trabajos, pero cada sede mantiene su propio inventario.

La demostración principal debe permitir registrar un cliente y su vehículo, registrar una entrada de material, registrar un trabajo, asociarle un consumo y comprobar que solo disminuye el inventario de la sede correspondiente. El historial del vehículo debe poder consultarse desde ambas sedes.

Estas son las historias aceptadas:

- HU-01: registrar cliente.
- HU-02: consultar cliente por documento.
- HU-03: registrar vehículo asociado a un cliente.
- HU-04: consultar vehículo por placa.
- HU-05: registrar trabajo con vehículo, sede, fecha, servicio y valor total.
- HU-06: consultar historial del vehículo desde ambas sedes.
- HU-08: registrar material y su unidad de medida.
- HU-09: registrar entrada de material por sede.
- HU-10: registrar consumo asociado a un trabajo y descontarlo de la sede correspondiente.
- HU-11: consultar existencias por sede.
- HU-12: consultar materiales y cantidades consumidos en un trabajo.
- HU-13: permitir al administrador corregir un consumo erróneo, dejando constancia del ajuste.

HU-07, consultar trabajos por sede y periodo, fue descartada expresamente.

TAREA:
Propón una prioridad MoSCoW para cada historia aceptada y explica brevemente su motivo. Considera las dependencias necesarias para completar la demostración principal.

FORMATO:
Una tabla con las columnas ID, Historia, Prioridad y Justificación. Después, explica en lenguaje sencillo qué podría aplazarse y qué efecto tendría. Registra HU-07 por separado como fuera de alcance.

RESTRICCIONES:
La priorización es una propuesta pendiente de revisión del equipo. No cambies los identificadores ni agregues funciones. No reincorpores HU-07. No inventes porcentajes obligatorios para cada categoría: si una categoría queda vacía, está bien. Diferencia lo indispensable para que funcione el recorrido principal de lo que puede esperar. No generes código ni criterios Gherkin todavía.

EJEMPLO:
HU-09 | Registrar entrada de material | Must | Permite disponer de existencias para demostrar el consumo de materiales.

### Resumen de la respuesta obtenida

La IA propuso:

- Must: HU-01, HU-03, HU-05, HU-06, HU-08, HU-09, HU-10 y HU-11.
- Should: HU-02, HU-04, HU-12 y HU-13.
- Could: ninguna.
- Won’t: HU-07, previamente descartada.

Justificación general:

Las historias Must permiten completar el recorrido desde el registro del cliente hasta la comprobación del inventario y la consulta del historial entre sedes.

Las búsquedas por documento y placa se propusieron como Should, condicionadas a que las funciones principales permitan seleccionar correctamente clientes y vehículos.

La consulta detallada de materiales por trabajo se propuso como Should, manteniendo obligatoria la relación entre consumo y trabajo.

La corrección de consumos se propuso como Should para la demostración académica, señalando que debería completarse antes de utilizar el sistema en una operación real.

### Comentarios de revisión asistida

Qué funcionó:

- Clasificó las doce historias aceptadas.
- Conservó HU-07 fuera del alcance.
- Justificó las prioridades según la demostración.
- No forzó el uso de todas las categorías.
- Explicó los efectos de aplazar funciones.
- No generó código ni criterios Gherkin.

Limitaciones:

- Aplazar HU-02 y HU-04 depende de una forma de selección que todavía debe detallarse.
- La importancia de corregir consumos debe revisarse con el equipo; su prioridad no quedó confirmada por el usuario.
- La clasificación se orientó a una demostración académica, no a una operación real completa.

### Correcciones y decisiones pendientes

No se modificó ni aprobó todavía la clasificación propuesta.

El equipo debe decidir:

1. Si las búsquedas por documento y placa deben ser Must.
2. Si la corrección de consumos debe ser Must.
3. Si acepta las demás prioridades.

### Revisión humana pendiente

La ejecución de este prompt no equivale a aprobar sus resultados.

La revisión conjunta con Jonathan y la evaluación por otro equipo siguen pendientes.
