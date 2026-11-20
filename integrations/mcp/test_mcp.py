import os
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from mcp.server.mcpserver.exceptions import ToolError
from sqlalchemy import create_engine, text
from demo_data import crear_demo
import server


class MCPTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ruta = Path(self.tmp.name) / 'demo.sqlite'
        crear_demo(self.ruta)
        self.env = dict(os.environ,SERNA_MCP_MODE='demo',SERNA_MCP_DEMO_DB=str(self.ruta),SERNA_MCP_ALLOW_DATABASE_READ='1')

    def tearDown(self):
        self.tmp.cleanup()

    def cliente(self, autorizado=True):
        env=dict(self.env,SERNA_MCP_ALLOW_DATABASE_READ='1' if autorizado else '0')
        return Client(StdioServerParameters(command=sys.executable,args=[str(Path(__file__).with_name('server.py'))],env=env))

    async def test_descubrimiento_mcp_y_herramientas_solo_lectura(self):
        async with self.cliente() as client:
            herramientas=(await client.list_tools()).tools
            self.assertEqual({t.name for t in herramientas},{'consultar_ventas_mes','buscar_instalaciones','consultar_instalacion','auditar_instalaciones'})
            self.assertTrue(all(t.annotations.read_only_hint for t in herramientas))
            self.assertTrue(client.protocol_version)
            recursos=await client.list_resources()
            self.assertIn('serna://ayuda', [str(r.uri) for r in recursos.resources])

    async def test_resultados_financieros_y_privacidad_por_protocolo(self):
        hoy=datetime.now(ZoneInfo('America/Bogota'))
        async with self.cliente() as client:
            ventas=await client.call_tool('consultar_ventas_mes',{'anio':hoy.year,'mes':hoy.month})
            self.assertFalse(ventas.is_error)
            self.assertEqual(ventas.structured_content['periodo']['totales']['ventas_cop'],900000)
            self.assertEqual(ventas.structured_content['periodo']['totales']['administrador_cop'],18000)
            busqueda=await client.call_tool('buscar_instalaciones',{'busqueda':'DEM123'})
            self.assertEqual(busqueda.structured_content['total'],1)
            detalle=await client.call_tool('consultar_instalacion',{'codigo':'SP1'})
            self.assertEqual(detalle.structured_content['valor_final_cop'],900000)
            self.assertNotIn('Cliente demostración',str(detalle.structured_content))
            self.assertNotIn('DEMO001',str(detalle.structured_content))

    async def test_validacion_y_codigo_inexistente(self):
        async with self.cliente() as client:
            for tool,args in [('consultar_ventas_mes',{'anio':2026,'mes':13}),
                              ('buscar_instalaciones',{'limite':10000}),
                              ('consultar_instalacion',{'codigo':'SP999'})]:
                result=await client.call_tool(tool,args)
                self.assertTrue(result.is_error)

    async def test_sin_habilitacion_no_consulta_datos(self):
        async with self.cliente(autorizado=False) as client:
            result=await client.call_tool('buscar_instalaciones',{})
            self.assertTrue(result.is_error)
            self.assertNotIn('DEM123',str(result))

    async def test_bloqueo_de_escritura_en_base_de_datos(self):
        engine=create_engine('sqlite:///'+str(self.ruta))
        with patch.dict(os.environ,self.env),patch.object(server,'_engine',engine):
            with self.assertRaises(ToolError):
                with server.lectura() as db:
                    db.execute(text('DELETE FROM instalaciones'))
            with server.lectura() as db:
                self.assertEqual(db.execute(text('SELECT count(*) FROM instalaciones')).scalar_one(),1)
        engine.dispose()

if __name__ == '__main__':
    unittest.main()
