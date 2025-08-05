from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import Movimientos as MovimientosModel, Usuario
from app.schemas.logistic import MovimientoCreate, Movimientos as MovimientosSchema
from app.crud.logistic import get_movimientos
from app.core.auth import get_current_user
from typing import List


router = APIRouter(prefix="/logistica", tags=["Logística"])

@router.post("/movimientos")
def crear_movimiento(
    movimiento: MovimientoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
    ):
    try:
        nuevo_movimiento = MovimientosModel(**movimiento.model_dump())
        db.add(nuevo_movimiento)
        db.commit()
        db.refresh(nuevo_movimiento)
        return nuevo_movimiento
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/movimientos", response_model=List[MovimientosSchema])
def obtener_movimientos(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 100, 
    current_user: Usuario = Depends(get_current_user)
    ):
    try:
        return get_movimientos(db, limit=limit, skip=skip)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
