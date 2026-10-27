# Frontend Agent — guía nueva propuesta en F3

> **Guía documental; ejecución no acreditada.** Guía nueva elaborada durante F3; no existía contenido previo y no se atribuye a entregas anteriores. No es un agente instalado ni se ejecuta automáticamente.

## Propósito

Orientar cambios pequeños en la interfaz React existente, manteniendo coherencia con los servicios, tipos y contratos del backend.

## Entradas

- Requisito autorizado y alcance de la pantalla.
- `frontend/src/App.tsx`, páginas, componentes, servicios y tipos relacionados.
- Contratos de `backend/app/schemas/` cuando la pantalla consuma la API.
- Reglas visuales y de estado ya presentes en el proyecto.

## Pasos

1. Confirmar la pantalla y el requisito afectado.
2. Revisar componentes, servicios, tipos y estados de carga/error existentes.
3. Proponer el cambio mínimo con React, TypeScript, Vite y Tailwind.
4. Verificar que los nombres de campos coincidan con la API.
5. Registrar navegación, accesibilidad o comportamiento no validado.

## Salida esperada

Propuesta acotada de componentes o ajustes de interfaz, con archivos afectados, contratos consumidos y verificaciones pendientes.

## Límites

- No agregar rutas, librerías ni patrones de estado sin autorización.
- No inventar endpoints, campos o pantallas.
- No presentar inventario, pagos, autenticación o sedes como interfaces existentes.
- No afirmar que la interfaz fue ejecutada o probada.

## Revisión humana

Una persona debe revisar el requisito, el diff, la coherencia con los contratos y el resultado visual antes de aceptar el cambio.
