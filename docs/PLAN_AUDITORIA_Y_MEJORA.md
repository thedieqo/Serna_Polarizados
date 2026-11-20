# PLAN DE AUDITORÍA Y MEJORA — SERNA POLARIZADOS

> Documento de planificación basado en revisión técnica preliminar. No es la ejecución del skill exacto solicitado por el profesor. No aplica correcciones, no conecta a bases de datos, no ejecuta pruebas de ataque o carga y no acredita cumplimiento académico.

**Declaración requerida:** “Pendiente de repetir o complementar con el skill exacto solicitado por el profesor”.

## 1. Identificación

- **Fecha de la revisión:** 2026-11-18.
- **Commit revisado:** `28829d9b447b7bbd79b5747d8b65bcec81e523b3`.
- **Directorio de trabajo:** `/Users/usuario/Desktop/ElectivaCpc/Serna_Polarizados`.
- **Rama observada:** `main`. No se creó ni cambió de rama.
- **Estado Git inicial:** `?? package-lock.json`, `?? package.json`. Estos archivos preexistentes se preservaron; no se agregaron al índice.
- **Alcance revisado:** `backend/app/**` (configuración, sesión, modelos, esquemas, CRUD, routers y `main.py`), `backend/requirements.txt`, `backend/.env.example`, `frontend/src/**`, `frontend/package.json`, `package.json`, documentación vigente (`readme.md`, `docs/INDICE_DOCUMENTAL.md`, `docs/PLAN_DESARROLLO.md`) y herramientas ya instaladas.
- **No revisado por decisión de alcance o falta de acceso:** contenido de `backend/.env`, `mcp.json`, datos reales de PostgreSQL/Supabase, servicios en la nube, cuentas, planes, logs de producción, rutas de inventario/garantías/RF-17..RF-27 (no implementadas), pruebas de penetración, pruebas de carga y validación con usuarios.

## 2. Disponibilidad del skill *Security Audit*

Se comprobaron ubicaciones locales habituales y el repositorio, sin instalar nada:

| Ubicación | Resultado |
| --- | --- |
| `~/.agents/skills` | Solo `pinokio`. |
| `~/.claude/skills` | Solo `pinokio`. |
| `~/.codex/skills/.system` | `imagegen`, `openai-docs`, `review-agent`, `skill-creator`, `skill-installer`. |
| `mi-framework-ia/skills/` | `code_review.md`, `backend_generation.md`, `frontend_generation.md`, `database_design.md`, `requirements_analysis.md`; son guías del repositorio, no el skill solicitado. |
| Skills disponibles en la sesión | `customize-opencode`, `pinokio`. |

No se encontró un skill con nombre, origen o versión identificables como *Security Audit*. `review-agent` es una guía de revisión de defectos de un cambio, no un sustituto de auditoría de seguridad; no se usó como tal. No se instaló ningún sustituto.

**Por lo tanto, la sección 3 es una revisión técnica preliminar propia y no debe presentarse como ejecución del skill de seguridad solicitado.**

## 3. Hallazgos

### 3.1 Problemas confirmados por lectura de código y comprobaciones locales

| ID | Severidad justificada | Archivo / línea | Evidencia | Impacto | Corrección mínima propuesta / estado |
| --- | --- | --- | --- | --- | --- |
| `AUD-01` | **Crítica**: no hay autenticación ni autorización sobre datos personales y registros de instalación; contradice RNF-05/RNF-07 documentados. | `backend/app/main.py:18-51`; `backend/app/api/v1/clientes.py:27-94`; `backend/app/api/v1/vehiculos.py:27-113`; `backend/app/api/v1/instalaciones.py:19-55`. | La app incluye los tres routers directamente y todas las operaciones dependen solo de `get_db`. El `openapi.json` local no mostró esquemas de seguridad. | Cualquier cliente con acceso a la API puede crear y consultar clientes, vehículos e instalaciones; no hay distinción por rol ni trazabilidad de usuario. | Añadir una dependencia de autenticación a nivel de routers y verificaciones de rol en operaciones sensibles; proteger u ocultar la documentación interactiva según entorno. No implementar roles nuevos sin la matriz de permisos pendiente. |
| `AUD-02` | **Alta**: la configuración TLS de la cadena de conexión puede descartarse silenciosamente. **Corregida en código el 2026-11-18**; TLS real sigue pendiente. | `backend/app/db/session.py:42-63`; `backend/tests/test_db_session.py`. | Confirmado: `urlparse` devolvía `username`/`password` escapados y descartaba `query` al reconstruir con `URL.create`. `make_url(...)` decodifica credenciales y query. Corrección aplicada con `make_url`, `URL.create(..., query=...)`, normalización de `postgres`/`postgresql` y error sin encadenar la DSN. | Antes: pérdida de `sslmode`/`sslrootcert` y credenciales mal interpretadas. Después: parámetros y credenciales preservados en la construcción; conexión real y TLS del proveedor no verificados. | Aplicada: usar `make_url` y propagar `dict(parsed.query)`; el fallo malformado lanza `RuntimeError` sin credenciales. No constituye auditoría con el skill pendiente. Propuesta para Supabase: conservar `sslmode=require` en `DATABASE_URL` y `sslrootcert` solo si se entrega una CA; verificación pendiente. |
| `AUD-03` | **Alta**: configuración insegura por defecto y ausencia de validación de secretos en producción. | `backend/app/core/config.py:26`, `:38`, `:40-45`, `:49`; `backend/.env.example:6`, `:11`. | `DATABASE_URL` tiene un valor por defecto con forma de credenciales de ejemplo, `DEBUG=True` por defecto y `Settings()` lee `backend/.env` al importar. No se mostró ni copió el contenido real de `.env`. | Si falta configuración de entorno, la app podría arrancar con debug activo y una DSN inválida o de ejemplo; mayor riesgo de fugas de información y mala configuración. | Exigir variables obligatorias en producción, fijar `DEBUG=False` por defecto y documentar solo nombres de variables. Mantener `.env` ignorado y fuera de publicación. |
| `AUD-04` | **Media-alta**: validación de entrada insuficiente en esquemas Pydantic. | `backend/app/schemas/cliente.py:27-29`; `backend/app/schemas/vehiculo.py:28-29`, `:41`; `backend/app/schemas/instalacion.py:23-29`; modelos `backend/app/models/cliente.py:34-36`, `backend/app/models/vehiculo.py:33-34`. | Los campos son `str`/`int` sin longitudes, formatos ni límites; `zonas` y `asignaciones_instaladores` aceptan `dict[str, Any]` arbitrario. Las columnas de texto no declaran longitud. | Se aceptarían valores vacíos, sobredimensionados o con estructura imprevisible; la consistencia de instalaciones depende del cliente que llame a la API. | Añadir `Field(min_length/max_length, pattern, ge/le)` y modelos Pydantic anidados para zonas e instaladores; alinear longitudes con las columnas. |
| `AUD-05` | **Media**: paginación sin límites y filtro que ignora paginación. | `backend/app/api/v1/clientes.py:54-62`; `backend/app/api/v1/vehiculos.py:65-73`; `backend/app/api/v1/instalaciones.py:35-44`; `backend/app/crud/instalacion.py:26-28`. | `skip` y `limit` son `int` sin restricciones; `skip` negativo y `limit` grande son aceptables por el tipo; `get_instalaciones_by_vehiculo` devuelve todas las filas. | Respuestas potencialmente muy grandes e API inconsistente. No se ejecutó prueba de carga; es un riesgo estructural confirmado en código. | Usar `Query(default=0, ge=0)` y `Query(default=100, ge=1, le=100)`; aplicar `offset/limit` también al filtro por vehículo. |
| `AUD-06` | **Media**: manejo de errores y transacciones inconsistente. | `backend/app/api/v1/clientes.py:45-51`; `backend/app/api/v1/vehiculos.py:46-62`; `backend/app/api/v1/instalaciones.py:19-32`; `backend/app/crud/cliente.py:57-59`; `backend/app/crud/vehiculo.py:73-75`; `backend/app/crud/instalacion.py:48-50`. | Los routers de clientes/vehículos capturan `IntegrityError`, pero los CRUD hacen `commit()` sin `rollback()` explícito; instalaciones no captura `IntegrityError`. La validación de duplicados es check-then-create. | Una carrera entre petición y restricción única puede terminar en 500; la sesión queda en estado fallido hasta el cierre de la dependencia. Futuras operaciones de inventario necesitarán atomicidad explícita. | Centralizar `rollback()` ante errores de integridad, capturar `IntegrityError` también en instalaciones y apoyarse en restricciones únicas de BD como fuente de verdad. |
| `AUD-07` | **Media**: documentación abierta y CORS limitado a desarrollo. | `backend/app/main.py:18-36`. | La app usa valores por defecto para `/docs`, `/redoc` y `/openapi.json`; `allow_origins` solo contiene `localhost` y `127.0.0.1:5173`. | En producción se publicaría el esquema completo y el frontend publicado sería bloqueado hasta configurar su origen. | Parametrizar orígenes CORS y exponer documentación solo en entornos autorizados; verificar `OPTIONS` desde el origen publicado. |
| `AUD-08` | **Media**: faltan controles automatizados de calidad y pruebas. | `package.json`; `frontend/package.json`; `backend/requirements.txt`; búsqueda de archivos `test/spec`. | ESLint `v10.14.0` está instalado en la raíz, pero no existe `eslint.config.*`: `eslint frontend/src --ext .ts,.tsx` terminó con código `2`. No hay `pytest`, `ruff`, `black`, `mypy`, `flake8`, `bandit` ni `httpx` en `backend/.venv`; no hay archivos de prueba. | No hay gate automático para regresiones, estilo, tipos de Python ni revisiones de seguridad repetibles. | Agregar configuración ESLint, dependencias de desarrollo y pruebas mínimas cuando se autorice. No instalar nada en esta revisión. |

