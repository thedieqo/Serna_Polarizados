TECNOLOGIAS_POLARIZADO = (
    {"id": "high_definition_premium", "label": "High Definition Premium"},
    {"id": "ultra_hd", "label": "Ultra HD"},
    {"id": "color_stable", "label": "Color Stable"},
    {"id": "ceramic_ir", "label": "Ceramic IR"},
)

OPACIDADES_POLARIZADO = (
    {"id": "5", "label": "5 %"},
    {"id": "20", "label": "20 %"},
    {"id": "35", "label": "35 %"},
)

INSTALADORES = (
    {"id": "daniel_mira", "label": "Daniel Mira"},
    {"id": "joseth_mora", "label": "Joseth Mora"},
)

TIPOS_FACTURA = (
    {"id": "normal", "label": "Normal"},
    {"id": "electronica", "label": "Electrónica"},
)

VIDRIOS_POLARIZADO = (
    {"id": "parabrisas", "label": "Parabrisas", "paneles": []},
    {"id": "laterales_delanteros", "label": "Laterales delanteros", "paneles": []},
    {"id": "laterales_traseros", "label": "Laterales traseros", "paneles": []},
    {"id": "luneta", "label": "Luneta", "paneles": []},
    {"id": "sunroof_simple", "label": "Techo solar simple", "paneles": []},
    {
        "id": "sunroof_doble",
        "label": "Techo solar doble",
        "paneles": ["delantero", "trasero"],
    },
)

PANELES_SUNROOF_DOBLE = ("delantero", "trasero")

TECNOLOGIA_IDS = frozenset(item["id"] for item in TECNOLOGIAS_POLARIZADO)
OPACIDAD_IDS = frozenset(item["id"] for item in OPACIDADES_POLARIZADO)
INSTALADOR_IDS = frozenset(item["id"] for item in INSTALADORES)
TIPO_FACTURA_IDS = frozenset(item["id"] for item in TIPOS_FACTURA)
VIDRIO_IDS = frozenset(item["id"] for item in VIDRIOS_POLARIZADO)

_LABELS = {
    "tecnologias": {item["id"]: item["label"] for item in TECNOLOGIAS_POLARIZADO},
    "opacidades": {item["id"]: item["label"] for item in OPACIDADES_POLARIZADO},
    "instaladores": {item["id"]: item["label"] for item in INSTALADORES},
    "tipos_factura": {item["id"]: item["label"] for item in TIPOS_FACTURA},
    "vidrios": {item["id"]: item["label"] for item in VIDRIOS_POLARIZADO},
}


def catalogos_response() -> dict:
    from app.core.pricing import catalogo_tarifas

    return {
        "servicio": "polarizado",
        "tecnologias": [dict(item) for item in TECNOLOGIAS_POLARIZADO],
        "opacidades": [dict(item) for item in OPACIDADES_POLARIZADO],
        "instaladores": [dict(item) for item in INSTALADORES],
        "tipos_factura": [dict(item) for item in TIPOS_FACTURA],
        "vidrios": [dict(item) for item in VIDRIOS_POLARIZADO],
        "tarifas": catalogo_tarifas(),
    }


def label_for(catalogo: str, item_id: str) -> str:
    return _LABELS[catalogo][item_id]
