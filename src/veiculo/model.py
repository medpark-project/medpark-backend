from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.db.session import Base


class Veiculo(Base):
    __tablename__ = "veiculos"

    placa = Column(String, primary_key=True, index=True)
    modelo = Column(String, nullable=True)
    cor = Column(String, nullable=True)

    mensalista_id = Column(Integer, ForeignKey("mensalistas.id"), nullable=True)

    tipo_veiculo_id = Column(Integer, ForeignKey("tipos_veiculo.id"), nullable=False)

    dono = relationship("Mensalista", back_populates="veiculo")

    tipo = relationship("TipoVeiculo", back_populates="veiculos")
