def test_create_read_tipo_veiculo(authenticated_client):
    tipo_veiculo_data = {"nome": "Motocicleta", "tarifa_hora": 3.50}

    response = authenticated_client.post("/tipos-veiculo/", json=tipo_veiculo_data)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["nome"] == tipo_veiculo_data["nome"]
    assert data["tarifa_hora"] == tipo_veiculo_data["tarifa_hora"]
    assert "id" in data

    created_id = data["id"]

    response = authenticated_client.get(f"/tipos-veiculo/{created_id}")

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["nome"] == tipo_veiculo_data["nome"]
    assert data["tarifa_hora"] == tipo_veiculo_data["tarifa_hora"]
    assert data["id"] == created_id


def test_read_all_tipos_veiculo(authenticated_client):
    # popula bd testes
    authenticated_client.post(
        "/tipos-veiculo/", json={"nome": "Moto", "tarifa_hora": 5.0}
    )
    authenticated_client.post(
        "/tipos-veiculo/", json={"nome": "Carro", "tarifa_hora": 6.50}
    )

    # requisição rota principal
    response = authenticated_client.get("/tipos-veiculo")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_update_tipo_veiculo(authenticated_client):
    response_create = authenticated_client.post(
        "/tipos-veiculo/", json={"nome": "Van", "tarifa_hora": 10.30}
    )
    created_id = response_create.json()["id"]
    update_data = {"nome": "Van Escolar", "tarifa_hora": 15.25}

    response_update = authenticated_client.put(
        f"/tipos-veiculo/{created_id}", json=update_data
    )

    assert response_update.status_code == 200
    data = response_update.json()
    assert data["nome"] == update_data["nome"]
    assert data["tarifa_hora"] == update_data["tarifa_hora"]
    assert data["id"] == created_id


def test_delete_tipo_veiculo(authenticated_client):
    response_create = authenticated_client.post(
        "/tipos-veiculo/", json={"nome": "Carro Luxo", "tarifa_hora": 100.0}
    )
    created_id = response_create.json()["id"]
    response_delete = authenticated_client.delete(f"/tipos-veiculo/{created_id}")

    assert response_delete.status_code == 200
    assert response_delete.json()["id"] == created_id

    # verificando que registro não está mais no bd
    response_read = authenticated_client.get(f"/tipos-veiculo/{created_id}")
    assert response_read.status_code == 404
