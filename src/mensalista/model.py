from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db.session import Base


class Mensalista(Base):
    __tablename__ = "mensalistas"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    rg = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    path_doc_pessoal = Column(String, nullable=False)
    path_doc_comprovante = Column(String, nullable=False)
    veiculo = relationship("Veiculo", back_populates="dono", uselist=False)
    assinaturas = relationship("AssinaturaPlano", back_populates="mensalista")
