from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.session import engine, Base
from src.tipo_veiculo.router import router as tipo_veiculo_router
from src.usuario.router import router as usuario_router
from src.tipo_veiculo import model as tipo_veiculo_model
from src.usuario import model as usuario_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando a aplicação e criando as tabelas do banco de dados...")
    Base.metadata.create_all(bind=engine)
    yield
    print("Finalizando a aplicação.")

def create_app() -> FastAPI:
    app = FastAPI(
        title="MedPark API",
        version="0.1.0",
        description="API para o sistema de gerenciamento de estacionamento MedPark.",
        lifespan=lifespan
    )

    @app.get("/")
    def read_root():
        return {"message": "Bem-vindo à API do MedPark!"}

    app.include_router(tipo_veiculo_router, prefix="/tipos-veiculo", tags=["Tipos de Veículo"])
    app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])
    
    return app

app = create_app()