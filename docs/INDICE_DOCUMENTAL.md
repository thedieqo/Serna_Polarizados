# Índice documental — Serna Polarizados

**Actualizado:** 2026-10-27 (F5)  
**Alcance:** F0, F1, F2, F3, F4 y F5. Este índice clasifica la documentación existente, registra el estado de las fases y distingue la documentación vigente, los antecedentes históricos y las guías nuevas propuestas. No adopta decisiones de alcance ni reescribe los documentos fuente.

## 1. Entrada rápida

- Estado actual del proyecto: [readme.md](../readme.md).
- Visión y límites: [vision.md](vision.md).
- Requisitos y criterios: [requisitos.md](requisitos.md).
- Trazabilidad con el código: [trazabilidad.md](trazabilidad.md).
- Diseño implementado: [diseno-back-front.md](diseno-back-front.md).
- Backlog y sprints: [planificacion.md](planificacion.md) (movido en F1).
- Arquitectura actual: [diagramas/arquitectura-actual.mmd](diagramas/arquitectura-actual.mmd).
- Clases actuales: [diagramas/clases-actual.mmd](diagramas/clases-actual.mmd).
- Framework IA: [config/project_config.md](../mi-framework-ia/config/project_config.md) y [core/orchestrator.md](../mi-framework-ia/core/orchestrator.md).
- Guías nuevas propuestas del framework: sección 5.
- Línea base y verificaciones de F0: [F0_LINEA_BASE_Y_VERIFICACIONES.md](F0_LINEA_BASE_Y_VERIFICACIONES.md).
- Extracción literal del prompt maestro: [ia/PROMPT_MAESTRO_ORIGINAL.md](ia/PROMPT_MAESTRO_ORIGINAL.md).
- Diferencias implementación vs. plan: sección 4 de este índice.
- Registros de F2, F3, F4 y F5: secciones 8, 9, 10 y 11.
- Evidencia histórica y privacidad: sección 6.

## 2. Mapa documental

