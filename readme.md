# Serna Polarizados — Sistema de Gestión

Proyecto académico de la asignatura **Electiva CPC: Integración de la IA en el Ciclo de Vida del Software**.

**Estado:** implementación parcial verificable en el repositorio. Existen clientes, vehículos e instalaciones en backend y frontend; el inventario, la autenticación y las pruebas automatizadas siguen pendientes.
**Última actualización documental:** 27 de octubre de 2026 (F2).

## 1. Descripción

Serna Polarizados es un proyecto de sistema web para organizar clientes, vehículos, instalaciones y, en una etapa posterior, el inventario de las dos sedes de la empresa en Ibagué.

El alcance documentado mantiene que ambas sedes compartirán clientes, vehículos e historial de trabajos, mientras que cada sede tendrá su propio inventario de rollos y recortes aprovechables. La implementación actual todavía no incorpora el concepto de sede ni el inventario.

El proyecto se desarrolla por dos estudiantes con apoyo de IA y revisión humana.

## 2. Problema identificado

La entrevista con una asesora y las aclaraciones del administrador participante identificaron estas dificultades:

- Información distribuida entre archivos de Excel, formularios y registros manuales.
- Dependencia de llamadas para recuperar antecedentes de instalaciones.
- Dificultades de los instaladores para registrar información desde sus teléfonos.
- Falta de registro sistemático de entradas, cortes y sobrantes.
- Poca claridad sobre las tecnologías y opacidades disponibles.

También se identificaron problemas de pagos y comisiones. Se documentaron como contexto, pero quedaron fuera de la primera versión.

La [síntesis de la entrevista](docs/ia/entrevista-cliente.md) distingue las declaraciones de la asesora de las decisiones posteriores del administrador.

## 3. Objetivo

Desarrollar un sistema web para las dos sedes de Serna Polarizados en Ibagué que centralice la información de clientes, vehículos y trabajos, y permita controlar el inventario de cada sede relacionando las piezas utilizadas con los trabajos realizados.

## 4. Alcance de la primera versión

### Clientes y vehículos

- Registrar clientes con nombre, documento y contacto.
- Registrar vehículos con placa, descripción y cliente asociado.
- Permitir varios vehículos por cliente.
- Consultar clientes por documento y vehículos por placa.
- Evitar documentos y placas duplicados.

**Estado en el código:** registro y listado de clientes y vehículos implementados; validación de documento y placa duplicados; consulta por documento, placa y cliente disponible en la API. La interfaz muestra formularios y listas, pero todavía no integra la búsqueda por documento o placa.

### Trabajos e historial

- Registrar vehículo, sede, fecha, servicio y valor total.
- Conservar los detalles registrados de tecnología, opacidad, instalador y retiro de película.
- Consultar el historial del vehículo desde ambas sedes.

**Estado en el código:** el modelo `Instalacion` registra vehículo, fecha, tipo de servicio, opacidad, zonas, asignaciones de instaladores, retiro de material anterior, observaciones y estado. No incluye sede ni valor total. La API permite crear, listar y consultar instalaciones, y filtrar por vehículo; la interfaz registra y lista instalaciones, pero no presenta un historial específico por vehículo.

La estructura de los detalles de instalación sigue pendiente de precisar.

### Inventario por sede

- Registrar tipos de material diferenciando tecnología y opacidad.
- Identificar rollos recibidos con sede, material, ancho y largo.
- Registrar el uso de material asociado a un trabajo y una pieza de origen.
- Registrar recortes aprovechables sin duplicar existencias.
- Consultar rollos y recortes disponibles por sede.
- Permitir al administrador corregir registros de uso y descartar piezas completas dañadas.

**Estado en el código:** no implementado. Estas funciones permanecen en los requisitos y en la planificación; no se presentan como terminadas.

Las dimensiones se registrarán en centímetros. Los recortes se representarán mediante rectángulos aprovechables medidos por el instalador.

El procedimiento exacto de corte, actualización del restante y corrección sigue pendiente de definición.

## 5. Reglas principales

- El sistema cubre únicamente las dos sedes de Ibagué.
- Clientes, vehículos e historial se comparten entre esas sedes.
- Cada trabajo pertenece a un vehículo y a una sede.
- Cada pieza de material pertenece a una sede.
- El material utilizado debe pertenecer a la sede del trabajo.
- No se puede utilizar más material del disponible.
- Un sobrante no puede seguir contado dentro de la pieza de origen.
- Las correcciones conservan autor, fecha, motivo y datos anteriores y nuevos.
- Las operaciones de inventario se guardan completas o no se aplican.
- Compartir información entre sedes no significa hacerla pública.

Las reglas y sus comprobaciones se detallan en [requisitos.md](docs/requisitos.md). Varias reglas dependen de módulos que todavía no existen en el código.

## 6. Fuera del alcance

