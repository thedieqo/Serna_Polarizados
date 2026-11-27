from decimal import Decimal
from typing import Literal
from uuid import UUID, uuid4
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError
from app.core.auth import get_current_identity, require_write_access, require_sede
from app.db.session import get_db
from app.db.registro_tables import trabajadores, trabajador_auditoria
from app.services import trabajo

router = APIRouter()

class Corte(BaseModel):
    model_config = ConfigDict(extra='forbid')
    slot: str = Field(max_length=80)
    metros: Decimal = Field(gt=0, le=200, max_digits=5, decimal_places=2)
    tipo_parabrisas: Literal['normal','camion','buseta'] = 'normal'

class Confirmacion(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: UUID
    instalacion_id: int = Field(gt=0)
    vidrios: list[Corte] = Field(min_length=1, max_length=30)

class Aprobacion(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    nombre: str = Field(min_length=2,max_length=100)
    email: str = Field(min_length=5,max_length=254, pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    activo: bool = True

@router.get('/mi-trabajo')
def mi_trabajo(identity=Depends(get_current_identity), db=Depends(get_db)):
    return trabajo.resumen(db, identity.email)

@router.get('/mi-trabajo/buscar')
def buscar(placa: str = Query(min_length=3,max_length=20), identity=Depends(get_current_identity), db=Depends(get_db)):
    if not trabajo.trabajador(db, identity.email):
        raise HTTPException(403, detail='Gerencia debe aprobar tu cuenta en esta sede.')
    return {'instalaciones':trabajo.buscar(db, placa)}

@router.post('/mi-trabajo/confirmar', dependencies=[Depends(require_write_access)])
def confirmar(payload: Confirmacion, identity=Depends(get_current_identity), db=Depends(get_db)):
    try:
        resultado = trabajo.confirmar(db, identity.email, payload)
        db.commit()
        return resultado
    except (trabajo.TrabajoError, IntegrityError) as exc:
        db.rollback()
        raise HTTPException(409, detail=str(exc) if isinstance(exc, trabajo.TrabajoError) else 'El trabajo ya fue registrado. Actualiza la búsqueda.') from exc

@router.get('/gerencia/instaladores')
def listar(db=Depends(get_db)):
    return {'instaladores':[dict(r) for r in db.execute(select(trabajadores).order_by(trabajadores.c.nombre)).mappings()]}

@router.post('/gerencia/instaladores', dependencies=[Depends(require_write_access)])
def aprobar(payload: Aprobacion, identity=Depends(get_current_identity), db=Depends(get_db), sede=Depends(require_sede)):
    email = payload.email.lower()
    from app.db.gerencia_tables import equipo
    from app.api.v1.personal import ficha, faltantes
    from app.services.personal import sincronizar_instalador
    persona = db.execute(select(equipo).where(equipo.c.email == email).with_for_update()).mappings().first()
    if payload.activo:
        if not persona:
            raise HTTPException(422, detail='Crea y completa primero la ficha en Gerencia → Empleados.')
        f = ficha(db, persona['id'])
        if not persona['activo'] or f['estado'] != 'activo' or persona['sede'] != sede or persona['perfil'] not in ('instalador', 'instalador_ppf') or faltantes(db, persona, f['datos']):
            raise HTTPException(422, detail='La ficha debe estar completa, activa y asignada como instalador a esta sede.')
    actual = db.execute(select(trabajadores).where(trabajadores.c.email == email).with_for_update()).mappings().first()
    ident = actual['id'] if actual else str(uuid4())
    valores = {'nombre':persona['nombre'] if persona else payload.nombre,'email':email,'activo':payload.activo,'aprobado_por':identity.email,'updated_at':datetime.now(timezone.utc)}
    try:
        if actual: db.execute(update(trabajadores).where(trabajadores.c.id == ident).values(**valores))
        else: db.execute(insert(trabajadores).values(id=ident,**valores))
        db.execute(insert(trabajador_auditoria).values(trabajador_id=ident,actor=identity.email,accion='aprobado' if payload.activo else 'desactivado'))
        if persona: sincronizar_instalador(db,persona,sede,payload.activo,identity.email)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409,detail='Este correo acaba de registrarse. Actualiza la lista.') from exc
    return {'id':ident,'aprobado':payload.activo}
