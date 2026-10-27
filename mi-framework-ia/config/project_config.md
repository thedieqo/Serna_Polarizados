# Configuración del Proyecto — Serna Polarizados

> **Guía documental; ejecución no acreditada.** Este archivo describe el contexto y las convenciones del proyecto. No configura un motor, un agente ejecutable ni un flujo automático.

## 1. Identidad y contexto

Serna Polarizados requiere un sistema web para organizar la operación administrativa y técnica. La visión, las reglas y el alcance académico se documentan en [`docs/requisitos.md`](../../docs/requisitos.md) y [`docs/vision.md`](../../docs/vision.md).

El contexto previo planteaba centralizar clientes, vehículos, servicios, citas, inventario, pagos e historial, inicialmente para dos sedes, incluida Ibagué. Esa motivación se conserva como propuesta; no describe módulos ya implementados.

El flujo de negocio propuesto es:

Cliente → Vehículo → Servicio → Instalación → Inventario → Pago → Historial

Ese flujo es una **referencia de alcance**, no una descripción de funcionalidades implementadas. El inventario, los pagos, las sedes y el historial específico todavía no existen en el código.

## 2. Estado actual comprobable

- El frontend permite gestionar clientes, vehículos e instalaciones mediante pestañas.
- El backend expone rutas para clientes, vehículos e instalaciones en `/api/v1`.
- La persistencia se define con SQLAlchemy sobre PostgreSQL.
- No hay autenticación, roles, permisos, migraciones, inventario, pagos, sedes ni pruebas automatizadas.
- La aplicación no se ha ejecutado ni probado en F0–F3; la evidencia es estática.

## 3. Stack actual

| Parte | Tecnología observada |
|---|---|
| Frontend | React 18 + TypeScript + Vite 5 + Tailwind CSS 3 + Axios |
| Backend | FastAPI + Pydantic v2 + SQLAlchemy 2 |
| Base de datos | PostgreSQL; `DATABASE_URL` puede apuntar a Supabase, extremo no verificado en F3 |
| Diagramas | Mermaid |
| Control de versiones | Git + GitHub |

`react-router-dom` está instalado, pero la navegación actual usa `useState` en `frontend/src/App.tsx`.

## 4. Arquitectura actual por capas

| Capa | Carpetas existentes | Responsabilidad concreta |
|---|---|---|
| Presentación | `frontend/src/pages`, `frontend/src/components` | Formularios, listados, estados de carga y mensajes de error. |
| Cliente HTTP | `frontend/src/services` | Centraliza Axios, la URL base y las llamadas a la API. |
| Contratos TypeScript | `frontend/src/types` | Define las formas de cliente, vehículo e instalación. |
| Rutas HTTP | `backend/app/api/v1` | Recibe solicitudes, valida parámetros y traduce errores a respuestas HTTP. |
| Lógica de aplicación | `backend/app/crud` | Ejecuta consultas y reglas simples de creación y lectura. |
| Contratos y validación | `backend/app/schemas` | Define entrada y salida con Pydantic. |
| Modelo ORM | `backend/app/models` | Declara tablas, atributos y relaciones de SQLAlchemy. |
| Configuración y sesión | `backend/app/core`, `backend/app/db` | Lee variables de entorno y construye el engine y las sesiones. |

La entrada del backend está en `backend/app/main.py`. La aplicación monta los routers con el prefijo `/api/v1`.

## 5. Alcance propuesto, no implementado

Los siguientes elementos aparecen en la visión, la configuración previa o la planificación, pero **no deben presentarse como código existente**:

- sedes e inventario por sede;
- citas, pagos, reportes y garantías;
- autenticación, RBAC y portal del cliente;
- historial específico y normalización de detalles de instalación;
- migraciones y pruebas automatizadas.

Roles previstos: Administrador, Asesor, Instalador y Cliente mediante QR. Módulos previstos: clientes y vehículos, citas y servicios, instaladores, inventario, pagos, historial y reportes básicos. Servicios previstos: polarizados, PPF, detailing, wrap, lavado y barbería.

Ninguno de esos roles, módulos o servicios se declara implementado. Toda incorporación requiere una decisión de alcance explícita.

## 6. Antecedente preservado

El diseño inicial del framework proponía HTML, CSS y JavaScript con Python/Flask y SQLite. Ese antecedente se conserva en los diagramas históricos de `docs/diagramas/` y no describe la implementación actual. La sustitución del stack se documenta en F2 y F3; no se atribuye al código una tecnología que no usa.

## 7. Restricciones

- Mantener el alcance académico y evitar microservicios.
- No inventar requisitos, resultados ni funcionalidades.
- No almacenar secretos, credenciales ni cadenas de conexión reales en Git.
- Toda propuesta de IA debe revisarse contra el código y los requisitos, y probarse cuando exista una prueba aplicable.
- No afirmar que una guía documental se ejecuta automáticamente ni que una salida fue probada sin evidencia.
- Priorizar las historias Must solo si están aprobadas y siguen vigentes.
