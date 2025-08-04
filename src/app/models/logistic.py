from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAEnum, func
from enum import Enum as PyEnum
from app.database.db import Base

class TipoMovimiento(PyEnum):
    entrada = "Entrada"
    salida = "Salida"
    devolucion = "Devolución"
    ajuste = "Ajuste"

class Movimientos(Base):
    __tablename__ = 'movimientos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    tipo_movimiento = Column(SQLAEnum(TipoMovimiento, name="tipomovimiento"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())
    usuario_movimiento = Column(String, nullable=False)