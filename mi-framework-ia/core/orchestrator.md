# Orchestrator — Serna Polarizados

## Propósito
Coordinar el uso de agentes y skills durante el desarrollo del sistema Serna Polarizados.

## Flujo general

Necesidad del negocio
→ Requirements Agent
→ Requirements Analysis
→ Database Design
→ Backend Agent
→ Backend Generation
→ Frontend Agent
→ Frontend Generation
→ Reviewer Agent
→ Code Review
→ Validación humana

## Reglas de orquestación

1. Leer primero `config/project_config.md`.
2. Consultar los requisitos existentes antes de generar soluciones.
3. Priorizar historias clasificadas como Must.
4. No implementar funcionalidades que no estén justificadas por requisitos.
5. Backend y frontend deben mantener coherencia con el mismo modelo de negocio.
6. Toda salida generada por IA debe pasar por revisión.
7. Ante información faltante, registrar el supuesto o solicitar aclaración.
8. No exponer contraseñas, tokens, API keys ni información sensible.

## Flujo por tarea

### Requisitos
Requirements Agent → Requirements Analysis → Reviewer Agent

### Base de datos
Requirements Agent → Database Design → Reviewer Agent

### Backend
Backend Agent → Backend Generation → Code Review

### Frontend
Frontend Agent → Frontend Generation → Code Review

## Criterio de finalización
Una tarea se considera terminada cuando:
- responde a un requisito;
- fue revisada;
- no introduce funcionalidades innecesarias;
- puede ser explicada por el equipo.