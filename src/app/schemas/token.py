from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from enum import Enum


class RolEnum(str, Enum):
    admin = "admin"
    produccion = "produccion"
    super_user = "super_user"

class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    nombre_completo: str | None = None
    rol: RolEnum = RolEnum.produccion

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    rol:str

class LoginForm(BaseModel):
    username: str
    password: str
