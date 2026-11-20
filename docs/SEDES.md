# Acceso y datos por sede

La pantalla de ingreso exige seleccionar una sede antes de continuar con Google. Cada solicitud lleva `X-Sede`; el backend comprueba que el correo verificado esté autorizado para esa sede. No basta modificar el selector o el encabezado para obtener acceso.

Los correos de `ADMIN_EMAILS` tienen acceso a El Carmen y Mirolindo. Las otras nueve cuentas autorizadas están en `backend/app/core/sedes.py`. No se crean cuentas Gmail automáticamente.

El Carmen conserva los datos anteriores en el esquema `public`. Cada otra sede utiliza su propio esquema PostgreSQL, con clientes, vehículos, instalaciones, novedades, catálogos y secuencias independientes. Los identificadores SP son locales a cada sede. Una misma placa puede registrarse en varias sedes, sin compartir sus datos. Los referidos se validan dentro de la sede seleccionada.

Para preparar una base nueva, desde backend ejecutar `python scripts/preparar_sedes.py` con el entorno del backend. Es transaccional: no borra ni mueve datos de El Carmen y no copia clientes a otras sedes. Las futuras migraciones deben aplicarse a todos los esquemas; no solo a public.

Para cambiar de sede, cerrar sesión y seleccionar otra. La elección es por pestaña y se conserva durante el retorno de Google.

MCP local: los datos reales requieren `SERNA_MCP_SEDE`, por ejemplo `el-carmen` o `cali`, además de la habilitación de lectura. El operador local de confianza tiene acceso a las credenciales; este mecanismo no implementa la sesión Google de la web. Las herramientas consultan únicamente el esquema seleccionado. La demo ficticia sigue independiente.

Pruebas: instalar `backend/requirements-dev.txt` en el entorno de desarrollo y ejecutar `python -m unittest discover -s tests` desde backend. Incluye rechazo HTTP de sedes ajenas y dos esquemas con el mismo documento e ID, verificando resultados separados.

Inventario sigue siendo una función pendiente de la aplicación. La separación no implementa un módulo de inventario nuevo.
