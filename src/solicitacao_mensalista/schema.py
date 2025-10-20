import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError
from validate_docbr import CPF

from .model import StatusSolicitacao


class SolicitacaoMensalistaBase(BaseModel):
    nome_completo: str = Field(..., min_length=1)
    email: EmailStr
    cpf: str = Field(..., min_length=1)
    rg: str = Field(..., min_length=1)
    telefone: Optional[str] = None  # Define o campo como opcional
    placa_veiculo: str
    plano_id: int

    @field_validator("cpf")
    def validate_cpf(cls, v):
        if not v:
            return v
        cpf_validator = CPF()
        if not cpf_validator.validate(v):
            raise PydanticCustomError("value_error", "CPF inválido.")
        return v

    @field_validator("placa_veiculo")
    def validate_placa(cls, v):
        padrao_placa = r"^[A-Z]{3}-?\d[A-Z0-9]\d{2}$"
        if not re.match(padrao_placa, v.upper()):
            raise PydanticCustomError(
                "value_error", "Formato de placa de veículo inválido."
            )
        return v.upper()


class SolicitacaoMensalistaCreate(SolicitacaoMensalistaBase):
    pass


class SolicitacaoMensalistaUpdate(BaseModel):
    status: StatusSolicitacao


class SolicitacaoMensalista(SolicitacaoMensalistaBase):
    id: int
    status: StatusSolicitacao
    path_doc_pessoal: str
    path_doc_comprovante: str

    model_config = ConfigDict(from_attributes=True)
