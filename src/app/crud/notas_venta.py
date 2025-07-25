from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.models import NotasVenta
from sqlalchemy import and_, or_
from typing import Optional

def get_notas_ventas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(NotasVenta).offset(skip).limit(limit).all()


def get_notas_filtradas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    folio: Optional[int] = None,
    vendedor: Optional[str] = None,
    estado: Optional[str] = None
):
    query = db.query(NotasVenta)
    
    # Aplicar filtros si están presentes
    filters = []
    if folio is not None:
        filters.append(NotasVenta.folio == folio)
    if vendedor is not None:
        filters.append(NotasVenta.vendedor.ilike(f"%{vendedor}%"))
    if estado is not None:
        filters.append(NotasVenta.estado == estado)
    
    if filters:
        query = query.filter(and_(*filters))
    
    return query.offset(skip).limit(limit).all()

def sincronizar_notas_venta(df, db: Session):
    try:
        # 1. Deshabilitar verificación de claves foráneas (SOLO DESARROLLO)
        db.execute(text("SET session_replication_role = 'replica';"))
        
        nuevas = 0
        actualizadas = 0
        
        for _, row in df.iterrows():
            folio = row["folio"]
            estado_nuevo = row["estado"]
            
            data = row.to_dict()
            
            nota = db.query(NotasVenta).filter_by(folio=folio).first()
            
            if nota is None:
                try:
                    # Insertar nueva nota
                    nota = NotasVenta(
                        folio=data['folio'],
                        fecha=data['fecha'],
                        cliente_id=data['cliente_id'],
                        cliente_rs=data['cliente_rs'],
                        vendedor=data['vendedor'],
                        sucursal=data['sucursal'],
                        neto=data['neto'],
                        estado=data['estado'],
                        obuma_id=data['obuma_id']
                    )
                    db.add(nota)
                    nuevas += 1
                except Exception as e:
                    print(f"Error al insertar folio {folio}: {str(e)}")
                    db.rollback()
                    continue
                    
            elif nota.estado != estado_nuevo:
                try:
                    # Actualizar solo el estado
                    nota.estado = estado_nuevo
                    actualizadas += 1
                except Exception as e:
                    print(f"Error al actualizar folio {folio}: {str(e)}")
                    db.rollback()
                    continue
        
        # 2. Volver a habilitar las restricciones antes del commit
        db.execute(text("SET session_replication_role = 'origin';"))
        db.commit()
        print(f"✅ Nuevas: {nuevas} | Actualizadas: {actualizadas}")
        
    except Exception as e:
        db.rollback()
        print(f"Error en commit: {str(e)}")
        raise  # Re-lanza la excepción para manejo superior
    finally:
        # 3. Asegurarse de que las restricciones se reestablezcan incluso si hay error
        db.execute(text("SET session_replication_role = 'origin';"))