from typing import Optional

from pydantic import BaseModel, ConfigDict


class PlanoMensalistaBase(BaseModel):
    nome: str
    preco_mensal: float
    descricao: str


class PlanoMensalistaCreate(PlanoMensalistaBase):
    pass


class PlanoMensalistaUpdate(PlanoMensalistaBase):
    nome: Optional[str] = None
    preco_mensal: Optional[float] = None
    descricao: Optional[str] = None


class PlanoMensalista(PlanoMensalistaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
