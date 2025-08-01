from app.database.models import EstadoPedido, EstadoNotaVenta
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional


class NotaVentaBase(BaseModel):
    folio: int = Field(..., description="Número único de folio de la nota")
    fecha: Optional[datetime] = Field(None, description="Fecha de emisión de la nota")
    cliente_id: int = Field(..., description="ID del cliente relacionado")
    vendedor: str = Field(..., max_length=100, description="Nombre del vendedor")
    sucursal: str = Field(..., max_length=100, description="Sucursal donde se emitió")
    neto: int = Field(..., ge=0, description="Monto neto de la venta")
    estado: EstadoNotaVenta = Field(..., description="Estado actual de la nota")
    obuma_id: int = Field(..., description="ID único del sistema Obuma")
    estado_pedido: EstadoPedido

class CambioNota(BaseModel):
    folio: int
    estado_pedido: EstadoPedido


class ClienteSimple(BaseModel):
    id_cliente: Optional[int] = Field(..., description="ID único del cliente")
    rut_cliente: Optional[str] = Field(..., description="RUT del cliente")
    razon_social_cliente: Optional[str] = Field(..., description="Razón social del cliente")
    nombre_fantasia: Optional[str] = Field(None, description="Nombre de fantasía del cliente")
    
    model_config = ConfigDict(from_attributes=True)

class ProductoNotaSimple(BaseModel):
    id: int
    item: str
    cantidad: int
    subtotal: int

    model_config = ConfigDict(from_attributes=True)


class NotaVentaResponse(NotaVentaBase):
    id: int
    productos: List[ProductoNotaSimple] = Field(default_factory=list)
    cliente: List[ClienteSimple]
    
    model_config = ConfigDict(from_attributes=True)

