from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import Usuario
from app.schemas.token import TokenData
from datetime import timedelta, timezone
from typing import List

access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user_roles_permisos(user: Usuario):
    roles = [rol.nombre_rol for rol in user.roles]
    permisos_set = set()

    for rol in user.roles:
        for permiso in rol.permisos:
            permisos_set.add(permiso.nombre)  # usar el nombre único del permiso

    return roles, list(permisos_set)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        telefono: str = payload.get("telefono")
        roles: List[str] = payload.get("roles", [])
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, telefono=telefono, roles=roles)
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
