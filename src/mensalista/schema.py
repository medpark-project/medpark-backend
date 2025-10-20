from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class MensalistaBase(BaseModel):
    nome_completo: str
    email: EmailStr
    cpf: str
    rg: str
    telefone: Optional[str] = None
    path_doc_pessoal: str
    path_doc_comprovante: str


class MensalistaCreate(MensalistaBase):
    pass


class MensalistaUpdate(BaseModel):
    nome_completo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None


class Mensalista(MensalistaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