| Documento | Clasificación | Estado actual | Acción posterior |
|---|---|---|---|
| `readme.md` | Vigente | Alineado en F2 con el código, el stack real y el estado parcial; distingue lo implementado de lo planificado | Mantener al día |
| `docs/PLAN_DESARROLLO.md` | Propuesta estratégica | El modelo de datos de §8 y el alcance ampliado **no están adoptados**; no se modificó en F2 | Decisión pendiente antes de cualquier refactor |
| `docs/vision.md` | Vigente | Actualizado en F2: conserva la visión y distingue el alcance implementado del pendiente | Mantener alineado con requisitos |
| `docs/requisitos.md` | Base vigente de RF-01..RF-16 | No contiene RF-17..RF-27 ni HU-15..HU-22; no se modificó en F2 | Decidir si el alcance ampliado se incorpora |
| `docs/trazabilidad.md` | Vigente | Actualizado en F2 con estados observados en el código y evidencia estática; no acredita pruebas | Actualizar cuando se ejecuten pruebas |
| `docs/diseno-back-front.md` | Vigente | Actualizado en F2 para describir React/TS/Tailwind + FastAPI + SQLAlchemy/PostgreSQL; F4 retiró la referencia a dos componentes vacíos; F5 precisó que la búsqueda existe en backend y servicios, falta integrarla en pantalla y no se probó funcionalmente | Mantener alineado con el código y los diagramas |
| `docs/analisis-competitivo.md` | Evidencia histórica | Documento de análisis previo | No reescribir |
| `docs/planificacion.md` | Propuesta de backlog | Movido en F1 a la ruta vigente; el enlace a `requisitos.md` resuelve; contenido sin cambios | Conservar; no reescribir |
| `docs/diagramas/arquitectura.mmd` | Antecedente histórico | Propuesta original con HTML/CSS/JS, Flask y SQLite; se conserva sin cambios como procedencia académica | No sobrescribir; el estado actual está en `arquitectura-actual.mmd` |
| `docs/diagramas/clases.mmd` | Antecedente histórico | Modelo propuesto con Trabajo, Sede, Pieza y material; no coincide con las tablas actuales | No sobrescribir; el estado actual está en `clases-actual.mmd` |
| `docs/diagramas/componentes.mmd` | Antecedente histórico | Propuesta funcional amplia con Flask/SQLite, RF/HU e inventario; no describe el código actual | No sobrescribir; conservar como evidencia del alcance propuesto |
| `docs/diagramas/secuencia-historial.mmd` | Antecedente histórico | Secuencia propuesta para historial con Flask y SQLite; el historial específico no está implementado | No sobrescribir; conservar como propuesta |
| `docs/diagramas/arquitectura-actual.mmd` | Documentación actual de F3 | React → Axios → rutas FastAPI → CRUD → SQLAlchemy → PostgreSQL, con carpetas existentes | Mantener alineado con el código |
| `docs/diagramas/clases-actual.mmd` | Documentación actual de F3 | Solo `Cliente`, `Vehiculo` e `Instalacion`, con atributos y relaciones observados | Mantener alineado con los modelos |
| `docs/ia/entrevista-cliente.md` | Evidencia fuente | Síntesis de entrevista y aclaraciones | No reescribir |
| `docs/ia/matriz-ia.md` | Registro de uso de IA | Actualizado en F2: herramientas documentadas, código actual y límites de evidencia; conserva el historial | Completar registros de prompts y revisiones |
| `docs/ia/prompts.md` | Evidencia histórica | Biblioteca de prompts; incluye traducción al inglés | No reescribir |
| `docs/ia/pruebas-gemini.md` | Evidencia histórica | Registro de pruebas con Gemini | No reescribir |
| `docs/ia/revision-historias-gemini.md` | Evidencia histórica | Revisión de historias; falta el prompt exacto | No inventar el prompt faltante |
| `HISTORIAL_PROMPTS_SERNA.md` | Evidencia histórica no versionada | Permanece íntegro en su ubicación; no se publica ni se redacta | Revisar datos sensibles antes de decidir su versionado |
| `docs/ia/PROMPT_MAESTRO_ORIGINAL.md` | Documento nuevo de F0 | Extracción literal verificada | Usar como referencia; no editar el bloque literal |
| `docs/F0_LINEA_BASE_Y_VERIFICACIONES.md` | Documento nuevo de F0 | Línea base, respaldo y verificaciones | Conservar como evidencia de F0 |
| `docs/INDICE_DOCUMENTAL.md` | Documento de F0, actualizado en F2, F3, F4 y F5 | Este índice central | Mantener actualizado |
| `mi-framework-ia/config/project_config.md` | Guía documental vigente | Actualizada en F3 con stack, capas y alcance actual; distingue propuestas no implementadas | Mantener alineada con el código |
| `mi-framework-ia/core/orchestrator.md` | Guía documental vigente | Actualizada en F3 como flujo de apoyo humano; no existe motor de orquestación | No presentarla como automatización |
| `mi-framework-ia/agents/backend_agent.md` | Guía documental vigente | Actualizada en F3 para FastAPI/SQLAlchemy/PostgreSQL y alcance real | Revisar antes de usarla como apoyo |
| `mi-framework-ia/skills/backend_generation.md` | Guía documental vigente | Actualizada en F3; propone cambios acotados, sin generación automática | Revisar contra requisitos |
| `mi-framework-ia/skills/code_review.md` | Guía documental vigente | Actualizada en F3; la revisión final es humana | Usar como lista de comprobación |
| `mi-framework-ia/skills/database_design.md` | Guía documental vigente | Actualizada en F3 con tablas actuales y entidades propuestas separadas | No confundir propuestas con tablas |
| `mi-framework-ia/agents/requirements_agent.md` | Guía nueva propuesta en F3 | Análisis de requisitos; ejecución no acreditada | Validar y adoptar si se decide |
| `mi-framework-ia/agents/frontend_agent.md` | Guía nueva propuesta en F3 | Apoyo a cambios de interfaz; ejecución no acreditada | Validar y adoptar si se decide |
| `mi-framework-ia/agents/reviewer_agent.md` | Guía nueva propuesta en F3 | Lista de revisión; ejecución no acreditada | Validar y adoptar si se decide |
| `mi-framework-ia/skills/frontend_generation.md` | Guía nueva propuesta en F3 | Apoyo a propuestas React; ejecución no acreditada | Validar y adoptar si se decide |
| `mi-framework-ia/skills/requirements_analysis.md` | Guía nueva propuesta en F3 | Análisis documental de requisitos; ejecución no acreditada | Validar y adoptar si se decide |
| `mi-framework-ia/tools/`, `interfaces/`, `evaluations/` | Carpetas de apoyo pendientes | Solo contienen `__init__.py` vacíos; no hay herramientas, interfaces ni evaluaciones implementadas | No agregar relleno; definir necesidad antes de crear archivos |

