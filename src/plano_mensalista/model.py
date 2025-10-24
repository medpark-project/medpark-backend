from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from src.db.session import Base


class PlanoMensalista(Base):
    __tablename__ = "planos_mensalista"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, unique=True, nullable=False)
    preco_mensal = Column(Float, nullable=False)
    descricao = Column(String, nullable=False)
    assinaturas = relationship("AssinaturaPlano", back_populates="plano")
