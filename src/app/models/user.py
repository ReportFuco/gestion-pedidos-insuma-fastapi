from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.db import Base


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