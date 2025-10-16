from sqlalchemy import Column, Float, Integer, String

from src.db.session import Base


class TipoVeiculo(Base):
    __tablename__ = "tipos_veiculo"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    tarifa_hora = Column(Float, nullable=False)
