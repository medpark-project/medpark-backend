from datetime import date, timedelta

import pytest
from validate_docbr import CPF

cpf_generator = CPF()


@pytest.fixture
def setup_mensalista_e_plano(authenticated_client):
    mensalista_res = authenticated_client.post(
        "/mensalistas/",
        json={
            "nome_completo": "Cliente Assinatura Teste",
            "email": "assinatura@teste.com",
            "cpf": cpf_generator.generate(),
            "rg": "123",
            "path_doc_pessoal": "a",
            "path_doc_comprovante": "b",
        },
    )
    assert mensalista_res.status_code == 201
    mensalista_id = mensalista_res.json()["id"]

    plano_res = authenticated_client.post(
        "/planos-mensalista/",
        json={
            "nome": "Plano para Assinatura",
            "preco_mensal": 200.0,
            "descricao": "Teste Assinatura",
        },
    )
    assert plano_res.status_code == 201
    plano_id = plano_res.json()["id"]

    return {"mensalista_id": mensalista_id, "plano_id": plano_id}


def test_create_assinatura_success(authenticated_client, setup_mensalista_e_plano):
    """Testa a criação de uma assinatura com sucesso."""
    data_inicio = date.today().isoformat()
    assinatura_data = {
        "mensalista_id": setup_mensalista_e_plano["mensalista_id"],
        "plano_id": setup_mensalista_e_plano["plano_id"],
        "data_inicio": data_inicio,
    }
    response = authenticated_client.post("/assinaturas/", json=assinatura_data)
    assert response.status_code == 201
    data = response.json()
    assert data["mensalista_id"] == assinatura_data["mensalista_id"]
    assert data["status"] == "ATIVA"


@pytest.mark.parametrize(
    "get_invalid_data, expected_status, expected_detail",
    [
        (
            lambda ids: {
                "mensalista_id": 9999,
                "plano_id": ids["plano_id"],
                "data_inicio": date.today().isoformat(),
            },
            404,
            "Mensalista não encontrado",
        ),
        (
            lambda ids: {
                "mensalista_id": ids["mensalista_id"],
                "plano_id": 9999,
                "data_inicio": date.today().isoformat(),
            },
            404,
            "Plano de Mensalista não encontrado",
        ),
    ],
)
def test_create_assinatura_fk_not_found_fails(
    authenticated_client,
    setup_mensalista_e_plano,
    get_invalid_data,
    expected_status,
    expected_detail,
):
    invalid_data = get_invalid_data(setup_mensalista_e_plano)
    response = authenticated_client.post("/assinaturas/", json=invalid_data)
    assert response.status_code == expected_status
    assert expected_detail in response.json()["detail"]


def test_create_assinatura_fails_if_mensalista_already_has_active_subscription(
    authenticated_client, setup_mensalista_e_plano
):
    data_inicio = date.today().isoformat()
    assinatura_data = {
        "mensalista_id": setup_mensalista_e_plano["mensalista_id"],
        "plano_id": setup_mensalista_e_plano["plano_id"],
        "data_inicio": data_inicio,
    }

    response1 = authenticated_client.post("/assinaturas/", json=assinatura_data)
    assert response1.status_code == 201

    response2 = authenticated_client.post("/assinaturas/", json=assinatura_data)
    string = "Este mensalista já possui uma assinatura ativa"
    assert response2.status_code == 409
    assert string in response2.json()["detail"]


def test_assinatura_lifecycle_flow(authenticated_client, setup_mensalista_e_plano):
    data_inicio = date.today().isoformat()
    assinatura_data = {
        "mensalista_id": setup_mensalista_e_plano["mensalista_id"],
        "plano_id": setup_mensalista_e_plano["plano_id"],
        "data_inicio": data_inicio,
    }
    response_create = authenticated_client.post("/assinaturas/", json=assinatura_data)
    assert response_create.status_code == 201
    assinatura_id = response_create.json()["id"]

    response_read_ativa = authenticated_client.get(
        f"/assinaturas/mensalista/{assinatura_data['mensalista_id']}/ativa"
    )
    assert response_read_ativa.status_code == 200
    assert response_read_ativa.json()["id"] == assinatura_id
    assert response_read_ativa.json()["status"] == "ATIVA"

    data_fim = (date.today() + timedelta(days=30)).isoformat()
    response_update = authenticated_client.put(
        f"/assinaturas/{assinatura_id}",
        json={"status": "CANCELADA", "data_fim": data_fim},
    )
    assert response_update.status_code == 200
    assert response_update.json()["status"] == "CANCELADA"
    assert response_update.json()["data_fim"] == data_fim

    response_read_ativa_depois = authenticated_client.get(
        f"/assinaturas/mensalista/{assinatura_data['mensalista_id']}/ativa"
    )
    assert response_read_ativa_depois.status_code == 404

    response_historico = authenticated_client.get(
        f"/assinaturas/mensalista/{assinatura_data['mensalista_id']}/historico"
    )
    assert response_historico.status_code == 200
    historico = response_historico.json()
    assert len(historico) >= 1
    assert historico[0]["status"] == "CANCELADA"
