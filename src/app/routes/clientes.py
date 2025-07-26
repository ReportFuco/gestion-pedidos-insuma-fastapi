from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.crud import clientes
from app.schemas.clientes import Cliente, ClienteCreate

from app.database.models import Usuario
from app.core.auth import get_current_user

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=List[Cliente])
def listar_clientes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
    ):

    return clientes.get_clientes(db, skip, limit)

@router.get("/{cliente_id}", response_model=Cliente)
def obtener_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
    ):
    
    db_cliente = clientes.get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.post("/", response_model=Cliente)
def crear_cliente(
    cliente: ClienteCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
    ):
    
    return clientes.create_cliente(db, cliente)