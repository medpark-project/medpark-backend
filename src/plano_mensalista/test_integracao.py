import pytest


def test_create_plano(authenticated_client):
    plano_data = {
        "nome": "Plano Básico",
        "preco_mensal": 150.0,
        "descricao": "Acesso diurno de Seg a Sex.",
    }
    response = authenticated_client.post("/planos-mensalista/", json=plano_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == plano_data["nome"]
    assert "id" in data


def test_read_all_planos(client, authenticated_client):
    authenticated_client.post(
        "/planos-mensalista/",
        json={"nome": "Plano Teste A", "preco_mensal": 100.0, "descricao": "Desc A"},
    )
    authenticated_client.post(
        "/planos-mensalista/",
        json={"nome": "Plano Teste B", "preco_mensal": 200.0, "descricao": "Desc B"},
    )

    response = client.get("/planos-mensalista/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_read_one_plano_not_found(client):
    response = client.get("/planos-mensalista/999")
    assert response.status_code == 404
    assert "Plano de Mensalista não encontrado" in response.json()["detail"]


def test_update_plano(authenticated_client):
    plano_data = {
        "nome": "Plano Original",
        "preco_mensal": 120.0,
        "descricao": "Desc Original",
    }
    response_create = authenticated_client.post("/planos-mensalista/", json=plano_data)
    created_id = response_create.json()["id"]

    update_data = {"descricao": "Nova descrição atualizada."}
    response_update = authenticated_client.put(
        f"/planos-mensalista/{created_id}", json=update_data
    )
    assert response_update.status_code == 200
    data = response_update.json()
    assert data["descricao"] == "Nova descrição atualizada."
    assert data["nome"] == "Plano Original"


def test_delete_plano(authenticated_client):
    plano_data = {
        "nome": "Plano a ser Deletado",
        "preco_mensal": 50.0,
        "descricao": "Desc Delete",
    }
    response_create = authenticated_client.post("/planos-mensalista/", json=plano_data)
    created_id = response_create.json()["id"]

    response_delete = authenticated_client.delete(f"/planos-mensalista/{created_id}")
    assert response_delete.status_code == 200

    response_read = authenticated_client.get(f"/planos-mensalista/{created_id}")
    assert response_read.status_code == 404


@pytest.mark.parametrize(
    "invalid_data, expected_status, expected_detail_substring",
    [
        ({"preco_mensal": 100.0, "descricao": "Plano sem nome"}, 422, "Field required"),
        (
            {"nome": "Plano sem preço", "descricao": "Plano sem preço"},
            422,
            "Field required",
        ),
        ({"nome": "Plano sem descrição", "preco_mensal": 100.0}, 422, "Field required"),
        (
            {
                "nome": "Plano com preço inválido",
                "preco_mensal": "cem reais",
                "descricao": "Teste",
            },
            422,
            "Input should be a valid number",
        ),
        (
            {"nome": 123, "preco_mensal": 100.0, "descricao": "Teste"},
            422,
            "Input should be a valid string",
        ),
        (
            {
                "nome": "Plano com preço negativo",
                "preco_mensal": -1.0,
                "descricao": "Teste",
            },
            422,
            "O preço mensal não pode ser negativo",
        ),
    ],
)
def test_create_plano_validation_errors(
    authenticated_client, invalid_data, expected_status, expected_detail_substring
):
    response = authenticated_client.post("/planos-mensalista/", json=invalid_data)

    assert response.status_code == expected_status
    assert expected_detail_substring in response.text


def test_update_plano_com_preco_negativo(authenticated_client):
    response_create = authenticated_client.post(
        "/planos-mensalista/",
        json={
            "nome": "Plano para Teste de Update",
            "preco_mensal": 100.0,
            "descricao": "Teste",
        },
    )
    created_id = response_create.json()["id"]

    response_update = authenticated_client.put(
        f"/planos-mensalista/{created_id}", json={"preco_mensal": -50.0}
    )

    assert response_update.status_code == 422
    assert "O preço mensal não pode ser negativo" in response_update.text
