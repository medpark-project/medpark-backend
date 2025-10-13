def test_create_plano(client):
    plano_data = {
        "nome": "Plano Básico",
        "preco_mensal": 150.0,
        "descricao": "Acesso diurno de Seg a Sex."
    }
    response = client.post("/planos-mensalista/", json=plano_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == plano_data["nome"]
    assert "id" in data

def test_create_plano_missing_description_fails(client):
    plano_data_invalido = {
        "nome": "Plano Inválido",
        "preco_mensal": 150.0
    }
    response = client.post("/planos-mensalista/", json=plano_data_invalido)
    
    assert response.status_code == 422 

def test_read_all_planos(client):
    client.post("/planos-mensalista/", json={"nome": "Plano Teste A", "preco_mensal": 100.0, "descricao": "Desc A"})
    client.post("/planos-mensalista/", json={"nome": "Plano Teste B", "preco_mensal": 200.0, "descricao": "Desc B"})

    response = client.get("/planos-mensalista/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_read_one_plano_not_found(client):
    response = client.get("/planos-mensalista/999")
    assert response.status_code == 404
    assert "Plano de Mensalista não encontrado" in response.json()["detail"]

def test_update_plano(client):
    plano_data = {"nome": "Plano Original", "preco_mensal": 120.0, "descricao": "Desc Original"}
    response_create = client.post("/planos-mensalista/", json=plano_data)
    created_id = response_create.json()["id"]
    
    update_data = {"descricao": "Nova descrição atualizada."}
    response_update = client.put(f"/planos-mensalista/{created_id}", json=update_data)
    assert response_update.status_code == 200
    data = response_update.json()
    assert data["descricao"] == "Nova descrição atualizada."
    assert data["nome"] == "Plano Original"

def test_delete_plano(client):
    plano_data = {"nome": "Plano a ser Deletado", "preco_mensal": 50.0, "descricao": "Desc Delete"}
    response_create = client.post("/planos-mensalista/", json=plano_data)
    created_id = response_create.json()["id"]

    response_delete = client.delete(f"/planos-mensalista/{created_id}")
    assert response_delete.status_code == 200

    response_read = client.get(f"/planos-mensalista/{created_id}")
    assert response_read.status_code == 404