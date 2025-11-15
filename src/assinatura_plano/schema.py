from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.plano_mensalista.schema import PlanoMensalista

from .model import StatusAssinatura


class AssinaturaPlanoBase(BaseModel):
    data_inicio: date
    data_fim: Optional[date] = None
    status: StatusAssinatura
    mensalista_id: int
    plano_id: int


class AssinaturaPlanoCreate(BaseModel):
    mensalista_id: int
    plano_id: int
    data_inicio: date


class AssinaturaPlanoUpdate(BaseModel):
    status: Optional[StatusAssinatura] = None
    data_fim: Optional[date] = None


class AssinaturaPlano(AssinaturaPlanoBase):
    id: int
    plano: PlanoMensalista
    model_config = ConfigDict(from_attributes=True)
