from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False)
    producto = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    categoria = Column(String, nullable=False)
    subcategoria = Column(String, nullable=True)
    fabricante = Column(String, nullable=True)
    tipo_producto = Column(String, nullable=True)
    imagen = Column(String, nullable=True)  

    def __repr__(self):
        return f"<Producto(sku='{self.sku}', producto='{self.producto}', precio={self.precio})>"