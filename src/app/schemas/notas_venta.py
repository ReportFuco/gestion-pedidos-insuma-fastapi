from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from enum import Enum


class EstadoNotaVentaEnum(str, Enum):
    EMITIDA = "EMITIDA"
    FACTURADA = "FACTURADA"
    ANULADA = "ANULADA"


class NotaVentaBase(BaseModel):
    folio: int = Field(..., description="Número único de folio de la nota")
    fecha: Optional[datetime] = Field(None, description="Fecha de emisión de la nota")
    cliente_id: int = Field(..., description="ID del cliente relacionado")
    vendedor: str = Field(..., max_length=100, description="Nombre del vendedor")
    sucursal: str = Field(..., max_length=100, description="Sucursal donde se emitió")
    neto: int = Field(..., ge=0, description="Monto neto de la venta")
    estado: EstadoNotaVentaEnum = Field(..., description="Estado actual de la nota")
    obuma_id: int = Field(..., description="ID único del sistema Obuma")


class NotaVentaCreate(NotaVentaBase):
    pass


class ProductoNotaSimple(BaseModel):
    id: int
    item: str
    cantidad: int

    model_config = ConfigDict(from_attributes=True)


class NotaVentaResponse(NotaVentaBase):
    id: int
    productos: List[ProductoNotaSimple] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class NotaVentaUpdate(BaseModel):
    fecha: Optional[datetime] = None
    estado: Optional[EstadoNotaVentaEnum] = None
    neto: Optional[int] = Field(None, ge=0)

    model_config = ConfigDict(from_attributes=True)
