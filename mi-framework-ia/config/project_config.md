# Configuración del Proyecto — Serna Polarizados

## Proyecto
Serna Polarizados - Sistema de Gestión Administrativa y Operativa

## Contexto
Sistema web para centralizar la operación de Serna Polarizados, inicialmente en dos sedes, incluyendo Ibagué.

## Problema
Actualmente información de clientes, vehículos, servicios, citas, inventario, pagos e historial se encuentra dispersa y depende de procesos manuales.

## Flujo principal
Cliente → Vehículo → Servicio → Instalación → Inventario → Pago → Historial

## Roles
- Administrador
- Asesor
- Instalador
- Cliente mediante QR

## Módulos MVP
- Clientes y vehículos
- Citas y servicios
- Instaladores
- Inventario
- Pagos
- Historial
- Reportes básicos

## Servicios
- Polarizados
- PPF
- Detailing
- Wrap
- Lavado
- Barbería

## Arquitectura
Monolito en capas:
- Presentación
- Lógica de negocio
- Acceso a datos
- Base de datos

## Stack propuesto
- Frontend: HTML, CSS y JavaScript
- Backend: Python + Flask
- Base de datos: SQLite
- Diagramas: Mermaid
- Control de versiones: Git + GitHub

## Restricciones
- Mantener alcance académico y manejable.
- No implementar microservicios.
- No almacenar secretos en Git.
- No inventar requisitos.
- Todo código generado por IA debe ser revisado y probado.
- Priorizar historias Must del MVP.