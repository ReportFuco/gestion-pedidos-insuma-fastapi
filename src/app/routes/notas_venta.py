from app.crud import notas_venta 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.schemas.notas_venta import NotaVentaResponse
from app.database.models import Usuario
from app.core.auth import get_current_user

# Imports del WebSCraping
from scraping.scripts.productos import scrapear_productos_notas
from scraping.scripts.scraper import ScrapingObuma as so
from scraping.config.config import OBUMA_CONFIG, OBUMA_TIKETS
import asyncio


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

@router.get("/scraping-front")
def obtener_nuevas_notas(
    db:Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):

    data = so(**OBUMA_CONFIG)
    df = data.extraer_datos()

    if not df.empty:

        try:
            notas_venta.sincronizar_notas_venta(df, db)
            notas_faltantes = asyncio.run(scrapear_productos_notas(db, OBUMA_TIKETS))

            return {"notas nuevas":"".join(notas_faltantes)}
    
        finally:
            db.close()
    else:
        return {"error": "No se obtuvo información"}


@router.put("/cambiar-estado")
def actualizar_estado_nota(cambio:notas_venta.CambioNota, db:Session = Depends(get_db)):
    nota_actualizada = notas_venta.cambiar_estado_nota(db, cambio)
    if not nota_actualizada:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return nota_actualizada