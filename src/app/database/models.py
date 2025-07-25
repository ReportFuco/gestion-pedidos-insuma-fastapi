from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Enum as SQLAEnum, Boolean
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLAEnum

from app.database.db import Base


class EstadoNotaVenta(PyEnum):
    EMITIDA = 'EMITIDA'
    FACTURADA = 'FACTURADA'
    ANULADA = 'ANULADA'


class Proveedores(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True)
    rut = Column(Integer, unique=True)
    razon_social = Column(String, unique=True, nullable=False)
    direccion_proveedor = Column(String, nullable=False)
    celular_proveedor = Column(String, nullable=False)
    nombre_contacto = Column(String, nullable=False)


class Clientes(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, unique=True)
    rut_cliente = Column(String, unique=True)
    contacto_cliente = Column(String)
    razon_social_cliente = Column(String)
    nombre_fantasia = Column(String)
    cliente_giro_comercial = Column(String)
    cliente_direccion_facturacion = Column(String)
    telefono_cliente = Column(String)
    cliente_mail = Column(String)
    fecha_registro = Column(DateTime, default=datetime.utcnow)


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

class ProductosNotas(Base):
    __tablename__ = "productos_notas"

    id = Column(Integer, primary_key=True)
    id_obuma = Column(BigInteger, nullable=False)
    item = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
