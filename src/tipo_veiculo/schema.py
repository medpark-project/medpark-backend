# biblioteca que fastapi usa para criar schemas
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TipoVeiculoBase(BaseModel):
    nome: str
    tarifa_hora: float


class TipoVeiculoCreate(TipoVeiculoBase):
    pass


class TipoVeiculoUpdate(TipoVeiculoBase):
    nome: Optional[str] = None
    tarifa_hora: Optional[float] = None
    pass


class TipoVeiculo(TipoVeiculoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
