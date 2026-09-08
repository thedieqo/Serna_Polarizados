# Revisión de historias con Gemini — Serna Polarizados

## 1. Datos de la revisión

- Documento evaluado: `requisitos.md`, versión consolidada del 8 de septiembre de 2026, anterior a la reorganización posterior de escenarios.
- Herramienta: Gemini, según la respuesta compartida por el integrante del proyecto.
- Modelo específico: no registrado.
- Fecha exacta de ejecución: pendiente de confirmar; la fecha del documento evaluado no demuestra la fecha de ejecución.
- Evidencia: respuesta de Gemini compartida en la conversación y reproducida a continuación.
- Prompt exacto de esta ejecución: no incluido en este archivo; pendiente de incorporar desde el registro original.

Este archivo conserva la evaluación, no una copia del documento de requisitos. Los requisitos actuales se consultan en [requisitos.md](../requisitos.md).

La respuesta original contiene errores señalados en la sección 3. Se conserva para mostrar qué produjo la herramienta y qué se corrigió después. No se presenta como una aprobación completa de las historias.

## 2. Respuesta original de Gemini

Basado estrictamente en la versión consolidada del documento de requisitos con fecha 8 de septiembre de 2026, presento la revisión de las historias de usuario frente a sus requisitos funcionales vinculados y criterios de aceptación.

---

### 1. Tabla de evaluación de historias de usuario

| ID | Título exacto actual | Requisitos funcionales vinculados | Hallazgo breve de revisión |
| --- | --- | --- | --- |
| **HU-01** | Registrar cliente | RF-01 | Cubre el registro exitoso y la validación de documento duplicado. Alineada con RF-01. |
| **HU-02** | Consultar cliente | RF-03 | Cubre la consulta por documento y el mensaje de no coincidencia. Alineada con RF-03. |
| **HU-03** | Registrar vehículo | RF-02 | Registra vehículos vinculados a un cliente existente y valida placas duplicadas. Alineada con RF-02. |
| **HU-04** | Consultar vehículo | RF-03 | Cubre la búsqueda por placa y la identificación del cliente asociado. Alineada con RF-03. |
| **HU-05** | Registrar trabajo y detalles | RF-04, RF-05 | Registra trabajos y detalles de instalación. Requiere concretar la estructura/campos obligatorios de detalles y la representación de múltiples tecnologías, opacidades o instaladores. |
| **HU-06** | Consultar historial | RF-06 | Permite consultar el historial del vehículo desde ambas sedes. Alineada con RF-06. |
| **HU-08** | Registrar tipo de material | RF-07 | Permite registrar tecnologías y opacidades para caracterizar materiales. Alineada con RF-07. |
| **HU-09** | Registrar rollo recibido | RF-08, RF-16 | Controla el ingreso de rollos con medidas positivas en centímetros e independización por sede. Alineada con RF-08 y RF-16. |
| **HU-10** | Registrar uso y sobrantes | RF-09, RF-10, RF-15, RF-16 | Contempla uso, sobrantes aprovechables, validación por sede y atomicidad (RF-15). Pendiente definir la mecánica exacta del registro del corte y del restante. |
| **HU-11** | Consultar disponibilidad | RF-11 | Muestra rollos y recortes por sede/material/dimensiones, excluyendo descartados. Alineada con RF-11. |
| **HU-12** | Consultar material de un trabajo | RF-12 | Asocia piezas y uso a un trabajo específico. Alineada con RF-12. |
| **HU-13** | Corregir registro de uso | RF-13 | Exclusivo del administrador con trazabilidad y atomicidad. Pendiente definir reglas específicas para sobrantes que ya han sido utilizados posteriormente. |
| **HU-14** | Descartar pieza dañada | RF-14 | Permite al administrador retirar del inventario disponible piezas dañadas. Su prioridad se encuentra explícitamente pendiente. |

---

### 2. Lista de comprobación corta (Checklist)

* **Rol:** Cumplido. Todas las historias definen un rol claro (*Asesor*, *Instalador* o *Administrador*).
* **Acción:** Cumplido. Cada historia expresa con precisión la funcionalidad requerida.
* **Beneficio:** Cumplido. Se clarifica el valor de negocio de cada acción en el enunciado de la historia.
* **Alcance:** Incompleto / Incierto en casos limítrofes. El alcance general excluye explícitamente facturación, comisiones, agendas y cálculo automático de cortes; sin embargo, existen casos de uso de inventario cuyos límites operativos no están cerrados.
* **Criterios de aceptación comprobables:** Parcialmente cumplido. La mayoría de los escenarios son directamente verificables mediante criterios Dado/Cuando/Entonces, pero carecen de especificidad en las reglas de corte y detalles de instalación.
* **Preguntas o puntos sin resolver:** Presentes explícitamente. Se identifican aspectos críticos no resueltos respecto al detalle de trabajos, precisión de medidas, cortes y correcciones dependientes.

---

### 3. Correcciones específicas y puntos no resueltos

Sin modificar ninguna de las decisiones confirmadas ni reescribir prioridades o unidades de medida aprobadas (como el uso estricto de centímetros), se requieren las siguientes precisiones:

1. **Definición del registro de corte y material restante (HU-10 / RF-09, RF-10):**
* Es un punto sin resolver cómo se registrará operativamente la pieza cortada y la deducción exacta del restante en la pieza de origen, dado que el documento explicita que no basta comparar áreas.


