from io import BytesIO

from validate_docbr import CPF

cpf_generator = CPF()


def test_full_user_journey_from_solicitacao_to_estacionamento(
    client, authenticated_client
):
    # --- PREPARAÇÃO (Criação das entidades base) ---
    print("\n--- Ato 1: Preparando o cenário...")

    tipo_veiculo_res = authenticated_client.post(
        "/tipos-veiculo/", json={"nome": "Carro Jornada Completa", "tarifa_hora": 12.0}
    )
    assert tipo_veiculo_res.status_code == 200
    tipo_veiculo_id = tipo_veiculo_res.json()["id"]

    plano_res = authenticated_client.post(
        "/planos-mensalista/",
        json={
            "nome": "Plano Jornada Completa",
            "preco_mensal": 300.0,
            "descricao": "Teste E2E",
        },
    )
    assert plano_res.status_code == 201
    plano_id = plano_res.json()["id"]

    print("--- Ato 2: Cliente envia a solicitação...")

    form_data = {
        "nome_completo": "Brunna da Jornada Completa",
        "email": "jornada.completa@teste.com",
        "cpf": cpf_generator.generate(),
        "rg": "11.222.333-X",
        "placa_veiculo": "EJE-2025",
        "plano_id": plano_id,
        "tipo_veiculo_id": tipo_veiculo_id,
    }
    files = {
        "doc_pessoal": ("doc_pessoal.pdf", BytesIO(b"pdf content"), "application/pdf"),
        "doc_comprovante": (
            "doc_comprovante.jpg",
            BytesIO(b"jpg content"),
            "image/jpeg",
        ),
    }

    solicitacao_res = client.post(
        "/solicitacoes-mensalista/", data=form_data, files=files
    )
    texto = f"Falha ao criar solicitação: {solicitacao_res.text}"
    assert solicitacao_res.status_code == 201, texto
    solicitacao_id = solicitacao_res.json()["id"]

    # --- APROVAÇÃO (Ação do Operador) ---
    print(f"--- Ato 3: Operador aprova a solicitação ID {solicitacao_id}...")

    aprovacao_res = authenticated_client.put(
        f"/solicitacoes-mensalista/{solicitacao_id}", json={"status": "APROVADO"}
    )
    assert aprovacao_res.status_code == 200
    assert aprovacao_res.json()["status"] == "APROVADO"

    print("--- Ato 4: Verificando se a integração funcionou...")

    # Verificação 1: O Mensalista foi criado?
    mensalistas_res = authenticated_client.get("/mensalistas/")
    lista_mensalistas = mensalistas_res.json()
    novo_mensalista = next(
        (m for m in lista_mensalistas if m["email"] == form_data["email"]), None
    )
    texto = "O mensalista não foi encontrado na lista após a aprovação."
    assert novo_mensalista is not None, texto
    novo_mensalista_id = novo_mensalista["id"]
    print(f"-> Sucesso! Mensalista ID {novo_mensalista_id} criado.")

    # Verificação 2: O Veículo foi criado e associado?
    veiculo_res = authenticated_client.get(f"/veiculos/{form_data['placa_veiculo']}")
    texto = "O veículo não foi encontrado após a aprovação."
    assert veiculo_res.status_code == 200, texto
    veiculo_data = veiculo_res.json()
    texto = "O veículo não foi associado ao mensalista correto."
    assert veiculo_data["mensalista_id"] == novo_mensalista_id, texto
    print(f"-> Sucesso! Veículo placa {veiculo_data['placa']} criado e associado.")

    # Verificação 3: A Assinatura foi criada?
    assinatura_res = authenticated_client.get(
        f"/assinaturas/mensalista/{novo_mensalista_id}/ativa"
    )
    texto = "A assinatura ativa não foi encontrada para o novo mensalista."
    assert assinatura_res.status_code == 200, texto
    assinatura_data = assinatura_res.json()
    texto = "A assinatura foi criada com o plano errado."
    assert assinatura_data["plano_id"] == plano_id, texto
    print(f"-> Sucesso! Assinatura ID {assinatura_data['id']} criada e ativa.")

    # --- O USO DO SISTEMA (Operação do Pátio) ---
    print("--- Ato 5: Simulando o uso do estacionamento pelo novo mensalista...")

    # Registrar Entrada
    entrada_res = authenticated_client.post(
        "/estacionamento/entrada", json={"veiculo_placa": form_data["placa_veiculo"]}
    )
    assert entrada_res.status_code == 201

    # Verificar se está no pátio
    ativos_res = authenticated_client.get("/estacionamento/ativos")
    veiculos_no_patio = ativos_res.json()
    assert any(
        v["veiculo_placa"] == form_data["placa_veiculo"] for v in veiculos_no_patio
    )
    print(f"-> Sucesso! Veículo {form_data['placa_veiculo']} entrou no pátio.")

    # Registrar Saída
    saida_res = authenticated_client.put(
        f"/estacionamento/saida/{form_data['placa_veiculo']}", json={"valor_pago": 0.0}
    )
    assert saida_res.status_code == 200
    assert saida_res.json()["hora_saida"] is not None
    print(f"-> Sucesso! Veículo {form_data['placa_veiculo']} saiu do pátio.")

    print("\nJORNADA COMPLETA TESTADA COM SUCESSO!")
