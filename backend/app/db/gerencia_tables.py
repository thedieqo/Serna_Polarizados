"""Directorio central de pruebas; no concede autorización de inicio de sesión."""
from sqlalchemy import MetaData,Table,Column,String,Integer,Boolean,DateTime,JSON,func
metadata=MetaData(schema='public')
equipo=Table('gerencia_equipo',metadata,
 Column('id',String,primary_key=True),Column('nombre',String(120),nullable=False),
 Column('email',String(254),nullable=False,unique=True),Column('perfil',String(40),nullable=False),
 Column('sede',String(40),nullable=True),Column('activo',Boolean,nullable=False,default=True),
 Column('es_prueba',Boolean,nullable=False,default=True),Column('revision',Integer,nullable=False,default=1),
 Column('created_at',DateTime(timezone=True),nullable=False,server_default=func.now()),
 Column('updated_at',DateTime(timezone=True),nullable=False,server_default=func.now()))
actividad=Table('gerencia_actividad',metadata,
 Column('id',Integer,primary_key=True),Column('empleado_id',String,nullable=False,index=True),
 Column('actor',String(254),nullable=False),Column('accion',String(40),nullable=False),
 Column('motivo',String(300),nullable=False),Column('antes',JSON),Column('despues',JSON),
 Column('created_at',DateTime(timezone=True),nullable=False,server_default=func.now()))
