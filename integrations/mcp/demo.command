#!/bin/bash
cd "$(dirname "$0")" || exit 1
if [ ! -x .venv/bin/python ]; then
  echo 'Primero instala el entorno siguiendo README.md de esta carpeta.'
  exit 1
fi
.venv/bin/python demo.py
read -r -p 'Presiona Enter para cerrar.'
