import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_core import PydanticCustomError


class VeiculoBase(BaseModel):
    placa: str
    modelo: Optional[str] = None
    cor: Optional[str] = None
    tipo_veiculo_id: int

    @field_validator("placa")  # O nome do campo foi corrigido para "placa"
    def validate_placa(cls, v):
        # Expressão regular que aceita o padrão antigo (ABC-1234) e o Mercosul (ABC1D23)
        padrao_placa = r"^[A-Z]{3}-?\d[A-Z0-9]\d{2}$"
        if not re.match(padrao_placa, v.upper()):
            raise PydanticCustomError(
                "value_error", "Formato de placa de veículo inválido."
            )
        return v.upper()


class VeiculoCreate(VeiculoBase):
    mensalista_id: Optional[int] = None


class VeiculoUpdate(BaseModel):
    modelo: Optional[str] = None
    cor: Optional[str] = None


class Veiculo(VeiculoBase):
    mensalista_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class VeiculoAssignOwner(BaseModel):
    mensalista_id: int
