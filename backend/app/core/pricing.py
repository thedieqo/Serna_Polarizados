from app.core.catalogs import label_for

PRECIO_PENDIENTE = "Precio pendiente de definir"
MONEDA = "COP"
VERSION_TARIFAS = "2026-11-20"

TARIFAS_TECNOLOGIA_COP = {
    "high_definition_premium": 250000,
    "ultra_hd": 350000,
    "color_stable": 400000,
    "ceramic_ir": 550000,
}

SECCION_UNICA = frozenset({"parabrisas", "luneta", "panoramico_trasero"})
SECCION_PAR = frozenset({"laterales_delanteros", "laterales_traseros"})

INCREMENTO_SEGURIDAD_LATERALES_COP = 100000

REGLAS_PENDIENTES = (
    "Precio de un lateral individual",
    "Tratamiento de fijos",
    "Sunroof doble",
    "Cálculo de pares con tecnologías diferentes",
)


def catalogo_tarifas() -> dict:
    return {
        "moneda": MONEDA,
        "version": VERSION_TARIFAS,
        "tecnologias": [
            {
                "id": tecnologia_id,
                "label": label_for("tecnologias", tecnologia_id),
                "precio_seccion_cop": precio,
            }
            for tecnologia_id, precio in TARIFAS_TECNOLOGIA_COP.items()
        ],
        "incremento_seguridad_laterales_cop": INCREMENTO_SEGURIDAD_LATERALES_COP,
        "incremento_seguridad_laterales_unidad": "Por pareja; $200.000 por los cuatro laterales",
        "reglas_pendientes": list(REGLAS_PENDIENTES),
    }


def desglose_para_detalle(detalle) -> dict:
    vidrio_id = detalle.vidrio_id
    tecnologia_id = detalle.tecnologia_id
    concepto = f"{label_for('vidrios', vidrio_id)} - {label_for('tecnologias', tecnologia_id)}"

    if tecnologia_id not in TARIFAS_TECNOLOGIA_COP:
        return {
            "concepto": concepto,
            "detalle": "Tecnología sin tarifa confirmada",
            "secciones": None,
            "tarifa_unitaria_cop": None,
            "importe_cop": None,
            "estado": "pendiente",
            "motivo_pendiente": PRECIO_PENDIENTE,
        }

    if vidrio_id in SECCION_UNICA:
        tarifa = TARIFAS_TECNOLOGIA_COP[tecnologia_id]
        return {
            "concepto": concepto,
            "detalle": "1 sección confirmada",
            "secciones": 1,
            "tarifa_unitaria_cop": tarifa,
            "importe_cop": tarifa,
            "estado": "definido",
            "motivo_pendiente": None,
        }

    if vidrio_id in SECCION_PAR:
        tarifa = TARIFAS_TECNOLOGIA_COP[tecnologia_id]
        return {
            "concepto": concepto,
            "detalle": "1 par/sección confirmado; no se tarifa por vidrio lateral individual",
            "secciones": 1,
            "tarifa_unitaria_cop": tarifa,
            "importe_cop": tarifa,
            "estado": "definido",
            "motivo_pendiente": None,
        }

    motivo = {
        "sunroof_simple": "Techo solar simple pendiente de tarifa",
        "sunroof_doble": "Sunroof doble pendiente de regla y tarifa",
    }.get(vidrio_id, "Vidrio sin regla de sección confirmada")
    return {
        "concepto": concepto,
        "detalle": motivo,
        "secciones": None,
        "tarifa_unitaria_cop": None,
        "importe_cop": None,
        "estado": "pendiente",
        "motivo_pendiente": PRECIO_PENDIENTE,
    }


def calcular_desglose(detalles) -> dict:
    conceptos = []
    agrupados = []
    for detalle in detalles:
        item = desglose_para_detalle(detalle)
        if getattr(detalle, 'pelicula_seguridad', False):
            item['importe_cop'] += INCREMENTO_SEGURIDAD_LATERALES_COP
            item['detalle'] += '; película de seguridad +$100.000 por pareja'
        if getattr(detalle, 'grupo', None) == 'cuatro_laterales':
            agrupados.append(item)
        else:
            conceptos.append(item)
    if agrupados:
        conceptos.append({
            'concepto': 'Cuatro laterales',
            'detalle': ' + '.join(f"{i['concepto']} ({i['detalle']})" for i in agrupados),
            'secciones': 2, 'tarifa_unitaria_cop': None,
            'importe_cop': sum(i['importe_cop'] for i in agrupados),
            'estado': 'definido', 'motivo_pendiente': None,
        })
    pendiente = any(item["estado"] == "pendiente" for item in conceptos)
    total = None if pendiente else sum(item["importe_cop"] for item in conceptos)
    return {
        "moneda": MONEDA,
        "version": VERSION_TARIFAS,
        "estado": "pendiente" if pendiente else "definido",
        "total_cop": total,
        "etiqueta_total": PRECIO_PENDIENTE if pendiente else "Total confirmado",
        "conceptos": conceptos,
    }


def tarifas_aplicadas(desglose: dict, detalles=None) -> dict:
    usadas = sorted(
        {
            item["tarifa_unitaria_cop"]
            for item in desglose["conceptos"]
            if item["estado"] == "definido" and item["tarifa_unitaria_cop"] is not None
        }
    )
    por_tecnologia = {
        tecnologia_id: precio
        for tecnologia_id, precio in TARIFAS_TECNOLOGIA_COP.items()
        if ((tecnologia_id in {d.tecnologia_id for d in detalles}) if detalles is not None else (precio in usadas))
    }
    return {
        "moneda": MONEDA,
        "version": VERSION_TARIFAS,
        "por_tecnologia": por_tecnologia,
        "incremento_seguridad_laterales_cop": INCREMENTO_SEGURIDAD_LATERALES_COP,
        "incremento_seguridad_laterales_unidad": "Por pareja; $200.000 por los cuatro laterales",
    }
