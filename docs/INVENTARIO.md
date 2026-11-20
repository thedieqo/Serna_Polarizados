# Inventario por sede

Cada sede tiene 24 existencias: cuatro tecnologías, tres opacidades (5/20/35 %) y dos materiales (polarizado o película de seguridad). La carga inicial autorizada es 200 m lineales por combinación, desde la activación. No se reconstruye consumo de instalaciones históricas.

Consumo por registro de vidrio: parabrisas 150 cm; laterales delanteros 80 cm por pareja; laterales traseros 80 cm por pareja; luneta 110 cm; sunroof sencillo 110 cm; doble 75 cm por panel (150 cm total). Cuatro laterales son dos parejas: 160 cm. Con película de seguridad se consume únicamente película de la tecnología/opacidad seleccionada.

`services/inventario.py` calcula en centímetros enteros. El guardado descuenta mediante UPDATE condicionado a existencias suficientes, dentro de la misma transacción de cliente, vehículo e instalación. Si falta material, todo se revierte. Generar resumen y consultar nunca descuentan. Los movimientos vinculan código SP, producto, cantidad y fecha de registro. No hay devolución automática por garantías ni anulación: el material instalado ya fue consumido.

Desde backend, ejecutar `python scripts/preparar_inventario.py` después de preparar las sedes. El script inicializa únicamente productos inexistentes, usa una transacción y un bloqueo de preparación; repetirlo no repone consumos. Las tablas tienen RLS habilitado sin políticas públicas; el acceso se realiza por el backend autorizado y separado por esquema.

La pestaña Inventario muestra saldo, consumo desde la carga inicial y últimos 100 movimientos. Esta versión no incluye compras, entradas adicionales, merma ni ajustes manuales. El indicador inicial de 200 m corresponde a la carga inicial actual, no a un rollo físico rastreado por número de lote.

La ruta de creación antigua `/instalaciones/` ya no permite altas sin detalle técnico. El formulario utiliza `/instalaciones/registro`, que controla los consumos.
