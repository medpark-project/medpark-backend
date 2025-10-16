from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from src.usuario.model import PerfilUsuario


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    perfil: PerfilUsuario


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    perfil: Optional[PerfilUsuario] = None


class Usuario(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
