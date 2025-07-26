from app.crud import notas_venta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.schemas.notas_venta import NotaVentaResponse
from app.database.models import Usuario
from app.core.auth import get_current_user


router = APIRouter(prefix="/notas-venta", tags=["Notas de venta"])

@router.get("/", response_model=List[NotaVentaResponse])
def get_notas_venta(
    skip: int = 0,
    limit: int = 100,
    folio: Optional[int] = None,
    vendedor: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    notas = notas_venta.get_notas_filtradas(
        db, 
        skip=skip, 
        limit=limit,
        folio=folio,
        vendedor=vendedor,
        estado=estado
    )
    
    if not notas:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron notas con los filtros aplicados"
        )
    return notas