# src/registro_estacionamento/model.py

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.session import Base


class RegistroEstacionamento(Base):
    __tablename__ = "registros_estacionamento"

    id = Column(Integer, primary_key=True, index=True)
    hora_entrada = Column(DateTime, nullable=False)
    hora_saida = Column(DateTime, nullable=True)
    valor_pago = Column(Float, nullable=True)

    veiculo_placa = Column(String, ForeignKey("veiculos.placa"), nullable=False)

    veiculo = relationship("Veiculo")
