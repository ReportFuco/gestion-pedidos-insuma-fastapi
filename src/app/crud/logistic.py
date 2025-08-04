from sqlalchemy.orm import Session
from app.models import Movimientos


def get_movimientos(db:Session, skip:int = 0, limit:int=100):
    return db.query(Movimientos).offset(skip).limit(limit).all()

    