**Procedencia de los diagramas históricos:** son los cuatro archivos versionados que ya existían al iniciar F3. Se conservaron sin cambios; no contienen fecha ni autoría verificable en su contenido, por lo que se describen como propuestas previas del repositorio y no se les atribuye otra entrega.

## 3. Límites de F0

- No se movieron ni eliminaron archivos existentes.
- No se modificó `readme.md` ni ningún otro documento existente.
- No se modificó backend, frontend, modelos, dependencias, configuración de conexión ni base de datos.
- No se modificó `.gitignore` ni `mcp.json`.
- No se ejecutó indexación, MCP, build, migración ni conexión a BD.
- No se hizo commit ni push.
- El único archivo existente modificado es `.cgcignore`.

Esta sección conserva el registro histórico de F0 y no se reescribe en F2.

## 4. Diferencias entre implementación y plan (decisiones pendientes)

Estas diferencias se registran para decisión. **No se adopta automáticamente el modelo de `PLAN_DESARROLLO.md` §8 ni se refactoriza el prototipo.**

| Área | Implementación actual | Plan/propuesta | Estado |
|---|---|---|---|
| Cliente | `nombre`, `documento`, `contacto` | Documento único y datos de contacto; el plan no detalla todos los campos | Implementado en código; validar obligatoriedad |
| Vehículo | `placa`, `descripcion`, `cliente_id` | Placa única, cliente asociado y datos como marca/modelo/color/tipo | Implementado en código; decisión pendiente sobre campos ampliados |
| Instalación | `vehiculo_id`, `fecha`, `tipo_servicio`, `opacidad`, `zonas` JSON, `asignaciones_instaladores` JSON, `retiro_material_anterior`, `observaciones`, `estado` | `sede`, `cliente`, `servicio`, `estado` catalogado, `valor`, superficies, detalles e instaladores normalizados | Divergencia funcional; decisión pendiente |
| Integridad | `cascade="all, delete-orphan"` en cliente→vehículos y vehículo→instalaciones | `ON DELETE RESTRICT` y conservación del historial | Decisión pendiente |
| Migraciones | No hay Alembic ni creación de esquema | Migraciones versionadas | Decisión pendiente |
| Pruebas | No hay pruebas automatizadas | Unitarias, integración, permisos y transacciones | Decisión pendiente |
| Autenticación/roles | API abierta; sin JWT/RBAC | Login, roles y permisos | Fase posterior |
| Frontend | Navegación por pestañas con `useState`; `react-router-dom` instalado sin uso | SPA con rutas | Fase posterior |
| Inventario | No implementado | Catálogos, piezas, movimientos, sobrantes, transferencias | Fase posterior |
| Garantías | No implementado | Registro y consulta ligados a instalaciones | Fase posterior |
| Documentación de stack | README, visión y diseño alineados en F2; F3 añadió arquitectura y clases actuales | Los cuatro diagramas históricos conservan Flask/SQLite/HTML como antecedente | Históricos preservados; actuales alineados en F3 |
| Alcance ampliado | Solo figura en `PLAN_DESARROLLO.md` | RF-17..RF-27 y HU-15..HU-22 | Requiere aprobación explícita |

