from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Table, Enum as SQLAEnum, Boolean
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

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    nombre_completo = Column(String)
    telefono = Column(String)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    ultima_conexion = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    roles = relationship("Roles", secondary="usuario_rol", back_populates="usuarios")


rol_permiso = Table(
    "rol_permiso",
    Base.metadata,
    Column("rol_id", ForeignKey("roles.id"), primary_key=True),
    Column("permiso_id", ForeignKey("permisos.id"), primary_key=True)
)

usuario_rol = Table(
    "usuario_rol",
    Base.metadata,
    Column("usuario_id", ForeignKey("usuarios.id"), primary_key=True),
    Column("rol_id", ForeignKey("roles.id"), primary_key=True)
)

class Permisos(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)

    roles = relationship("Roles", secondary="rol_permiso", back_populates="permisos")

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=False) 
    nombre_rol = Column(String)
    area = Column(String, nullable=True)

    usuarios = relationship("Usuario", secondary="usuario_rol", back_populates="roles")
    permisos = relationship("Permisos", secondary="rol_permiso", back_populates="roles")


class Proveedores(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
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

