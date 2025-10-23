from sqlalchemy.orm import Session

from . import model, schema


def get_veiculo_by_placa(db: Session, placa: str) -> model.Veiculo | None:
    return db.query(model.Veiculo).filter(model.Veiculo.placa == placa).first()


def get_all_veiculos_by_mensalista(
    db: Session, mensalista_id: int, skip: int = 0, limit: int = 100
) -> list[model.Veiculo]:
    return (
        db.query(model.Veiculo)
        .filter(model.Veiculo.mensalista_id == mensalista_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_veiculos(
    db: Session, skip: int = 0, limit: int = 100
) -> list[model.Veiculo]:
    return db.query(model.Veiculo).offset(skip).limit(limit).all()


def create_veiculo(db: Session, veiculo: schema.VeiculoCreate) -> model.Veiculo:
    db_veiculo = model.Veiculo(**veiculo.model_dump())
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo


def update_veiculo(
    db: Session, db_veiculo: model.Veiculo, veiculo: schema.VeiculoUpdate
) -> model.Veiculo:
    update_data = veiculo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_veiculo, key, value)

    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo


def delete_veiculo(db: Session, db_veiculo: model.Veiculo) -> model.Veiculo:
    db.delete(db_veiculo)
    db.commit()
    return db_veiculo


def assign_mensalista_to_veiculo(
    db: Session, db_veiculo: model.Veiculo, mensalista_id: int
) -> model.Veiculo:
    db_veiculo.mensalista_id = mensalista_id

    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo
