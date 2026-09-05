# Análisis competitivo — Serna Polarizados

## 1. Objetivo

Comparar tres soluciones existentes para identificar funciones útiles y orientar el alcance del proyecto académico de Serna Polarizados.

La comparación se concentra en clientes, vehículos, historial de trabajos e inventario para dos sedes de Ibagué.

## 2. Método

Se consultaron páginas oficiales de Shopmonkey, AutoLeap y Odoo el 5 de septiembre de 2026.

Shopmonkey y AutoLeap son referentes especializados en talleres automotrices. Odoo es una alternativa de gestión empresarial con módulos que cubren partes de la necesidad.

El análisis es documental: no se instalaron ni probaron los sistemas. Las observaciones sobre su adaptación a Serna son aspectos por evaluar, no fallos demostrados.

## 3. Tabla comparativa

| Solución | Funciones documentadas | Relación con Serna | Aspectos por verificar |
| --- | --- | --- | --- |
| Shopmonkey | Registro de clientes y vehículos, asociación de vehículos a clientes e historial de servicios. También presenta herramientas de inventario. [1][2] | Es un referente para organizar la relación cliente–vehículo–trabajo y consultar antecedentes. | Comprobar cómo maneja materiales de polarizado medidos en metros o rollos y cómo se ajusta a la operación de las dos sedes. |
| AutoLeap | Control de inventario, seguimiento de piezas utilizadas por trabajo y consulta de existencias entre ubicaciones. [3] | Es un referente para relacionar materiales con trabajos y distinguir existencias por sede. | Comprobar el manejo de consumos fraccionarios de películas de polarizado y su adaptación a los servicios de Serna. |
| Odoo | Gestión de contactos y organización del inventario mediante almacenes y ubicaciones. [4][5] | Es una alternativa para centralizar clientes y representar los inventarios separados de las sedes. | Determinar qué configuración o desarrollo permitiría unir clientes, vehículos, trabajos y consumo de materiales. Las fuentes consultadas no demuestran ese flujo completo para un negocio de polarizados. |

## 4. Aprendizajes para el proyecto

- La información del cliente debe estar relacionada con sus vehículos y trabajos anteriores.
- El registro de un consumo debe permitir identificar a qué trabajo corresponde.
- Las existencias deben distinguirse por sede.
- Compartir información entre sedes no significa mezclar sus inventarios.
- El manejo de materiales en metros o rollos necesita reglas claras antes de programarse.

Estos puntos orientan el diseño; no obligan a reproducir todas las funciones de los sistemas comparados.

## 5. Propuesta de valor de Serna

El proyecto propone un sistema académico enfocado en la operación acordada para las dos sedes de Ibagué:

- Clientes y vehículos compartidos.
- Historial de trabajos consultable desde ambas sedes.
- Inventario independiente por sede.
- Consumos de materiales relacionados con cada trabajo.

El valor esperado está en adaptar un alcance pequeño a las necesidades identificadas del negocio.

No se afirma que el proyecto sea más completo, económico o eficiente que las soluciones comerciales. Esas comparaciones requerirían pruebas y datos adicionales.

## 6. Decisión para la primera versión

Mantener el alcance en clientes, vehículos, trabajos e inventario por sede.

La comparación no justifica agregar pagos, facturación, agenda, compras ni otras funciones que quedaron fuera del MVP.

Las unidades de medida, los consumos fraccionarios y las correcciones de inventario se precisarán durante el análisis de requisitos.

## 7. Fuentes oficiales

[1] [Shopmonkey: clientes, vehículos e historial de servicios](https://support.shopmonkey.io/hc/en-us/articles/38744260861204-Lists-Page).

[2] [Shopmonkey: gestión de inventario](https://www.shopmonkey.io/demo-inventory-management).

[3] [AutoLeap: inventario y gestión entre ubicaciones](https://autoleap.com/features/inventory/).

[4] [Odoo 18: gestión de contactos](https://www.odoo.com/documentation/18.0/applications/essentials/contacts.html).

[5] [Odoo 17: almacenes y almacenamiento](https://www.odoo.com/documentation/17.0/applications/inventory_and_mrp/inventory/warehouses_storage.html).

Se consultaron las versiones de documentación indicadas. No se evaluaron precios, planes comerciales ni disponibilidad de soporte local.

## 8. Uso de IA y revisión pendiente

Fecha: 5 de septiembre de 2026.

Herramienta: Codex, con búsqueda web.

Apoyo realizado: consulta de fuentes oficiales, preparación de la comparación y redacción del borrador.

Criterios aplicados: separar funciones documentadas de aspectos por verificar, evitar precios sin comprobar y conservar el alcance acordado.

Pendiente del equipo: revisar las fuentes y el contenido con Jonathan, registrar sus correcciones y realizar el intercambio y evaluación de prompts solicitado en clase. Esa revisión no se presenta como realizada.
