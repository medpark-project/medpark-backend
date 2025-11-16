import pytest


@pytest.fixture(autouse=True)
def setup_default_tipo_veiculo(authenticated_client):
    response = authenticated_client.get("/tipos-veiculo/1")
    if response.status_code == 404:
        authenticated_client.post(
            "/tipos-veiculo/", json={"nome": "Automóvel Padrão", "tarifa_hora": 10.0}
        )


def test_entrada_e_saida_de_veiculo_avulso_flow(authenticated_client):
    placa_veiculo_avulso = "AVU1B34"
    response_entrada = authenticated_client.post(
        "/estacionamento/entrada",
        json={"veiculo_placa": placa_veiculo_avulso, "tipo_veiculo_id": 1},
    )
    assert response_entrada.status_code == 201, response_entrada.text
    data_entrada = response_entrada.json()
    assert data_entrada["veiculo_placa"] == placa_veiculo_avulso

    response_ativos = authenticated_client.get("/estacionamento/ativos")
    veiculos_no_patio = response_ativos.json()
    assert any(v["veiculo_placa"] == placa_veiculo_avulso for v in veiculos_no_patio)

    valor_do_pagamento = 10.0
    response_saida = authenticated_client.put(
        f"/estacionamento/saida/{placa_veiculo_avulso}",
        json={"valor_pago": valor_do_pagamento},
    )
    assert response_saida.status_code == 200, response_saida.text
    data_saida = response_saida.json()
    assert data_saida["hora_saida"] is not None
    assert data_saida["valor_pago"] == valor_do_pagamento


def test_entrada_veiculo_ja_estacionado_falha(authenticated_client):
    placa = "ABC-0002"

    response1 = authenticated_client.post(
        "/estacionamento/entrada", json={"veiculo_placa": placa, "tipo_veiculo_id": 1}
    )
    assert response1.status_code == 201

    response2 = authenticated_client.post(
        "/estacionamento/entrada", json={"veiculo_placa": placa, "tipo_veiculo_id": 1}
    )
    assert response2.status_code == 409
    assert "já possui um registro de entrada ativo" in response2.json()["detail"]


def test_saida_veiculo_nao_encontrado_falha(authenticated_client):
    placa = "FNT1B34"

    response = authenticated_client.put(
        f"/estacionamento/saida/{placa}", json={"valor_pago": 10.0}
    )
    assert response.status_code == 404
    assert "Nenhum registro de entrada ativo encontrado" in response.json()["detail"]