### 3.2 Riesgos pendientes de verificar

| ID | Riesgo | Por qué no se confirma | Verificación requerida |
| --- | --- | --- | --- |
| `AUD-R1` | Esquema real de PostgreSQL, índices, restricciones y respaldos. | No se conectó a BD; no hay Alembic ni migraciones versionadas en el repositorio. | Con acceso autorizado a un entorno temporal, comparar el esquema con los modelos y revisar política de respaldos. No ejecutar nada sobre producción. |
| `AUD-R2` | Cabeceras de seguridad, limitación de tasa y terminación TLS reales en la plataforma. | No existe servicio desplegado ni configuración de infraestructura versionada. | Revisar configuración de Vercel/Render/Supabase y cabeceras HTTP después de un despliegue autorizado. |
| `AUD-R3` | Exposición de `openapi.json` y `/docs` en un entorno público. | Solo se comprobó localmente con configuración ficticia. | Repetir comprobación contra el entorno publicado y aplicar `AUD-07`. |
| `AUD-R4` | Comportamiento concurrente y consistencia ante fallos parciales. | No se ejecutaron pruebas de concurrencia, carga ni integración real. | Pruebas de integración con BD temporal y casos de doble creación/rollback. |

## 4. Herramientas y dependencias disponibles

- **Frontend:** `frontend/node_modules/.bin/tsc` y `frontend/node_modules/.bin/vite` disponibles y usados; ESLint raíz `v10.14.0` disponible pero sin configuración (`eslint.config.*` ausente; intento con código `2`).
- **Backend:** Python `3.14.0`, FastAPI `0.115.14`, SQLAlchemy `2.0.55`, Pydantic `2.14.1`, pydantic-settings `2.16.1`, psycopg2-binary `2.9.13`, uvicorn `0.54.0` y dependencias transitivas presentes en `.venv`.
- **Ausentes en el entorno backend:** `pytest`, `ruff`, `black`, `mypy`, `flake8`, `bandit`, `httpx`. No se instalaron.
- **Propuesta sin instalar:** configurar ESLint plano; añadir `pytest` + `httpx` para pruebas API; añadir `ruff`/`mypy` como apoyo; añadir `bandit` solo si se decide auditoría estática periódica. Registrar las versiones en un archivo de development requirements cuando se autorice.

## 5. Verificaciones locales ya realizadas

Realizadas el 2026-11-18 sobre el commit `28829d9b447b7bbd79b5747d8b65bcec81e523b3`:

| Comprobación | Resultado | Limitación |
| --- | --- | --- |
| `git rev-parse --show-toplevel`, `git rev-parse HEAD`, `git status --porcelain=v1` | Raíz confirmada; HEAD confirmado; solo los dos archivos untracked preexistentes. | No valida contenido remoto; no se hizo `fetch`. |
| `frontend/node_modules/.bin/tsc --noEmit -p frontend/tsconfig.json` | Código `0`, sin errores. | No prueba comportamiento en navegador. |
| `node_modules/.bin/vite build --outDir <temporal> --emptyOutDir` desde `frontend/` | Código `0`; 97 módulos; artefactos con hashes iguales a `frontend/dist`. | Salida temporal fuera del repositorio; no prueba despliegue. |
| Import de `app.main` con variables ficticias y `PYTHONDONTWRITEBYTECODE=1` | Código `0`; 17 rutas; 10 paths en OpenAPI. | No consultó BD; no acredita permisos ni reglas de negocio. |
| Arranque local efímero con Uvicorn en `127.0.0.1` y configuración ficticia | `GET /` y `GET /openapi.json` respondieron `200`; proceso iniciado fue detenido. | Solo loopback; no se llamaron endpoints de BD. `curl` presentó timeouts por proxy local; se usó `urllib` sin proxy y se conservaron los errores. |
| Comparación final de la verificación inicial | Estado y hashes idénticos a los iniciales en ese momento. | No cubre archivos ignorados no listados; después se aplicó la corrección de `AUD-02`. |
| Confirmación previa del defecto con SQLAlchemy `2.0.55` | `urlparse` conservó `%40`/`%2F` en credenciales y dejó la query fuera; `make_url` devolvió credenciales decodificadas y `sslmode`/`sslrootcert`. | Solo análisis local con valores ficticios; sin conexión. |
| `python -m unittest discover -s tests -v` desde `backend/` con `PYTHONDONTWRITEBYTECODE=1` | Código `0`; 5 pruebas OK con stub de `app.core.config`: query preservada, credenciales escapadas, componentes, sin `psycopg2.connect` y error sin credenciales. | Engine simulado; `backend/.env` no leído; no valida TLS real ni comportamiento del proveedor. |

**Límites globales:** no se ejecutaron migraciones, MCP, indexación ni pruebas de ataque o carga. La conexión de solo lectura y las consultas GET contra Supabase se registran en la sección 9; la validación completa de TLS sigue pendiente. Después de la auditoría inicial se aplicó únicamente la corrección de `AUD-02` y sus pruebas; los demás hallazgos siguen propuestos.

## 6. Comprobaciones necesarias después de corregir

