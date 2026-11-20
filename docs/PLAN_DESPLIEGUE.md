# PLAN DE DESPLIEGUE — SERNA POLARIZADOS

> Propuesta de infraestructura para el stack existente. No crea servicios, no contrata planes, no publica código, no ejecuta migraciones, no conecta a Supabase y no declara despliegue realizado. Las correcciones pendientes están descritas en `docs/PLAN_AUDITORIA_Y_MEJORA.md`.

## 1. Identificación

- **Fecha de la propuesta:** 2026-11-18.
- **Commit considerado:** `28829d9b447b7bbd79b5747d8b65bcec81e523b3`.
- **Repositorio:** `/Users/usuario/Desktop/ElectivaCpc/Serna_Polarizados`.
- **Stack actual:** React 18 + TypeScript + Vite + Tailwind en `frontend/`; FastAPI + SQLAlchemy + Pydantic en `backend/`; PostgreSQL/Supabase como destino de datos.
- **Principios:** un solo repositorio, sin división, sin tecnologías innecesarias, sin microservicios y sin sustituir el stack implementado.

## 2. Evaluación de candidatos

| Capa | Vercel | Render | Decisión preliminar |
| --- | --- | --- | --- |
| Frontend Vite | La documentación oficial permite fijar **Root Directory** en un subdirectorio del monorepo, definir **Build Command** y **Output Directory**, y servirse sobre HTTPS con certificados automáticos. Encaja con `frontend/`. | Render puede alojar sitios estáticos, pero su guía específica no se consultó en detalle en esta revisión; no se propone como configuración aprobada. | **Vercel** para el frontend. |
| Backend FastAPI | No seleccionado: la app actual es un proceso ASGI de larga duración; llevarla a Functions exigiría un adaptador o cambios adicionales no autorizados. | La guía oficial de FastAPI indica Web Service con Python, `pip install -r requirements.txt` y `uvicorn main:app --host 0.0.0.0 --port $PORT`; admite Root Directory y rama de despliegue. | **Render Web Service** para el backend. |
| PostgreSQL | No aplica como base de datos administrada en este plan. | Render ofrece PostgreSQL con URL externa cifrada por TLS, pero también se evaluó Supabase por ser el destino previsto en el código y la documentación. | **Supabase PostgreSQL** como primera opción; Render Postgres como alternativa equivalente si se decide en el acceso. |

No se crearon servicios, no se seleccionaron planes de pago y no se generaron credenciales.

## 3. Topología propuesta

```text
[Navegador]
   │ HTTPS
   ▼
[Vercel — proyecto frontend]  root: frontend/
   │ HTTPS / JSON → VITE_API_BASE_URL
   ▼
[Render Web Service — FastAPI]  root: backend/
   │ SQLAlchemy + DATABASE_URL con TLS
   ▼
[PostgreSQL administrado — Supabase o Render Postgres]
```

## 4. Configuración por servicio

### 4.1 Frontend en Vercel

- **Directorio raíz del servicio:** `frontend/`.
- **Framework Preset:** Vite (detección automática; confirmar en Project Settings).
- **Root Directory:** `frontend`.
- **Install Command:** `npm ci` (existe `frontend/package-lock.json`).
- **Build Command:** `npm run build`.
- **Output Directory:** `dist`.
- **Rama de despliegue automático:** `produccion` (propuesta; aún no creada).
- **Variable de entorno necesaria:** `VITE_API_BASE_URL`.
- **Verificación local equivalente ya realizada:** `tsc --noEmit` y `vite build` con salida temporal; no prueba el entorno Vercel.

### 4.2 Backend en Render Web Service

- **Directorio raíz del servicio:** `backend/`.
- **Root Directory:** `backend`.
- **Runtime:** Python 3.
- **Build Command:** `pip install -r requirements.txt`.
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- **Puerto:** `$PORT` lo proporciona Render; no fijar un valor manual.
- **Health Check Path:** `/` (existe y no consulta base de datos).
- **Rama de despliegue automático:** `produccion` (propuesta; aún no creada).
- **Variables:** las listadas en la sección 5. No incluir valores en el repositorio.
- **Documentación:** Render inicia el servicio con el comando anterior y permite configurar variables, Health Check y Root Directory en el panel.

