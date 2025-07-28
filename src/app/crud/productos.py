from sqlalchemy.orm import Session
from app.database.models import ProductosNotas
from app.schemas.producto import ProductoBase
import pandas as pd


def get_productos_id(db:Session, skip:int = 0):
    query = db.query(ProductosNotas.id_obuma).all()

    return [r[0] for r in query]


def insert_productos(db: Session, df_productos):
    for _, row in df_productos.iterrows():
        producto_data = ProductoBase(**row.to_dict())
        db_producto = ProductosNotas(**producto_data.model_dump())
        db.add(db_producto)
    db.commit()