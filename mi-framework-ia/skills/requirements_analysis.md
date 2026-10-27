# Skill: Requirements Analysis — guía nueva propuesta en F3

> **Guía documental; ejecución no acreditada.** Guía nueva elaborada durante F3; no existía contenido previo y no se atribuye a entregas anteriores. No analiza documentos automáticamente ni forma parte de un motor de orquestación.

## Propósito

Analizar requisitos existentes para detectar ambigüedades, dependencias y diferencias entre lo documentado y lo implementado.

## Entradas

- `docs/requisitos.md`, `docs/vision.md` y `docs/trazabilidad.md`.
- Historias, criterios de aceptación y decisiones registradas.
- Código actual cuando se necesite contrastar alcance.

## Pasos

1. Leer el requisito y localizar su fuente.
2. Identificar actor, necesidad, regla y resultado esperado.
3. Separar lo confirmado de supuestos y preguntas abiertas.
4. Contrastar con el código solo para describir el estado actual.
5. Detectar duplicidades, conflictos o dependencias no documentadas.
6. Proponer aclaraciones para revisión humana.

## Salida esperada

Tabla o lista con requisito, fuente, ambigüedad detectada, evidencia y pregunta o decisión pendiente. No se modifica el requisito original.

## Límites

- No inventar prioridades, actores ni aceptación del cliente.
- No aprobar alcance nuevo.
- No afirmar que una funcionalidad está implementada por aparecer en un documento.
- No ejecutar pruebas ni modificar archivos fuente.

## Revisión humana

La persona responsable decide qué aclaraciones son válidas y si el requisito debe actualizarse.