**Opciones para la decisión pendiente:** adoptar el plan y refactorizar; ajustar el plan al prototipo; o mantener el prototipo y posponer el alcance ampliado. Ninguna opción está aprobada.

## 5. Framework IA: guías actuales y nuevas propuestas

F3 completa los cinco documentos que estaban vacíos como **guías nuevas propuestas durante esta reorganización**. No se atribuyen a entregas anteriores ni se presentan como agentes ejecutados. Todas indican: “Guía documental; ejecución no acreditada”.

| Guía | Clasificación | Propósito |
|---|---|---|
| [`agents/requirements_agent.md`](../mi-framework-ia/agents/requirements_agent.md) | Nueva propuesta F3 | Convertir necesidades documentadas en requisitos verificables. |
| [`skills/requirements_analysis.md`](../mi-framework-ia/skills/requirements_analysis.md) | Nueva propuesta F3 | Detectar ambigüedades y diferencias entre requisitos y código. |
| [`agents/frontend_agent.md`](../mi-framework-ia/agents/frontend_agent.md) | Nueva propuesta F3 | Orientar cambios acotados en React/TypeScript. |
| [`skills/frontend_generation.md`](../mi-framework-ia/skills/frontend_generation.md) | Nueva propuesta F3 | Preparar propuestas de interfaz compatibles con la API. |
| [`agents/reviewer_agent.md`](../mi-framework-ia/agents/reviewer_agent.md) | Nueva propuesta F3 | Proporcionar una lista de revisión con decisión humana. |

Las guías existentes `project_config.md`, `orchestrator.md`, `backend_agent.md`, `backend_generation.md`, `code_review.md` y `database_design.md` se actualizaron en F3. Conservan la diferencia entre antecedente, estado actual y propuesta futura.

Las carpetas `tools/`, `interfaces/` y `evaluations/` contienen únicamente `__init__.py` vacíos. No hay herramientas, interfaces ni evaluaciones implementadas. Los seis `__init__.py` del framework son marcadores de paquete y no se modificaron.

## 6. Evidencia histórica y privacidad

- `HISTORIAL_PROMPTS_SERNA.md` permanece en su ubicación actual, sin editar y sin versionar.
- SHA-256 del archivo completo: `720134ba7f648f58d74638127178e65618cf5f24e9fddfe7b7e6b97730c1d699`.
- Se identificaron 36 ocurrencias de rutas locales (34 únicas) en el historial. El escaneo de patrones de credenciales sobre el historial dio 0 coincidencias, pero eso **no certifica** que el archivo esté libre de datos sensibles.
- No se preparó publicación ni copia redactada. La revisión de datos sensibles y la decisión de versionado quedan pendientes.
- `backend/.env` no fue leído, mostrado ni escaneado. Se asume que puede contener credenciales.
- El escaneo de secretos de F0 sobre archivos a versionar se limita a los archivos nuevos o modificados; no se aplica a `backend/.env`. Además, se ejecutó un escaneo de patrones sobre `HISTORIAL_PROMPTS_SERNA.md` (0 coincidencias), que tampoco certifica su contenido.

## 7. Problemas conocidos

