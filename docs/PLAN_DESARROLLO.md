# PLAN DE DESARROLLO — SERNA POLARIZADOS

> Documento de planificación. No representa software implementado, pruebas ejecutadas ni funcionalidades desplegadas.

## 1. Contexto y objetivos del proyecto

**Contexto.** Serna Polarizados instala polarizados, películas de seguridad y PPF. La operación de sus sedes en Ibagué se apoya en Excel, formularios y registros manuales; la información está dispersa, recuperar antecedentes puede requerir llamadas y no se registran sistemáticamente entradas, cortes y sobrantes. El proyecto es, además, la actividad de la asignatura Electiva CPC.

**Objetivo general.** Construir un sistema web empresarial, responsive y preparado para evolucionar a PWA, que centralice clientes, vehículos, instalaciones, inventario por sede y garantías, con historial compartido entre sedes.

**Objetivos específicos.**
- Gestionar el flujo: nueva instalación → cliente → vehículo → sede → servicio → instaladores → materiales → guardado → historial del vehículo.
- Controlar inventario por sede (marcas, tecnologías, polarizados, películas de seguridad, PPF transparente/mate, opacidades, referencias, entradas, salidas, transferencias, consumo, sobrantes, desperdicios, existencias e historial).
- Gestionar garantías vinculadas a instalaciones específicas.
- Aplicar autenticación, roles, auditoría y un flujo de autorización superior para modificar registros existentes.
- Mantener registro documental del proyecto y trazabilidad requisito→historia→prueba.

**Estado de partida.** Repositorio en análisis y diseño, sin aplicación implementada, sin pruebas ejecutadas y sin assets visuales (logo, colores, tipografías, prototipo Stitch).

## 2. Requisitos funcionales y no funcionales

### 2.1 Requisitos funcionales vigentes (base documentada)

| ID | Requisito |
| --- | --- |
| RF-01 | Registrar clientes (nombre, documento, contacto) sin documentos duplicados. |
| RF-02 | Registrar vehículos (placa, descripción) asociados a un cliente, sin placas duplicadas. |
| RF-03 | Consultar clientes por documento y vehículos por placa. |
| RF-04 | Registrar trabajos/instalaciones con vehículo, sede, fecha, servicio y valor. |
| RF-05 | Registrar detalles de instalación (tecnología, opacidad, instalador, retiro de película). |
| RF-06 | Consultar historial del vehículo desde ambas sedes. |
| RF-07 | Registrar tipos de material diferenciando tecnología y opacidad. |
| RF-08 | Registrar rollos con identificación, sede, material y dimensiones en centímetros. |
| RF-09 | Registrar uso de material asociado a un trabajo y pieza de la misma sede. |
| RF-10 | Registrar sobrantes aprovechables sin duplicar existencias. |
| RF-11 | Consultar rollos y recortes disponibles por sede, material y dimensiones. |
| RF-12 | Consultar piezas y usos asociados a un trabajo. |
| RF-13 | Corregir registros de uso conservando consistencia y constancia del ajuste. |
| RF-14 | Descartar piezas completas dañadas con motivo. |
| RF-15 | Mostrar confirmación solo tras guardado correcto. |
| RF-16 | Validar dimensiones positivas y disponibilidad antes de aplicar operaciones. |

### 2.2 Requisitos funcionales nuevos (alcance ampliado del brief)

| ID | Requisito |
| --- | --- |
| RF-17 | Registrar instalación con superficies intervenidas e instaladores asignados por superficie. |
| RF-18 | Gestionar estados de instalación configurables. |
| RF-19 | Registrar marcas, tecnologías, tipo de película (incl. PPF transparente/mate), opacidades y referencias. |
| RF-20 | Registrar entradas y salidas de inventario por sede. |
| RF-21 | Registrar transferencias de material entre sedes con trazabilidad. |
| RF-22 | Registrar material consumido, instalado, sobrantes reutilizables y desperdicios. |
| RF-23 | Consultar existencias disponibles por sede y material. |
| RF-24 | Consultar historial de movimientos de inventario. |
| RF-25 | Registrar y consultar garantías relacionadas con instalaciones específicas. |
| RF-26 | Consultar historial por placa y por documento del cliente. |
| RF-27 | Solicitar y aprobar modificaciones de instalaciones/vehículos ya registrados. |