2. **Estructura detallada de instalación (HU-05 / RF-05):**
* Está sin resolver la estructura de datos obligatoria para el registro de instalación, así como el mecanismo para soportar múltiples tecnologías, opacidades o instaladores en un mismo trabajo.


3. **Reglas de corrección para sobrantes utilizados (HU-13 / RF-13):**
* Es un punto sin resolver cómo debe comportarse el sistema al corregir un registro de uso si el sobrante derivado de esa operación ya fue utilizado en un trabajo posterior.


4. **Tratamiento de daños parciales y anulaciones (HU-14 / RF-14):**
* HU-14 solo contempla el descarte de piezas completas. Falta definir las reglas de negocio para material dañado parcialmente, anulaciones y registro de material equivocado.


5. **Precisión de las dimensiones:**
* Aunque está confirmado que las dimensiones se registran en centímetros y deben ser positivas, permanece sin resolver el nivel de precisión decimal requerido para las medidas.


6. **Prioridad de la historia HU-14:**
* La historia HU-14 (*Descartar pieza dañada*) tiene su prioridad como **pendiente de asignación** y debe ser priorizada por el equipo.


7. **Matriz de permisos y perfiles:**
* La matriz detallada de permisos e identificación formal de usuarios permanece sin resolver, aun cuando la exclusividad del Administrador para corregir (HU-13) y descartar (HU-14) está confirmada.

## 3. Revisión posterior con apoyo de Codex

Las siguientes observaciones son posteriores a la respuesta anterior y no se atribuyen a Gemini.

| Punto | Qué se detectó | Corrección de interpretación |
| --- | --- | --- |
| HU-10: atribución de atomicidad a RF-15 | Gemini vinculó el guardado conjunto a RF-15. | La consistencia y el guardado completo corresponden a RNF-03. RF-15 exige mostrar éxito únicamente después del guardado correcto. |
| Checklist: acción totalmente precisa | Gemini calificó como cumplida la precisión de todas las acciones. | Debe considerarse parcial: HU-05, HU-10 y HU-13 conservan procedimientos o detalles sin cerrar. |
| Daños parciales, anulaciones y material equivocado | La respuesta agrupó estos pendientes bajo HU-14 y RF-14. | HU-14 cubre únicamente el descarte completo. Los demás casos no son funciones automáticamente aprobadas ni pertenecen todos al descarte. Su tratamiento debe decidirse según los requisitos. |
| Historias alineadas con requisitos | La correspondencia entre una historia y su RF puede ser correcta. | Eso no demuestra que la historia tenga todos sus criterios completos, que sea estimable ni que esté implementada. |

## 4. Checklist interpretado después de la revisión

Esta tabla resume la revisión asistida posterior; no es una segunda respuesta de Gemini.

| Aspecto | Estado | Justificación |
| --- | --- | --- |
| Rol | Cumple en los enunciados | Las historias identifican asesor, instalador o administrador. La matriz completa de permisos sigue pendiente. |
| Acción | Parcial | Existen acciones reconocibles, pero HU-05, HU-10 y HU-13 necesitan precisiones. |
| Beneficio | Cumple en los enunciados | Las historias explican para qué se necesita la acción. |
| Alcance | Parcial | Las exclusiones generales están identificadas; algunos procedimientos de inventario siguen abiertos. |
| Criterios verificables | Parcial | Hay escenarios de éxito y error, pero no se han cerrado todas las reglas necesarias para probar las historias. |
| Pendientes explícitos | Cumple | Se reconocen detalles de instalación, corte, corrección, precisión, permisos y prioridad de HU-14. |

Este checklist no constituye una evaluación completa de INVEST. No se han demostrado la estimación ni el tamaño de todas las historias.

## 5. Seguimiento respecto a los requisitos actuales

Después de la evaluación se reorganizó el documento de requisitos con apoyo de Codex:

- Se separaron escenarios de consultas con y sin resultados.
- Se explicitó la conservación de varios vehículos por cliente.
- Se relacionó el guardado completo con RNF-03.
- Se organizaron escenarios de validación y fallo de guardado.
- Se conservaron visibles los pendientes de HU-05, HU-10 y HU-13.
- HU-14 mantuvo su prioridad pendiente.
- HU-07 permaneció descartada.

Esta actualización documental no se presenta como una nueva revisión realizada por Gemini.

## 6. Pendientes

- Incorporar el prompt exacto de esta ejecución y confirmar su fecha si se conserva el registro.
- Precisar la estructura de los detalles de instalación de HU-05.
- Definir el registro de corte y restante de HU-10.
- Definir las correcciones de HU-13 cuando existen sobrantes utilizados posteriormente.
- Definir la precisión de las medidas en centímetros.
- Asignar prioridad a HU-14 y revisar el esfuerzo del inventario.
- Completar la identificación de usuarios y los permisos detallados.
- Revisar conjuntamente con Jonathan y validar los resultados derivados con la asesora.

Los pendientes de negocio no se resuelven mediante una calificación favorable de la IA. Su estado vigente se mantiene en [requisitos.md](../requisitos.md).

## 7. Resultado

Se recuperó la evaluación original de Gemini y se documentaron sus errores y las correcciones posteriores, conservando las 13 historias activas y HU-07 fuera del alcance.

La revisión es evidencia del análisis de requisitos. No demuestra que exista software implementado, pruebas ejecutadas ni aprobación conjunta del equipo.

