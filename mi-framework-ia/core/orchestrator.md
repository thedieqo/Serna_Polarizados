# Orchestrator — Serna Polarizados

> **Guía documental; ejecución no acreditada.** No existe un motor de orquestación, un planificador ni una cadena ejecutable de agentes. Este documento solo describe cómo podría coordinarse el trabajo humano con las guías del framework.

## Propósito

Orientar la revisión y producción de artefactos de desarrollo, manteniendo la coherencia entre requisitos, frontend, backend, base de datos y revisión humana.

## Participantes documentales

- [`requirements_agent.md`](../agents/requirements_agent.md) y [`requirements_analysis.md`](../skills/requirements_analysis.md): análisis de requisitos.
- [`backend_agent.md`](../agents/backend_agent.md) y [`backend_generation.md`](../skills/backend_generation.md): apoyo al backend.
- [`frontend_agent.md`](../agents/frontend_agent.md) y [`frontend_generation.md`](../skills/frontend_generation.md): apoyo al frontend.
- [`reviewer_agent.md`](../agents/reviewer_agent.md) y [`code_review.md`](../skills/code_review.md): revisión crítica.
- [`database_design.md`](../skills/database_design.md): análisis de persistencia.

En F3 estas guías son documentación de apoyo. No hay agentes conectados, herramientas instaladas ni ejecución autónoma.

## Flujo propuesto

```text
Necesidad documentada
→ análisis de requisitos
→ revisión de alcance
→ diseño de datos, si aplica
→ trabajo de backend o frontend, si está autorizado
→ revisión
→ validación humana
```

El flujo es una secuencia de trabajo sugerida, no una promesa de automatización.

## Reglas de coordinación

1. Leer primero la documentación vigente y este archivo de configuración.
2. Contrastar toda propuesta con los requisitos y con el código existente.
3. Distinguir explícitamente entre antecedente, estado actual y propuesta futura.
4. No implementar funcionalidades sin autorización de alcance.
5. Mantener los contratos de datos entre frontend, schemas y modelos.
6. No inventar resultados de ejecución, pruebas o uso de IA.
7. No exponer credenciales ni información sensible.
8. Registrar supuestos y límites cuando falte información.

## Flujos por tarea

| Tarea | Secuencia documental |
|---|---|
| Requisitos | Requirements Agent → Requirements Analysis → Reviewer Agent |
| Base de datos | Requirements Agent → Database Design → Reviewer Agent |
| Backend | Backend Agent → Backend Generation → Code Review |
| Frontend | Frontend Agent → Frontend Generation → Code Review |

## Criterio de finalización

Una tarea se considera terminada cuando responde a un requisito autorizado, fue revisada por una persona, no amplía el alcance por iniciativa propia y puede explicarse con la evidencia disponible.

## Límites

- No se agregan archivos ejecutables, dependencias ni integraciones.
- No se afirma que el flujo haya sido ejecutado.
- La carpeta `core/` contiene únicamente `__init__.py` y este documento.
- La revisión humana es obligatoria antes de aceptar cualquier salida.
