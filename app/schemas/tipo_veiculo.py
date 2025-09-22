# biblioteca que fastapi usa para criar schemas
from pydantic import BaseModel

class TipoVeiculoBase(BaseModel):
    nome: str
    tarifa_hora: float

class TipoVeiculoCreate(TipoVeiculoBase):
    pass

class TipoVeiculo(TipoVeiculoBase):
    id: int

    class Config:
        from_attributes = True