### 2.3 Requisitos no funcionales

| ID | Necesidad |
| --- | --- |
| RNF-01 | Registro utilizable desde teléfono. |
| RNF-02 | Flujo comprensible para instaladores con poca familiaridad tecnológica. |
| RNF-03 | Consistencia: operaciones completas o no aplicadas. |
| RNF-04 | Trazabilidad de correcciones (autor, fecha, motivo, datos antes/después). |
| RNF-05 | Respeto de permisos por perfil. |
| RNF-06 | Compatibilidad con dispositivos/navegadores acordados. |
| RNF-07 | Autenticación obligatoria. |
| RNF-08 | Auditoría de cambios. |
| RNF-09 | Protección de datos personales. |
| RNF-10 | Copias de seguridad y recuperación. |
| RNF-11 | Diseño responsive y PWA-ready. |
| RNF-12 | Rendimiento (umbral pendiente de aprobación). |

## 3. Historias de usuario

Se conservan 13 historias activas (HU-01 a HU-06, HU-08 a HU-14; **HU-07 descartada**). Se añaden historias para el alcance ampliado.

| ID | Historia | Requisitos | Prioridad |
| --- | --- | --- | --- |
| HU-01 | Registrar cliente | RF-01 | Must |
| HU-02 | Consultar cliente | RF-03 | Must |
| HU-03 | Registrar vehículo | RF-02 | Must |
| HU-04 | Consultar vehículo | RF-03 | Must |
| HU-05 | Registrar trabajo/instalación y detalles | RF-04, RF-05 | Must |
| HU-06 | Consultar historial | RF-06 | Must |
| HU-08 | Registrar tipo de material | RF-07 | Must (referencia) |
| HU-09 | Registrar rollo recibido | RF-08, RF-16 | Must (referencia) |
| HU-10 | Registrar uso y sobrantes | RF-09, RF-10, RF-15, RF-16 | Must (referencia) |
| HU-11 | Consultar disponibilidad | RF-11 | Must (referencia) |
| HU-12 | Consultar material de un trabajo | RF-12 | Should |
| HU-13 | Corregir registro de uso | RF-13 | Must (referencia) |
| HU-14 | Descartar pieza dañada | RF-14 | Pendiente |
| HU-15 | Registrar instalación con superficies e instaladores por superficie | RF-17, RF-04, RF-05 | Must (propuesta) |
| HU-16 | Gestionar estado de instalación | RF-18 | Must (propuesta) |
| HU-17 | Gestionar catálogo de materiales (incl. PPF) | RF-19 | Must (propuesta) |
| HU-18 | Transferir material entre sedes | RF-21, RF-24 | Must (propuesta) |
| HU-19 | Consultar historial por placa y documento | RF-26 | Must (propuesta) |
| HU-20 | Solicitar modificación de instalación/vehículo | RF-27 | Must (propuesta) |
| HU-21 | Aprobar modificación (Gerente) | RF-27 | Must (propuesta) |
| HU-22 | Registrar y consultar garantías | RF-25 | Must (propuesta) |

**Formato de criterios.** Cada historia mantendrá escenarios Gherkin (Dado/Cuando/Entonces) de éxito y error. Los criterios de HU-05, HU-10 y HU-13 permanecen parciales hasta cerrar las decisiones de la sección 11. Una historia con criterios esenciales pendientes no se considera terminada.

## 4. Arquitectura propuesta

**Estilo:** frontend SPA desacoplado + backend monolítico modular con API REST. No se usan microservicios.

```
[Navegador / PWA]
      │ HTTPS (JSON)
[Frontend React + TypeScript + Tailwind]  → Vercel
      │ API REST (JWT)
[Backend FastAPI]
  ├── Capa API (routers, esquemas Pydantic, validación)
  ├── Capa Servicios (reglas, permisos, transacciones, auditoría)
  └── Capa Repositorios/ORM (SQLAlchemy)
      │
[PostgreSQL — Supabase]
```

