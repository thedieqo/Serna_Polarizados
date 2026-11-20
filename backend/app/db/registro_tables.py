from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
    text,
)

metadata = MetaData()

catalogo_tecnologias_polarizado = Table(
    "catalogo_tecnologias_polarizado",
    metadata,
    Column("id", String, primary_key=True),
    Column("label", String, nullable=False),
)

catalogo_opacidades_polarizado = Table(
    "catalogo_opacidades_polarizado",
    metadata,
    Column("id", String, primary_key=True),
    Column("label", String, nullable=False),
)

catalogo_instaladores = Table(
    "catalogo_instaladores",
    metadata,
    Column("id", String, primary_key=True),
    Column("label", String, nullable=False),
)

catalogo_tipos_factura = Table(
    "catalogo_tipos_factura",
    metadata,
    Column("id", String, primary_key=True),
    Column("label", String, nullable=False),
)

catalogo_vidrios_polarizado = Table(
    "catalogo_vidrios_polarizado",
    metadata,
    Column("id", String, primary_key=True),
    Column("label", String, nullable=False),
)

clientes = Table(
    "clientes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String, nullable=False),
    Column("documento", String, nullable=False, unique=True, index=True),
    Column("contacto", String, nullable=False),
    Column("telefono", String, nullable=True),
    Column("email", String, nullable=True),
)

vehiculos = Table(
    "vehiculos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("placa", String, nullable=False, unique=True, index=True),
    Column("descripcion", String, nullable=True),
    Column("cliente_id", Integer, ForeignKey("clientes.id"), nullable=False, index=True),
    Column("marca", String, nullable=True),
)

instalaciones = Table(
    "instalaciones",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("vehiculo_id", Integer, ForeignKey("vehiculos.id"), nullable=False, index=True),
    Column("fecha", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("tipo_servicio", String, nullable=False),
    Column("opacidad", String, nullable=True),
    Column("zonas", JSON, nullable=False),
    Column("asignaciones_instaladores", JSON, nullable=False),
    Column("retiro_material_anterior", Boolean, default=False, nullable=False),
    Column("observaciones", Text, nullable=True),
    Column("estado", String, nullable=False),
    Column("tipo_factura", String, nullable=True),
    Column("desglose_precios", JSON, nullable=True),
    Column("tarifas_aplicadas", JSON, nullable=True),
    Column("moneda", String, nullable=True),
    Column("precio_estado", String, nullable=True),
    Column("precio_total_cop", Integer, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now(), nullable=True),
)

instalacion_detalles = Table(
    "instalacion_detalles",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "instalacion_id",
        Integer,
        ForeignKey("instalaciones.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "vidrio_id",
        String,
        ForeignKey("catalogo_vidrios_polarizado.id"),
        nullable=False,
    ),
    Column("panel", String, nullable=True),
    Column(
        "tecnologia_id",
        String,
        ForeignKey("catalogo_tecnologias_polarizado.id"),
        nullable=False,
    ),
    Column(
        "opacidad_id",
        String,
        ForeignKey("catalogo_opacidades_polarizado.id"),
        nullable=False,
    ),
    Column(
        "instalador_id",
        String,
        ForeignKey("catalogo_instaladores.id"),
        nullable=False,
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)

Index(
    "instalacion_detalles_vidrio_panel_uniq",
    instalacion_detalles.c.instalacion_id,
    instalacion_detalles.c.vidrio_id,
    text("COALESCE(panel, 'unico')"),
    unique=True,
)

instalacion_novedades = Table(
    "instalacion_novedades",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "instalacion_id",
        Integer,
        ForeignKey("instalaciones.id"),
        nullable=False,
        index=True,
    ),
    Column("fecha_atencion", DateTime(timezone=True), nullable=False),
    Column("motivo", String, nullable=False),
    Column("descripcion", Text, nullable=False),
    Column("registrado_por", String, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)

Index(
    "instalacion_novedades_instalacion_fecha_idx",
    instalacion_novedades.c.instalacion_id,
    instalacion_novedades.c.fecha_atencion.desc(),
)

from sqlalchemy import CheckConstraint, UniqueConstraint
inventario = Table(
    'inventario', metadata,
    Column('sku', String, primary_key=True),
    Column('tecnologia_id', String, nullable=False),
    Column('opacidad_id', String, nullable=False),
    Column('material', String, nullable=False),
    Column('disponible_cm', Integer, nullable=False),
    CheckConstraint('disponible_cm >= 0', name='inventario_no_negativo'),
)
inventario_movimientos = Table(
    'inventario_movimientos', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String, ForeignKey('inventario.sku'), nullable=False),
    Column('instalacion_id', Integer, ForeignKey('instalaciones.id'), nullable=True),
    Column('cantidad_cm', Integer, nullable=False),
    Column('motivo', String, nullable=False),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False),
    UniqueConstraint('instalacion_id', 'sku', name='inventario_consumo_instalacion_unico'),
)
