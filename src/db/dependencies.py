from src.db.session import SessionLocal


def get_db():
    # cria nova sessao com db para a requisicao
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
