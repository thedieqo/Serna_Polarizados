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
