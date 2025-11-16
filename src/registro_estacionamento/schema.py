from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.veiculo.schema import Veiculo


class RegistroEstacionamentoBase(BaseModel):
    hora_entrada: datetime
    hora_saida: Optional[datetime] = None
    valor_pago: Optional[float] = None
    veiculo_placa: str


class RegistroEstacionamentoCreate(BaseModel):
    veiculo_placa: str
    tipo_veiculo_id: Optional[int] = None


class RegistroEstacionamentoUpdate(BaseModel):
    valor_pago: float


class RegistroEstacionamento(RegistroEstacionamentoBase):
    id: int
    veiculo: Veiculo
    model_config = ConfigDict(from_attributes=True)