1. Repetir la auditoría con el skill exacto solicitado por el profesor y comparar hallazgos.
2. Repetir `tsc`, build temporal, import/OpenAPI y arranque local con configuración ficticia; añadir comprobación de esquemas de seguridad en OpenAPI.
3. Ejecutar pruebas unitarias y de integración contra una BD temporal autorizada: duplicados, rollback, paginación, respuestas 401/403 y CORS.
4. Verificar que `DEBUG=False` en producción y que las variables obligatorias fallan quick si faltan.
5. Confirmar en un entorno autorizado que la URL de conexión conserva TLS (`sslmode=require` o equivalente del proveedor) sin imprimir valores privados; la conservación local ya quedó demostrada por pruebas unitarias, pero la conexión TLS real sigue pendiente.
6. Revisar cabeceras HTTPS, certificados y documentación expuesta en un despliegue autorizado.
7. Revisar el diff final, hashes de evidencia y estado Git; no hacer commit ni push sin autorización.

## 7. Procedimiento reutilizable para futuras auditorías

1. Fijar alcance, fecha, commit, rama y estado Git; registrar hashes de archivos sensibles sin leer su contenido.
2. Buscar el skill exacto en ubicaciones locales y declarar su ausencia si no se identifica; no usar sustitutos no autorizados.
3. Revisar primero autenticación/autorización, secretos y configuración, validación de entradas, errores/transacciones, TLS de BD, paginación, dependencias y pruebas.
4. Clasificar cada hallazgo como confirmado o riesgo pendiente; asignar ID, severidad justificada, ubicación exacta, evidencia, impacto y corrección mínima.
5. Ejecutar solo verificaciones locales no destructivas con dependencias ya instaladas y salida temporal fuera del repo.
6. Proteger credenciales: variables ficticias, sin valores reales en comandos ni registros, sin bytecode persistente cuando sea relevante.
7. Proponer correcciones sin aplicarlas en la auditoría; definir comprobaciones posteriores antes de implementar.
8. Repetir auditoría después de corregir y conservar evidencia de diferencias.

## 8. Límites y declaraciones

- Esta revisión no es el skill *Security Audit* solicitado: **“Pendiente de repetir o complementar con el skill exacto solicitado por el profesor”**.
- No se afirma que existan vulnerabilidades explotables; se describen condiciones observables en código y su impacto potencial.
- No se afirma capacidad de usuarios, rendimiento, disponibilidad ni resultados de pruebas no ejecutadas.
- No se declara cumplimiento total de la rúbrica docente ni de requisitos no funcionales.
- Durante la auditoría inicial no se modificó código; después se modificaron archivos de backend, frontend, pruebas y documentación para `AUD-02`, integración local, corrección de puerto y Fase 1 del flujo de instalaciones. No se cambiaron dependencias, secretos, esquema real, datos ni ramas; no se hizo commit, push, despliegue, indexación ni MCP.

## 9. Integración local con Supabase (2026-11-18)

### 9.1 Conexión de solo lectura
- Ejecutada una sola vez tras la confirmación de *Restoration complete*: `RESULT exit=0`, sin errores sanitizados.
- `SELECT 1` OK. Esquema `public`: presentes `clientes`, `instalaciones`, `vehiculos`; sin ausencias. Solo se consultaron metadatos; no se leyeron filas de clientes ni datos personales.
- Configuración intacta: `sslmode=require`, sin `sslrootcert`; `certificate_chain_verification=False` y `server_name_verification=False`.
- `pg_stat_ssl` a través del pooler informó `ssl=False`, sin versión ni cifrado. Ese resultado no basta para determinar el cifrado del tramo cliente–pooler. **TLS extremo a extremo pendiente.** `verify-ca` valida la cadena del certificado; `verify-full` valida además el nombre del servidor; ninguno de los dos está activo.
- `backend/.env` no se modificó ni se imprimieron sus valores.

### 9.2 Consultas de API
- Backend Uvicorn en `127.0.0.1:8000`, PID `48577` tras el reinicio de la corrección de puerto y PID `5430` tras la Fase 1, usando la configuración local de `backend/.env`.
- `GET /api/v1/clientes/?limit=1` → `200`, `application/json`, validación `ok`, `rows=1`.
- `GET /api/v1/vehiculos/?limit=1` → `200`, `application/json`, validación `ok`, `rows=1`.
- `GET /api/v1/instalaciones/?limit=1` → `200`, `application/json`, validación `ok`, `rows=1`.
- No se mostraron cuerpos de respuesta. La validación comparó únicamente nombres de claves con `ClienteRead`, `VehiculoRead` e `InstalacionRead`; no hubo claves faltantes ni sobrantes. No se ejecutaron POST, PUT, PATCH ni DELETE.

### 9.3 Columnas y modelos
- Comparación de metadatos de `public` contra los modelos SQLAlchemy: `clientes`, `vehiculos` e `instalaciones` con `status=ok`; sin columnas solo en modelo ni solo en base de datos.
- Log del backend: `TRACEBACK_COUNT=0`, `ERROR_TOKEN_COUNT=0`.

### 9.4 Frontend, fallo de puerto y verificación en navegador
- Fallo observado: Chrome recibió una app distinta (“CAMPORA Demo”) en `http://127.0.0.1:5173`, atendida por el listener IPv6 ajeno `com.docker.backend` PID `89775`. Python sí recibía “Serna Polarizados” desde el Vite local; por tanto, el fallo no era de imports, montaje React ni CORS de la API. No se detuvo ni modificó el proceso Docker.
- Corrección mínima: Vite se reinició en `127.0.0.1:5174`, PID `48820`, con `VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1` inyectado solo en el proceso. No existe `frontend/.env` y no se cambió archivo alguno del frontend.
- Se respaldó `backend/app/main.py` en `/var/folders/2m/26w20_xn0wxc03mgss7033nw0000gn/T/opencode/serna-dbfix.4Uwouf/backup/main.py.pre-port-fix` (hash previo `cdf335e7f9b8e3deadb0294871a911337bdf92c279ad18561ae2ba12b4bc57d3`). Se añadieron los orígenes `http://localhost:5174` y `http://127.0.0.1:5174`; el backend se reinició para aplicarlos.
- Verificación real en Chrome mediante DevTools: título `Serna Polarizados`, `#root` con un hijo, tres botones de navegación y tablas renderizadas en Clientes, Vehículos e Instalaciones. Peticiones a `/api/v1/clientes`, `/api/v1/vehiculos` e `/api/v1/instalaciones` respondieron `200` sin errores CORS. Único error de consola: `404` de `favicon.ico`, no bloqueante.
- URL exacta para volver a probar: `http://127.0.0.1:5174`.
- Procesos iniciados para detener después: PID `5430` (backend, reemplaza a `48577`) y PID `48820` (frontend).

## 10. Fase 1 — flujo centrado en instalaciones (2026-11-18)

### 10.1 Alcance implementado
- `backend/app/core/config.py` incorpora `ADMIN_EMAILS` con valor por defecto vacío y normalización a correos en minúsculas. Los correos confirmados quedan documentados solo en `backend/.env.example`, sin presencia en el frontend ni autorización automática.
- `backend/app/core/catalogs.py` centraliza tecnologías, opacidades, instaladores, tipos de factura y vidrios confirmados. Incluye techo solar doble con paneles `delantero` y `trasero`.
- `backend/app/schemas/registro_instalacion.py` define contratos de entrada, validación de catálogos, regla de un detalle por vidrio/panel y salida de resumen. Una instalación puede combinar tecnologías distintas entre vidrios; cada vidrio conserva una sola tecnología.
- `backend/app/db/schema_status.py` inspecciona metadatos en modo solo lectura y reporta tablas/columnas ausentes. No ejecuta DDL ni consulta filas.
- `backend/app/api/v1/instalaciones.py` expone `GET /catalogos`, `GET /schema-status` y `POST /preview`. El endpoint de resumen no escribe en base de datos.
- `backend/sql/V001__preconditions.sql`, `V001__instalaciones_polarizado.sql` y `V001__rollback.sql` preparan el cambio aditivo futuro y su reversión. **No se ejecutaron.**
- El frontend abre `Instalaciones` por defecto, muestra el listado histórico y el botón `Nueva instalación`. El formulario integrado obtiene catálogos del backend, genera un resumen y mantiene `Guardar instalación (pendiente)` deshabilitado.

