from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .model import StatusPagamento


class PagamentoMensalidadeBase(BaseModel):
    data_vencimento: date
    data_pagamento: Optional[date] = None
    valor_pago: Optional[float] = None
    mes_referencia: int
    status: StatusPagamento
    assinatura_id: int


class PagamentoMensalidadeCreate(BaseModel):
    assinatura_id: int
    data_vencimento: date
    mes_referencia: int


class PagamentoMensalidadeUpdate(BaseModel):
    status: Optional[StatusPagamento] = None
    data_pagamento: Optional[date] = None
    valor_pago: Optional[float] = None


class PagamentoMensalidade(PagamentoMensalidadeBase):
    id: int
    valor_cobranca: float
    model_config = ConfigDict(from_attributes=True)
