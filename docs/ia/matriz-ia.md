# Uso de IA en Serna Polarizados

## 1. Contexto

**Fecha de actualización:** 8 de septiembre de 2026.

Proyecto académico para las dos sedes de Serna Polarizados en Ibagué. La primera versión incluye clientes, vehículos, historial de trabajos e inventario independiente por sede, con identificación de rollos y recortes aprovechables.

El proyecto está en análisis y diseño. La implementación está pendiente.

La siguiente matriz describe cómo se utilizará la IA durante las siete fases del ciclo de vida del software. Las herramientas candidatas para fases futuras no se presentan como utilizadas.

## 2. Matriz de uso de IA

| Fase | Tarea con apoyo de IA | Herramientas utilizadas o candidatas | Riesgo y revisión del equipo |
| --- | --- | --- | --- |
| Planeación | Ayudar a delimitar la primera versión, proponer prioridades y organizar actividades. | Codex utilizado; apoyo futuro sujeto a la tarea. | Puede ampliar el alcance o proponer plazos sin fundamento. Revisaremos las propuestas según las necesidades confirmadas y la capacidad de los dos integrantes. |
| Análisis de requisitos | Obtener borradores de requisitos e historias a partir de la entrevista y las aclaraciones; revisar criterios de aceptación y trazabilidad. | Gemini y Codex utilizados. | Puede inventar reglas o confundir propuestas con decisiones. Contrastaremos cada resultado con las fuentes y conservaremos los pendientes de validación. |
| Diseño | Proponer responsabilidades de las capas, pantallas, relaciones de datos y diagramas. | Codex utilizado para el diseño inicial; revisión de diagramas pendiente. | Puede omitir relaciones o asumir cómo funcionan los cortes y las correcciones. Revisaremos el diseño contra los requisitos vigentes antes de programar. |
| Codificación | Apoyar funciones pequeñas con Python, Flask, SQLite, HTML, CSS y JavaScript. | Codex como candidato; fase pendiente. | Puede generar código incorrecto o que no comprendamos. Leeremos, explicaremos y comprobaremos cada cambio antes de incorporarlo. |
| Pruebas | Proponer y apoyar comprobaciones de clientes, vehículos, trabajos e inventario por sede. | Codex o Gemini como candidatos; ejecución de pruebas de software pendiente. | Puede omitir errores importantes. Comprobaremos duplicados, dimensiones inválidas, piezas de otra sede, permisos y fallos de guardado, según los requisitos definidos. |
| Despliegue | Ayudar a preparar instrucciones de instalación y configuración. | Codex como candidato; fase pendiente. | Puede sugerir configuraciones inadecuadas. Revisaremos las instrucciones y evitaremos publicar credenciales. |
| Mantenimiento | Ayudar a analizar errores y proponer correcciones. | Codex como candidato; fase pendiente. | Puede diagnosticar sin evidencia. Reproduciremos el problema y comprobaremos la solución antes de aceptarla. |

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

Los criterios escritos son especificaciones para pruebas futuras. No equivalen a pruebas ejecutadas ni a software funcionando.

## 4. Evidencias

| Documento | Evidencia que conserva |
| --- | --- |
| [Entrevista y aclaraciones](entrevista-cliente.md) | Contexto del negocio y decisiones posteriores del administrador. |
| [Biblioteca de prompts](prompts.md) | Instrucciones utilizadas, resultados y observaciones. |
| [Pruebas con Gemini](pruebas-gemini.md) | Prompts de análisis y resúmenes de sus resultados. |
| [Revisión de historias](revision-historias-gemini.md) | Archivo destinado a la evaluación de historias y sus correcciones; contenido pendiente de ajuste. |
| [Requisitos vigentes](../requisitos.md) | Resultado consolidado, reglas confirmadas y decisiones pendientes. |

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

Ninguna respuesta de IA se considerará, por sí sola, una decisión del negocio o una prueba de que el sistema funciona.
