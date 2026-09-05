# Visión del proyecto — Serna Polarizados

## 1. Visión

Para el personal de las dos sedes de Serna Polarizados en Ibagué, que necesita consultar la información de sus clientes y controlar los materiales utilizados, se propone un sistema web que centralice clientes, vehículos e historial de trabajos y mantenga un inventario independiente por sede.

El sistema busca facilitar la consulta compartida de información y relacionar cada trabajo con los materiales consumidos en la sede correspondiente.

## 2. Situación actual

El negocio utiliza registros manuales y archivos de Excel para organizar su operación.

En el registro de trabajos compartido se observan datos como fecha, servicio, valor total, propietario, vehículo, placa, contacto y documento. También existen columnas de pagos, que quedan fuera de la primera versión del proyecto.

Cada sede maneja su propio inventario. Ambas necesitan consultar la información de los clientes, sus vehículos y los trabajos realizados, independientemente de la sede donde fueron atendidos.

## 3. Personas involucradas

- Administrador: necesita supervisar la operación y consultar el inventario.
- Asesor: necesita registrar y consultar clientes, vehículos y trabajos.
- Instalador: aporta información de los trabajos y los materiales utilizados.
- Cliente: proporciona sus datos y los de su vehículo.

Los permisos específicos se definirán durante el análisis de requisitos. El cliente no tendrá un portal de autoservicio en la primera versión.

## 4. Necesidades principales

- Encontrar la información de un cliente y sus vehículos.
- Consultar el historial de trabajos de un vehículo desde ambas sedes.
- Identificar en qué sede se realizó cada trabajo.
- Conocer las existencias de materiales de cada sede.
- Registrar entradas y consumos de materiales.
- Identificar los materiales utilizados en cada trabajo.

## 5. Primera versión propuesta

La primera versión incluirá:

1. Registro y consulta de clientes.
2. Registro de vehículos asociados a un cliente.
3. Registro de trabajos con fecha, sede, vehículo, servicio y valor total.
4. Consulta compartida del historial de trabajos.
5. Registro de materiales y sus unidades de medida.
6. Control de entradas, consumos y existencias por sede.
7. Relación entre los trabajos realizados y los materiales consumidos.

## 6. Límites

El proyecto se limita a las dos sedes de Ibagué.

No incluye inicialmente agenda de citas, registro por QR, gestión de pagos, facturación electrónica, integración con Siigo, gastos, informes financieros, proveedores, órdenes de compra ni alertas automáticas.

Registrar el valor total de un trabajo no equivale a gestionar su pago.

## 7. Resultado esperado

El equipo deberá poder demostrar, con datos ficticios, que:

- Un cliente puede quedar registrado con su vehículo.
- Un trabajo puede asociarse al vehículo y a la sede donde se realizó.
- El consumo de materiales modifica el inventario de esa sede.
- El inventario de la otra sede permanece sin cambios.
- El historial del vehículo puede consultarse desde ambas sedes.

Estos resultados se convertirán después en historias de usuario y criterios de aceptación verificables.

## 8. Restricciones y decisiones iniciales

- Proyecto académico desarrollado por dos integrantes durante el semestre.
- Backend previsto con Python y Flask.
- Frontend previsto con HTML, CSS y JavaScript.
- Base de datos prevista con SQLite.
- Arquitectura de monolito en capas.
- Documentación y control de cambios en GitHub.
- Apoyo de IA con revisión y corrección humana.

## 9. Aspectos pendientes de precisar

Durante el análisis se detallarán:

- Los permisos de cada perfil.
- Los campos obligatorios y sus validaciones.
- Las unidades y reglas de medición de materiales.
- El procedimiento para corregir registros equivocados.

Estos pendientes no amplían el alcance; permiten definir cómo funcionarán las funciones acordadas.
