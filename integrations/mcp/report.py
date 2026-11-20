"""Informe HTML local, escapado, fuera del repositorio."""
import html
import json
import tempfile
import webbrowser
from pathlib import Path


def mostrar(resultado):
    contenido = html.escape(json.dumps(resultado, ensure_ascii=False, indent=2))
    pagina = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>Auditoría Serna</title>
    <style>body{{background:#0d1320;color:#eef2ff;font:18px system-ui;max-width:1000px;margin:50px auto;padding:20px}}section{{padding:25px;background:#1b2435;border-radius:16px}}pre{{white-space:pre-wrap;font-size:15px}}h1{{color:#a8bfff}}</style>
    <h1>Serna · Auditoría de instalaciones</h1><p>Resultado obtenido mediante una llamada MCP.</p>
    <section><h2>{resultado['revisados']} instalaciones revisadas · {resultado['cantidad_hallazgos']} hallazgos</h2>
    <p>{html.escape(resultado['fuente'])}</p><p>Reglas: pagos completos, suma de medios de pago, comisión del 2 % y saldo cero.</p>
    <p>Sin hallazgos significa que estas comprobaciones no detectaron diferencias en esta página de registros.</p><pre>{contenido}</pre></section></html>"""
    with tempfile.NamedTemporaryFile(suffix='.html', prefix='serna-auditoria-', delete=False, mode='w') as archivo:
        archivo.write(pagina)
        ruta = Path(archivo.name)
    print('Informe visual:', ruta)
    webbrowser.open(ruta.as_uri())
