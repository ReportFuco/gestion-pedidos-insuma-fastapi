from sqlalchemy.orm import Session
from app.models import ProductosNotas, Producto as ProductoModel
from app.schemas.producto import ProductoBase
from sqlalchemy import and_


def get_productos_filtro(
    db: Session,
    skip: int = 0,
    limit: int = 400,
    sku: str = None,
    producto: str = None,
    categoria: str = None
):
    
    query = db.query(ProductoModel)
    
    # Aplicar filtros solo si los parámetros no son None
    filters = []
    if sku is not None:
        filters.append(ProductoModel.sku.ilike(f"%{sku}%"))
    if producto is not None:
        filters.append(ProductoModel.producto.ilike(f"%{producto}%"))
    if categoria is not None:
        filters.append(ProductoModel.categoria.ilike(f"%{categoria}%"))
    
    if filters:
        query = query.filter(and_(*filters))
    
    return query.offset(skip).limit(limit).all()

def get_productos_id(db:Session, skip:int = 0):
    query = db.query(ProductosNotas.id_obuma).all()

    return [r[0] for r in query]


def insert_productos(db: Session, df_productos):
    for _, row in df_productos.iterrows():
        producto_data = ProductoBase(**row.to_dict())
        db_producto = ProductosNotas(**producto_data.model_dump())
        db.add(db_producto)
    db.commit()