### 10.2 Decisiones preservadas
- Servicio activo del nuevo formulario: solo `Polarizado`. No se habilitó película de seguridad ni PPF.
- Tipo de factura `normal` o `electrónica`: solo dato del registro; sin DIAN, correo ni integración externa.
- Sin sesión ficticia, botón de omisión ni localStorage. Autenticación Google/Supabase real queda para una etapa posterior antes de publicar.
- Se conservan los cambios previos de `AUD-02`, los orígenes CORS locales y el puerto `5174`. No se modificó Docker ni el puerto ocupado `5173`.

### 10.3 Verificación
- Pruebas: `15` casos OK (`unittest discover -s tests`) en backend.
- TypeScript y build: `npm run build` OK en frontend.
- API local: `/catalogos` `200` con `4` tecnologías, `3` opacidades, `2` instaladores, `2` tipos de factura y `6` vidrios; `/schema-status` `200` con `save_enabled=false`; `/preview` `200` con resumen y `guardado_habilitado=false`.
- Chrome en `http://127.0.0.1:5174`: formulario cargado, catálogos visibles, resumen generado con datos sintéticos, banner de guardado deshabilitado y botón de guardado inactivo. No hubo mensajes de consola de error ni advertencia. Todas las peticiones nuevas fueron `GET` o `POST /preview`; no se envió ningún `POST /instalaciones/`.
- Log del backend `backend-fase1.log`: vacío, sin tracebacks.

### 10.4 Pendiente
- Autenticación real con Google/Supabase y verificación JWT/JWKS/issuer/audiencia/expiración, además de la lista de administradores.
- Aplicación supervisada del SQL versionado y habilitación condicional del guardado transaccional.
- Definición formal del catálogo y reglas de película de seguridad en laterales.
- URLs productivas, CORS productivo y ejecución del skill exacto *Security Audit* siguen pendientes.

## 11. Fase 2 — persistencia transaccional (2026-11-18)

### 11.1 Alcance implementado
- `backend/app/db/registro_tables.py` define tablas SQLAlchemy Core separadas para no alterar los modelos ORM históricos antes de aplicar la migración.
- `backend/app/services/registro_instalacion.py` guarda propietario, vehículo, instalación y detalles en una sola transacción. Reutiliza cliente por `documento` y vehículo por `placa`; compara datos sin sobrescribirlos; devuelve conflicto `409` cuando el propietario o los datos no coinciden; revierte todo ante fallo; traduce violaciones de unicidad a `DUPLICADO_CONCURRENTE`.
- `backend/app/core/auth.py` mantiene `AUTH_READY=False`. `REGISTRO_WRITE_ENABLED` también nace en `False` en `backend/app/core/config.py` y `backend/.env.example`.
- `POST /api/v1/instalaciones/registro` responde `503 ESCRITURA_NO_HABILITADA` mientras no existan migración y autenticación real. El endpoint no acepta identidad, correo de administrador ni `user_id` del frontend: los contratos usan `extra="forbid"`.
- `GET /api/v1/instalaciones/schema-status` incorpora `write_enabled` y el motivo `ESCRITURA_CERRADA`; `save_enabled` continúa en `false`.
- El frontend mantiene `Guardar instalación (pendiente)` deshabilitado y no llama al endpoint de escritura.

### 11.2 Reglas de guardado
- Se conservan columnas históricas: `tipo_servicio="polarizado"`, `opacidad` sin valor global, `zonas` con vidrio/panel/tecnología/opacidad y `asignaciones_instaladores` con vidrio/panel/instalador.
- `tipo_factura` guarda el identificador `normal` o `electronica`; solo es dato del registro, sin DIAN, correo ni integración externa.
- `instalacion_detalles` guarda una fila por vidrio o panel confirmado. `sunroof_doble` exige `delantero` y `trasero`; el índice único `instalacion_detalles_vidrio_panel_uniq` evita duplicados concurrentes.
- Si un cliente existente tiene datos diferentes, o una placa pertenece a otro cliente o tiene datos diferentes, no se modifica nada y se responde `409` con código y campos en conflicto.
- Para clientes nuevos sin `contacto`, se almacena cadena vacía para cumplir `NOT NULL` sin inventar un dato de contacto.

### 11.3 SQL exacto para revisión — no ejecutado
Origen: `backend/sql/V001__instalaciones_polarizado.sql`. El bloque inicial coincide con `backend/sql/V001__preconditions.sql`.

```sql
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'clientes'
    ) THEN
        RAISE EXCEPTION 'Falta la tabla public.clientes';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'vehiculos'
    ) THEN
        RAISE EXCEPTION 'Falta la tabla public.vehiculos';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'instalaciones'
    ) THEN
        RAISE EXCEPTION 'Falta la tabla public.instalaciones';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_indexes
        WHERE schemaname = 'public'
          AND tablename = 'clientes'
          AND indexdef ILIKE '%UNIQUE%'
          AND indexdef LIKE '%(documento)%'
    ) THEN
        RAISE EXCEPTION 'Falta restricción única en public.clientes.documento';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_indexes
        WHERE schemaname = 'public'
          AND tablename = 'vehiculos'
          AND indexdef ILIKE '%UNIQUE%'
          AND indexdef LIKE '%(placa)%'
    ) THEN
        RAISE EXCEPTION 'Falta restricción única en public.vehiculos.placa';
    END IF;
END $$;

ALTER TABLE public.clientes ADD COLUMN IF NOT EXISTS telefono text;
ALTER TABLE public.clientes ADD COLUMN IF NOT EXISTS email text;
ALTER TABLE public.vehiculos ADD COLUMN IF NOT EXISTS marca text;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS tipo_factura text;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'instalaciones_tipo_factura_check'
    ) THEN
        ALTER TABLE public.instalaciones
        ADD CONSTRAINT instalaciones_tipo_factura_check
        CHECK (tipo_factura IN ('normal', 'electronica'));
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS public.catalogo_tecnologias_polarizado (
    id text PRIMARY KEY,
    label text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.catalogo_opacidades_polarizado (
    id text PRIMARY KEY,
    label text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.catalogo_instaladores (
    id text PRIMARY KEY,
    label text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.catalogo_tipos_factura (
    id text PRIMARY KEY,
    label text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.catalogo_vidrios_polarizado (
    id text PRIMARY KEY,
    label text NOT NULL,
    paneles text[] NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS public.instalacion_detalles (
    id bigserial PRIMARY KEY,
    instalacion_id integer NOT NULL REFERENCES public.instalaciones(id) ON DELETE CASCADE,
    vidrio_id text NOT NULL REFERENCES public.catalogo_vidrios_polarizado(id),
    panel text,
    tecnologia_id text NOT NULL REFERENCES public.catalogo_tecnologias_polarizado(id),
    opacidad_id text NOT NULL REFERENCES public.catalogo_opacidades_polarizado(id),
    instalador_id text NOT NULL REFERENCES public.catalogo_instaladores(id),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT instalacion_detalles_vidrio_panel_check CHECK (
        (vidrio_id = 'sunroof_doble' AND panel IN ('delantero', 'trasero'))
        OR (vidrio_id <> 'sunroof_doble' AND panel IS NULL)
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS instalacion_detalles_vidrio_panel_uniq
ON public.instalacion_detalles (
    instalacion_id,
    vidrio_id,
    COALESCE(panel, 'unico')
);

INSERT INTO public.catalogo_tecnologias_polarizado (id, label) VALUES
    ('high_definition_premium', 'High Definition Premium'),
    ('ultra_hd', 'Ultra HD'),
    ('color_stable', 'Color Stable'),
    ('ceramic_ir', 'Ceramic IR')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.catalogo_opacidades_polarizado (id, label) VALUES
    ('5', '5 %'),
    ('20', '20 %'),
    ('35', '35 %')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.catalogo_instaladores (id, label) VALUES
    ('daniel_mira', 'Daniel Mira'),
    ('joseth_mora', 'Joseth Mora')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.catalogo_tipos_factura (id, label) VALUES
    ('normal', 'Normal'),
    ('electronica', 'Electrónica')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.catalogo_vidrios_polarizado (id, label, paneles) VALUES
    ('parabrisas', 'Parabrisas', '{}'),
    ('laterales_delanteros', 'Laterales delanteros', '{}'),
    ('laterales_traseros', 'Laterales traseros', '{}'),
    ('luneta', 'Luneta', '{}'),
    ('sunroof_simple', 'Techo solar simple', '{}'),
    ('sunroof_doble', 'Techo solar doble', ARRAY['delantero', 'trasero'])
ON CONFLICT (id) DO NOTHING;
```

