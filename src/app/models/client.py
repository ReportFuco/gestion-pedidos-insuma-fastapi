from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.db import Base



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