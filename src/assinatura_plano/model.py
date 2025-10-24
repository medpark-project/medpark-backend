import enum

from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship

from src.db.session import Base


class StatusAssinatura(str, enum.Enum):
    ATIVA = "ATIVA"
    INATIVA = "INATIVA"
    CANCELADA = "CANCELADA"


class AssinaturaPlano(Base):
    __tablename__ = "assinaturas_plano"

    id = Column(Integer, primary_key=True, index=True)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)  # Pode não ter data de fim
    status = Column(
        SQLAlchemyEnum(StatusAssinatura), nullable=False, default=StatusAssinatura.ATIVA
    )

    mensalista_id = Column(Integer, ForeignKey("mensalistas.id"), nullable=False)
    plano_id = Column(Integer, ForeignKey("planos_mensalista.id"), nullable=False)

    mensalista = relationship("Mensalista", back_populates="assinaturas")
    plano = relationship("PlanoMensalista", back_populates="assinaturas")

    pagamentos = relationship("PagamentoMensalidade", back_populates="assinatura")
