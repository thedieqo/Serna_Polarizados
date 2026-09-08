# Análisis competitivo — Serna Polarizados

## 1. Objetivo

Comparar funciones publicadas de Shopmonkey, AutoLeap y Odoo para identificar aprendizajes aplicables al proyecto académico de Serna Polarizados.

La comparación se concentra en clientes, vehículos, historial de trabajos e inventario independiente para las dos sedes de Ibagué.

## 2. Método y límites

**Análisis inicial:** 5 de septiembre de 2026.  
**Actualización y consulta de fuentes:** 8 de septiembre de 2026.

Se consultaron páginas oficiales de los tres sistemas. Para Odoo, esta revisión utiliza documentación de la versión 18.

El análisis es documental: no se instalaron ni probaron los sistemas y no se solicitaron demostraciones.

- **Funciones documentadas:** capacidades descritas por el proveedor.
- **Utilidad para Serna:** interpretación del equipo sobre su relación con el proyecto.
- **No verificado:** aspecto que las fuentes consultadas no permiten confirmar para nuestra operación.

No se evaluaron precios, planes comerciales ni soporte local. Tampoco se comprobó que alguno de los sistemas cubra exactamente el flujo de rollos, cortes y recortes definido para Serna.

## 3. Comparación

| Sistema | Funciones documentadas | Utilidad para Serna — interpretación | Aspectos pendientes de verificar |
| --- | --- | --- | --- |
| Shopmonkey | Permite registrar clientes y vehículos, asociarlos y consultar su historial de servicios. Su página de inventario describe consulta de existencias, incorporación de piezas a trabajos y registro de cambios. [Clientes y vehículos](https://support.shopmonkey.io/hc/en-us/articles/38744260861204-Lists-Page) y [gestión de inventario](https://www.shopmonkey.io/demo-inventory-management). | Sirve como referencia para conectar cliente, vehículo y trabajo, y conservar información sobre el material utilizado. | **No verificado:** manejo de rollos con anchos distintos, recortes con dimensiones en centímetros y correcciones cuando un sobrante ya fue utilizado. |
| AutoLeap | Su página de inventario describe seguimiento de existencias relacionado con trabajos y visibilidad del inventario entre ubicaciones. [Inventario de AutoLeap](https://autoleap.com/features/inventory/). | Orienta la relación entre trabajos y materiales y la consulta de disponibilidad diferenciada por sede. | **No verificado:** identificación de cada recorte, relación con su pieza de origen y prevención de duplicaciones al registrar sobrantes de película. |
| Odoo | Documenta la creación de contactos y la organización del inventario mediante almacenes y ubicaciones. [Contactos de Odoo 18](https://www.odoo.com/documentation/18.0/applications/essentials/contacts.html) y [organización del inventario](https://www.odoo.com/documentation/18.0/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management.html). | Sirve como referencia para organizar clientes y distinguir físicamente dónde se conserva el material. | **No verificado:** configuración o desarrollo necesario para unir clientes, vehículos, instalaciones, rollos y recortes en el recorrido específico de Serna. |

Que un aspecto no esté verificado no significa que el sistema carezca de esa función. Significa que esta revisión no obtuvo evidencia suficiente para afirmarlo.

## 4. Tres aprendizajes aplicables

1. **Relacionar clientes, vehículos y trabajos.** La información conectada permite consultar antecedentes sin reconstruir cada atención a partir de archivos separados.
2. **Identificar la sede del inventario.** La consulta compartida de información debe conservar la separación de las piezas disponibles en cada sede.
3. **Relacionar el uso de material con el trabajo y su origen.** En Serna, esto requiere identificar rollos y recortes y evitar contar un sobrante también dentro de la pieza de origen.

Estos aprendizajes son interpretaciones para nuestro diseño. El registro de recortes y sus reglas procede de la entrevista y las aclaraciones del administrador, no de una función comprobada en los productos comparados.

## 5. Aplicación al proyecto

La primera versión mantendrá:

- Clientes y vehículos compartidos.
- Historial de trabajos consultable desde ambas sedes.
- Inventario independiente por sede.
- Identificación de rollos y recortes.
- Uso de material relacionado con cada trabajo.
- Correcciones y descartes conforme a los requisitos acordados.

Las dimensiones se registrarán en centímetros. La precisión de las medidas, el procedimiento de corte y las correcciones con sobrantes utilizados siguen pendientes.

La comparación no modifica las prioridades ni agrega funciones al alcance aprobado.

## 6. Propuesta de valor

Serna Polarizados propone un sistema académico ajustado a las necesidades identificadas de sus dos sedes de Ibagué: consultar antecedentes de vehículos y registrar el uso de materiales manteniendo separado el inventario de cada sede.

No se afirma que el proyecto sea superior, más económico o más eficiente que las soluciones comerciales. No se han realizado pruebas ni mediciones que permitan esa comparación.

El valor esperado deberá comprobarse durante el desarrollo y la evaluación con usuarios.

## 7. Exclusiones

Este análisis no justifica incorporar pagos, comisiones, facturación, agenda, QR, proveedores, compras, alertas automáticas, cotización de PPF ni sedes adicionales.

El alcance vigente y sus decisiones pendientes están en [requisitos.md](requisitos.md).

## 8. Uso de IA y revisión pendiente

**Herramienta:** Codex, con búsqueda web.

**Apoyo realizado:**

- Consulta de fuentes oficiales.
- Preparación y actualización de la comparación.
- Separación entre funciones publicadas e interpretaciones.
- Actualización de las conclusiones al inventario de rollos y recortes.
- Unificación de las referencias de Odoo en la versión 18.

Esta actualización no modifica las evidencias históricas de prompts que citaron otras versiones de documentación.

**Pendiente del equipo:**

- Revisar las fuentes y las interpretaciones con Jonathan.
- Registrar las observaciones y correcciones de esa revisión.
- Completar el intercambio y evaluación de prompts solicitado en clase.

Estas actividades pendientes no se presentan como realizadas.
