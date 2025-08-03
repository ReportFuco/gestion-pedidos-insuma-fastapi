from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Enum as SQLAEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLAEnum
from app.database.db import Base


class EstadoNotaVenta(PyEnum):
    EMITIDA = 'EMITIDA'
    FACTURADA = 'FACTURADA'
    ANULADA = 'ANULADA'

class EstadoPedido(PyEnum):
    pendiente = 'Pendiente'
    en_proceso = 'En proceso'
    Terminado = 'Terminado'
    entregado = 'Entregado'

class Proveedores(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rut = Column(Integer, unique=True)
    razon_social = Column(String, unique=True, nullable=False)
    direccion_proveedor = Column(String, nullable=False)
    celular_proveedor = Column(String, nullable=False)
    nombre_contacto = Column(String, nullable=False)


class Empleados(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True)
    rut_empleado = Column(String, unique=True, nullable=False)
    nombre_empleado = Column(String, nullable=False)
    apellido_empleado = Column(String, nullable=False)
    email_empleado = Column(String, unique=True)
    es_vendedor = Column(Boolean, default=False)


class NotasVenta(Base):
    __tablename__ = "notas_de_venta"

    id = Column(Integer, primary_key=True)
    folio = Column(BigInteger, nullable=False, unique=True)
    fecha = Column(DateTime, nullable=True)
    cliente_id = Column(Integer, nullable=False)
    cliente_rs = Column(String(200), nullable=False)
    vendedor = Column(String(200), nullable=False)
    sucursal = Column(String(200), nullable=False)
    neto = Column(Integer, nullable=False)
    estado = Column(SQLAEnum(EstadoNotaVenta, name='estadonotaventa'))
    obuma_id = Column(BigInteger, nullable=False, unique=True)
    estado_pedido = Column(SQLAEnum(EstadoPedido, name='estadoproducto'), default=EstadoPedido.pendiente, nullable=False)
    cliente = relationship("Clientes", primaryjoin="NotasVenta.cliente_id == foreign(Clientes.id_cliente)", viewonly=True)
    productos = relationship(
        "ProductosNotas",
        primaryjoin="NotasVenta.obuma_id == foreign(ProductosNotas.id_obuma)",
        viewonly=True
    )

class ProductosNotas(Base):
    __tablename__ = "productos_notas"

    id = Column(Integer, primary_key=True)
    id_obuma = Column(BigInteger, nullable=False)
    item = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)

