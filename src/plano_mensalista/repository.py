from sqlalchemy.orm import Session
from src.plano_mensalista import model, schema


def get_plano(db: Session, plano_mensalista_id: int) -> model.PlanoMensalista | None:
    return (
        db.query(model.PlanoMensalista)
        .filter(model.PlanoMensalista.id == plano_mensalista_id)
        .first()
    )


def get_all_planos(
    db: Session, skip: int = 0, limit: int = 100
) -> list[model.PlanoMensalista]:
    return db.query(model.PlanoMensalista).offset(skip).limit(limit).all()


def create_plano(
    db: Session, plano_mensalista: schema.PlanoMensalistaCreate
) -> model.PlanoMensalista:
    if plano_mensalista.preco_mensal < 0:
        raise ValueError("O preço mensal não pode ser negativo.")

    db_plano_mensalista = model.PlanoMensalista(
        nome=plano_mensalista.nome,
        preco_mensal=plano_mensalista.preco_mensal,
        descricao=plano_mensalista.descricao,
    )
    db.add(db_plano_mensalista)
    db.commit()
    db.refresh(db_plano_mensalista)
    return db_plano_mensalista


def update_plano(
    db: Session,
    db_plano_mensalista: model.PlanoMensalista,
    plano_mensalista: schema.PlanoMensalistaUpdate,
) -> model.PlanoMensalista:
    update_data = plano_mensalista.model_dump(exclude_unset=True)

    if ("preco_mensal" in update_data) and update_data["preco_mensal"] < 0:
        raise ValueError("O preço mensal não pode ser negativo.")

    for key, value in update_data.items():
        setattr(db_plano_mensalista, key, value)

    db.add(db_plano_mensalista)
    db.commit()
    db.refresh(db_plano_mensalista)
    return db_plano_mensalista


def delete_plano(
    db: Session, db_plano_mensalista: model.PlanoMensalista
) -> model.PlanoMensalista:
    db.delete(db_plano_mensalista)
    db.commit()
    return db_plano_mensalista
