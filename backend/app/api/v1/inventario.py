from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.inventario import consultar
router=APIRouter(prefix='/inventario',tags=['Inventario'])
@router.get('/')
def read_inventario(db:Session=Depends(get_db)):
    return consultar(db)