### 4.3 Base de datos

- **Primera opción:** PostgreSQL administrado en Supabase, usando la cadena de conexión que entregue el proveedor.
- **Alternativa:** PostgreSQL de Render en la misma región que el Web Service; la documentación oficial indica usar la URL interna para menor latencia y la externa para conexiones fuera de Render.
- **TLS:** la conexión externa de Render está cifrada y rechaza `sslmode=disable`; fijar `sslmode=require` o el mecanismo equivalente del proveedor. **Bloqueo:** `backend/app/db/session.py:43-56` descarta actualmente los parámetros de la query al reconstruir la URL (hallazgo `AUD-02`).
- **No se conectó a ninguna base de datos.**

## 5. Variables por nombre

| Variable | Servicio | Uso | Observaciones |
| --- | --- | --- | --- |
| `DATABASE_URL` | Backend | Cadena de conexión PostgreSQL | Debe conservar TLS. Valor solo en el panel del proveedor. |
| `POSTGRES_USER` | Backend | Componente opcional de conexión | Si se usa, debe ser coherente con `DATABASE_URL`. |
| `POSTGRES_PASSWORD` | Backend | Componente opcional de conexión | Secreto; nunca en Git ni en logs. |
| `POSTGRES_HOST` | Backend | Componente opcional de conexión | Host del proveedor. |
| `POSTGRES_PORT` | Backend | Componente opcional de conexión | Normalmente el puerto PostgreSQL del proveedor. |
| `POSTGRES_DB` | Backend | Componente opcional de conexión | Nombre de base de datos. |
| `APP_NAME` | Backend | Metadato de la app | Valor no privado. |
| `APP_VERSION` | Backend | Metadato de la app | Valor no privado. |
| `DEBUG` | Backend | Control de modo depuración | Debe ser `False` en producción (hallazgo `AUD-03`). |
| `CORS_ORIGINS` | Backend | Orígenes permitidos | Nueva variable propuesta; requiere cambio de código porque hoy están hardcodeados (`AUD-07`). |
| `VITE_API_BASE_URL` | Frontend | URL base de Axios | Debe apuntar a la API publicada, con sufijo `/api/v1`. |
| `PORT` | Backend | Puerto asignado por Render | Lo inyecta la plataforma; no definir manualmente. |

No se listan valores privados. `backend/.env` sigue siendo local e ignorado por Git.

## 6. URL de API, CORS, HTTPS y TLS

- **API:** `https://<backend-service>.onrender.com/api/v1`. El nombre real del servicio se decide al crear el servicio autorizado.
- **Frontend:** `https://<frontend-project>.vercel.app` o dominio propio autorizado.
- **`VITE_API_BASE_URL`:** debe construirse desde la URL pública del backend, no desde `localhost`.
- **CORS:** hoy `backend/app/main.py:25-28` solo permite `http://localhost:5173` y `http://127.0.0.1:5173`. Antes de publicar se debe parametrizar el origen Vercel/dominio propio y verificar una petición `OPTIONS` desde ese origen.
- **HTTPS frontend:** la documentación oficial de Vercel indica HTTPS automático para URLs de deployment y dominios, con redirección HTTP→HTTPS `308` y certificados gestionados.
- **HTTPS backend:** Render sirve el Web Service sobre HTTPS en su subdominio; verificar certificado y redirección tras el despliegue.
- **TLS a PostgreSQL:** exigir `sslmode=require` o equivalente; corregir primero `AUD-02` para que el parámetro no se pierda al construir la URL de SQLAlchemy.

## 7. Preparación del esquema existente

