# Personal por sede

Gerencia → Sedes → Empleados muestra tarjetas con foto y primer nombre/apellido. Nombres y apellidos se capturan por separado para no deducir el apellido de un nombre compuesto.

La ficha comienza pendiente. Activarla requiere nombres, apellidos, cédula única, teléfono, correo empresarial, grupo sanguíneo, EPS, cargo, sede (salvo cargos generales), capacidades y foto. Contacto de emergencia, hoja de vida y contrato son opcionales. No se inventan datos para completar los registros ficticios existentes.

El administrador consulta nombre, foto, contacto, cargo, capacidades y estado exclusivamente de su sede. Puede buscar personal activo de otras sedes por nombre/capacidades para solicitar un traslado, sin obtener contacto, cédula, salud ni documentos. Gerencia consulta y actualiza la ficha completa.

## Traslados y accesos

El administrador solicita para su propia sede. Gerencia aprueba o rechaza con motivo. Solo se admite una solicitud pendiente por empleado y una decisión por solicitud. Al aprobar se comprueba la sede de origen y el estado vigente. La ficha tiene una sede actual; solicitudes y actividad conservan origen, destino, solicitante, decisión y fecha. Trabajos y pagos anteriores no se trasladan ni borran.

Las cuentas de instaladores previamente aprobadas se desactivan en otras sedes y habilitan en el destino en la misma transacción, conservando sus identificadores anteriores. Activar una ficha no concede un nuevo acceso: la aprobación operativa de instaladores exige ahora ficha completa y activa en esa sede. Los permisos de cargos nuevos continúan pendientes de definición y las cuentas administrativas de sede conservan sus autorizaciones existentes.

## Archivos privados

Almacenados en PostgreSQL con RLS, sin URL pública. Solo Gerencia carga y descarga CV/contrato; el administrador puede obtener la foto del personal de su sede. Respuestas sin caché, tipos JPG/PNG/PDF comprobados por cabecera, nombres de descarga controlados. Máximo 2 MB por foto y 8 MB por documento, reemplazo auditado. La auditoría conserva metadatos de cargas, no versiones anteriores del archivo. Antes de ampliar significativamente el volumen documental conviene migrar el contenido a almacenamiento privado de objetos manteniendo estas autorizaciones.

## Preparación y validación

Desde backend: `.venv/bin/python scripts/preparar_personal.py` muestra el plan; agregar `--apply` crea las tres tablas faltantes y habilita RLS. Migración aditiva e idempotente, sin modificar empleados ni permisos existentes. Aplicar antes del despliegue.

Pruebas: `python -m unittest discover -s tests`; frontend: `npm run build --prefix frontend` y pruebas de pagos existentes. Cobertura de privacidad por rol/sede, archivos, requisitos de activación, cédula duplicada, revisión obsoleta, aprobación/rechazo, decisiones repetidas y conservación de identificadores. La comprobación adicional de interacción utiliza React con DOM simulado, no un navegador real.
