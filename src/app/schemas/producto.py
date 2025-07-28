from pydantic import BaseModel


class ProductoBase(BaseModel):
    id_obuma:int
    item: str
    cantidad:int
    subtotal:int

    class Config:
        from_attributes = True