### 11.4 Verificación
- Pruebas: `24` casos OK, incluidas reutilización, conflictos, rollback, duplicado concurrente y endpoint cerrado. Todas usan SQLite en memoria.
- TypeScript y build: `npm run build` OK. `git diff --check` y `compileall` sin salida.
- API local: `GET /schema-status` `200` con `save_enabled=false`, `write_enabled=false`, `schema_ready=false` y `ESCRITURA_CERRADA`; `POST /registro` `503 ESCRITURA_NO_HABILITADA`. No se escribió en Supabase.
- Chrome en `http://127.0.0.1:5174`: catálogos cargados, botón de guardado inactivo, sin errores ni advertencias de consola. Network solo registra `GET`, incluidos `catalogos` y `schema-status`; no hay `POST /registro`.

### 11.5 Siguiente etapa
- Conectar Google/Supabase Auth y validar JWT/JWKS/issuer/audiencia/expiración en backend antes de cambiar `AUTH_READY`.
- Aplicar el SQL bajo supervisión, confirmar `/schema-status` con `schema_ready=true` y solo entonces evaluar `REGISTRO_WRITE_ENABLED=true`.
- Definir catálogo y reglas de película de seguridad; mantener esa selección bloqueada hasta entonces.

## 12. Fase 3 — navegación, historial, precios y garantía (2026-11-18)

### 12.1 Navegación y formulario
- `frontend/src/App.tsx` expone exactamente tres apartados: `Nueva instalación`, `Registro de instalaciones` e `Inventario`. No hay pestañas `Clientes` ni `Vehículos`; sus entidades y servicios no se eliminaron.
- `Nueva instalación` conserva fecha, retiro de material, observaciones, propietario, vehículo, factura y detalles por vidrio. Muestra un único campo `Teléfono`; el backend sincroniza `contacto` y `telefono` para mantener compatibilidad con registros históricos y contratos existentes.
- `Registro de instalaciones` es exclusivamente historial y consulta; no mezcla el formulario de creación.
- `Inventario` muestra únicamente `Próximamente`.

### 12.2 Historial
- `GET /api/v1/instalaciones/historial` acepta `q`, `skip` y `limit`. Ordena por `fecha DESC`, con desempate `id DESC`. La búsqueda `q` se ejecuta en base sobre documento del propietario o placa del vehículo.
- `GET /api/v1/instalaciones/{instalacion_id}/detalle` devuelve propietario, vehículo, fecha, vidrios, tecnologías, opacidades, instaladores, retiro, observaciones y desglose cuando existe. Los registros históricos sin precios muestran `Sin información de precios en el registro histórico`.
- El frontend pagina, busca y abre el detalle sin incluir creación.

### 12.3 Precios COP
- `backend/app/core/pricing.py` centraliza tarifas y reglas. Tarifas confirmadas por sección: `High Definition Premium=250000`, `Ultra HD=350000`, `Color Stable=400000`, `Ceramic IR=550000` COP.
- `parabrisas`, `luneta` y `panorámico trasero` cuentan una sección. `laterales_delanteros` y `laterales_traseros` cuentan una sección por par, no por vidrio individual.
- El desglose incluye `concepto`, `secciones`, `importe_cop`, `estado`, `moneda`, `total_cop` y `etiqueta_total`. Los importes son cálculo del backend; los contratos prohíben recibir totales del navegador.
- Casos pendientes: unidad del incremento de película de seguridad en laterales (`100000`), lateral individual, fijos, sunroof doble y pares con tecnologías diferentes. Se muestran como `Precio pendiente de definir` y no producen total definitivo. No se hace backfill de precios en instalaciones antiguas.

### 12.4 Garantía
- `backend/app/services/garantias.py` agrega novedades a la instalación original sin sobrescribirla. Campos: `fecha_atencion`, `motivo`, `descripcion` y `registrado_por`, tomado de la identidad autenticada, nunca del cuerpo.
- `POST /api/v1/instalaciones/{instalacion_id}/novedades` sigue cerrado con `503 ESCRITURA_NO_HABILITADA` mientras no existan Auth y permisos de administrador reales. No hay agenda, aprobación automática ni vencimientos.

### 12.5 SQL exacto para revisión — no ejecutado
Origen: `backend/sql/V002__precios_instalaciones.sql`.

```sql
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS desglose_precios jsonb;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS tarifas_aplicadas jsonb;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS moneda text;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS precio_estado text;
ALTER TABLE public.instalaciones ADD COLUMN IF NOT EXISTS precio_total_cop bigint;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'instalaciones_precio_estado_check'
    ) THEN
        ALTER TABLE public.instalaciones
        ADD CONSTRAINT instalaciones_precio_estado_check
        CHECK (precio_estado IN ('definido', 'pendiente'));
    END IF;
END $$;
```

Origen: `backend/sql/V003__novedades_garantia.sql`.

```sql
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'instalaciones'
    ) THEN
        RAISE EXCEPTION 'Falta la tabla public.instalaciones';
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS public.instalacion_novedades (
    id bigserial PRIMARY KEY,
    instalacion_id integer NOT NULL REFERENCES public.instalaciones(id) ON DELETE CASCADE,
    fecha_atencion timestamptz NOT NULL,
    motivo text NOT NULL,
    descripcion text NOT NULL,
    registrado_por text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS instalacion_novedades_instalacion_fecha_idx
ON public.instalacion_novedades (instalacion_id, fecha_atencion DESC);
```

### 12.6 Verificación
- Pruebas: `37` casos OK con `.venv/bin/python -m unittest discover -s tests -v`, incluidos orden, paginación, búsqueda en base, detalle, tarifas, casos pendientes, teléfono único y novedades aditivas. Todas usan SQLite en memoria.
- TypeScript y build: `npm run build` OK.
- API local: tarifas COP correctas en `/catalogos`; `/historial?skip=0&limit=2` devolvió ids `[5, 4]` de `7`; búsqueda por placa `VGP76G` devolvió `[5]`; `/5/detalle` devolvió propietaria, placa, vidrios y opacidades; preview confirmado `350000`; preview pendiente devolvió `total_cop=null`. `/registro` y `/novedades` devolvieron `503 ESCRITURA_NO_HABILITADA`. No se escribió en Supabase.
- Chrome en `http://127.0.0.1:5174`: tres pestañas exactas, un solo teléfono, resumen con desglose `Total confirmado: $ 250.000`, historial ordenado y buscable, detalle visible e `Inventario` con `Próximamente`. No hay errores de aplicación; el único `404` es `favicon.ico` y persisten avisos de accesibilidad preexistentes en campos sin etiqueta.