- **Consistencia:** operaciones de inventario e instalación como transacción única con rollback.
- **Datos compartidos:** clientes, vehículos, historial y garantías. **Datos por sede:** instalaciones, piezas, movimientos y transferencias.
- **Autorización de cambios:** solicitud → revisión → aprobación del Gerente/Administrador general → aplicación auditada.
- **Capas lógicas del backend:** presentación/API, negocio, acceso a datos, base de datos.
- **PWA:** manifest + service worker, sin reescritura futura.

## 5. Tecnologías propuestas y justificación

| Capa | Elección | Justificación |
| --- | --- | --- |
| Frontend | React + TypeScript + Tailwind CSS | Componentización, tipado, estilos consistentes; base para PWA y accesibilidad. |
| Hosting frontend | Vercel | Despliegue continuo, HTTPS y CDN para SPA/PWA. |
| Backend | Python + FastAPI | Tipado, validación Pydantic, OpenAPI automático, rendimiento async; continuidad con Python. |
| Hosting backend | PaaS compatible con Python (Render/Railway/Fly) | Portable y económico; se decide en preparación de despliegue. |
| Base de datos | PostgreSQL en Supabase | Relacional, transaccional, alojado, respaldos; RLS/auth opcionales. |
| Versionado | Git + GitHub | Ya utilizado por el equipo. |
| Diagramas | Mermaid | Ya utilizado. |
| PWA | Manifest + service worker | Evolución sin reescritura. |

**Nota de cambio.** Estas tecnologías **sustituyen** el stack documentado (Flask/SQLite/HTML-CSS-JS) por decisión del equipo. Implica migración de tipos SQLite→PostgreSQL y curva de aprendizaje React/FastAPI; se asume PostgreSQL desde el inicio para evitar doble migración. Costos: free tier al inicio, revisión de límites de Supabase/Vercel.

## 6. Plan de construcción del backend

- **Arquitectura:** routers API → servicios (reglas) → repositorios (SQLAlchemy); Pydantic para validación; errores uniformes; OpenAPI.
- **Autenticación:** login con JWT (access/refresh), hash de contraseñas con argon2/bcrypt, middleware de autorización.
- **Roles y permisos:** Administrador, Gerente, Asesor, Instalador. Corrección/descarte solo Administrador; aprobación de modificaciones solo Gerente; asesor/instalador según operación.
- **Módulos:**
  - Clientes y vehículos (unicidad, búsquedas).
  - Instalaciones (superficies, instaladores por superficie, materiales, valor, estado).
  - Catálogos de material (marca, tecnología, tipo de película, opacidad, referencia).
  - Inventario (entradas, salidas, transferencias, consumo, sobrantes, desperdicios, existencias, historial).
  - Garantías (registro, consulta, relación con instalación).
  - Historial (por placa y documento).
  - Auditoría y solicitudes de modificación.
- **Reglas transversales:** material de la sede de la instalación; no usar más de lo disponible; un sobrante no se cuenta dos veces; dimensiones positivas; atomicidad.
- **Validaciones:** dobles (backend obligatorio; frontend de apoyo).
- **Pruebas:** unitarias de servicios/reglas, integración de endpoints, permisos, transacciones y concurrencia.

## 7. Plan de construcción del frontend

- **Arquitectura:** React + TypeScript + Vite; enrutado; cliente API con manejo de token; estado ligero; Tailwind con tokens de diseño (pendientes de identidad).
- **Navegación por rol:** login → dashboard; menús según permisos.
- **Pantallas:**
  - Inicio de sesión.
  - Panel administrativo.
  - Registro de instalaciones (flujo guiado: cliente → vehículo → sede → servicio → superficies → instaladores por superficie → materiales → valor → estado).
  - Consulta de historial (placa/documento).
  - Gestión de inventario (existencias, entradas, salidas, transferencias, movimientos).
  - Gestión de garantías.
  - Panel de gerencia (consultas, reportes, indicadores, aprobación de modificaciones).
  - Solicitud de modificación.
