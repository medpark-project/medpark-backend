# src/registro_estacionamento/schema.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RegistroEstacionamentoBase(BaseModel):
    hora_entrada: datetime
    hora_saida: Optional[datetime] = None
    valor_pago: Optional[float] = None
    veiculo_placa: str


class RegistroEstacionamentoCreate(BaseModel):
    veiculo_placa: str


class RegistroEstacionamentoUpdate(BaseModel):
    valor_pago: float


class RegistroEstacionamento(RegistroEstacionamentoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
