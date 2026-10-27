# Skill: Code Review — guía propuesta en F3

> **Guía documental; ejecución no acreditada.** No existe un revisor automático. La revisión final siempre la realiza una persona.

## Propósito

Revisar críticamente cambios de código y documentación generados con apoyo humano o de IA.

## Entradas

- Diff o propuesta de cambio.
- Requisito y alcance autorizado.
- Código actual de frontend, backend y configuración.
- Documentación vigente y evidencia disponible.

## Verificaciones

- El cambio responde al requisito y no amplía el alcance.
- Respeta React/TypeScript/Vite/Tailwind y FastAPI/SQLAlchemy/PostgreSQL.
- Mantiene coherencia entre componentes, servicios, tipos, routers, schemas, CRUD y modelos.
- Conserva nombres, validaciones y contratos existentes cuando corresponde.
- No expone credenciales ni datos sensibles.
- No presenta propuestas como funcionalidades implementadas.
- No afirma pruebas, ejecución o resultados sin evidencia.

## Salida esperada

Tabla breve:

| Problema | Impacto | Corrección recomendada |
|---|---|---|
| Hallazgo concreto | Riesgo técnico o académico | Acción mínima y verificable |

## Límites

- No aprobar un cambio solo porque compila o parece correcto.
- No convertir observaciones en nuevas funcionalidades.
- No sustituir la revisión humana ni inventar resultados de pruebas.

## Revisión humana

La persona revisora decide si acepta, corrige o rechaza el cambio, y deja constancia de la evidencia utilizada.
