from app.crud import productos
from fastapi import APIRouter, Depends
from typing import List, Optional
from app.core.auth import get_current_user
from app.models import Usuario
from app.database.db import get_db
from sqlalchemy.orm import Session
from app.schemas.producto import ProductoResponse


router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=List[ProductoResponse])
def get_notas_venta(
    skip: int = 0,
    limit: int = 400,
    sku: Optional[str] = None,
    producto: Optional[str] = None,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    notas = productos.get_productos_filtro(
        db, 
        skip=skip, 
        limit=limit,
        sku=sku,
        producto=producto,
        categoria=categoria,
    )
    
    return notas or []