- Cálculo de comisiones y remuneraciones.
- Gestión o verificación de pagos.
- Facturación e integración con Siigo.
- Agenda de citas y registro por QR.
- Gastos e informes financieros.
- Proveedores y compras.
- Alertas automáticas de inventario.
- Cotización de PPF.
- Gestión completa de garantías.
- Sedes adicionales, incluida Bogotá.
- Cálculo automático de cortes y representación de formas irregulares.

Registrar el valor del trabajo no equivale a gestionar su pago.

El historial podrá apoyar consultas de antecedentes para garantías, sin administrar el proceso completo.

## 7. Personas involucradas

| Persona | Participación prevista |
| --- | --- |
| Administrador | Registrar y consultar información, corregir registros de uso y registrar descartes completos. |
| Asesor | Registrar y consultar clientes, vehículos y trabajos. |
| Instalador | Registrar el uso de material y los sobrantes de sus operaciones. |
| Cliente | Proporcionar sus datos y los de su vehículo, sin portal de autoservicio. |

La identificación de usuarios y los permisos detallados siguen pendientes. La API no tiene autenticación ni control de roles. La corrección de registros de uso está reservada al administrador en los requisitos, pero esa restricción todavía no está implementada.

## 8. Demostración prevista

Con datos ficticios, el equipo buscará demostrar este recorrido:

1. Registrar un cliente y su vehículo.
2. Registrar un tipo de material y un rollo recibido en una sede.
3. Registrar un trabajo para el vehículo en esa sede.
4. Asociar el uso de material al trabajo y a su pieza de origen.
5. Registrar los sobrantes aprovechables sin duplicar material.
6. Comprobar que únicamente cambia el inventario de esa sede.
7. Consultar el historial del vehículo desde la otra sede.

El recorrido de inventario se completará cuando se defina el procedimiento de corte y registro del restante.

**Estado actual:** el código permite registrar y consultar clientes, vehículos e instalaciones. Los pasos de inventario, sede, valor, historial específico y control de permisos todavía no están implementados. Esta demostración está prevista; no se ha ejecutado ni documentado como prueba en F2.

## 9. Tecnologías y arquitectura

| Elemento | Implementación actual |
| --- | --- |
| Backend | Python y FastAPI |
| Frontend | React 18, TypeScript, Vite y Tailwind CSS |
| Cliente HTTP | Axios |
| Base de datos | PostgreSQL; la configuración admite Supabase mediante `DATABASE_URL` |
| ORM | SQLAlchemy 2 |
| Validación | Pydantic v2 y pydantic-settings |
| Control de versiones | Git y GitHub |
| Arquitectura | SPA desacoplada y backend monolítico organizado por capas |

La aplicación se organiza en:

- **Presentación:** aplicación React con páginas, componentes, servicios y tipos.
- **API:** routers FastAPI para clientes, vehículos e instalaciones.
- **Negocio y acceso a datos:** operaciones CRUD y modelos SQLAlchemy.
- **Persistencia:** PostgreSQL mediante una cadena de conexión configurable.

Las capas del backend forman parte de una misma aplicación. No se usan microservicios.

```text
frontend/src (React/TS/Tailwind)
        │ Axios + JSON
        ▼
backend/app/main.py (FastAPI)
        │ routers /api/v1
        ▼
crud + schemas + models (SQLAlchemy)
        │
        ▼
PostgreSQL / Supabase
```

El [diseño de backend y frontend](docs/diseno-back-front.md) describe la estructura actual y conserva el antecedente histórico. Los diagramas `.mmd` siguen desactualizados y no se modificaron en F2.

### Puesta en marcha local

Los comandos siguientes corresponden a la estructura y los manifiestos existentes. **F2 no los ejecutó ni verificó la conexión a la base de datos.**

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar backend/.env con la cadena DATABASE_URL real.
uvicorn app.main:app --reload
```

Frontend, en otra terminal:

```bash
cd frontend
npm install
npm run dev
```

Por defecto, el frontend usa `http://localhost:8000/api/v1` como URL base y Vite sirve la aplicación en `http://localhost:5173`. La API permite ese origen mediante CORS. No se deben versionar credenciales reales en `.env` ni en la documentación.

## 10. Documentación

