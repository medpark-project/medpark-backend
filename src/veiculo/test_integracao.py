import pytest
from validate_docbr import CPF

cpf_generator = CPF()


def test_create_veiculo_success(authenticated_client):
    tipo_veiculo_res = authenticated_client.post(
        "/tipos-veiculo/", json={"nome": "Automóvel", "tarifa_hora": 15.0}
    )
    tipo_veiculo_id = tipo_veiculo_res.json()["id"]

    mensalista_res = authenticated_client.post(
        "/mensalistas/",
        json={
            "nome_completo": "Dono do Carro",
            "email": "dono@carro.com",
            "cpf": cpf_generator.generate(),
            "rg": "123",
            "path_doc_pessoal": "a",
            "path_doc_comprovante": "b",
        },
    )
    mensalista_id = mensalista_res.json()["id"]

    veiculo_data = {
        "placa": "XYZ-1234",
        "modelo": "Fusca",
        "cor": "Azul",
        "tipo_veiculo_id": tipo_veiculo_id,
        "mensalista_id": mensalista_id,
    }
    response = authenticated_client.post("/veiculos/", json=veiculo_data)

    assert response.status_code == 201
    data = response.json()
    assert data["placa"] == veiculo_data["placa"]
    assert data["mensalista_id"] == mensalista_id


@pytest.mark.parametrize(
    "field, value, status_code, detail",
    [
        ("mensalista_id", 999, 404, "Mensalista não encontrado."),
        ("tipo_veiculo_id", 999, 404, "Tipo de Veículo não encontrado."),
        ("placa", "INVALIDA", 422, "Formato de placa de veículo inválido."),
    ],
)
def test_create_veiculo_validation_fails(
    authenticated_client, field, value, status_code, detail
):
    tipo_veiculo_res = authenticated_client.post(
        "/tipos-veiculo/", json={"nome": "Automóvel 2", "tarifa_hora": 15.0}
    )
    mensalista_res = authenticated_client.post(
        "/mensalistas/",
        json={
            "nome_completo": "Dono 2",
            "email": "dono2@carro.com",
            "cpf": cpf_generator.generate(),
            "rg": "123",
            "path_doc_pessoal": "a",
            "path_doc_comprovante": "b",
        },
    )

    valid_data = {
        "placa": "ABC-4321",
        "modelo": "Gol",
        "cor": "Branco",
        "tipo_veiculo_id": tipo_veiculo_res.json()["id"],
        "mensalista_id": mensalista_res.json()["id"],
    }
    valid_data[field] = value

    response = authenticated_client.post("/veiculos/", json=valid_data)

    assert response.status_code == status_code
    assert detail in response.text
