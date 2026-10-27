# F0 — Línea base y verificaciones

**Fecha:** 2026-10-27  
**Alcance:** registrar la línea base, el respaldo privado y la fidelidad de la extracción del prompt maestro. F0 no refactoriza código ni adopta decisiones de modelo o alcance.  
**Estado:** ejecutado; sin commit ni push.

## 1. Línea base previa a F0

- Repositorio: raíz local de `Serna_Polarizados`; la ruta absoluta no se registra en este documento.
- Rama: `main`
- Commit: `f2a5c93b99f362a447779557255996d3b1a14b42`
- Remoto: `https://github.com/thedieqo/Serna_Polarizados.git`
- `git status --porcelain` inicial:

```text
?? .cgcignore
?? HISTORIAL_PROMPTS_SERNA.md
```

- Archivos versionados: 88.
- Distribución por nivel superior:

```text
 1 .gitignore
26 backend
16 docs
27 frontend
17 mi-framework-ia
 1 readme.md
```

- Archivos no versionados: `.cgcignore` y `HISTORIAL_PROMPTS_SERNA.md`.
- Archivos ignorados relevantes: `backend/.env`, `mcp.json`, `.DS_Store`.
- Sin diferencias versionadas (`git diff` vacío) antes de F0.

### Archivos versionados de 0 bytes (18)

```text
backend/app/__init__.py
backend/app/api/__init__.py
backend/app/api/v1/__init__.py
backend/app/core/__init__.py
backend/app/db/__init__.py
frontend/src/components/ClienteSearch.tsx
frontend/src/components/VehiculoSearch.tsx
mi-framework-ia/agents/__init__.py
mi-framework-ia/agents/frontend_agent.md
mi-framework-ia/agents/requirements_agent.md
mi-framework-ia/agents/reviewer_agent.md
mi-framework-ia/core/__init__.py
mi-framework-ia/evaluations/__init__.py
mi-framework-ia/interfaces/__init__.py
mi-framework-ia/skills/__init__.py
mi-framework-ia/skills/frontend_generation.md
mi-framework-ia/skills/requirements_analysis.md
mi-framework-ia/tools/__init__.py
```

Los 5 documentos vacíos del framework quedan pendientes y no se completaron. Los 6 `__init__.py` del framework son marcadores de paquete.

### Hashes de referencia

- `HISTORIAL_PROMPTS_SERNA.md` (archivo completo): `720134ba7f648f58d74638127178e65618cf5f24e9fddfe7b7e6b97730c1d699`
- Bloque del primer prompt (líneas 10–409): `d197083c8182528c6354a12864dd951d187fa5e5efc7e4d074a5a313abb017e2`
- Tamaño del bloque: 400 líneas, 8100 bytes.
- `HISTORIAL_PROMPTS_SERNA.md`: 299124 bytes, 5279 líneas.

## 2. Respaldo privado

Se creó un respaldo **fuera del repositorio**, con permisos restringidos. La ruta absoluta no se registra en este documento versionable. Contenido:

- `repo_all.bundle`: historial Git completo (`--all`).
- `private_untracked_ignored.tgz`: `HISTORIAL_PROMPTS_SERNA.md`, `.cgcignore`, `mcp.json`, `backend/.env`.
- `SHA256SUMS`: hashes de los archivos anteriores y del respaldo.

No se mostraron secretos ni el contenido de `backend/.env`.

### Verificación del respaldo

- `git bundle verify`: correcto; 4 refs; historial completo.
- `tar -tzf`: los 4 archivos esperados.
- `shasum -a 256 -c`: todos los hashes correctos.
- Restauración en carpeta temporal separada: HEAD restaurado `f2a5c93b99f362a447779557255996d3b1a14b42`, igual al HEAD actual; 88 archivos versionados.
- Comparación por bytes (`cmp`) de los 4 archivos restaurados: coinciden.
- La carpeta temporal de restauración se eliminó después de verificar; no se sobrescribió el proyecto.

## 3. Prompt maestro

