from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    id_cliente: Optional[int] = None
    rut_cliente: Optional[str] = None
    contacto_cliente: Optional[str] = None
    razon_social_cliente: Optional[str] = None
    nombre_fantasia: Optional[str] = None
    cliente_giro_comercial: Optional[str] = None
    cliente_direccion_facturacion: Optional[str] = None
    telefono_cliente: Optional[str] = None
    cliente_mail: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True