- Resuelto en F1: el backlog se movió a `docs/planificacion.md`; su enlace a `requisitos.md` resuelve. La carpeta redundante se eliminó por quedar vacía.
- Resuelto en F2: `readme.md`, `vision.md`, `diseno-back-front.md`, `trazabilidad.md` y `matriz-ia.md` fueron alineados con el código y el stack real.
- Resuelto en F3: se agregaron diagramas actuales sin alterar los cuatro antecedentes históricos; se alinearon las guías del framework y se completaron las cinco guías nuevas propuestas.
- Resuelto en F4: se retiraron tres archivos `.DS_Store` y los dos componentes frontend vacíos que no se importaban; se actualizó solo la descripción vigente del diseño.
- Precisado en F5: la búsqueda por documento y placa está implementada en backend, tiene funciones CRUD y servicios frontend, pero no está integrada en pantalla ni probada funcionalmente.
- Los diagramas históricos siguen mostrando Flask/SQLite/HTML de forma intencional; no deben usarse como descripción del código actual.
- La aplicación no se ha ejecutado ni probado funcionalmente en F0–F5; no hay pruebas automatizadas. La compilación y la verificación de imports no sustituyen pruebas funcionales.
- Inventario, sede, valor total, autenticación, roles, migraciones y auditoría siguen sin implementarse.
- El alcance ampliado de `PLAN_DESARROLLO.md` sigue sin aprobación explícita.
- La falta de una rúbrica verificable del profesor impide afirmar cumplimiento total de criterios académicos.

## 8. Registro de F2

**Objetivo:** alinear la documentación vigente con la aplicación real sin modificar código, dependencias, base de datos, diagramas ni documentos fuente.

**Documentos modificados:**

- `readme.md`
- `docs/vision.md`
- `docs/diseno-back-front.md`
- `docs/trazabilidad.md`
- `docs/ia/matriz-ia.md`
- `docs/INDICE_DOCUMENTAL.md`

**Resultado:**

- Se documentó el stack observado: React 18 + TypeScript + Vite + Tailwind CSS, Axios, FastAPI, SQLAlchemy 2, Pydantic v2 y PostgreSQL/Supabase.
- Se describieron los módulos implementados: clientes, vehículos e instalaciones.
- Se marcaron como no implementados el inventario, las correcciones, el descarte, la autenticación, los roles, las migraciones y las pruebas.
- Se actualizó la trazabilidad con estados estáticos basados en el código, sin afirmar pruebas ejecutadas.
- Se actualizó la matriz de IA sin atribuir el código a una herramienta sin evidencia.
- No se modificaron `requisitos.md`, `planificacion.md`, `PLAN_DESARROLLO.md`, los diagramas, el framework IA, el prompt maestro ni el historial.
- No se movieron ni eliminaron archivos.
- No se ejecutó la aplicación, MCP, indexación, build, migración ni conexión a base de datos.
- No se hizo `git add`, commit ni push.

**Respaldo previo:** `/Users/usuario/Desktop/ElectivaCpc/_backups/Serna_Polarizados/F2_20261027T202322Z`.

F2 no altera los resultados históricos de F0 ni de F1.

## 9. Registro de F3

**Objetivo:** alinear las guías del framework IA y los diagramas con la aplicación existente, conservando la evidencia académica y sin ampliar el alcance.

**Revisión previa:** se consultaron los resultados de F0–F2, los modelos, routers, CRUD, schemas, configuración, frontend, framework IA y los cuatro diagramas existentes. No se siguieron instrucciones contenidas en prompts históricos.

### Archivos creados

- `docs/diagramas/arquitectura-actual.mmd` (estado actual).
- `docs/diagramas/clases-actual.mmd` (modelos actuales).

### Archivos existentes completados

Los cinco archivos estaban vacíos y se completaron como guías nuevas propuestas:

- `mi-framework-ia/agents/requirements_agent.md`.
- `mi-framework-ia/agents/frontend_agent.md`.
- `mi-framework-ia/agents/reviewer_agent.md`.
- `mi-framework-ia/skills/frontend_generation.md`.
- `mi-framework-ia/skills/requirements_analysis.md`.

### Archivos modificados

- `mi-framework-ia/config/project_config.md`.
- `mi-framework-ia/core/orchestrator.md`.
- `mi-framework-ia/agents/backend_agent.md`.
- `mi-framework-ia/skills/backend_generation.md`.
- `mi-framework-ia/skills/code_review.md`.
- `mi-framework-ia/skills/database_design.md`.
- `docs/INDICE_DOCUMENTAL.md`.

