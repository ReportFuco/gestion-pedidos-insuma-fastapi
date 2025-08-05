from pydantic import BaseModel
from typing import Optional

# Estos son productos-notas
class ProductoBase(BaseModel):
    id_obuma:int
    item: str
    cantidad:int
    subtotal:int

    class Config:
        from_attributes = True

# Estos son productos-notas
class ProductoShema(BaseModel):
    sku: str
    producto:str
    precio: int
    categoria: str
    subcategoria:str
    fabricante:str
    tipo_producto:str
    imagen:str

class ProductosBase(BaseModel):
    sku: str
    producto: str
    precio: int
    categoria: str
    subcategoria: Optional[str] = None
    fabricante: Optional[str] = None
    tipo_producto: Optional[str] = None
    imagen: Optional[str] = None

class ProductosCreate(ProductosBase):
    pass

class ProductosUpdate(BaseModel):
    sku: Optional[str] = None
    producto: Optional[str] = None
    precio: Optional[int] = None
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    fabricante: Optional[str] = None
    tipo_producto: Optional[str] = None
    imagen: Optional[str] = None

class ProductoResponse(BaseModel):
    id: int
    sku: str
    producto: str
    precio: int
    categoria: str
    subcategoria: Optional[str] = None
    fabricante: Optional[str] = None
    tipo_producto: Optional[str] = None
    imagen: Optional[str] = None

    class Config:
        orm_mode = True