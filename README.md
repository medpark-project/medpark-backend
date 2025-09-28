# MedPark - Backend

API backend para o sistema de gerenciamento de estacionamentos de hospitais MedPark, desenvolvida com FastAPI, PostgreSQL e Docker.

## Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework:** FastAPI
- **Banco de Dados:** PostgreSQL
- **Ambiente de Container:** Docker & Docker Compose
- **ORM (Mapeamento Objeto-Relacional):** SQLAlchemy
- **Validação de Dados:** Pydantic
- **Testes:** Pytest & HTTPX

---

## Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento na sua máquina.

### Pré-requisitos

- [Git](https://git-scm.com/) instalado.
- [Docker](https://www.docker.com/products/docker-desktop/) e Docker Compose instalados e em execução.

### Passos para Instalação

1.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/medpark-project/medpark-backend.git](https://github.com/medpark-project/medpark-backend.git)
    cd medpark-backend
    ```

2.  **Iniciar os Contêineres:**
    O Docker Compose irá ler o arquivo `docker-compose.yml`, construir a imagem da API, baixar a imagem do PostgreSQL e iniciar os dois contêineres de forma orquestrada.

    ```bash
    docker compose up -d --build
    ```
    * `-d`: Modo "detached", roda os contêineres em segundo plano.
    * `--build`: Força a reconstrução da imagem da API na primeira vez.

A aplicação estará disponível em instantes.

## Testando a Aplicação

### API
- A API estará rodando em `http://localhost:8000`.
- A documentação interativa (Swagger UI) está disponível em `http://localhost:8000/docs`.
- A documentação alternativa (ReDoc) está disponível em `http://localhost:8000/redoc`.

### Banco de Dados
- O banco de dados PostgreSQL está rodando e acessível na sua máquina local (`localhost`).
- Use um cliente de banco de dados (como DBeaver ou PGAdmin) com as seguintes credenciais para se conectar:
    - **Host:** `localhost`
    - **Porta:** `5432`
    - **Banco de Dados:** `medpark_db`
    - **Usuário:** `medpark_user`
    - **Senha:** `medpark_password`

### Testes Automatizados
Os testes são executados automaticamente toda vez que o contêiner do backend é iniciado. Para executá-los manualmente, use o comando:
```bash
docker compose exec backend pytest
```