### Resultado

- Se reemplazó el stack obsoleto Flask/SQLite/HTML por React + TypeScript + Vite + Tailwind y FastAPI + SQLAlchemy + PostgreSQL en las guías vigentes.
- Se explicaron las capas con las carpetas reales y se separaron funcionalidades actuales de propuestas.
- Se documentó que los agentes y skills son guías de apoyo, sin motor de orquestación ni ejecución automática.
- Las cinco guías nuevas incluyen propósito, entradas, pasos, salida esperada, límites, revisión humana y la leyenda “Guía documental; ejecución no acreditada”.
- Se conservaron intactos y sin renombrar `arquitectura.mmd`, `clases.mmd`, `componentes.mmd` y `secuencia-historial.mmd` como antecedentes históricos.
- Los nuevos diagramas solo muestran el flujo y los modelos implementados; no incluyen autenticación, inventario, pagos, migraciones ni sedes como funcionalidades.
- Se conservaron los seis `__init__.py` y las carpetas `tools/`, `interfaces/` y `evaluations/`; no se agregaron archivos de relleno.

### Verificación y límites

- Enlaces locales validados en 27 Markdown y 92 enlaces; 0 rotos.
- La sintaxis Mermaid se revisó de forma estática. No hay `mmdc` ni otro renderizador Mermaid disponible localmente, por lo que **la validación visual queda pendiente**.
- No se modificaron backend, frontend, dependencias, base de datos, requisitos, planificación, `PLAN_DESARROLLO.md`, prompt maestro original, historial, secretos, `.gitignore`, `.cgcignore` ni `mcp.json`.
- No se movieron ni eliminaron archivos.
- No se ejecutó MCP, indexación, aplicación, build, migración, conexión a BD ni instalación de herramientas.
- No se hizo `git add`, commit ni push.
- No se declara cumplimiento total de requisitos docentes ni se atribuye el código a una herramienta de IA.

**Respaldo previo:** `/Users/usuario/Desktop/ElectivaCpc/_backups/Serna_Polarizados/F3_20261027T203006Z`.

F3 no altera los registros históricos de F0, F1 ni F2.

## 10. Registro de F4

**Objetivo:** ejecutar una limpieza mínima de archivos innecesarios, conservando los resultados de F0–F3 y sin modificar lógica de aplicación, dependencias, base de datos ni configuración.

**Precondiciones comprobadas:**

- Los tres `.DS_Store` eran metadatos de macOS ignorados por Git.
- `ClienteSearch.tsx` y `VehiculoSearch.tsx` tenían 0 bytes, no contenían imports ni exportaciones y ninguna página los importaba.
- El respaldo F3 solo cubría `mi-framework-ia/.DS_Store`; antes de eliminar se creó un respaldo F4 con los cinco candidatos y los documentos a actualizar.
- El respaldo F4 está en `/Users/usuario/Desktop/ElectivaCpc/_backups/Serna_Polarizados/F4_20261027T204922Z`; `f4_candidates_before.tgz` tiene SHA-256 `863b46aaee356d10b804bf4a49548776ffbce4efb3eccc3acf06e0b3553a9949`. Su contenido y hashes se verificaron mediante una restauración temporal.

### Archivos eliminados

- `.DS_Store`
- `docs/.DS_Store`
- `mi-framework-ia/.DS_Store`
- `frontend/src/components/ClienteSearch.tsx`
- `frontend/src/components/VehiculoSearch.tsx`

Los tres primeros eran metadatos del sistema. Los dos componentes estaban vacíos, no se importaban y no se ejecutaban. Su retiro **no cancela** los requisitos de búsqueda por documento o placa ni implica que la búsqueda esté integrada en pantalla; los endpoints y servicios existen.

### Documentos actualizados

