def test_create_read_tipo_veiculo(client):
    tipo_veiculo_data = {"nome": "Motocicleta", "tarifa_hora": 3.50}

    response = client.post("/tipos-veiculo/", json=tipo_veiculo_data)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["nome"] == tipo_veiculo_data["nome"]
    assert data["tarifa_hora"] == tipo_veiculo_data["tarifa_hora"]
    assert "id" in data

    created_id = data["id"]

    response = client.get(f"/tipos-veiculo/{created_id}")

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["nome"] == tipo_veiculo_data["nome"]
    assert data["tarifa_hora"] == tipo_veiculo_data["tarifa_hora"]
    assert data["id"] == created_id