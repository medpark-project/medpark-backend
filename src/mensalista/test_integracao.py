import pytest
from validate_docbr import CPF

cpf_generator = CPF()


def test_create_mensalista_success(authenticated_client):
    mensalista_data = {
        "nome_completo": "João da Silva",
        "email": "joao.silva@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "123456789",
        "telefone": "11999998888",
        "path_doc_pessoal": "/uploads/docs/doc1.pdf",
        "path_doc_comprovante": "/uploads/docs/comprov1.pdf",
    }
    response = authenticated_client.post("/mensalistas/", json=mensalista_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == mensalista_data["email"]
    assert "id" in data


def test_create_mensalista_duplicate_email_fails(authenticated_client):
    mensalista_data = {
        "nome_completo": "Maria Oliveira",
        "email": "maria.oliveira@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "987654321",
        "path_doc_pessoal": "/uploads/docs/doc2.pdf",
        "path_doc_comprovante": "/uploads/docs/comprov2.pdf",
    }

    response1 = authenticated_client.post("/mensalistas/", json=mensalista_data)
    assert response1.status_code == 201

    mensalista_data["cpf"] = cpf_generator.generate()
    response2 = authenticated_client.post("/mensalistas/", json=mensalista_data)
    assert response2.status_code == 400
    assert "E-mail já cadastrado" in response2.json()["detail"]


@pytest.mark.parametrize(
    "missing_field",
    ["nome_completo", "email", "cpf", "rg", "path_doc_pessoal", "path_doc_comprovante"],
)
def test_create_mensalista_missing_field_fails(authenticated_client, missing_field):
    mensalista_data = {
        "nome_completo": "Incompleto",
        "email": "incompleto@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "123",
        "path_doc_pessoal": "/uploads/doc.pdf",
        "path_doc_comprovante": "/uploads/comprov.pdf",
    }

    del mensalista_data[missing_field]

    response = authenticated_client.post("/mensalistas/", json=mensalista_data)
    assert response.status_code == 422


def test_read_all_mensalistas(authenticated_client):
    authenticated_client.post(
        "/mensalistas/",
        json={
            "nome_completo": "User 1",
            "email": "user1@teste.com",
            "cpf": cpf_generator.generate(),
            "rg": "1",
            "path_doc_pessoal": "a",
            "path_doc_comprovante": "b",
        },
    )
    authenticated_client.post(
        "/mensalistas/",
        json={
            "nome_completo": "User 2",
            "email": "user2@teste.com",
            "cpf": cpf_generator.generate(),
            "rg": "2",
            "path_doc_pessoal": "c",
            "path_doc_comprovante": "d",
        },
    )

    response = authenticated_client.get("/mensalistas/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_read_one_mensalista_success(authenticated_client):
    mensalista_data = {
        "nome_completo": "Busca Teste",
        "email": "busca@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "1234",
        "path_doc_pessoal": "a",
        "path_doc_comprovante": "b",
    }
    response_create = authenticated_client.post("/mensalistas/", json=mensalista_data)
    created_id = response_create.json()["id"]

    response_read = authenticated_client.get(f"/mensalistas/{created_id}")
    assert response_read.status_code == 200
    data = response_read.json()
    assert data["id"] == created_id
    assert data["email"] == mensalista_data["email"]


def test_read_one_mensalista_not_found(authenticated_client):
    response = authenticated_client.get("/mensalistas/9999")
    assert response.status_code == 404


def test_update_mensalista_success(authenticated_client):
    mensalista_data = {
        "nome_completo": "Nome Original",
        "email": "original@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "123",
        "path_doc_pessoal": "a",
        "path_doc_comprovante": "b",
    }
    response_create = authenticated_client.post("/mensalistas/", json=mensalista_data)
    created_id = response_create.json()["id"]

    update_data = {"nome_completo": "Nome Atualizado", "telefone": "11987654321"}
    response_update = authenticated_client.put(
        f"/mensalistas/{created_id}", json=update_data
    )
    assert response_update.status_code == 200
    data = response_update.json()
    assert data["nome_completo"] == "Nome Atualizado"
    assert data["telefone"] == "11987654321"


def test_update_mensalista_not_found(authenticated_client):
    response = authenticated_client.put(
        "/mensalistas/9999", json={"nome_completo": "Fantasma"}
    )
    assert response.status_code == 404


def test_delete_mensalista_success(authenticated_client):
    mensalista_data = {
        "nome_completo": "Para Deletar",
        "email": "deletar@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "456",
        "path_doc_pessoal": "a",
        "path_doc_comprovante": "b",
    }
    response_create = authenticated_client.post("/mensalistas/", json=mensalista_data)
    created_id = response_create.json()["id"]

    response_delete = authenticated_client.delete(f"/mensalistas/{created_id}")
    assert response_delete.status_code == 200

    response_read = authenticated_client.get(f"/mensalistas/{created_id}")
    assert response_read.status_code == 404


def test_delete_mensalista_not_found(authenticated_client):
    """Testa a deleção de um mensalista com um ID que não existe."""
    response = authenticated_client.delete("/mensalistas/9999")
    assert response.status_code == 404
