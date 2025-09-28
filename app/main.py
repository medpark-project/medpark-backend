from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.endpoints import tipo_veiculo as api_tipo_veiculo
from app.api.endpoints import usuario as api_usuario
from app.models import tipo_veiculo, usuario


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedPark API",
    version="0.1.0",
    description="API para o sistema de gerenciamento de estacionamento MedPark."
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do MedPark! Conexão com o banco de dados estabelecida."}

app.include_router(api_tipo_veiculo.router, prefix="/tipos-veiculo", tags=["Tipos de Veículo"])
app.include_router(api_usuario.router, prefix="/usuarios", tags=["Usuarios"])