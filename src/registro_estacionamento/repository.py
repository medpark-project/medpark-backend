from datetime import datetime

from sqlalchemy.orm import Session

from . import model, schema


def create_registro_entrada(
    db: Session, registro: schema.RegistroEstacionamentoCreate
) -> model.RegistroEstacionamento:
    db_registro = model.RegistroEstacionamento(
        veiculo_placa=registro.veiculo_placa, hora_entrada=datetime.now()
    )
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro


def get_registro_aberto_por_placa(
    db: Session, veiculo_placa: str
) -> model.RegistroEstacionamento | None:
    return (
        db.query(model.RegistroEstacionamento)
        .filter(
            model.RegistroEstacionamento.veiculo_placa == veiculo_placa,
            model.RegistroEstacionamento.hora_saida.is_(None),
        )
        .first()
    )


def get_all_registros_ativos(db: Session) -> list[model.RegistroEstacionamento]:
    return (
        db.query(model.RegistroEstacionamento)
        .filter(model.RegistroEstacionamento.hora_saida.is_(None))
        .order_by(model.RegistroEstacionamento.hora_entrada.asc())
        .all()
    )


def update_registro_saida(
    db: Session,
    db_registro: model.RegistroEstacionamento,
    registro_in: schema.RegistroEstacionamentoUpdate,
) -> model.RegistroEstacionamento:
    db_registro.hora_saida = datetime.now()
    db_registro.valor_pago = registro_in.valor_pago

    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro
