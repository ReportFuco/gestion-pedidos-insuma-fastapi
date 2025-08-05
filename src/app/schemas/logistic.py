from pydantic import BaseModel
from datetime import datetime
from app.models import TipoMovimiento


class Movimientos(BaseModel):
    id:int
    nombre:str
    sku:str
    categoria:str
    tipo_movimiento:TipoMovimiento
    cantidad:int
    fecha_creacion: datetime
    usuario_movimiento:str

class MovimientoCreate(BaseModel):
    nombre:str
    sku:str
    categoria:str
    tipo_movimiento:TipoMovimiento
    cantidad:int
    usuario_movimiento:str