- `docs/diseno-back-front.md`: se reemplazó la descripción que afirmaba que los componentes existían; ahora indica que fueron retirados en F4 y que la integración de la búsqueda en pantalla sigue pendiente.
- `docs/INDICE_DOCUMENTAL.md`: este registro F4.

### Referencias históricas preservadas

`docs/F0_LINEA_BASE_Y_VERIFICACIONES.md` conserva sin cambios las líneas 44–45, que mencionan los dos componentes. Esa referencia es evidencia histórica y no se borró.

**Nota F4 (2026-10-27):** los archivos mencionados en esas líneas fueron eliminados durante F4; la mención permanece como registro de la línea base original.

### Verificación antes y después

- `tsc --noEmit`: 0 errores antes y después.
- `vite build`: completó antes y después; 97 módulos transformados. La compilación estándar final generó artefactos idénticos a `frontend/dist`; la salida de control se generó fuera del repositorio y no se alteró `dist`.
- Backend: `compileall` y `import app.main` completaron sin errores antes y después. No se inició la aplicación, no se consultó Supabase y no se escribió en la base de datos.
- Enlaces locales: 27 Markdown, 92 enlaces, 0 rotos.
- `git diff --check`: sin errores.
- `HISTORIAL_PROMPTS_SERNA.md`, `docs/ia/PROMPT_MAESTRO_ORIGINAL.md` y `.cgcignore` conservan los hashes registrados en la sección 6.
- Los logs de verificación F4 están en el respaldo, bajo `verification/before` y `verification/after`.

### Límites

- No se modificó lógica de aplicación. Aparte de los dos componentes vacíos eliminados, no se alteraron archivos de backend ni frontend; tampoco dependencias, base de datos, requisitos, planificación, `PLAN_DESARROLLO.md`, prompt maestro original, historial, secretos, `.gitignore`, `.cgcignore` ni `mcp.json`.
- No se eliminaron `__init__.py`, `tools/`, `interfaces/`, `evaluations/`, diagramas históricos, `node_modules`, `.venv` ni `dist`.
- No se ejecutó MCP, indexación, instalación de herramientas ni conexión a base de datos.
- No se hizo `git add`, commit ni push.
- No se ejecutaron pruebas funcionales; solo compilación, imports y validaciones documentales.
- No se declara cumplimiento total de requisitos docentes.

F4 no altera los registros históricos de F0, F1, F2 ni F3.

## 11. Registro de F5

**Objetivo:** verificar y cerrar F0–F4, auditar el diff acumulado, comprobar privacidad e integridad y corregir solo la documentación vigente sobre la búsqueda. F5 no implementa funcionalidades, no amplía el alcance y no modifica código.

### Auditoría del diff acumulado

- Se revisaron `git diff`, los archivos untracked y el estado de Git. Los cambios corresponden a F0–F4; no se detectaron cambios inesperados.
- F0: `.cgcignore`, `docs/F0_LINEA_BASE_Y_VERIFICACIONES.md`, `docs/INDICE_DOCUMENTAL.md`, `docs/ia/PROMPT_MAESTRO_ORIGINAL.md` y `HISTORIAL_PROMPTS_SERNA.md` (este último privado).
- F1: se eliminó `docs/docs/planificacion.md` y se agregó `docs/planificacion.md`.
- F2: se actualizaron `readme.md`, `docs/vision.md`, `docs/diseno-back-front.md`, `docs/trazabilidad.md` y `docs/ia/matriz-ia.md`.
- F3: se actualizaron las guías de `mi-framework-ia` y se crearon los dos diagramas actuales.
- F4: se eliminaron los dos componentes vacíos y se actualizaron el diseño y este índice.
- F5: solo se corrigieron `docs/diseno-back-front.md` y este índice.
- El diff de `backend` y `frontend` contiene únicamente las dos eliminaciones vacías autorizadas; no se modificó lógica de aplicación ni dependencias.

### Estado real de la búsqueda

