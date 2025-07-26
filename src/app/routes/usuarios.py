from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Usuario
from app.schemas.token import UsuarioCreate
from app.core.auth import get_password_hash

router = APIRouter()

@router.post("/usuarios", status_code=201)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if existente:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    nuevo_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        nombre_completo=usuario.nombre_completo,
        password=get_password_hash(usuario.password),
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"msg": "Usuario creado exitosamente", "id": nuevo_usuario.id}
