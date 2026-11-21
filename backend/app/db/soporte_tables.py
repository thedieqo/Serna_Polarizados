"""Directorio y conversaciones privadas de soporte, independientes de permisos operativos."""
from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Index, func
metadata = MetaData(schema='public')
empleados = Table('soporte_empleados', metadata,
    Column('id', String, primary_key=True),
    Column('nombre', String, nullable=False),
    Column('documento', String, nullable=False, unique=True),
    Column('email', String, nullable=False, unique=True),
    Column('sede', String, nullable=False),
    Column('activo', Boolean, nullable=False, default=True),
    Column('registrado_por', String, nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False, server_default=func.now()),
)
mensajes = Table('soporte_mensajes', metadata,
    Column('id', Integer, primary_key=True),
    Column('solicitud_id', String, nullable=False, unique=True),
    Column('empleado_id', String, ForeignKey('public.soporte_empleados.id'), nullable=False),
    Column('autor_email', String, nullable=False),
    Column('autor_tipo', String, nullable=False),
    Column('texto', Text, nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False, server_default=func.now()),
)
Index('soporte_mensajes_conversacion_idx',mensajes.c.empleado_id,mensajes.c.id)
auditoria = Table('soporte_auditoria', metadata,
    Column('id', Integer, primary_key=True),
    Column('empleado_id', String, ForeignKey('public.soporte_empleados.id'), nullable=False),
    Column('actor', String, nullable=False),
    Column('accion', String, nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False, server_default=func.now()),
)

intentos = Table('soporte_intentos', metadata,
    Column('id', Integer, primary_key=True),
    Column('origen', String(64), nullable=False, index=True),
    Column('created_at', DateTime(timezone=True), nullable=False, server_default=func.now()),
)
