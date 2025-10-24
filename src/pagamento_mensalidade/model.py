import enum

from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship

from src.db.session import Base


class StatusPagamento(str, enum.Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ATRASADO = "ATRASADO"
    CANCELADO = "CANCELADO"


class PagamentoMensalidade(Base):
    __tablename__ = "pagamentos_mensalidade"

    id = Column(Integer, primary_key=True, index=True)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    valor_pago = Column(Float, nullable=True)
    mes_referencia = Column(Integer, nullable=False)
    status = Column(
        SQLAlchemyEnum(StatusPagamento),
        nullable=False,
        default=StatusPagamento.PENDENTE,
    )

    assinatura_id = Column(Integer, ForeignKey("assinaturas_plano.id"), nullable=False)

    assinatura = relationship("AssinaturaPlano", back_populates="pagamentos")
