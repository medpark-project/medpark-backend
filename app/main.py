from fastapi import FastAPI
from app.db.session import engine, Base
from app.models import tipo_veiculo

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedPark API",
    version="0.1.0",
    description="API para o sistema de gerenciamento de estacionamento MedPark."
)

@app.get("/")
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo à API do MedPark! Conexão com o banco de dados estabelecida."}