### 12.7 Pendiente
- Aplicar V002 y V003 bajo supervisión y confirmar `/schema-status` con los nuevos requisitos.
- Conectar Google/Supabase Auth antes de habilitar `AUTH_READY`, escrituras y novedades de garantía.
- Definir las reglas de precios pendientes antes de mostrar totales definitivos para esos casos.

## 13. Autenticación Google con Supabase

### 13.1 Arquitectura implementada
- La SPA usa el flujo oficial de Supabase con PKCE: `supabase.auth.signInWithOAuth({ provider: 'google' })`, `getSession`, `onAuthStateChange`, `refreshSession` y `signOut`. No hay sesiones simuladas, banderas de desarrollo ni tokens manipulados a mano.
- El frontend adjunta el access token como `Authorization: Bearer <token>` en cada llamada a la API. Solo un `401 TOKEN_EXPIRADO` intenta refresh una sola vez; si falla, emite `auth:expired` y muestra la pantalla de acceso sin datos protegidos. Un `401 TOKEN_INVALIDO` no dispara refresh ni cierra la sesión.
- El backend no confía en correos ni roles enviados por el navegador. `SupabaseTokenVerifier` valida el JWT con JWKS público de Supabase, algoritmos asimétricos permitidos, `kid`, firma, `iss`, `aud`, `exp`, `sub` y `role=authenticated`. El estado del correo se obtiene de `GET /auth/v1/user` (`email_confirmed_at`), no de un claim del token. Para proyectos antiguos con HS256 se incluye el modo `auth_server` con la misma comprobación.
- Autorización: solo los dos correos administradores configurados en el entorno local pueden acceder, con correo verificado. Sesión ausente o token inválido devuelve `401`; usuario verificado no autorizado o correo sin verificar devuelve `403`; configuración incompleta devuelve `503`.
- `/` y `/health` devuelven solo estado del servicio. `/api/v1/auth/session` está fuera del middleware de autorización para poder informar el estado de sesión. Todas las rutas de clientes, vehículos, instalaciones, catálogos, historial, búsqueda, detalle, registro y novedades exigen administrador autenticado.
- El guardado se habilitó solo después de comprobar Auth, allowlist, esquema y permisos; `REGISTRO_WRITE_ENABLED=True` queda únicamente en `backend/.env` ignorado. Las migraciones aditivas se aplicaron y las pruebas de escritura se hicieron sin persistir datos.

### 13.2 Variables de ejemplo — sin secretos
Backend, en `backend/.env`, copiando de `backend/.env.example`:

```dotenv
ADMIN_EMAILS=correo.admin.1@example.com,correo.admin.2@example.com
REGISTRO_WRITE_ENABLED=False
SUPABASE_URL=<URL_DEL_PROYECTO_SUPABASE>
SUPABASE_PUBLISHABLE_KEY=<PUBLISHABLE_KEY_DE_SUPABASE>
SUPABASE_JWKS_URL=<OPCIONAL_SOLO_SI_SUPABASE_MUESTRA_OTRA_URL>
SUPABASE_JWT_ISSUER=<OPCIONAL_SOLO_SI_SUPABASE_MUESTRA_OTRO_ISSUER>
SUPABASE_JWT_AUDIENCE=authenticated
SUPABASE_VERIFY_MODE=jwks
```

Frontend, en `frontend/.env.local`, copiando de `frontend/.env.example`:

```dotenv
VITE_SUPABASE_URL=<URL_DEL_PROYECTO_SUPABASE>
VITE_SUPABASE_PUBLISHABLE_KEY=<PUBLISHABLE_KEY_DE_SUPABASE>
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

- Usar solo la URL y la publishable/anon key. No usar `service_role`, contraseña de base de datos ni secretos del servidor en el frontend.
- Para proyectos Supabase nuevos, mantener `SUPABASE_VERIFY_MODE=jwks`. Si el proyecto es antiguo y usa claves HS256 legacy, cambiar a `auth_server`; el backend validará el token contra el servidor de Auth de Supabase.
- Los valores reales deben cargarse localmente; no han sido pegados en este chat ni en archivos versionados.

### 13.3 Configuración externa pendiente
1. En Google Cloud, crear o seleccionar un proyecto y configurar Google Auth Platform / pantalla de consentimiento con los datos reales del propietario.
2. En `Audience`, usar `External` con ambos correos como usuarios de prueba mientras la app esté en testing, o configurar el acceso interno apropiado. Verificar que los dos correos administradores puedan iniciar sesión.
3. Crear un `OAuth client ID` de tipo `Web application`.
4. En `Authorized redirect URIs`, pegar literalmente la callback que Supabase muestra en `Authentication > Providers > Google` como `Callback URL (for OAuth)`. No inventar ni reutilizar un project ref: el valor real es el que muestre el Dashboard.
5. En Supabase, habilitar `Authentication > Providers > Google` y pegar el `Client ID` y `Client Secret` de Google.
6. En Supabase, ir a `Authentication > URL Configuration`; fijar `Site URL` en `http://127.0.0.1:5174` y agregar `http://127.0.0.1:5174/` como Redirect URL permitida para desarrollo local.
7. Copiar la Project URL y la publishable/anon key a los archivos de entorno locales. No copiar la service_role key.
8. Probar inicio de sesión con ambos correos. Solo después de eso puede afirmarse que el flujo Google completo funciona.

### 13.4 Verificación local realizada
- Backend: `compileall -q app tests` OK; `unittest discover -s tests -v` OK con `55` casos, incluidos dobles para sesión ausente, token inválido, token expirado, correo no verificado, administrador permitido, segundo administrador permitido, usuario no autorizado, ausencia de configuración, rutas protegidas, firma JWKS, `iss`, `aud`, `exp` y algoritmos no asimétricos.
- API local con backend reiniciado en PID `89989`: `/health` → `200 ok`; `/api/v1/auth/session`, catálogos, historial, clientes, vehículos y registro sin token → `401 AUTENTICACION_REQUERIDA`; token presente sin variables Supabase → `503 AUTENTICACION_NO_CONFIGURADA`; log del backend vacío, sin tokens impresos.
- Frontend: `npm run build` OK con `tsc` y Vite. En Chrome `http://127.0.0.1:5174` aparece la pantalla `Serna Polarizados`, `Acceso de administradores`, aviso de variables pendientes y botón `Continuar con Google` deshabilitado. No se renderizan datos protegidos. Único error de consola: `404` de `favicon.ico`; sin logs de tokens.
- Dependencias: `PyJWT[crypto]>=2.10,<3` en backend y `@supabase/supabase-js` en frontend. `npm install` reportó vulnerabilidades preexistentes/transitivas; no se ejecutó `npm audit fix` ni se cambiaron dependencias no relacionadas.
- No se hizo commit, push, despliegue, cambio de SQL ni escritura en Supabase.

### 13.5 Estado de la lista anterior
- Los valores reales de Supabase están cargados solo en entornos locales ignorados; los pasos externos de Google/Supabase quedaron resueltos para el ingreso comprobado.
- El flujo Google completo quedó confirmado con un correo administrador real; la verificación con el segundo correo sigue pendiente si se considera necesaria.
- V001, V002, V003 y V004 ya se aplicaron; el detalle está en §13.9.
- Las escrituras se habilitaron únicamente después de verificar esquema, auth y permisos efectivos; no se habilitaron antes.