- Endpoints presentes: `GET /api/v1/clientes/by-documento/{documento}`, `GET /api/v1/vehiculos/by-placa/{placa}` y `GET /api/v1/vehiculos/by-cliente/{cliente_id}`.
- Funciones CRUD presentes: `get_cliente_by_documento`, `get_vehiculo_by_placa` y `get_vehiculos_by_cliente`.
- Servicios frontend presentes: `clientesService.getByDocumento`, `vehiculosService.getByPlaca` y `vehiculosService.getByCliente`.
- Ninguna página, componente o `App.tsx` consume esos métodos: **la búsqueda no está integrada en pantalla**.
- No se ejecutaron pruebas funcionales ni consultas a PostgreSQL/Supabase: **el funcionamiento de extremo a extremo no está acreditado**.
- La documentación vigente se corrigió para distinguir backend, servicio frontend, interfaz y prueba funcional; no se declara la búsqueda como terminada.

### Privacidad e integridad

- `backend/.env` está ignorado por `.gitignore:5` y no está versionado.
- `mcp.json` está ignorado por `.gitignore:36` y no está versionado.
- `.DS_Store` está ignorado por `.gitignore:24` y no existía al verificar; esto no impide que macOS lo regenere.
- No se copiaron valores de entorno ni configuración privada.
- `HISTORIAL_PROMPTS_SERNA.md` conserva SHA-256 `720134ba7f648f58d74638127178e65618cf5f24e9fddfe7b7e6b97730c1d699` y queda fuera de la publicación.
- `docs/ia/PROMPT_MAESTRO_ORIGINAL.md` conserva SHA-256 `aa15dcbd68c059345c048adadd888e95b987d9a12d4ff2ddc0715ef36dd6f544`; no contiene rutas locales, correos ni claves detectables, pero incluye un identificador de sesión que debe considerarse antes de publicarlo.
- `.cgcignore` conserva SHA-256 `28bcdb226466dcba6ff39382e5467cf2d7022b30cd7bb08c05ddb67da3d6cd66`.
- Requisitos, planificación, entrevista, prompts, pruebas, revisión de historias, análisis competitivo y diagramas históricos no presentan cambios en Git.

### Verificación

- Se reutilizan las verificaciones F4 de `tsc --noEmit` (0 errores) y `vite build` (97 módulos), porque F5 no cambió código relevante.
- En F5, `import app.main` completó correctamente y enumeró 12 rutas `/api/v1`; no se inició el servidor ni se consultó la base de datos.
- Enlaces locales: 27 Markdown publicables, 92 enlaces y 0 rotos; se excluyeron enlaces externos y el historial privado.
- `git diff --check`: sin errores.
- No hay un renderizador Mermaid local (`mmdc`, `mermaid` ni binario equivalente); la validación visual sigue pendiente y no se instalaron herramientas.
- Respaldo previo de los dos documentos modificados: `/Users/usuario/Desktop/ElectivaCpc/_backups/Serna_Polarizados/F5_20261027T211516Z`; `f5_docs_before.tgz` tiene SHA-256 `b0bf86a9dad9555072b30b8dfcf3bc6c073899b8fb067709e3342033d58e6985`.

### Cierre

- La reorganización documental y de archivos F0–F5 puede darse por terminada.
- No se modificaron código de aplicación, dependencias, base de datos, secretos, `.gitignore`, `.cgcignore` ni `mcp.json`; no se agregaron carpetas ni informes.
- No se hizo `git add`, commit ni push.
- Permanecen pendientes la integración y prueba funcional de la búsqueda, las pruebas automatizadas, la revisión de autenticación/seguridad, las migraciones y la decisión sobre integración con Supabase.
- La validación visual Mermaid y la verificación contra la rúbrica docente siguen pendientes; no se declara cumplimiento total.
- El cierre de la reorganización no implica que la aplicación esté completa ni lista para producción.

F5 no altera los registros históricos de F0, F1, F2, F3 ni F4.
