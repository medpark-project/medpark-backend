import pytest
from unittest.mock import MagicMock
from src.plano_mensalista.repository import create_plano
from src.plano_mensalista.schema import PlanoMensalistaCreate


def test_create_plano_com_preco_negativo():
    plano_negativo = PlanoMensalistaCreate(
        nome="Plano Inválido", preco_mensal=-50.0, descricao="Preço negativo uhul :)"
    )
    db_mock = MagicMock()

    with pytest.raises(ValueError, match="O preço mensal não pode ser negativo."):
        create_plano(db=db_mock, plano_mensalista=plano_negativo)
