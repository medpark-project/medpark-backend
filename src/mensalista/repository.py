from sqlalchemy.orm import Session

from . import model, schema


def get_mensalista(db: Session, mensalista_id: int) -> model.Mensalista | None:
    return (
        db.query(model.Mensalista).filter(model.Mensalista.id == mensalista_id).first()
    )


def get_mensalista_by_email(db: Session, email: str) -> model.Mensalista | None:
    return db.query(model.Mensalista).filter(model.Mensalista.email == email).first()


def get_all_mensalistas(
    db: Session, skip: int = 0, limit: int = 100
) -> list[model.Mensalista]:
    return db.query(model.Mensalista).offset(skip).limit(limit).all()


def create_mensalista(
    db: Session, mensalista: schema.MensalistaCreate
) -> model.Mensalista:
    db_mensalista = model.Mensalista(**mensalista.model_dump())

    db.add(db_mensalista)
    db.commit()
    db.refresh(db_mensalista)
    return db_mensalista


def update_mensalista(
    db: Session, db_mensalista: model.Mensalista, mensalista_in: schema.MensalistaUpdate
) -> model.Mensalista:
    update_data = mensalista_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_mensalista, key, value)

    db.add(db_mensalista)
    db.commit()
    db.refresh(db_mensalista)
    return db_mensalista


def delete_mensalista(db: Session, db_mensalista: model.Mensalista) -> model.Mensalista:
    db.delete(db_mensalista)
    db.commit()
    return db_mensalista