- **Componentes reutilizables:** tablas, formularios, buscadores, selectores de superficie/instalador, badges de estado, modales, notificaciones.
- **Responsive y accesibilidad:** mobile-first, sin scroll horizontal, etiquetas claras, contraste, teclado, foco y ARIA.
- **PWA:** instalable, cache básico, manifest.
- **Diseño visual:** condicionado a recibir logo, paleta, tipografías y prototipo Stitch. **No se inventa identidad corporativa.**

## 8. Diseño de la base de datos

**Entidades principales.**

- **Seguridad:** `usuario` (nombre, email, password_hash, rol, sede, activo), `auditoria` (usuario, entidad, entidad_id, acción, datos_antes, datos_despues, motivo, ip, fecha), `solicitud_modificacion` (entidad, entidad_id, datos_propuestos, motivo, estado, solicitado_por, aprobado_por, fecha).
- **Núcleo:** `sede`, `cliente` (documento UNIQUE), `vehiculo` (placa UNIQUE, cliente_id), `servicio`, `estado_instalacion`, `instalacion` (fecha, sede, cliente, vehículo, servicio, estado, valor), `superficie`, `instalacion_detalle` (superficie, tecnología, opacidad, tipo de película, marca), `instalador`, `instalacion_instalador` (instalación, instalador, superficie).
- **Inventario:** `marca_material`, `tecnologia`, `tipo_pelicula`, `opacidad`, `material`, `pieza` (material, sede, tipo rollo/recorte, dimensiones, estado, pieza_origen_id), `movimiento_inventario` (tipo, medidas, sede origen/destino, instalación, usuario, motivo), `instalacion_material` (instalación, pieza origen, superficie, medidas, sobrante), `transferencia` (pieza, sede origen/destino, estado, solicitante, aprobador).
- **Garantías:** `garantia` (instalación, vehículo, cliente, tipo, cobertura, vigencia, estado), `garantia_evento` (fecha, descripción, resolución, estado).

**Relaciones clave.**
- Cliente 1—N Vehículo.
- Vehículo 1—N Instalación; Sede 1—N Instalación.
- Instalación N—N Instalador (con superficie).
- Instalación 1—N Detalle (por superficie).
- Material 1—N Pieza; Pieza 1—N Pieza (sobrantes/origen); Sede 1—N Pieza.
- Instalación 1—N InstalaciónMaterial; Pieza 1—N Movimiento.
- Instalación 1—N Garantía.

**Restricciones e integridad.** UNIQUE en documento y placa; CHECK de dimensiones > 0; FK con `ON DELETE RESTRICT`; índices en `placa`, `numero_documento`, `sede_id`, `instalacion_id`, `pieza_origen_id`. **Migraciones versionadas** (Alembic). **Respaldos:** automáticos de Supabase + export periódico. Sin definirlas todavía: unidad de medida, fórmula de consumo y precisión decimal (sección 11).

## 9. Fases de desarrollo

Cada fase se ejecutará por etapas y solo avanzará con aprobación. Formato de cada etapa: objetivo, tareas, dependencias, archivos, requisitos, criterios de aceptación, pruebas, resultado esperado y condición de aprobación.

