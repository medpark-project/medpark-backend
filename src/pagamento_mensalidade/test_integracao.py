from datetime import date, timedelta

import pytest
from validate_docbr import CPF

cpf_generator = CPF()


@pytest.fixture
def setup_assinatura(authenticated_client):
    mensalista_res = authenticated_client.post(
        "/mensalistas/",
        json={
            "nome_completo": "Cliente Pagamento Teste",
            "email": "pagamento@teste.com",
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
            "nome": "Plano para Pagamento",
            "preco_mensal": 250.0,
            "descricao": "Teste Pagamento",
        },
    )
    assert plano_res.status_code == 201
    plano_id = plano_res.json()["id"]

    assinatura_res = authenticated_client.post(
        "/assinaturas/",
        json={
            "mensalista_id": mensalista_id,
            "plano_id": plano_id,
            "data_inicio": date.today().isoformat(),
        },
    )
    assert assinatura_res.status_code == 201
    return assinatura_res.json()["id"]


def test_create_pagamento_success(authenticated_client, setup_assinatura):
    assinatura_id = setup_assinatura
    pagamento_data = {
        "assinatura_id": assinatura_id,
        "data_vencimento": (date.today() + timedelta(days=10)).isoformat(),
        "mes_referencia": 202510,
    }
    response = authenticated_client.post("/pagamentos/", json=pagamento_data)
    assert response.status_code == 201
    data = response.json()
    assert data["assinatura_id"] == assinatura_id
    assert data["status"] == "PENDENTE"


def test_create_pagamento_com_assinatura_invalida_falha(authenticated_client):
    pagamento_data = {
        "assinatura_id": 9999,
        "data_vencimento": date.today().isoformat(),
        "mes_referencia": 202511,
    }
    response = authenticated_client.post("/pagamentos/", json=pagamento_data)
    assert response.status_code == 404
    assert "Assinatura não encontrada" in response.json()["detail"]


def test_pagamento_lifecycle_flow(authenticated_client, setup_assinatura):
    assinatura_id = setup_assinatura

    authenticated_client.post(
        "/pagamentos/",
        json={
            "assinatura_id": assinatura_id,
            "data_vencimento": date(2025, 10, 5).isoformat(),
            "mes_referencia": 202510,
        },
    )
    response_create2 = authenticated_client.post(
        "/pagamentos/",
        json={
            "assinatura_id": assinatura_id,
            "data_vencimento": date(2025, 11, 5).isoformat(),
            "mes_referencia": 202511,
        },
    )
    pagamento_a_ser_pago_id = response_create2.json()["id"]

    response_read = authenticated_client.get(f"/pagamentos/assinatura/{assinatura_id}")
    assert response_read.status_code == 200
    historico = response_read.json()
    assert isinstance(historico, list)
    assert len(historico) == 2

    update_data = {
        "status": "PAGO",
        "data_pagamento": date.today().isoformat(),
        "valor_pago": 250.0,
    }
    response_update = authenticated_client.put(
        f"/pagamentos/{pagamento_a_ser_pago_id}", json=update_data
    )
    assert response_update.status_code == 200
    data_atualizada = response_update.json()
    assert data_atualizada["status"] == "PAGO"
    assert data_atualizada["valor_pago"] == 250.0

    response_update_fail = authenticated_client.put(
        "/pagamentos/9999", json=update_data
    )
    assert response_update_fail.status_code == 404
