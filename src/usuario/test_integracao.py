def test_create_usuario_sucesso(client):
    user_data = {
        "nome": "Administrador Teste",
        "email": "admin@gmail.com",
        "perfil": "ADMIN",
        "senha": "senha123",
    }
    response = client.post("/usuarios/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "senha_hash" not in data


def test_create_user_duplicate_email(client):
    user_data = {
        "nome": "Usuario Unico",
        "email": "unico@teste.com",
        "perfil": "OPERATOR",
        "senha": "senhaforte123",
    }

    response1 = client.post("/usuarios/", json=user_data)
    assert response1.status_code == 201

    response2 = client.post("/usuarios/", json=user_data)
    assert response2.status_code == 400
    assert "E-mail já cadastrado" in response2.json()["detail"]


def test_read_all_usuarios(client):
    client.post(
        "/usuarios/",
        json={
            "nome": "João Silva",
            "email": "joao@gmail.com",
            "perfil": "OPERATOR",
            "senha": "senh@123",
        },
    )
    client.post(
        "/usuarios/",
        json={
            "nome": "Ana Santos",
            "email": "ana@gmail.com",
            "perfil": "ADMIN",
            "senha": "s3nha123",
        },
    )

    response = client.get("/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_read_usuario_sucesso(client):
    user_data = {
        "nome": "Pedro Freitas",
        "email": "pedro@gmail.com",
        "perfil": "OPERATOR",
        "senha": "senha123",
    }
    response_create = client.post("/usuarios/", json=user_data)
    created_id = response_create.json()["id"]

    response_read = client.get(f"/usuarios/{created_id}")
    assert response_read.status_code == 200
    data = response_read.json()
    assert data["id"] == created_id
    assert data["email"] == user_data["email"]


def test_read_usuario_nao_encontrado(client):
    response = client.get("/usuarios/999")
    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]


def test_update_usuario_sucesso(client):
    user_data = {
        "nome": "Maria de Paula",
        "email": "maria@gmail.com",
        "perfil": "OPERATOR",
        "senha": "senha123",
    }
    response_create = client.post("/usuarios/", json=user_data)
    created_id = response_create.json()["id"]

    update_data = {"nome": "Maria de Fátima"}
    response_update = client.put(f"/usuarios/{created_id}", json=update_data)
    assert response_update.status_code == 200
    data = response_update.json()
    assert data["nome"] == "Maria de Fátima"
    assert data["email"] == user_data["email"]


def test_update_usuario_nao_encontrado(client):
    response = client.put("/usuarios/999", json={"nome": "Fantasma"})
    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]


def test_delete_usuario_sucesso(client):
    user_data = {
        "nome": "Lambi",
        "email": "lambi@gmail.com",
        "perfil": "OPERATOR",
        "senha": "senha123",
    }
    response_create = client.post("/usuarios/", json=user_data)
    created_id = response_create.json()["id"]

    response_delete = client.delete(f"/usuarios/{created_id}")
    assert response_delete.status_code == 200

    response_read = client.get(f"/usuarios/{created_id}")
    assert response_read.status_code == 404


def test_delete_usuario_nao_encontrado(client):
    response = client.delete("/usuarios/999")
    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]