- Archivo de extracción: `docs/ia/PROMPT_MAESTRO_ORIGINAL.md`.
- Bloque fuente: entre `## User` (línea 9) y `---` (línea 410); contenido literal en líneas 10–409.
- SHA-256 del bloque fuente y del bloque extraído: `d197083c8182528c6354a12864dd951d187fa5e5efc7e4d074a5a313abb017e2`.
- Comparación exacta por bytes: `True`.
- El archivo contiene otros bloques `## User` posteriores (líneas 3962, 4372 y 4435); son seguimientos y no el prompt inicial de planificación.
- La cabecera y los marcadores de la extracción no forman parte del bloque original.

## 4. Cambios de F0

- Creado: `docs/ia/PROMPT_MAESTRO_ORIGINAL.md`.
- Creado: `docs/F0_LINEA_BASE_Y_VERIFICACIONES.md`.
- Creado: `docs/INDICE_DOCUMENTAL.md`.
- Modificado: `.cgcignore` (ya era untracked).
- No se movieron ni eliminaron archivos existentes.
- No se modificaron backend, frontend, modelos, dependencias, configuración de conexión ni BD.
- No se modificaron `.gitignore` ni `mcp.json`.
- No se ejecutó indexación, MCP, build, migración ni conexión a BD.

## 5. Verificación final

### Integridad

- `HISTORIAL_PROMPTS_SERNA.md`: hash antes y después `720134ba7f648f58d74638127178e65618cf5f24e9fddfe7b7e6b97730c1d699`; sin cambios. Tamaño: 299124 bytes, 5279 líneas.
- Bloque del prompt (líneas 10–409): 400 líneas, 8100 bytes; hash `d197083c8182528c6354a12864dd951d187fa5e5efc7e4d074a5a313abb017e2`; comparación exacta con la extracción: `True`.
- `docs/ia/PROMPT_MAESTRO_ORIGINAL.md`: SHA-256 del archivo completo (cabecera + bloque + marcadores) `aa15dcbd68c059345c048adadd888e95b987d9a12d4ff2ddc0715ef36dd6f544`.
- `docs/INDICE_DOCUMENTAL.md`: SHA-256 `4ee4e6c1fc202dc0f07da6121a65f6736e6646070eee19e14d1d38197949c8d2`.
- `mcp.json` y `backend/.env`: sin cambios respecto al respaldo; no se leyó ni mostró su contenido.
- `.gitignore`: sin cambios.
- `.cgcignore`: solo se añadieron patrones al final; hash anterior `318812b8fbc5206fba39031d33118f24880baaf5f178cd411201796e17ffad14`; hash nuevo `28bcdb226466dcba6ff39382e5467cf2d7022b30cd7bb08c05ddb67da3d6cd66`.
- No se movieron ni eliminaron archivos existentes.

### Enlaces

- Se revisaron 27 archivos Markdown y 50 enlaces.
- Enlace roto: 1, ya conocido: `docs/docs/planificacion.md` → `requisitos.md`.
- No se introdujeron enlaces rotos nuevos.
- `HISTORIAL_PROMPTS_SERNA.md` quedó fuera del chequeo de enlaces por ser evidencia histórica.

### Secretos

- Se escanearon los 4 archivos nuevos o modificados de F0 (`.cgcignore` y los 3 documentos): 0 coincidencias potenciales.
- El escaneo no incluye `HISTORIAL_PROMPTS_SERNA.md` ni `backend/.env`; no certifica que estén libres de secretos.
- No se leyó, mostró ni copió el contenido de `backend/.env`.

### Git

- HEAD sin cambios: `f2a5c93b99f362a447779557255996d3b1a14b42`.
- `git diff` versionado: vacío; no hay cambios en staging.
- Estado final: 5 rutas untracked, todas esperadas:

```text
?? .cgcignore
?? HISTORIAL_PROMPTS_SERNA.md
?? docs/F0_LINEA_BASE_Y_VERIFICACIONES.md
?? docs/INDICE_DOCUMENTAL.md
?? docs/ia/PROMPT_MAESTRO_ORIGINAL.md
```

- Backend y frontend: sin diferencias respecto a HEAD ni archivos untracked en esas rutas.
- No se ejecutó `git add`, commit ni push.
- No se ejecutó indexación ni MCP; por tanto, la sintaxis de `.cgcignore` no se validó en tiempo de ejecución con el indexador.
