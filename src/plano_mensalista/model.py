from sqlalchemy import Column, Integer, String, Float
from src.db.session import Base


class PlanoMensalista(Base):
    __tablename__ = "planos_mensalista"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, unique=True, nullable=False)
    preco_mensal = Column(Float, nullable=False)
    descricao = Column(String, nullable=False)
