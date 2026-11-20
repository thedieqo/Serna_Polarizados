# MCP — Serna Polarizados

Servidor local MCP (Model Context Protocol) para consultar la información del negocio mediante herramientas. Incluye un cliente de demostración que negocia el protocolo, descubre las herramientas y ejecuta consultas reales mediante MCP. No requiere un asistente de IA para la demostración.

## Arquitectura

Cliente MCP → transporte stdio → servidor MCP → servicios existentes → base de datos en modo de solo lectura.

El módulo tiene un entorno Python independiente. No cambia los formularios, las dependencias del backend ni la aplicación desplegada. No abre un puerto público ni agrega una ruta `/mcp` a Render. Una interfaz de chat con IA no forma parte de esta implementación.

## Preparación

Desde la raíz del repositorio, con Python 3.13:

```sh
python3 -m venv integrations/mcp/.venv
integrations/mcp/.venv/bin/python -m pip install -r integrations/mcp/requirements.txt
```

No instalar estas dependencias en el entorno del backend: esta integración usa su propio SDK y entorno.

## Demostración para la presentación

```sh
integrations/mcp/.venv/bin/python integrations/mcp/demo.py
```

En macOS también se puede abrir `demo.command` después de preparar el entorno.

La demostración crea una base temporal con datos ficticios, conecta un cliente MCP al servidor y ejecuta las tres herramientas. Se verá una venta de $900.000 después del descuento, comisión del administrador de $18.000 y mano de obra de $100.000. Al terminar elimina la base temporal. No crea registros en Supabase.

1. Mostrar el nombre del servidor y la versión de protocolo negociada.
2. Mostrar las tres herramientas descubiertas por el cliente.
3. Mostrar ventas y ganancias del mes.
4. Mostrar la búsqueda y el detalle de SP1.
5. Señalar que los resultados identifican explícitamente su fuente como datos ficticios.

Para consultar los datos reales configurados en `backend/.env`:

```sh
integrations/mcp/.venv/bin/python integrations/mcp/demo.py --real
```

Este modo consulta ventas y hasta tres instalaciones, sin crearlas ni modificarlas. Los resultados dependen de los registros existentes.

## Herramientas

| Herramienta | Parámetros | Resultado |
|---|---|---|
| `consultar_ventas_mes` | `anio`, `mes`, `corte` opcional: `mes`, `primera`, `segunda` | Ventas, descuentos, comisión del administrador y ganancias por instalador; incluye acumulado mensual hasta ahora. |
| `buscar_instalaciones` | `busqueda` opcional por placa o documento, `limite` de 1 a 20, `desplazamiento` | Códigos SP, placas, marcas, fechas y servicios. |
| `consultar_instalacion` | `codigo`, por ejemplo `SP1` | Detalle técnico y financiero, pagos, mano de obra y garantía disponible. |

También publica el recurso `serna://ayuda`. Las ganancias calculadas no confirman que el personal ya haya recibido el pago. Los datos históricos incompletos conservan sus valores faltantes.

## Conectar un cliente compatible con MCP

Ejemplo de configuración; sustituir las rutas por las absolutas del equipo:

```json
{
  "mcpServers": {
    "serna-polarizados": {
      "command": "/ruta/Serna_Polarizados/integrations/mcp/.venv/bin/python",
      "args": ["/ruta/Serna_Polarizados/integrations/mcp/server.py"],
      "env": {"SERNA_MCP_ALLOW_DATABASE_READ": "1"}
    }
  }
}
```

El formato de instalación depende del cliente. No incluir contraseñas en este archivo ni subir `backend/.env` a GitHub.

## Acceso y protección de datos

Es una integración **local para operadores y clientes MCP de confianza** que ya tienen acceso a la configuración del equipo. La variable `SERNA_MCP_ALLOW_DATABASE_READ=1` habilita las consultas; no reemplaza una autenticación. No utiliza el inicio de sesión Google de la web ni está preparada para exponerse como servicio público.

Cada consulta PostgreSQL abre una transacción `READ ONLY` con límite de ejecución de diez segundos y termina con rollback. La demostración SQLite activa `query_only`. No existen herramientas de escritura ni de SQL arbitrario. Las respuestas omiten nombre, documento, teléfono y correo del propietario; sí incluyen placas y datos del negocio. Las credenciales no se entregan como argumentos ni resultados.

## Verificación

```sh
integrations/mcp/.venv/bin/python -m unittest discover -s integrations/mcp -p 'test_*.py'
```

Las pruebas verifican descubrimiento y llamadas MCP, resultados financieros, omisión de datos de contacto, validación de entradas, habilitación local y rechazo de escritura. Usan una base temporal independiente.

## Explicación breve para el profesor

“Implementamos MCP, un protocolo que permite que un cliente descubra y use herramientas de nuestro sistema. Nuestro servidor ofrece consultas de ventas mensuales, búsqueda de instalaciones y detalle de una instalación. En la demostración, el cliente negocia la conexión, descubre esas herramientas y recibe resultados estructurados. Reutilizamos las reglas del negocio y ejecutamos las consultas en modo de solo lectura. La integración funciona en un módulo independiente, por lo que la plataforma web sigue operando normalmente.”

Implementación basada en el [SDK oficial de Python](https://github.com/modelcontextprotocol/python-sdk) y su [documentación del cliente](https://py.sdk.modelcontextprotocol.io/client/).
