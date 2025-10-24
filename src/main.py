from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.assinatura_plano import model as assinatura_plano_model  # noqa: F401
from src.assinatura_plano.router import router as assinatura_plano_router
from src.db.session import Base, engine
from src.mensalista import model as mensalista_model  # noqa: F401
from src.mensalista.router import router as mensalista_router
from src.pagamento_mensalidade import model as pagamento_mensalidade_model  # noqa: F401
from src.pagamento_mensalidade.router import router as pagamento_mensalidade_router
from src.plano_mensalista import model as plano_model  # noqa: F401
from src.plano_mensalista.router import router as plano_router
from src.registro_estacionamento import (
    model as registro_estacionamento_model,  # noqa: F401
)
from src.registro_estacionamento.router import router as registro_estacionamento_router
from src.solicitacao_mensalista import (
    model as solicitacao_mensalista_model,  # noqa: F401
)
from src.solicitacao_mensalista.router import router as solicitacao_router
from src.tipo_veiculo import model as tipo_veiculo_model  # noqa: F401
from src.tipo_veiculo.router import router as tipo_veiculo_router
from src.usuario import model as usuario_model  # noqa: F401
from src.usuario.router import router as usuario_router
from src.veiculo import model as veiculo_model  # noqa: F401
from src.veiculo.router import router as veiculo_router


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
        lifespan=lifespan,
    )

    @app.get("/")
    def read_root():
        return {"message": "Bem-vindo à API do MedPark!"}

    app.include_router(
        tipo_veiculo_router, prefix="/tipos-veiculo", tags=["Tipos de Veículo"]
    )

    app.include_router(
        plano_router, prefix="/planos-mensalista", tags=["Planos de Mensalista"]
    )

    app.include_router(
        solicitacao_router,
        prefix="/solicitacoes-mensalista",
        tags=["Solicitações de Mensalista"],
    )

    app.include_router(mensalista_router, prefix="/mensalistas", tags=["Mensalistas"])

    app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])

    app.include_router(veiculo_router, prefix="/veiculos", tags=["Veículos "])

    app.include_router(
        assinatura_plano_router, prefix="/assinaturas", tags=["Assinaturas de Plano"]
    )

    app.include_router(
        pagamento_mensalidade_router,
        prefix="/pagamentos",
        tags=["Pagamentos de Mensalidade"],
    )

    app.include_router(
        registro_estacionamento_router,
        prefix="/estacionamento",
        tags=["Registro de Estacionamento"],
    )

    return app


app = create_app()
