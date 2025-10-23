from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from pydantic_core import PydanticCustomError
from validate_docbr import CPF


class MensalistaBase(BaseModel):
    nome_completo: str
    email: EmailStr
    cpf: str
    rg: str
    telefone: Optional[str] = None
    path_doc_pessoal: str
    path_doc_comprovante: str

    @field_validator("cpf")
    def validate_cpf(cls, v):
        if not v:
            return v
        cpf_validator = CPF()
        if not cpf_validator.validate(v):
            raise PydanticCustomError("value_error", "CPF inválido.")
        return v


class MensalistaCreate(MensalistaBase):
    pass


class MensalistaUpdate(BaseModel):
    nome_completo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None


class Mensalista(MensalistaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
