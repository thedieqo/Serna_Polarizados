# Prompt maestro original — Serna Polarizados

## Procedencia

- Archivo fuente: `HISTORIAL_PROMPTS_SERNA.md`
- Sesión: `ses_eaa47bb43ffezliPIv96pNt6S8`
- Bloque identificado: primer bloque `## User` de la sesión de planificación.
- Encabezado del bloque: línea 9 (`## User`).
- Contenido literal: líneas 10–409 del archivo fuente.
- Límite posterior: línea 410 (`---`); línea 412 (`## Assistant ...`).
- SHA-256 del bloque fuente (líneas 10–409): `d197083c8182528c6354a12864dd951d187fa5e5efc7e4d074a5a313abb017e2`
- Tamaño del bloque: 400 líneas, 8100 bytes.
- Fecha de extracción: 2026-10-27.
- Método: `sed -n '10,409p' HISTORIAL_PROMPTS_SERNA.md`.
- Nota: el contenido entre los marcadores es copia literal. No se corrigió, tradujo, resumió ni completó. La cabecera y los marcadores no forman parte del bloque original.

El archivo contiene otros bloques `## User` posteriores (líneas 3962, 4372 y 4435), que son seguimientos de la misma sesión y no el prompt inicial de planificación. No se identificó ambigüedad sobre cuál es el primer bloque.

<!-- BEGIN LITERAL PROMPT -->

Actúa como arquitecto de software senior, ingeniero de
requisitos, especialista en bases de datos y director técnico
de proyectos empresariales.

PROYECTO: SERNA POLARIZADOS

CONTEXTO GENERAL

Estamos desarrollando un sistema empresarial real para
Serna Polarizados, empresa dedicada a la instalación de
polarizados, películas de seguridad y protección PPF.

El proyecto también corresponde a la asignatura
Electiva CPC de Ingeniería de Sistemas.

OBJETIVO PRINCIPAL

Diseñar un plan integral, profesional y ejecutable para
construir un sistema web empresarial, responsive y
preparado para evolucionar a PWA.

El sistema debe centralizar la información operativa
de las diferentes sedes.

FASE 1: ANALIZAR EL REPOSITORIO

Antes de generar el plan:

1. Examina toda la estructura del proyecto.
2. Lee completamente README.md.
3. Analiza los requisitos funcionales.
4. Analiza los requisitos no funcionales.
5. Revisa las historias de usuario.
6. Revisa los criterios de aceptación Gherkin.
7. Examina los diagramas UML.
8. Analiza la arquitectura existente.
9. Revisa los documentos de planificación.
10. Identifica los prototipos disponibles.
11. Revisa las tecnologías previamente propuestas.
12. Identifica inconsistencias y documentación faltante.

Utiliza exclusivamente información comprobable del
repositorio para describir el estado actual.

No inventes funcionalidades existentes.

FASE 2: DEFINIR EL SISTEMA

El módulo central será GESTIÓN DE INSTALACIONES.

Flujo principal:

Nueva instalación
→ Buscar o registrar cliente
→ Buscar o registrar vehículo
→ Seleccionar sede
→ Configurar servicio
→ Asignar instaladores
→ Registrar materiales
→ Guardar instalación
→ Actualizar historial del vehículo

DATOS DEL CLIENTE

- Nombre completo.
- Cédula o NIT.
- Teléfono.
- Correo electrónico.

DATOS DEL VEHÍCULO

- Placa.
- Marca.
- Modelo.
- Color.
- Tipo de vehículo.
- Cliente asociado.

DATOS DE INSTALACIÓN

- Fecha.
- Sede.
- Cliente.
- Vehículo.
- Servicio realizado.
- Marca del material.
- Tecnología.
- Tipo de película.
- Opacidad.
- Instaladores asignados.
- Partes del vehículo intervenidas.
- Material utilizado.
- Valor del servicio.
- Estado de instalación.

GESTIÓN DE INSTALADORES

Una instalación puede tener varios instaladores.

Cada instalador puede trabajar en partes específicas:

- Laterales delanteros.
- Laterales traseros.
- Panorámico delantero.
- Panorámico trasero.
- Sunroof.
- Vehículo completo.
- Otras superficies configurables.

La asignación debe permitir seleccionar individualmente
las superficies intervenidas.

GESTIÓN DE INVENTARIO

Diseñar un sistema de inventario por sede.

Debe contemplar:

- Marcas.
- Tecnologías.
- Polarizados.
- Películas de seguridad.
- Opacidades.
- Referencias.
- PPF transparente.
- PPF mate.
- Entradas.
- Salidas.
- Transferencias entre sedes.
- Material consumido.
- Material instalado.
- Sobrantes reutilizables.
- Desperdicios.
- Existencias disponibles.
- Historial de movimientos.

No asumir unidades de medida ni fórmulas de consumo
sin validarlas previamente con el equipo.

GESTIÓN DE GARANTÍAS

Un cliente puede tener varios vehículos.

Un vehículo puede tener varias instalaciones.

Cada instalación puede tener registros de garantía.

El sistema debe permitir:

- Consultar historial por placa.
- Consultar historial por documento del cliente.
- Consultar instalaciones anteriores.
- Registrar garantías.
- Consultar garantías anteriores.
- Relacionar garantías con instalaciones específicas.

ROLES Y PERMISOS

