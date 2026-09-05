# Diseño inicial de backend y frontend

## Estado

Propuesta de diseño basada en las historias de usuario y prioridades revisadas.

Este documento describe responsabilidades y pantallas. No representa funcionalidades implementadas ni sustituye los diagramas pendientes de la sesión 4.

## 1. Organización general

El sistema será una aplicación Flask con páginas HTML, estilos CSS, interacción con JavaScript y almacenamiento en SQLite.

- Frontend: muestra formularios, información y mensajes.
- Backend: recibe solicitudes, comprueba permisos y reglas, y coordina las operaciones.
- Acceso a datos: guarda y consulta información en SQLite.

Las validaciones del navegador ayudan al usuario, pero el backend debe comprobarlas también.

## 2. Clientes y vehículos

Historias: HU-01, HU-02, HU-03 y HU-04.

### Frontend

- Formulario de cliente: nombre, documento y contacto.
- Búsqueda de cliente por documento.
- Formulario de vehículo: descripción, placa y cliente asociado.
- Búsqueda de vehículo por placa.
- Presentación de los vehículos asociados a un cliente.

### Backend

- Registrar y consultar clientes.
- Impedir documentos duplicados.
- Registrar vehículos vinculados a clientes existentes.
- Impedir placas duplicadas.
- Permitir varios vehículos por cliente.
- Informar cuando una búsqueda no tenga resultados.

## 3. Trabajos e historial

Historias: HU-05 y HU-06.

### Frontend

- Formulario de trabajo: vehículo, sede, fecha, servicio y valor total.
- Vista del historial de un vehículo.
- Identificación de la sede donde se realizó cada trabajo.

### Backend

- Comprobar que el vehículo y la sede existan.
- Guardar la relación entre trabajo, vehículo y sede.
- Consultar los trabajos del vehículo desde ambas sedes.
- Mantener el valor del trabajo separado de cualquier gestión de pagos, que está fuera del alcance.

## 4. Materiales e inventario

Historias: HU-08, HU-09, HU-10 y HU-11.

### Frontend

- Formulario de material con nombre y unidad de medida.
- Formulario de entrada con sede, material y cantidad.
- Formulario de consumo dentro del trabajo correspondiente.
- Consulta de existencias por sede.
- Mensajes para cantidades inválidas o existencias insuficientes.

### Backend

- Registrar materiales y sus unidades.
- Registrar entradas y actualizar las existencias de la sede seleccionada.
- Registrar consumos asociados a trabajos.
- Obtener la sede del consumo a partir del trabajo.
- Descontar únicamente del inventario de esa sede.
- Rechazar cantidades iguales o menores que cero.
- Rechazar consumos superiores a las existencias.
- Guardar el consumo y actualizar las existencias como una sola operación: se completan ambos cambios o ninguno.

## 5. Corrección de consumos

Historia: HU-13.

### Frontend

- Mostrar el consumo original.
- Permitir al administrador indicar la cantidad corregida y el motivo.
- Mostrar el resultado del ajuste.

### Backend

- Comprobar que quien corrige sea administrador.
- Calcular la diferencia entre la cantidad anterior y la nueva.
- Actualizar exclusivamente el inventario de la sede del trabajo.
- Comprobar existencias suficientes si aumenta el consumo.
- Conservar quién corrigió, cuándo, el motivo y ambas cantidades.
- Guardar el ajuste y actualizar las existencias como una sola operación.

La anulación completa y el cambio de material siguen pendientes de definición.

## 6. Función posterior a las indispensables

Historia: HU-12 — Should.

Se incorporará una consulta del detalle de materiales y cantidades consumidos por trabajo después de las funciones Must.

La asociación de consumos con trabajos se guardará desde el principio, aunque esa consulta se construya después.

## 7. Información compartida y separada

### Compartida entre sedes

- Clientes.
- Vehículos.
- Historial de trabajos.

### Identificada por sede

- Trabajos realizados.
- Existencias de cada material.
- Entradas, consumos y ajustes.

Un mismo material puede tener cantidades diferentes en cada sede.

## 8. Decisiones pendientes antes de implementar

- Definir las unidades y precisión de cantidades con el instalador.
- Precisar campos obligatorios y formatos.
- Definir cómo se identifica cada usuario y se aplican sus permisos.
- Resolver los casos de anulación completa o material equivocado.
- Revisar este diseño con Jonathan.
- Completar y revisar los diagramas de la sesión 4.

## 9. Orden propuesto de implementación futura

1. Clientes y vehículos.
2. Registro de trabajos e historial compartido.
3. Materiales, entradas y consulta de existencias.
4. Consumos vinculados a trabajos.
5. Correcciones de consumos.
6. Consulta detallada de materiales por trabajo.

La identificación de usuarios y los permisos deberán resolverse para verificar las funciones que dependen del perfil.
