from io import BytesIO

import pytest
from validate_docbr import CPF

cpf_generator = CPF()


def test_create_solicitacao_success(client, authenticated_client):
    plano_response = authenticated_client.post(
        "/planos-mensalista/",
        json={
            "nome": "Plano Teste para Solicitacao",
            "preco_mensal": 100.0,
            "descricao": "Teste",
        },
    )
    plano_id = plano_response.json()["id"]

    form_data = {
        "nome_completo": "Candidato Teste",
        "email": "candidato@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "12.345.678-9",
        "placa_veiculo": "BRA2E19",
        "plano_id": plano_id,
    }
    files = {
        "doc_pessoal": ("doc.pdf", BytesIO(b"pdf content"), "application/pdf"),
        "doc_comprovante": ("comprovante.jpg", BytesIO(b"jpg content"), "image/jpeg"),
    }
    response = client.post("/solicitacoes-mensalista/", data=form_data, files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == form_data["email"]
    assert data["status"] == "PENDENTE"


@pytest.mark.parametrize(
    "campo_invalido, valor_invalido, mensagem_erro_esperada",
    [
        ("nome_completo", "", "Field required"),
        ("email", "email-invalido", "value is not a valid email address"),
        ("cpf", "12345678900", "CPF inválido."),
        ("placa_veiculo", "ABC-123", "Formato de placa de veículo inválido."),
        ("plano_id", 999, "não foi encontrado"),
    ],
)
def test_create_solicitacao_validation_errors(
    client, authenticated_client, campo_invalido, valor_invalido, mensagem_erro_esperada
):
    plano_response = authenticated_client.post(
        "/planos-mensalista/",
        json={"nome": "Plano Valido", "preco_mensal": 100.0, "descricao": "Teste"},
    )
    valid_data = {
        "nome_completo": "Candidato Válido",
        "email": "candidato@gmail.com",
        "cpf": cpf_generator.generate(),
        "rg": "11.222.333-4",
        "placa_veiculo": "VAL1D23",
        "plano_id": plano_response.json()["id"],
    }
    if valor_invalido == "":
        del valid_data[campo_invalido]
    else:
        valid_data[campo_invalido] = valor_invalido

    files = {
        "doc_pessoal": ("doc.pdf", BytesIO(b"pdf"), "application/pdf"),
        "doc_comprovante": ("comprov.jpg", BytesIO(b"jpg"), "image/jpeg"),
    }
    response = client.post("/solicitacoes-mensalista/", data=valid_data, files=files)

    error_detail = response.json()["detail"]
    if isinstance(error_detail, list):
        assert any(mensagem_erro_esperada in error["msg"] for error in error_detail)
    else:
        assert mensagem_erro_esperada in error_detail


def test_create_solicitacao_missing_files(client, authenticated_client):
    plano_response = authenticated_client.post(
        "/planos-mensalista/",
        json={
            "nome": "Plano para Teste de Arquivo",
            "preco_mensal": 100.0,
            "descricao": "Teste",
        },
    )
    form_data = {
        "nome_completo": "Candidato Sem Arquivo",
        "email": "semarquivo@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "12.345.678-9",
        "placa_veiculo": "ARQ-5678",
        "plano_id": plano_response.json()["id"],
    }
    response = client.post("/solicitacoes-mensalista/", data=form_data)
    assert response.status_code == 422
    assert "Field required" in response.text


def test_update_solicitacao_status(client, authenticated_client):
    plano_response = authenticated_client.post(
        "/planos-mensalista/",
        json={"nome": "Plano para Update", "preco_mensal": 100.0, "descricao": "Teste"},
    )
    form_data = {
        "nome_completo": "Candidato a ser Aprovado",
        "email": "aprovar@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "11.222.333-4",
        "placa_veiculo": "APR-1234",
        "plano_id": plano_response.json()["id"],
    }
    files = {
        "doc_pessoal": ("doc.pdf", BytesIO(b"pdf"), "application/pdf"),
        "doc_comprovante": ("comprov.jpg", BytesIO(b"jpg"), "image/jpeg"),
    }
    response_create = client.post(
        "/solicitacoes-mensalista/", data=form_data, files=files
    )
    assert response_create.status_code == 201, response_create.text
    created_id = response_create.json()["id"]

    update_data = {"status": "APROVADO"}
    response_update = authenticated_client.put(
        f"/solicitacoes-mensalista/{created_id}", json=update_data
    )

    assert response_update.status_code == 200
    assert response_update.json()["status"] == "APROVADO"