Administrador:
- Registrar información.
- Gestionar instalaciones.
- Consultar información.
- Gestionar inventario según permisos.
- Solicitar modificaciones de registros existentes.

Gerente:
- Consultar información.
- Visualizar reportes.
- Consultar indicadores.
- No modificar registros operativos.

IMPORTANTE:

Existe un requisito de autorización superior para
modificar instalaciones o vehículos ya registrados.

Diseñar el flujo de autorización, pero solicitar
confirmación sobre quién aprueba los cambios.

SEGURIDAD

Considerar:

- Autenticación.
- Autorización basada en roles.
- Registro de auditoría.
- Protección de datos personales.
- Validación de formularios.
- Copias de seguridad.
- Protección de credenciales.
- Integridad de registros.
- Prevención de modificaciones no autorizadas.

FASE 3: ARQUITECTURA Y TECNOLOGÍAS

Evaluar las tecnologías documentadas en el repositorio
y compararlas con esta propuesta:

Frontend:
React + TypeScript + Tailwind CSS.

Backend:
Python + FastAPI.

Base de datos:
PostgreSQL.

Base de datos alojada:
Supabase PostgreSQL.

Frontend:
Vercel.

Backend:
Evaluar servicios compatibles con Python.

Aplicación:
Web responsive con posibilidad de PWA.

Justificar cada elección.

No cambiar automáticamente las tecnologías
documentadas.

Considerar costos, mantenimiento, seguridad,
escalabilidad y facilidad de aprendizaje.

FASE 4: DISEÑO VISUAL

El diseño debe respetar la identidad de
SERNA POLARIZADOS.

Existe un prototipo realizado en Google Stitch.

Antes de diseñar interfaces:

- Identificar prototipos disponibles.
- Identificar logo oficial.
- Identificar colores corporativos.
- Identificar tipografías.
- Identificar pantallas por rol.
- Identificar componentes reutilizables.

Si faltan archivos visuales, solicitarlos.

No inventar logos ni colores corporativos.

FASE 5: PLAN DE DESARROLLO

Generar un plan separado en:

A. BACKEND

- Arquitectura.
- Modelos de datos.
- Relaciones.
- API.
- Autenticación.
- Roles.
- Permisos.
- Gestión de clientes.
- Gestión de vehículos.
- Gestión de instalaciones.
- Gestión de inventario.
- Gestión de garantías.
- Auditoría.
- Validaciones.
- Pruebas.

B. FRONTEND

- Arquitectura.
- Diseño visual.
- Componentes.
- Navegación.
- Inicio de sesión.
- Panel administrativo.
- Registro de instalaciones.
- Consulta de historial.
- Gestión de inventario.
- Gestión de garantías.
- Panel de gerencia.
- Reportes.
- Diseño responsive.
- Accesibilidad.

C. BASE DE DATOS

- Entidades.
- Relaciones.
- Restricciones.
- Integridad referencial.
- Índices.
- Migraciones.
- Estrategia de respaldos.

D. CALIDAD

- Pruebas unitarias.
- Pruebas de integración.
- Pruebas funcionales.
- Pruebas de permisos.
- Pruebas de seguridad.
- Validación con usuarios.

E. DESPLIEGUE FUTURO

- Hosting.
- Base de datos en la nube.
- Variables de entorno.
- HTTPS.
- Dominio.
- Copias de seguridad.
- Monitoreo.

No desplegar todavía.

FASE 6: ORGANIZACIÓN DEL TRABAJO

Dividir el desarrollo en etapas pequeñas.

Cada etapa debe contener:

- Objetivo.
- Tareas.
- Dependencias.
- Archivos involucrados.
- Requisitos relacionados.
- Criterios de aceptación.
- Pruebas.
- Resultado esperado.
- Condiciones para aprobar la etapa.

El desarrollo futuro deberá ejecutarse por etapas.

Después de cada etapa:

1. Revisar los cambios.
2. Ejecutar pruebas.
3. Comparar resultados con requisitos.
4. Informar errores.
5. Solicitar aprobación.
6. Continuar únicamente con autorización.

No realizar commits ni push automáticos sin
autorización explícita.

ENTREGABLE

Preparar el contenido de:

docs/PLAN_DESARROLLO.md

El documento debe incluir:

1. Resumen ejecutivo.
2. Diagnóstico del repositorio.
3. Alcance.
4. Requisitos.
5. Arquitectura.
6. Tecnologías.
7. Modelo de datos.
8. Plan backend.
9. Plan frontend.
10. Inventario.
11. Garantías.
12. Seguridad.
13. Pruebas.
14. Despliegue.
15. Cronograma por fases.
16. Riesgos.
17. Preguntas pendientes.
18. Criterios de aceptación.

IMPORTANTE

Estamos en MODO PLAN.

NO PROGRAMAR.
NO INSTALAR DEPENDENCIAS.
NO MODIFICAR CÓDIGO.
NO DESPLEGAR.
NO EJECUTAR EL PLAN.
NO REALIZAR COMMITS.
NO HACER PUSH.

Primero analiza el proyecto.

Después identifica contradicciones y decisiones pendientes.

Si necesitas aclaraciones, pregunta antes de
tomar decisiones que afecten el diseño.

Finalmente, presenta el plan para revisión.

El objetivo de esta sesión es obtener un plan
de construcción profesional, no desarrollar
el sistema todavía. 

<!-- END LITERAL PROMPT -->
