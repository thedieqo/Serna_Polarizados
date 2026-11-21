from fastapi import APIRouter, Depends
from app.core.auth import get_current_identity
router=APIRouter()
@router.get('/mi-trabajo')
def mi_trabajo(identity=Depends(get_current_identity)):
    # Sin asociación confirmada, no inferir trabajador por nombre ni por el perfil elegido.
    return {'asignado':False,'mensaje':'Tu cuenta todavía no tiene un instalador asignado. Solicita la asignación a Gerencia.','trabajos':[]}