- Los modelos actuales definen `clientes`, `vehiculos` e `instalaciones` con claves primarias, índices, unicidad de `documento` y `placa`, foreign keys y columnas JSON.
- No hay Alembic, archivos de migración ni llamadas `create_all` en el repositorio.
- **Plan propuesto, sin ejecutar:**
  1. Revisar y aprobar el SQL derivado de los modelos actuales.
  2. Versionar migraciones en una tarea futura autorizada.
  3. Aplicar primero en una base de datos temporal de staging con respaldo previo.
  4. Comparar esquema resultante vs. modelos: unicidad, FKs, índices, `DateTime(timezone=True)` y columnas JSON.
  5. Decidir explícitamente el comportamiento de borrado: hoy los modelos declaran `cascade="all, delete-orphan"`, mientras el plan estratégico propone `ON DELETE RESTRICT`; no se cambia en esta propuesta.
  6. Solo después de aprobación, repetir sobre el entorno de producción con ventana y respaldo.
- **No se ejecutó ninguna migración ni creación de esquema.**

## 8. Rama de producción y despliegues automáticos

- **Rama propuesta:** `produccion`, derivada de `main` en el momento que se autorice.
- **Estado actual:** solo se observó `main`; no se creó rama, no se hizo `fetch`, `commit`, `push` ni cambio de HEAD.
- **Flujo propuesto:**
  - `main` conserva integración y cambios revisados.
  - `produccion` recibe únicamente versiones aprobadas para publicar.
  - Vercel y Render configuran sus proyectos para desplegar automáticamente al recibir pushes a `produccion`.
  - Los cambios de `frontend/` y `backend/` dispararán el despliegue correspondiente según su Root Directory.
- No se publica desde `main` hasta que exista la rama y la autorización.

## 9. Verificación posterior y reversión

### 9.1 Verificación posterior

1. Confirmar HTTPS y certificado válido en frontend y backend.
2. Verificar que el frontend carga con `VITE_API_BASE_URL` público y sin URLs de localhost.
3. Comprobar `GET /` y la documentación/OpenAPI según la política definida en `AUD-07`.
4. Comprobar `OPTIONS` CORS desde el origen Vercel/dominio propio.
5. Verificar que la conexión a BD usa TLS y que no aparecen secretos en logs.
6. Ejecutar una lectura funcional autorizada contra datos de prueba; no ejecutar pruebas de ataque o carga.
7. Revisar logs de Render y Vercel, health check y estado de los deployments.
8. Registrar fecha, commit desplegado, servicios, variables por nombre y resultado; sin valores privados.

### 9.2 Reversión

- **Frontend:** usar la promoción/rollback a un deployment anterior de Vercel.
- **Backend:** usar el rollback a un deploy anterior de Render.
- **Base de datos:** no existe rollback automático; conservar respaldo y decidir restauración solo con autorización. Si el problema es de configuración, reapuntar la variable de conexión a la última base conocida como válida.
- **Orden recomendado:** detener o revertir el cambio que produjo el error, mantener la versión anterior sirviendo tráfico, verificar de nuevo y documentar la causa. No eliminar servicios ni datos.

## 10. Bloqueos previos a publicar

1. Repetir o complementar la auditoría con el skill exacto solicitado por el profesor.
2. Resolver `AUD-01`: autenticación, autorización y protección de datos.
3. Resolver `AUD-02`: conservar TLS en la URL de SQLAlchemy.
4. Resolver `AUD-03`: configuración de producción con `DEBUG=False` y secretos fuera del repositorio.
5. Resolver `AUD-07`: CORS con el origen público y política de documentación/OpenAPI.
6. Preparar y revisar migraciones del esquema actual; no ejecutar sobre producción sin aprobación y respaldo.
7. Añadir pruebas mínimas y configuración ESLint/lint Python según `AUD-08`.
8. Obtener acceso a las cuentas de Vercel, Render y Supabase y decidir planes/región/dominios.
9. Confirmar la URL pública definitiva del backend y el dominio del frontend antes de fijar `VITE_API_BASE_URL` y CORS.
10. Crear y aprobar la rama `produccion`; publicar solo desde ella.

## 11. Fuentes oficiales consultadas

Documentación consultada el 2026-11-18 mediante Context7:

- Vercel — Monorepos / Root Directory: https://vercel.com/docs/monorepos
- Vercel — Configure a Build: https://vercel.com/docs/builds/configure-a-build
- Vercel — `vercel.json`: https://vercel.com/docs/project-configuration/vercel-json
- Vercel — Encryption and TLS: https://vercel.com/docs/cdn-security
- Vercel — SSL certificates: https://vercel.com/docs/domains/working-with-ssl
- Render — Deploy a FastAPI App: https://render.com/docs/deploy-fastapi
- Render — Web Services: https://render.com/docs/web-services
- Render — Monorepo Support / Root Directory: https://render.com/docs/monorepo-support
- Render — Health checks: https://render.com/docs/health-checks
- Render — PostgreSQL external connections and TLS: https://render.com/docs/postgresql-creating-connecting

## 12. Límites y estado local real

- No se crearon servicios, dominios, bases de datos, ramas ni planes. No se hizo commit, push ni despliegue.
- Estado local al 2026-11-19: autenticación Google/Supabase comprobada con una sesión administradora real; migraciones aditivas `V001` a `V004` aplicadas con respaldo previo y posterior; RLS y revoked de `anon`/`authenticated` verificados; `REGISTRO_WRITE_ENABLED=True` solo en `backend/.env` ignorado; esquema, guardado y resumen de API en estado habilitado. El detalle está en `PLAN_AUDITORIA_Y_MEJORA.md` §13.9.
- La comprobación visual final se hace de forma manual en el Chrome habitual del usuario porque Google rechazó el ingreso en el navegador automatizado. No se intentó evadir ese bloqueo ni copiar sesiones o tokens entre navegadores; la instrucción y los datos ficticios están en §13.10 del plan de auditoría, y su resultado sigue pendiente.
- Se usaron credenciales locales desde archivos de entorno ignorados para las verificaciones autorizadas; no se imprimieron secretos, tokens, claves ni correos, y nada de eso se copió al repositorio.
- No se afirma que el sistema esté listo para producción; los bloqueos de la sección 10 permanecen abiertos hasta revisión, rama aprobada y despliegue autorizado.
- No se declara cumplimiento académico ni resultados de pruebas no ejecutadas.

## 13. Configuración mínima preparada para publicación
- Frontend Vercel: `frontend/vercel.json` declara `framework: vite`, `buildCommand: npm run build`, `outputDirectory: dist` y rewrite SPA a `/index.html`. En el proyecto de Vercel debe fijarse `Root Directory = frontend`. Comando verificado localmente: `npm run build` OK.
- Backend Render: `render.yaml` declara un servicio web Python en rama `produccion`, `rootDir: backend`, `buildCommand: pip install -r requirements.txt`, `startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT`, `healthCheckPath: /`. El arranque con `PORT` exportado se verificó localmente: `GET /` → `200 ok`.
- CORS: `Settings.FRONTEND_ORIGINS` y `backend/app/main.py` reemplazan la lista fija de localhost. En Render debe configurarse con el origen Vercel definitivo, separado por comas si hay varios; no se usa comodín. Localmente conserva los cuatro orígenes `5173/5174`.
- Auth/Supabase: mantener el proveedor Google y su callback actual. Fijar `Site URL` y URLs de redirección permitidas a la URL Vercel definitiva, además de las locales que se conserven. No copiar `service_role`, secretos de Google ni cadenas privadas al frontend.
- Secretos: escaneo de 94 archivos versionados o destinados a versión solo encontró el placeholder `usuario:contrasena@localhost` en `.env.example` y el default de `config.py`. `backend/.env` y `frontend/.env.local` están ignorados. No se imprimieron valores reales.
- Rama: la configuración apunta a `produccion`; no se creó rama, commit, push ni despliegue en esta entrega.
- Variables a configurar en Vercel: `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`, `VITE_API_BASE_URL` con la URL pública de Render más `/api/v1`.
- Variables a configurar en Render: `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`, `ADMIN_EMAILS`, `FRONTEND_ORIGINS`. Ya quedan fijadas en el Blueprint `REGISTRO_WRITE_ENABLED=true` y `DEBUG=False`. Opcionales si el proyecto Supabase lo exige: `SUPABASE_JWT_ISSUER`, `SUPABASE_JWT_AUDIENCE`, `SUPABASE_VERIFY_MODE`, `SUPABASE_JWKS_URL`.