### 13.6 Diagnóstico de `TOKEN_INVALIDO` tras el ingreso Google
- Evidencia sanitizada: el frontend envía `session.access_token` (`frontend/src/services/api.ts:21`), no el token del proveedor Google. Frontend y backend comparten el mismo proyecto y key de Supabase. El JWKS configurado responde `200`, con una clave EC y `kid`; por eso no se atribuyó el fallo a resolución de claves.
- Causa comprobada por la definición oficial de `AccessTokenClaims` de Supabase Auth: el access token no incluye el claim superior `email_verified`. El verificador lo exigía como requerido en `backend/app/core/token_verifier.py`, por lo que `jwt.decode` fallaba y se mapeaba a `401 TOKEN_INVALIDO`, aunque la firma, emisor, audiencia y expiración fueran válidos.
- Corrección mínima: se conservó la verificación criptográfica JWKS de firma, `iss`, `aud`, `exp`, `sub` y `role`; se dejó de exigir el claim ausente y se consulta `GET /auth/v1/user` con el mismo access token para obtener el estado confiable del correo desde `email_confirmed_at`. Un claim `email_verified` falso o verdadero en el token ya no decide la autorización.
- Comportamiento de sesión: el interceptor ya no fuerza refresh ni `auth:expired` para `TOKEN_INVALIDO`; solo refresca ante `TOKEN_EXPIRADO`. Se añadió una guard contra llamadas duplicadas de `/auth/session` durante el evento inicial de Supabase.
- Pruebas: 58 casos OK, incluidos token sin `email_verified` con perfil confirmado, perfil no confirmado → `403 CORREO_NO_VERIFICADO`, fallo del perfil → `503`, y firma/emisor/audiencia/expiración rechazados. `npm run build` OK. Queda pendiente la verificación real en navegador con una sesión Google válida de los administradores autorizados.

### 13.7 Comprobación real del usuario
- El usuario completó el flujo de Google en el navegador controlado por herramientas y confirmó que se muestra el formulario de instalación; no se registraron tokens, correos ni datos personales en esta comprobación.
- Este hecho es una comprobación manual del usuario, distinta de las 58 pruebas automatizadas de la sección anterior; las pruebas automatizadas no sustituyen este ingreso real.
- El estado visible del formulario es `ESQUEMA_PENDIENTE` y `ESCRITURA_CERRADA`, coherente con la configuración actual: la autenticación ya funciona, pero el esquema de soporte y el habilitador de escritura siguen pendientes.
- Se conserva la restricción de no aplicar migraciones ni habilitar escrituras sin aprobación explícita; el siguiente paso es solo inspección, respaldo y propuesta.

### 13.8 Inspección real del esquema antes de migrar
- Inspección ejecutada contra PostgreSQL 17.11 con `transaction_read_only=on`; solo se consultaron catálogos y conteos. No se ejecutó DDL/DML, no se imprimieron filas, credenciales ni cadenas de conexión.
- No hay ledger de migraciones de la aplicación en `public`; las únicas tablas de migración encontradas pertenecen a esquemas internos `auth`, `realtime` y `storage`. Por eso la comparación se hizo objeto por objeto y no se asumió ninguna migración aplicada.
- Tablas reales en `public`: solo `clientes`, `vehiculos` e `instalaciones`. Faltan las 7 tablas esperadas: cinco catálogos, `instalacion_detalles` e `instalacion_novedades`.
- Columnas ausentes: `clientes.telefono`, `clientes.email`, `vehiculos.marca`, `instalaciones.tipo_factura`, `instalaciones.desglose_precios`, `instalaciones.tarifas_aplicadas`, `instalaciones.moneda`, `instalaciones.precio_estado`, `instalaciones.precio_total_cop`.
- Restricciones ausentes: `instalaciones_tipo_factura_check` e `instalaciones_precio_estado_check`. Sí existen los índices únicos previos `ix_clientes_documento` e `ix_vehiculos_placa`, por lo que `V001__preconditions.sql` pasaría.
- Con la publishable/anon key, `GET /rest/v1/{tabla}?limit=0` devuelve `200` para las tres tablas existentes y `404 PGRST205` para las siete faltantes. No se devolvieron filas.
- RLS está desactivado en las tres tablas existentes y no hay policies. Los roles `anon`, `authenticated` y `service_role` tienen privilegios completos de tabla (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, `REFERENCES`, `TRIGGER`). Esto amplía la exposición de datos personales y debe resolverse antes de habilitar escrituras; no se modificó en esta inspección.
- Correspondencia de migraciones: `V001__instalaciones_polarizado.sql` cubre 6 tablas, las 3 columnas base y el check de `tipo_factura`; `V002__precios_instalaciones.sql` cubre las 5 columnas de precios y su check; `V003__novedades_garantia.sql` cubre `instalacion_novedades` y su índice. `V001__rollback.sql` no debe ejecutarse: contiene `DROP` de tablas y columnas.
- Conservación: los tres archivos propuestos usan `ADD COLUMN IF NOT EXISTS`, `CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS` e `INSERT ... ON CONFLICT DO NOTHING`; no contienen `DROP`, `TRUNCATE` ni actualizaciones de filas existentes. Las columnas nuevas son anulables, por lo que no exigen backfill ni reescritura de registros antiguos.
- Respaldo privado: se generó fuera del repositorio un respaldo lógico con DDL de las tres tablas base, CSV por tabla, manifiesto, `SHA256SUMS` y un `restore.py` sin secretos. Permisos `0600`; hashes y cabeceras/conteos verificados. La ruta absoluta no se registra aquí. No se ejecutó una restauración real porque no hay `psql`/`pg_restore` ni servidor PostgreSQL local; el procedimiento quedó documentado en el propio directorio privado.
- Transaccionalidad confirmada por código y pruebas: `guardar_registro` realiza propietario, vehículo, instalación y detalles en una sola `Session`, llama a `flush()` y solo después a `commit()`; cualquier excepción ejecuta `rollback()`. La prueba `test_rollback_completo_si_falla_detalle` fuerza un fallo después de insertar instalación y verifica cero filas en las cuatro tablas.
- Prueba ficticia posterior propuesta: ejecutar `guardar_registro` con el payload ficticio de `tests/test_registro_persistence.py` dentro de una transacción explícita que se revierte, comprobando dentro de ella conteos `1/1/1/3`; así no quedan registros en la base real. Solo después de aprobación se podría repetir desde la UI con datos ficticios y limpieza controlada.

