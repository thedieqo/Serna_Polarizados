"""Cliente MCP real por stdio. Por defecto usa datos ficticios temporales."""
import argparse
import asyncio
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from demo_data import crear_demo


async def demostrar(real, carpeta):
    env = dict(os.environ, SERNA_MCP_ALLOW_DATABASE_READ='1', SERNA_MCP_MODE='real' if real else 'demo')
    if not real:
        ruta = Path(carpeta) / 'demostracion.sqlite'
        crear_demo(ruta)
        env['SERNA_MCP_DEMO_DB'] = str(ruta)
    params = StdioServerParameters(command=sys.executable, args=[str(Path(__file__).with_name('server.py'))], env=env)
    print('MODO:', 'DATOS REALES · SOLO LECTURA' if real else 'DEMOSTRACIÓN · DATOS FICTICIOS')
    async with Client(params) as cliente:
        print('Servidor MCP conectado:', cliente.server_info.name)
        print('Protocolo negociado:', cliente.protocol_version)
        herramientas = await cliente.list_tools()
        print('Herramientas descubiertas:', ', '.join(t.name for t in herramientas.tools))
        ahora = datetime.now(ZoneInfo('America/Bogota'))
        llamadas = [('consultar_ventas_mes', {'anio':ahora.year,'mes':ahora.month}),
                    ('buscar_instalaciones', {'limite':3}), ('auditar_instalaciones', {})]
        if not real: llamadas.append(('consultar_instalacion', {'codigo':'SP1'}))
        for nombre, argumentos in llamadas:
            resultado = await cliente.call_tool(nombre, argumentos)
            print('\nHerramienta:',nombre,'· Argumentos:',json.dumps(argumentos))
            if resultado.is_error:
                raise RuntimeError('La consulta MCP falló. Revisa la configuración local.')
            print(json.dumps(resultado.structured_content,ensure_ascii=False,indent=2,default=str))
            if nombre == 'auditar_instalaciones':
                from report import mostrar
                mostrar(resultado.structured_content)
    print('\nDemostración completada: no se modificaron datos reales.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--real',action='store_true',help='Consultar la base configurada en backend/.env, sin escribir.')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='serna-mcp-') as carpeta:
        asyncio.run(demostrar(args.real,carpeta))
