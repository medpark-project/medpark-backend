from unittest.mock import MagicMock

import pytest

from src.tipo_veiculo import repository
from src.tipo_veiculo.schema import TipoVeiculoCreate, TipoVeiculoUpdate


def test_create_tipo_veiculo_tarifa_negativa():
    tipo_veiculo_negativo = TipoVeiculoCreate(nome="Barco", tarifa_hora=-10.0)

    db_mock = MagicMock()

    with pytest.raises(ValueError, match="A tarifa por hora não pode ser negativa."):
        repository.create_tipo_veiculo(db=db_mock, tipo_veiculo=tipo_veiculo_negativo)


def test_create_tipo_veiculo_tarifa_valida():
    tipo_veiculo_valido = TipoVeiculoCreate(nome="Carro", tarifa_hora=15.0)
    db_mock = MagicMock()

    repository.create_tipo_veiculo(db=db_mock, tipo_veiculo=tipo_veiculo_valido)
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()


def test_update_tipo_veiculo_tarifa_negativa():
    tipo_veiculo_update_negativo = TipoVeiculoUpdate(tarifa_hora=-1.0)
    db_mock = MagicMock()
    # objeto fake que veio do bd fake
    db_tipo_veiculo_mock = MagicMock()

    with pytest.raises(ValueError, match="A tarifa por hora não pode ser negativa."):
        repository.update_tipo_veiculo(
            db=db_mock,
            db_tipo_veiculo=db_tipo_veiculo_mock,
            tipo_veiculo=tipo_veiculo_update_negativo,
        )