| Documento | Contenido |
| --- | --- |
| [Índice documental](docs/INDICE_DOCUMENTAL.md) | Clasificación, estado y registro de fases. |
| [Visión](docs/vision.md) | Problema, propuesta de valor y límites del proyecto. |
| [Requisitos](docs/requisitos.md) | Reglas, requisitos funcionales y no funcionales, historias y criterios de aceptación. |
| [Trazabilidad](docs/trazabilidad.md) | Relación entre necesidades, requisitos, historias, código y comprobaciones. |
| [Diseño de backend y frontend](docs/diseno-back-front.md) | Estructura, recorrido y responsabilidades implementadas. |
| [Planificación](docs/planificacion.md) | Backlog y propuesta de sprints. |
| [Plan de desarrollo](docs/PLAN_DESARROLLO.md) | Propuesta estratégica ampliada; no adoptada automáticamente. |
| [Análisis competitivo](docs/analisis-competitivo.md) | Comparación documental de soluciones existentes. |
| [Diagrama de arquitectura](docs/diagramas/arquitectura.mmd) | Representación histórica; pendiente de actualización. |
| [Entrevista y aclaraciones](docs/ia/entrevista-cliente.md) | Síntesis de la entrevista y decisiones posteriores. |
| [Matriz de uso de IA](docs/ia/matriz-ia.md) | Apoyo utilizado, evidencia y revisión del equipo. |
| [Biblioteca de prompts](docs/ia/prompts.md) | Instrucciones utilizadas, resultados y observaciones. |
| [Pruebas con Gemini](docs/ia/pruebas-gemini.md) | Prompts de análisis y resúmenes de resultados. |
| [Revisión de historias con Gemini](docs/ia/revision-historias-gemini.md) | Revisión y correcciones posteriores. |
| [Prompt maestro original](docs/ia/PROMPT_MAESTRO_ORIGINAL.md) | Extracción literal verificada. |
| [Línea base F0](docs/F0_LINEA_BASE_Y_VERIFICACIONES.md) | Respaldo y verificaciones iniciales. |

La existencia de un archivo no significa que su revisión esté terminada.

## 11. Uso de inteligencia artificial

Se ha utilizado IA para apoyar la delimitación del alcance, el análisis de requisitos, la redacción de historias y la propuesta de diseño.

- **Gemini:** generación y revisión de borradores de requisitos.
- **Codex:** apoyo en organización, revisión y redacción de documentación y en la propuesta de diseño.

Los registros distinguen instrucciones, respuestas, correcciones y decisiones confirmadas. Los prompts originales se conservan como evidencia histórica; las traducciones o mejoras no se presentan como ejecutadas sin haberlas probado.

El repositorio contiene código de backend y frontend, pero la documentación disponible no atribuye cada archivo a una ejecución concreta de IA. Esa trazabilidad debe completarse en la [matriz de uso de IA](docs/ia/matriz-ia.md).

La revisión de IA no sustituye la validación del negocio ni la revisión de los integrantes.

## 12. Estado y próximos pasos

### Implementado en el código

- Modelos SQLAlchemy de cliente, vehículo e instalación.
- Esquemas Pydantic de creación y lectura.
- CRUD de clientes, vehículos e instalaciones.
- API REST con routers `/api/v1/clientes`, `/api/v1/vehiculos` y `/api/v1/instalaciones`.
- Validación de documento y placa duplicados.
- Búsqueda de cliente por documento, vehículo por placa y vehículos por cliente.
- Listado y filtro de instalaciones por vehículo.
- Interfaz React con pestañas para clientes, vehículos e instalaciones.
- Formularios y listados de las tres entidades.
- Configuración de PostgreSQL/Supabase y CORS para el frontend local.

### Documentado pero no implementado

- Inventario, tipos de material, rollos, sobrantes y disponibilidad.
- Registro de uso de material y correcciones con constancia.
- Descarte de piezas dañadas.
- Sede y valor total en la instalación.
- Historial específico por vehículo en la interfaz.
- Autenticación, roles y autorización.
- Migraciones de base de datos.
- Pruebas automatizadas.

### Pendiente de definición o verificación

- Precisar los detalles de instalación de HU-05.
- Definir el procedimiento de corte y restante de HU-10.
- Definir las correcciones de HU-13, incluidos los casos con sobrantes utilizados.
- Acordar la precisión de las medidas.
- Completar la identificación de usuarios y los permisos.
- Asignar prioridad a HU-14 y revisar el esfuerzo de inventario.
- Acordar condiciones de evaluación de los requisitos no funcionales.
- Completar la revisión de evidencias de IA y documentos restantes.
- Actualizar y revisar los diagramas.
- Revisar con Jonathan y validar los resultados derivados con la asesora.
- Ejecutar la aplicación y registrar pruebas; F2 no ejecutó el sistema.

Los sprints todavía no se presentan como iniciados ni completados. Las decisiones pendientes no se consideran resueltas por aparecer en un documento.

## 13. Equipo

Proyecto desarrollado por dos estudiantes:

- Integrante que administra una sede de Serna Polarizados: Diego Alberto Ñanguma Briñez.
- Jonathan Diaz Salgado

La distribución de tareas se acordará entre ambos y se reflejará en la planificación.

## 14. Alcance de esta entrega

Este repositorio contiene documentación de análisis, diseño y una implementación parcial de clientes, vehículos e instalaciones.

