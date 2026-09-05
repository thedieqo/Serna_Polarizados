# Trazabilidad — Serna Polarizados

## Propósito

Relacionar las necesidades del negocio con las historias de usuario y los criterios que permiten comprobarlas.

Las necesidades proceden del README inicial y de las decisiones expresadas por un integrante del equipo durante la conversación. No se presenta como realizada una entrevista adicional con el negocio.

## Necesidades identificadas

### N-01 — Organizar clientes y vehículos

El negocio necesita registrar y recuperar los datos de clientes y sus vehículos, actualmente manejados mediante registros manuales y Excel.

Origen: README inicial, registro de Excel compartido y revisión de las historias con el usuario.

### N-02 — Conservar los trabajos realizados

Cada trabajo debe quedar relacionado con un vehículo y con la sede donde se realizó, incluyendo fecha, servicio y valor total.

Origen: alcance acordado y aceptación de HU-05.

### N-03 — Compartir el historial entre sedes

Las dos sedes de Ibagué deben consultar la información de clientes, vehículos y trabajos anteriores.

Origen: confirmación expresa del usuario de que ambas sedes deben consultar esa información.

### N-04 — Separar el inventario por sede

Cada sede administra sus propias existencias y movimientos de materiales.

Origen: confirmación expresa del usuario de que cada sede maneja su propio inventario.

### N-05 — Relacionar consumos con trabajos

El material utilizado debe asociarse al trabajo y descontarse únicamente del inventario de la sede correspondiente.

Origen: alcance acordado y aceptación de HU-10 y HU-12.

### N-06 — Corregir errores de consumo

El administrador debe poder corregir consumos erróneos, dejando constancia del ajuste.

Origen: aprobación expresa de HU-13 y de las validaciones de corrección.

## Relación entre necesidades e historias

- HU-01 — Registrar cliente.
  Necesidad: N-01.
  Prioridad: Must.
  Comprobación: registro correcto y rechazo de documento duplicado.

- HU-02 — Consultar cliente por documento.
  Necesidad: N-01.
  Prioridad: Must.
  Comprobación: consulta con coincidencia y sin coincidencia.

- HU-03 — Registrar vehículo.
  Necesidad: N-01.
  Prioridad: Must.
  Comprobación: asociación con cliente, varios vehículos por cliente y rechazo de placa duplicada.

- HU-04 — Consultar vehículo por placa.
  Necesidad: N-01.
  Prioridad: Must.
  Comprobación: consulta con coincidencia y sin coincidencia.

- HU-05 — Registrar trabajo.
  Necesidad: N-02.
  Prioridad: Must.
  Comprobación: trabajo guardado con vehículo, sede, fecha, servicio y valor total.

- HU-06 — Consultar historial del vehículo.
  Necesidad: N-03.
  Prioridad: Must.
  Comprobación: consulta desde la otra sede e historial sin trabajos.

- HU-08 — Registrar material.
  Necesidad: N-04.
  Prioridad: Must.
  Comprobación: material disponible con su unidad de medida.

- HU-09 — Registrar entrada.
  Necesidad: N-04.
  Prioridad: Must.
  Comprobación: aumento exclusivo de la sede seleccionada y rechazo de cantidades no positivas.

- HU-10 — Registrar consumo.
  Necesidades: N-04 y N-05.
  Prioridad: Must.
  Comprobación: asociación con trabajo, descuento en su sede y rechazo de cantidades inválidas o superiores a las existencias.

- HU-11 — Consultar existencias.
  Necesidad: N-04.
  Prioridad: Must.
  Comprobación: cantidades diferenciadas por sede y unidad de medida.

- HU-12 — Consultar materiales de un trabajo.
  Necesidad: N-05.
  Prioridad: Should.
  Comprobación: criterios detallados pendientes antes de su implementación.

- HU-13 — Corregir consumo.
  Necesidad: N-06.
  Prioridad: Must.
  Comprobación: ajuste por diferencia, control de existencias y registro de autor, momento, motivo y cantidades.

Los escenarios completos están en requisitos.md.

## Historia descartada

HU-07 — Consultar trabajos por sede y periodo.

La IA la propuso y el usuario la descartó por no ser necesaria para la primera versión. No se asigna como compromiso del MVP.

## Estado de revisión

- Historias y prioridades revisadas con un integrante.
- Seis validaciones aprobadas por ese integrante.
- Revisión conjunta con Jonathan pendiente.
- Diagramas de diseño pendientes.

La existencia de criterios escritos no significa que se hayan ejecutado pruebas de software: todavía no se ha implementado el sistema.
