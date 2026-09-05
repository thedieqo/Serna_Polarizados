# Serna Polarizados - Sistema de Gestión

## Descripción

Proyecto académico desarrollado para Serna Polarizados, orientado a la creación de un sistema web que centralice y optimice procesos administrativos que actualmente se gestionan de forma manual o mediante archivos de Excel.

La solución se implementará inicialmente en dos sedes, incluyendo Ibagué, con posibilidad de escalar posteriormente a otras sedes de la empresa.

## Problemática

Actualmente la información relacionada con clientes, vehículos, servicios, inventario, pagos y operación se encuentra distribuida en diferentes procesos y archivos.

Esto dificulta principalmente:

- El seguimiento de clientes y vehículos.
- La consulta del historial de servicios.
- El control de materiales e inventario.
- La identificación oportuna de productos que deben reabastecerse.
- La trazabilidad de servicios, pagos y actividades realizadas.
- La generación de información administrativa para la toma de decisiones.

## Objetivo

Desarrollar un sistema web que permita centralizar la operación administrativa de Serna Polarizados, relacionando en una misma plataforma:

**Cliente → Vehículo → Servicio → Instalación → Inventario → Pago → Historial**

## Usuarios y roles

El sistema contará inicialmente con cuatro tipos de usuario:

- **Administrador:** supervisión general, usuarios, inventario, pagos, gastos, reportes y control de la operación.
- **Asesor:** registro de clientes, vehículos, citas, servicios, precios, descuentos autorizados y pagos.
- **Instalador:** consulta de trabajos asignados, actualización del servicio y registro de materiales utilizados.
- **Cliente:** registro de sus datos y vehículo mediante código QR, sin necesidad de iniciar sesión.

El administrador tendrá acceso general para supervisar las funciones de los demás roles.

## Módulos principales

### Clientes y vehículos
Registro centralizado de clientes y sus vehículos. Un cliente podrá tener varios vehículos y el historial podrá consultarse mediante datos como documento o placa.

### Citas y servicios
Permitirá gestionar citas y clientes que lleguen directamente a la sede.

Una atención podrá incluir varios servicios y uno o varios instaladores.

Estados principales:

`Agendada → En proceso → Completada`

También se contemplarán estados como **cancelada, reprogramada y no asistió**.

### Inventario
Control de materiales utilizados en los servicios, principalmente mediante unidades como metros y rollos.

Permitirá registrar:

- Entradas y consumos.
- Stock disponible y stock mínimo.
- Material utilizado en cada servicio.
- Alertas de bajo inventario.
- Proveedores.
- Historial de movimientos.

### Pagos y facturación
Registro de precios, descuentos y medios de pago como:

- Efectivo.
- Transferencia.
- Tarjeta.
- Sistecrédito.

La facturación electrónica actualmente se gestiona mediante **Siigo**. El sistema buscará centralizar la información necesaria para este proceso y se evaluará la viabilidad de una integración.

### Reportes
Generación y consulta de información administrativa relacionada con ventas, servicios, clientes, inventario, pagos, gastos y operación de las sedes.

## Servicios

El sistema permitirá configurar los servicios disponibles según cada sede:

- Polarizados.
- PPF.
- Detailing.
- Wrap.
- Lavado de vehículos.
- Barbería.

Los precios podrán variar dependiendo del servicio, tipo de vehículo, material utilizado y complejidad del trabajo.

## Flujo general

```text
Cliente
   ↓
Vehículo
   ↓
Cita / Ingreso directo
   ↓
Selección de servicios
   ↓
Asignación de instalador(es)
   ↓
Ejecución del servicio
   ↓
Registro de materiales
   ↓
Actualización de inventario
   ↓
Pago / Facturación
   ↓
Historial del vehículo

## Alcance de la primera versión

El sistema se utilizará en las dos sedes de Serna Polarizados en Ibagué e incluirá:

- Registrar clientes con nombre, documento y contacto.
- Registrar los vehículos de cada cliente, incluyendo vehículo y placa.
- Registrar los trabajos de cada vehículo, indicando fecha, sede, servicio realizado y valor total.
- Consultar desde ambas sedes la información de los clientes, sus vehículos y su historial de trabajos.
- Controlar por separado el inventario de materiales de cada sede, registrando entradas, consumos y existencias.
- Relacionar los materiales utilizados con el trabajo correspondiente y descontarlos del inventario de la sede donde se realizó.

La primera versión se concentrará en clientes, vehículos, trabajos e inventario. La gestión de pagos y facturación, la integración con Siigo y los demás módulos del planteamiento general quedan fuera de este alcance inicial.
