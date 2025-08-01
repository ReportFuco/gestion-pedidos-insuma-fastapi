from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from typing import List


class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    telefono: str
    password: str
    nombre_completo: str | None = None
    roles_ids: List[int]


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    telefono: str | None = None
    roles: List[str] = []

class LoginForm(BaseModel):
    username: str
    password: str
