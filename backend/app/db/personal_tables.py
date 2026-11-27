"""Fichas y archivos privados. Extensión aditiva del directorio central."""
from sqlalchemy import Table, Column, String, Integer, DateTime, JSON, LargeBinary, ForeignKey, func
from app.db.gerencia_tables import metadata
fichas = Table('personal_fichas', metadata,
 Column('empleado_id', String, ForeignKey('public.gerencia_equipo.id'), primary_key=True),
 Column('documento', String(30), unique=True), Column('datos', JSON, nullable=False),
 Column('estado', String(20), nullable=False, default='pendiente'))
archivos = Table('personal_archivos', metadata,
 Column('empleado_id', String, ForeignKey('public.gerencia_equipo.id'), primary_key=True),
 Column('tipo', String(20), primary_key=True), Column('mime', String(40), nullable=False),
 Column('contenido', LargeBinary, nullable=False), Column('created_at', DateTime(timezone=True), server_default=func.now()))
traslados = Table('personal_traslados', metadata,
 Column('id', String, primary_key=True), Column('empleado_id', String, ForeignKey('public.gerencia_equipo.id'), nullable=False),
 Column('origen', String(40), nullable=False), Column('destino', String(40), nullable=False),
 Column('solicitante', String(254), nullable=False), Column('motivo', String(300), nullable=False),
 Column('estado', String(20), nullable=False, default='pendiente'),
 Column('resuelto_por', String(254)), Column('respuesta', String(300)),
 Column('created_at', DateTime(timezone=True), server_default=func.now()), Column('resuelto_at', DateTime(timezone=True)))
