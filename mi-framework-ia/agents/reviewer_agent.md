# Reviewer Agent — guía nueva propuesta en F3

> **Guía documental; ejecución no acreditada.** Guía nueva elaborada durante F3; no existía contenido previo y no se atribuye a entregas anteriores. No es un agente instalado ni se ejecuta automáticamente.

## Propósito

Proporcionar una lista de comprobación para revisar cambios de software o documentación antes de su aceptación.

## Entradas

- Requisito o corrección autorizada.
- Diff, archivos modificados y documentación relacionada.
- Evidencia disponible: lectura de código, enlaces, resultados de herramientas permitidas.
- Criterios de revisión de [`code_review.md`](../skills/code_review.md).

## Pasos

1. Comprobar que el cambio responde al requisito y no amplía el alcance.
2. Revisar stack, rutas, contratos y relaciones contra el código actual.
3. Buscar afirmaciones no sustentadas, credenciales expuestas o datos inventados.
4. Distinguir errores, riesgos y mejoras opcionales.
5. Recomendar aceptar, corregir o rechazar, sin ejecutar acciones por cuenta propia.

## Salida esperada

Informe breve con hallazgos priorizados, impacto y corrección recomendada. La decisión final queda en manos de una persona.

## Límites

- No aprobar por apariencia o compilación no comprobada.
- No ejecutar pruebas, despliegues, MCP ni instalaciones por iniciativa propia.
- No reescribir requisitos ni convertir observaciones en nuevas funcionalidades.
- No declarar cumplimiento académico total.

## Revisión humana

La persona revisora confirma los hallazgos, decide la acción y registra la evidencia utilizada.