No contiene todavía el inventario, la autenticación, las migraciones ni evidencia de pruebas de funcionamiento. Los criterios escritos describen cómo se comprobarán las funciones durante el desarrollo; su existencia no acredita que hayan sido ejecutados.


## 15. Actualización operativa: confirmación de trabajo (21 de noviembre de 2026)

Esta sección actualiza el alcance histórico descrito arriba. La aplicación incluye autenticación, separación por sede, ventas, inventario y control de trabajo.

1. Gerencia entra en la sede y abre **Instaladores**. Crea/aprueba el nombre y correo Google del trabajador; puede desactivar el acceso. La acción queda en `trabajador_auditoria` de esa sede.
2. Administración guarda la venta totalmente pagada. Las nuevas ventas no descuentan material ni generan honorarios al guardarse; la asignación en el formulario es orientativa.
3. El instalador aprobado entra en **Mi trabajo**, busca la placa, selecciona la venta y los vidrios realizados y registra metros lineales reales (dos decimales).
4. Confirmar guarda simultáneamente trabajo, remuneración y consumo. Un vidrio no se confirma dos veces. La falta de material revierte toda la operación. La tecnología, opacidad y tipo de material se toman de la venta.
5. El instalador consulta solo sus ganancias y trabajos de la sede. Los cortes son 1–15 y 16–último día del mes. Los nuevos honorarios se contabilizan por fecha de confirmación, incluso si la venta corresponde a otro mes. Son importes ganados, no comprobantes de pago de nómina.

Tarifas: lateral individual $12.500; custodia $6.250; parabrisas camión/buseta $35.000; parabrisas normal, luneta, sunroof sencillo y cada panel de sunroof doble $25.000. Las custodias son opcionales. Con película de seguridad se consume únicamente el rollo de película.

Antes de desplegar este cambio, ejecutar desde `backend`: `.venv/bin/python scripts/preparar_trabajo.py`. La migración aditiva prepara las once sedes, activa RLS en las tablas nuevas y conserva movimientos anteriores. Las instalaciones anteriores no admiten reconfirmación en el nuevo flujo para evitar consumo duplicado. No se asigna automáticamente el correo de pruebas a ningún trabajador: Gerencia debe crear su asociación explícita.

Validación: 104 pruebas backend y compilación frontend; comprobación concurrente en un esquema PostgreSQL temporal con dos instaladores sobre el mismo vidrio, resultado de un único consumo y remuneración. El esquema temporal se eliminó al terminar. La validación visual local utilizó datos ficticios y no creó instalaciones reales.

## 16. Entrada por correo verificado (21 de noviembre de 2026)

La portada muestra el logotipo, la bienvenida y un único botón de Google. Los perfiles de Gerencia, Dueño, Administración e Instalador no se muestran antes de iniciar sesión.

`GET /api/v1/auth/accesos` exige identidad verificada y devuelve únicamente los perfiles y sedes de esa cuenta. Un único perfil/sede abre su interfaz automáticamente; si existen varias opciones se solicita la selección después del ingreso. Cada petición de negocio sigue validando perfil y sede en el servidor. Modificar el navegador no otorga permisos.

La cuenta temporal de pruebas conserva sus cuatro perfiles; el resto conserva sus autorizaciones existentes. Los instaladores se descubren por las aprobaciones activas de Gerencia en cada sede. La selección se recuerda durante la sesión y se elimina al cambiar de cuenta.

Validación: 111 pruebas backend, compilación frontend y cinco recorridos de interfaz con identidad/API simuladas (bienvenida sin roles públicos, entrada automática, selección de sede, selección de perfil y rechazo sin permisos). La revisión visual mediante captura automática no se completó por una restricción del entorno.


## Contacto y chat con Gerencia

La portada permite ingresar una identificación registrada y enviar una inquietud sin iniciar sesión ni redirigir a Google. El formulario no muestra nombres, correos ni conversaciones anteriores. Se comprueba que el registro siga activo tanto al consultar como al enviar; hay límites de intentos y de mensajes e idempotencia para evitar duplicados.

Gerencia → **Mensajes del equipo** → **Empleados autorizados** gestiona los contactos. Este directorio no concede permisos operativos. Las consultas públicas se identifican como **remitente sin verificar**: la cédula identifica un registro, pero no acredita quién escribe. Gerencia conserva el mensaje en el historial. La consulta de conversaciones anteriores y las respuestas requieren una sesión autorizada.

Preparación: desde `backend`, ejecutar `.venv/bin/python scripts/preparar_soporte.py`. Crea las tablas de soporte con RLS, incluyendo límites de intentos compartidos entre procesos. No crea contactos automáticamente. Los registros personales se administran en la base de datos, no en el código fuente.

Pruebas: `python -m unittest discover -s tests` desde backend cubre envío público, privacidad del historial, identidad, revocación, límites, paginación e idempotencia.
