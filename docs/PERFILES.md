# Entrada privada y perfiles — primera etapa

La portada ofrece Gerencia, Propietario, Administrador e Instalador. El perfil elegido se envía como `X-Rol`, pero el servidor lo contrasta con la cuenta de Google verificada y restringe las rutas. Elegir una tarjeta no concede permisos a una cuenta no autorizada.

Por autorización expresa, `diegonangumaw@gmail.com` tiene los cuatro perfiles de prueba. Los demás correos de sede conservan únicamente Administración. Esta cuenta temporal reúne privilegios; para operación real se necesitan cuentas personales y asignaciones independientes.

- Gerencia: acceso a las operaciones existentes en cualquiera de las once sedes, seleccionando sede al ingresar.
- Propietario: consulta de ventas y remuneraciones por sede. No permite escrituras ni acceso al registro de clientes.
- Administración: registro, historial e inventario de sus sedes autorizadas. No accede a reportes generales de remuneraciones.
- Instalador: acceso únicamente al espacio personal. Sin asignación de trabajador confirmada, muestra sin asignación y no devuelve registros de otros instaladores.

## Funciones aún pendientes

La apertura de sedes y habilitación de correos desde una consola de Gerencia no están implementadas. La configuración continúa en el servidor. Los gastos operativos y utilidad neta tampoco están registrados: no se presentan cifras inventadas.

El siguiente flujo acordado de clientes queda para una etapa posterior: QR, nombre completo, tipo y número de documento, correo, teléfono, sede, vehículo, placa, tecnología, valor y medio de pago; recepción por Administración, datos protegidos y aprobación de Gerencia para cambios. Antes de implementarlo se definirá qué valores confirma el cliente y cuáles valida el servidor, protección contra envíos abusivos y trazabilidad de aprobaciones.

## Ampliación solicitada: ejecución por instaladores

El perfil Instalador debe registrar el trabajo realizado, no limitarse a consultar ganancias:
- Cuenta creada o aprobada exclusivamente por Gerencia, asociada a trabajador y sede.
- Búsqueda por placa dentro de la sede autorizada.
- Selección de vidrios individuales: parabrisas, laterales por lado/posición, luneta y techos; categorías de vehículos grandes por definir.
- Registro de metros lineales realmente cortados por tecnología, opacidad y material.
- Confirmación del trabajo, consumo trazable e importes ganados por el trabajador.

Pendiente confirmar: orden venta/trabajo, consumo directo frente a reserva y tarifas por vidrio individual y vehículo grande. No aplicar consumo real además del automático actual: el cambio requiere una transición explícita que evite doble descuento, repetición de confirmaciones y doble liquidación. La cuenta de prueba aún no se asocia a un instalador concreto.
