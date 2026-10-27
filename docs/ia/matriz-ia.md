# Uso de IA en Serna Polarizados

## 1. Contexto

**Fecha de actualización:** 27 de octubre de 2026 (F2).

Proyecto académico para las dos sedes de Serna Polarizados en Ibagué. La primera versión documentada incluye clientes, vehículos, historial de trabajos e inventario independiente por sede, con identificación de rollos y recortes aprovechables.

El repositorio contiene una implementación parcial de clientes, vehículos e instalaciones. El inventario, la autenticación, las migraciones y las pruebas automatizadas siguen pendientes. La existencia de código no demuestra que la aplicación haya sido ejecutada o probada.

La matriz describe el uso de IA documentado y las herramientas candidatas para fases futuras. Las herramientas candidatas no se presentan como utilizadas.

## 2. Matriz de uso de IA

| Fase | Tarea con apoyo de IA | Herramientas utilizadas o candidatas | Riesgo y revisión del equipo |
| --- | --- | --- | --- |
| Planeación | Ayudar a delimitar la primera versión, proponer prioridades y organizar actividades. | Codex utilizado; apoyo futuro sujeto a la tarea. | Puede ampliar el alcance o proponer plazos sin fundamento. Revisaremos las propuestas según las necesidades confirmadas y la capacidad de los dos integrantes. |
| Análisis de requisitos | Obtener borradores de requisitos e historias a partir de la entrevista y las aclaraciones; revisar criterios de aceptación y trazabilidad. | Gemini y Codex utilizados. | Puede inventar reglas o confundir propuestas con decisiones. Contrastaremos cada resultado con las fuentes y conservaremos los pendientes de validación. |
| Diseño | Proponer responsabilidades de las capas, pantallas, relaciones de datos y diagramas. | Codex utilizado para el diseño inicial. El diseño actual se contrastó con el código en F2. | Puede omitir relaciones o asumir cómo funcionan los cortes y las correcciones. Revisaremos el diseño contra los requisitos vigentes. |
| Codificación | Implementar clientes, vehículos e instalaciones con Python, FastAPI, SQLAlchemy, React, TypeScript y Tailwind CSS. | El repositorio contiene código. Los documentos no registran de forma suficiente qué herramienta generó cada archivo, por lo que no se atribuye a una ejecución concreta. | Puede generar código incorrecto o que no comprendamos. Debe leerse, explicarse y comprobarse cada cambio antes de incorporarlo. |
| Pruebas | Proponer y apoyar comprobaciones de clientes, vehículos, trabajos e inventario por sede. | Herramienta candidata; no hay pruebas automatizadas registradas. | Puede omitir errores importantes. Deben comprobarse duplicados, dimensiones inválidas, piezas de otra sede, permisos y fallos de guardado, según los requisitos definidos. |
| Despliegue | Ayudar a preparar instrucciones de instalación y configuración. | Herramienta candidata; fase pendiente. | Puede sugerir configuraciones inadecuadas. Revisaremos las instrucciones y evitaremos publicar credenciales. |
| Mantenimiento | Ayudar a analizar errores y proponer correcciones. | Herramienta candidata; fase pendiente. | Puede diagnosticar sin evidencia. Reproduciremos el problema y comprobaremos la solución antes de aceptarla. |

Los editores de diagramas sirven para representar y revisar el diseño. Su utilización, por sí sola, no demuestra una ejecución de IA ni una conexión MCP.

## 3. Uso realizado hasta el momento

Se ha utilizado IA para:

- Revisar el alcance y distinguir reglas confirmadas de decisiones pendientes.
- Preparar borradores de visión y análisis competitivo.
- Proponer requisitos, historias y prioridades.
- Revisar resultados de Gemini e identificar errores.
- Organizar criterios de aceptación y trazabilidad.
- Proponer el diseño inicial de backend y frontend.
- Actualizar documentos después de las aclaraciones sobre rollos y sobrantes.

El código actual incluye modelos, esquemas, CRUD, endpoints y una interfaz React. La documentación no conserva, para cada archivo, el prompt exacto y la respuesta que habrían originado ese código. Esa falta de evidencia debe declararse y no atribuirse a una herramienta específica.

Los criterios escritos son especificaciones para pruebas futuras. No equivalen a pruebas ejecutadas ni a software completamente funcionando. F2 tampoco ejecutó la aplicación.

## 4. Evidencias

| Documento | Evidencia que conserva |
| --- | --- |
| [Entrevista y aclaraciones](entrevista-cliente.md) | Contexto del negocio y decisiones posteriores del administrador. |
| [Biblioteca de prompts](prompts.md) | Instrucciones utilizadas, resultados y observaciones. |
| [Pruebas con Gemini](pruebas-gemini.md) | Prompts de análisis y resúmenes de sus resultados. |
| [Revisión de historias](revision-historias-gemini.md) | Evaluación de historias, errores señalados y correcciones posteriores. |
| [Requisitos vigentes](../requisitos.md) | Resultado consolidado, reglas confirmadas y decisiones pendientes. |
| [Prompt maestro original](PROMPT_MAESTRO_ORIGINAL.md) | Extracción literal verificada del bloque entregado al equipo. |
| [Línea base F0](../F0_LINEA_BASE_Y_VERIFICACIONES.md) | Respaldo, huellas y verificaciones de la intervención inicial. |
| [Índice documental](../INDICE_DOCUMENTAL.md) | Clasificación, estado y registro de fases. |
| [Trazabilidad](../trazabilidad.md) | Relación entre requisitos, historias y código observado. |

Las respuestas completas de Gemini que aún no estén incorporadas siguen pendientes. No se presenta un resumen como si fuera la respuesta original completa.

## 5. Responsabilidad del equipo

La IA propone borradores. Los integrantes deben comprender, revisar y corregir lo que incorporan al proyecto.

Para cada uso se registrará:

- La herramienta y la fecha.
- El prompt utilizado.
- La respuesta o un resumen identificado como tal.
- Los errores o limitaciones encontrados.
- Las correcciones realizadas.
- La revisión humana efectuada y lo que siga pendiente.

Los prompts históricos se conservarán en su idioma original. Las traducciones o versiones mejoradas se identificarán como tales y solo se marcarán como ejecutadas después de probarlas.

La revisión conjunta con Jonathan y la validación posterior de los requisitos derivados con la asesora siguen pendientes.

Ninguna respuesta de IA se considerará, por sí sola, una decisión del negocio o una prueba de que el sistema funciona. Tampoco se afirmará que una herramienta generó el código si no existe evidencia suficiente.
