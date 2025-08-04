from pydantic import BaseModel
from app.models import TipoMovimiento


class MovimientoCreate(BaseModel):
    nombre:str
    categoria:str
    tipo_movimiento:TipoMovimiento
    cantidad:int
    usuario_movimiento:str