### 13.9 Aplicación supervisada y cierre de acceso directo
- Autorización ejecutada: se aplicaron solo cambios aditivos y de permisos; no se usaron `DROP`, `TRUNCATE`, actualizaciones de filas existentes ni `service_role`. No se hizo commit, push ni despliegue.
- Respaldos privados fuera del repositorio: uno previo a la migración y otro posterior, ambos con DDL, CSV por tabla, manifiesto, instantánea de seguridad y `SHA256SUMS`. Permisos `0600`; hashes, cabeceras y conteos verificados. La ruta absoluta y el contenido no se registran aquí. La restauración real sigue sin ejecutarse por falta de `psql`/`pg_restore` y servidor local, por lo que no se presenta como probada.
- Revisión previa: no aparecieron sentencias destructivas en `V001__preconditions.sql`, `V001__instalaciones_polarizado.sql`, `V002__precios_instalaciones.sql`, `V003__novedades_garantia.sql` ni `V004__proteger_tablas_negocio.sql`. `V001__rollback.sql` quedó explícitamente excluido.
- Migraciones aplicadas en una sola transacción y confirmadas: `V001__preconditions.sql` → `V001__instalaciones_polarizado.sql` → `V002__precios_instalaciones.sql` → `V003__novedades_garantia.sql` → `V004__proteger_tablas_negocio.sql`. Los conteos de `clientes`, `vehiculos` e `instalaciones` no cambiaron.
- Estado tras migración: `missing_requirements=[]`, `schema_ready=true`, `write_enabled=false` y `reasons=["ESCRITURA_CERRADA"]` antes de activar el habilitador. La tabla `instalacion_novedades` y los índices `instalacion_detalles_vidrio_panel_uniq` e `instalacion_novedades_instalacion_fecha_idx` se verificaron directamente en catálogo.
- `V004__proteger_tablas_negocio.sql` habilitó RLS en las 10 tablas de negocio, revocó privilegios de tabla y secuencia a `anon` y `authenticated`, conservó el acceso del rol `postgres` usado por FastAPI y recargó el esquema de PostgREST. No se crearon policies: el acceso legítimo ocurre por el owner de las tablas, no por el API público.
- Permisos efectivos comprobados: `SET LOCAL ROLE anon` y `SET LOCAL ROLE authenticated` seguidos de `SELECT` en `public.clientes` devuelven `42501` en ambos casos. Con la publishable key y sin token, `GET /rest/v1/{tabla}?limit=0` devuelve `401` con `42501` para las 10 tablas. Las rutas locales sin sesión devuelven `401 AUTENTICACION_REQUERIDA` y un token inválido devuelve `401 TOKEN_INVALIDO`.
- Escrituras habilitadas solo después de esas comprobaciones mediante `REGISTRO_WRITE_ENABLED=True` en `backend/.env` ignorado. El backend se reinició y `schema_status` pasó a `save_enabled=true`, `write_enabled=true`, `reasons=[]`, sin exponer secretos ni correos en logs. `preview` también informa `guardado_habilitado=true` con `motivos=[]`, y el botón verde `Guardar instalación` queda activo después de generar el resumen.
- Transaccionalidad comprobada contra la base real sin persistencia: un guardado ficticio con tres vidrios dio conteos internos `1/1/1/3` dentro de la transacción; después del rollback los conteos volvieron a su estado original. Un fallo forzado en el tercer detalle también dejó los conteos originales. No quedaron registros de prueba en la base.
- Pruebas finales: `compileall -q app tests` OK, `unittest discover -s tests -v` OK con `58` casos, `npm run build` OK y `git diff --check` OK. Dos pruebas que asumían escritura cerrada se ajustaron para fijar explícitamente el flag a `False` dentro de la prueba, sin depender del entorno local.
- El navegador controlado por herramientas se reinició y Google rechazó el ingreso con `No puedes acceder`. El usuario decidió hacer la comprobación visual en su Chrome habitual y pidió no evadir el bloqueo ni copiar sesiones/tokens entre navegadores; esa restricción se respeta. No se imprimieron tokens, claves ni correos.
- Para cerrar la brecha entre API y UI se ajustaron `get_schema_status`, `build_preview`/endpoint de resumen, tipos y servicio del frontend, y `InstalacionForm`: el resumen refleja el estado real y existe una acción `Guardar instalación` que envía el mismo payload validado a `POST /instalaciones/registro`. `58` pruebas OK, `npm run build` OK y backend reiniciado en PID `92783`.
- Pendiente: ejecución manual por el usuario en su navegador con los datos de §13.10, verificación de persistencia tras recarga y búsqueda, y evidencia real de usuario no autorizado si se dispone de una sesión Google no administradora.

### 13.10 Prueba manual del usuario — instrucción entregada, resultado pendiente
- Esta sección registra una prueba manual del usuario. No es una prueba automatizada y no debe presentarse como tal hasta que el usuario confirme cada resultado en su navegador.
- El usuario usará su Chrome habitual en `http://127.0.0.1:5174`. No se copiará sesión, token ni clave entre navegadores.
- Datos ficticios exactos, marcados como `DEMOSTRACIÓN`, sin datos personales reales:
  - Propietario → Documento: `DEMO-20261119-001`; Nombre: `DEMOSTRACION PRUEBA`; Teléfono: `0000000000`; Correo electrónico: `demo.20261119@example.invalid`.
  - Tipo de factura: `Normal`.
  - Vehículo → Placa: `DEMO-001`; Marca: `DEMOSTRACION`; Descripción: `VEHICULO DEMOSTRATIVO - NO DATOS REALES`.
  - Datos adicionales → Fecha: `2026-11-20T10:00`; Retiro de material anterior: sin marcar; Observaciones: `PRUEBA MANUAL DEMOSTRACION - REGISTRO FICTICIO`.
  - Vidrio 1: `Parabrisas`, sin panel, `Ultra HD`, `35 %`, `Daniel Mira`.
  - Vidrio 2: `Techo solar doble`, panel `delantero`, `Ceramic IR`, `20 %`, `Joseth Mora`.
  - Vidrio 3: `Techo solar doble`, panel `trasero`, `Ceramic IR`, `20 %`, `Joseth Mora`.
- Procedimiento: pulsar `+ Agregar vidrio` dos veces; completar los tres vidrios; pulsar `Generar resumen`; confirmar `Cantidad de vidrios: 3`, `Guardado: habilitado` y el botón verde `Guardar instalación`; pulsar guardar; recargar la página; buscar `DEMO-20261119-001` y luego `DEMO-001` en el campo `Cédula del propietario o placa del vehículo`; abrir `Ver detalle` y confirmar los tres vidrios y sus tecnologías.
- Resultado esperado del resumen: `Total confirmado: $ 250.000` para el parabrisas y `Precio pendiente de definir` para los dos paneles del techo solar doble; por eso el total general también es `Precio pendiente de definir`. Esto es coherente con las reglas de precios pendientes y no debe interpretarse como un error.
- Evidencia manual recibida del usuario, no automatizada: visualizó el historial y un resumen con Ultra HD en cuatro secciones a `$ 350.000` por sección y total `$ 1.400.000`. El resumen todavía indicaba que no estaba guardado.
- No se registra persistencia confirmada para `DFH864`: el usuario aún no ha reportado el resultado de guardar, recargar y buscar esa placa. Una consulta de solo lectura a la base devolvió `0` filas con esa placa en el momento de la revisión.
- El mensaje de resumen observado puede corresponder a una pantalla/bundle anterior al ajuste que hace que `preview` refleje `schema_status`; el código y la API actuales ya devuelven `guardado_habilitado=true`. No se afirma que la persistencia haya sido probada.

### 13.11 Revisión de instalaciones 10 y 11 y bloqueo de envíos repetidos
- Revisión de solo lectura, sin borrar ni modificar registros. Las instalaciones `10` y `11` comparten vehículo, placa (no se repite aquí), fecha y hora de trabajo, `tipo_factura=electronica`, estado `programado`, retiro de material anterior y un solo vidrio cada una.
- No comparten payload: la instalación `10` registra `Parabrisas - High Definition Premium`, 1 sección, `$ 250.000`; la instalación `11` registra `Parabrisas - Ceramic IR`, 1 sección, `$ 550.000`. El desglose y los detalles difieren.
- Sus `created_at` están separados por `30.06` segundos; cada detalle tiene el mismo `created_at` que su instalación y ambas tienen `updated_at=null`. No hay evidencia de reenvío idéntico; la lectura más consistente es dos envíos manuales independientes con cambio de tecnología entre ellos.
- No existe una restricción única en base por `vehículo + fecha`, por lo que un doble envío con payload idéntico sí podría crear dos filas. Para reducirlo en la UI se reforzó `InstalacionForm`: un `ref` sincrónico bloquea un segundo clic durante la petición, y el botón queda deshabilitado mientras procesa y después de mostrar el resultado exitoso. Tras un error vuelve a habilitarse.
- Verificación local tras el ajuste: `58` pruebas OK, `npm run build` OK y backend reiniciado en PID `33204`. No se agregó funcionalidad nueva ni se borraron registros.
