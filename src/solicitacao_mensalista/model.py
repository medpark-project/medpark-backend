import enum

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)

from src.db.session import Base


class StatusSolicitacao(str, enum.Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"


class SolicitacaoMensalista(Base):
    __tablename__ = "solicitacoes_mensalista"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    rg = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    placa_veiculo = Column(String, nullable=False)
    path_doc_pessoal = Column(String, nullable=False)
    path_doc_comprovante = Column(String, nullable=False)

    status = Column(
        SQLAlchemyEnum(StatusSolicitacao),
        nullable=False,
        default=StatusSolicitacao.PENDENTE,
    )

    plano_id = Column(Integer, ForeignKey("planos_mensalista.id"), nullable=False)
