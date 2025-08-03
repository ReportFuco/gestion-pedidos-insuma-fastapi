
from sqlalchemy.orm import Session
from app.models import Clientes
from app.schemas.clientes import ClienteCreate

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Clientes).offset(skip).limit(limit).all()

def get_cliente(db: Session, cliente_id: int):
    return db.query(Clientes).filter(Clientes.id_cliente == cliente_id).first()

def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Clientes(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