| Fase | Objetivo | Requisitos |
| --- | --- | --- |
| 0. Re-baseline documental | Actualizar `requisitos.md`, `vision.md`, `trazabilidad.md`, diagramas y framework al alcance y stack nuevos. | Gobernanza |
| 1. Definiciones de negocio | Cerrar unidades, consumo, corte, garantías, estados y permisos. | §11 |
| 2. Fundaciones | Repos backend/frontend, PostgreSQL, migraciones, CI, entornos, identidad visual. | RNF |
| 3. Autenticación y roles | Login, JWT, RBAC base. | RNF-05, RNF-07 |
| 4. Clientes y vehículos | Registro, unicidad, búsquedas. | RF-01..03, RF-26 |
| 5. Instalaciones | Registro con superficies, instaladores, materiales y estado. | RF-04, RF-05, RF-17, RF-18 |
| 6. Historial | Consulta por placa y documento. | RF-06, RF-26 |
| 7. Inventario base | Catálogos (incl. PPF), rollos, disponibilidad. | RF-07, RF-08, RF-11, RF-19, RF-23 |
| 8. Consumo y sobrantes | Uso atómico, sobrantes, desperdicios. | RF-09, RF-10, RF-15, RF-16, RF-22 |
| 9. Transferencias | Traslado entre sedes trazable. | RF-21, RF-24 |
| 10. Correcciones y descartes | Ajustes con constancia. | RF-13, RF-14 |
| 11. Auditoría y aprobaciones | Solicitud y aprobación del Gerente. | RF-27, RNF-08 |
| 12. Garantías | Registro, consulta y relación con instalaciones. | RF-25 |
| 13. Frontend y PWA | Pantallas, responsive, accesibilidad. | RNF-11 |
| 14. Pruebas y validación | Unitarias, integración, permisos, seguridad, usuarios. | RNF-01..06 |
| 15. Preparación de despliegue | Hosting, variables, HTTPS, respaldos, monitoreo. | §10 |

**Cierre de cada etapa:** revisar cambios → ejecutar pruebas → comparar con requisitos → informar errores → solicitar aprobación → continuar solo con autorización. Sin commits ni push automáticos.

## 10. Pruebas y criterios de aceptación

### 10.1 Tipos de prueba
- **Unitarias:** reglas de negocio (unicidad, medidas, disponibilidad, sede, estados, permisos).
- **Integración:** endpoints + base de datos (transacciones y rollback).
- **Funcionales:** escenarios Gherkin de las historias.
- **Permisos:** rechazo por rol; corrección/descarte solo Administrador; aprobación solo Gerente.
- **Seguridad:** autenticación, manipulación de tokens, accesos indebidos, inyección, exposición de datos.
- **Validación con usuarios:** recorrido desde teléfono y facilidad de uso.
- **Consistencia:** simular fallo y verificar ausencia de cambios parciales.

### 10.2 Criterios de aceptación del plan
- El documento contiene las 11 secciones solicitadas y es coherente con las decisiones del equipo.
- Alcance, stack, roles y aprobador quedan explícitos y trazables.
- Cada fase define objetivo, dependencias, requisitos, criterios y pruebas.
- Los pendientes de la sección 11 permanecen visibles; no se asume ninguna fórmula ni unidad.
- Se declara que no hay implementación, pruebas ni despliegue ejecutados.
- No se realizan commits ni push sin autorización.

### 10.3 Criterios de aceptación del producto (por etapa)
- Cada historia seleccionada cumple sus criterios de aceptación y escenarios de error.
- Las operaciones de inventario son atómicas y respetan la sede.
- Los permisos se validan en backend.
- La documentación y la trazabilidad quedan actualizadas.

## 11. Decisiones pendientes

1. **Unidad de medida** del material (polarizado en rollo por ancho×largo; PPF por placa/rollo) y su registro.
2. **Fórmula de consumo** y comprobación de que un corte **cabe** en la pieza (no por área).
3. **Procedimiento de corte y material restante** (HU-10) y **precisión decimal** en centímetros.
4. **Correcciones con sobrantes ya utilizados**, anulaciones y material equivocado (HU-13).
5. **Garantías:** cobertura, vigencia, tipos, estados y eventos de reclamo.
6. **Transferencias:** si requieren aprobación, estados y responsables.
7. **Estados de instalación** válidos y sus transiciones.
8. **Matriz de permisos** exacta por rol (incl. qué modifica Asesor/Instalador).
9. **Rol Asesor/Instalador** en el nuevo modelo (el brief solo detalla Administrador y Gerente).
10. **Obligatoriedad de datos** de contacto del cliente y datos del vehículo.
11. **Identidad visual y prototipo Stitch** (logo, colores, tipografías): pendientes de recibir.
12. **Umbrales no funcionales** (tiempos de respuesta, concurrencia, dispositivos/navegadores).
