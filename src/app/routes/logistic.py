from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.logistic import MovimientoCreate
from app.models import Movimientos

router = APIRouter()

@router.post("/movimientos")
def crear_movimiento(movimiento: MovimientoCreate, db: Session = Depends(get_db)):
    nuevo_movimiento = Movimientos(**movimiento.model_dump())
    db.add(nuevo_movimiento)
    db.commit()
    db.refresh(nuevo_movimiento)
    return nuevo_movimiento
