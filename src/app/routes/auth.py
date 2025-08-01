from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.auth import verify_password, create_access_token
from app.database.models import Usuario, Roles
from app.database.db import get_db
from app.schemas.token import UsuarioCreate
from app.core.auth import get_password_hash


router = APIRouter(tags=["Auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    # Extraer nombres de los roles
    roles = [rol.nombre_rol for rol in user.roles]

    access_token = create_access_token(data={
        "sub": user.username,
        "telefono": user.telefono,
        "roles": roles
    })
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=201)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Revisar si existe usuario o email
    if db.query(Usuario).filter(Usuario.username == usuario.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="El email ya está en uso")

    # Traer roles de la base de datos
    roles = db.query(Roles).filter(Roles.id.in_(usuario.roles_ids)).all()
    if len(roles) != len(usuario.roles_ids):
        raise HTTPException(status_code=400, detail="Uno o más roles no existen")

    # Crear usuario y asignar roles
    nuevo_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        telefono=usuario.telefono,
        nombre_completo=usuario.nombre_completo,
        password=get_password_hash(usuario.password),
        roles=roles
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"msg": "Usuario creado correctamente", "username": nuevo_usuario.username}

