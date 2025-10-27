from unittest.mock import MagicMock

from src.tipo_veiculo import repository
from src.tipo_veiculo.schema import TipoVeiculoCreate


def test_create_tipo_veiculo_tarifa_valida():
    tipo_veiculo_valido = TipoVeiculoCreate(nome="Carro", tarifa_hora=15.0)
    db_mock = MagicMock()

    repository.create_tipo_veiculo(db=db_mock, tipo_veiculo=tipo_veiculo_valido)
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()
