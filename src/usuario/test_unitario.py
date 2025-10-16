# app/tests/unit/test_crud_usuario.py

from unittest.mock import MagicMock

import pytest

from src.usuario.repository import create_usuario
from src.usuario.schema import UsuarioCreate


def test_create_usuario_senha_curta():
    user_data = UsuarioCreate(
        nome="Teste", email="teste@email.com", perfil="OPERATOR", senha="123"
    )
    db_mock = MagicMock()

    with pytest.raises(ValueError, match="A senha deve ter no mínimo 8 caracteres."):
        create_usuario(db=db_mock, usuario=user_data)


def test_create_usuario_senha_valida(client):
    user_data = UsuarioCreate(
        nome="Teste Valido",
        email="valid@email.com",
        perfil="OPERATOR",
        senha="senha_valida_123",
    )
    db_mock = MagicMock()

    create_usuario(db=db_mock, usuario=user_data)

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()
