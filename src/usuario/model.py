from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from src.db.session import Base
import enum


class PerfilUsuario(str, enum.Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(SQLAlchemyEnum(PerfilUsuario), nullable=False)
