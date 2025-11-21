from datetime import date

from sqlalchemy.orm import Session, joinedload

from . import model, schema


def get_assinatura(db: Session, assinatura_id: int) -> model.AssinaturaPlano | None:
    return (
        db.query(model.AssinaturaPlano)
        .filter(model.AssinaturaPlano.id == assinatura_id)
        .first()
    )


def get_all_assinaturas_by_mensalista(
    db: Session, mensalista_id: int
) -> list[model.AssinaturaPlano]:
    return (
        db.query(model.AssinaturaPlano)
        .filter(model.AssinaturaPlano.mensalista_id == mensalista_id)
        .all()
    )


def get_assinatura_ativa_por_mensalista(
    db: Session, mensalista_id: int
) -> model.AssinaturaPlano | None:
    return (
        db.query(model.AssinaturaPlano)
        .options(
            joinedload(model.AssinaturaPlano.plano),
            joinedload(model.AssinaturaPlano.pagamentos),
        )
        .filter(
            model.AssinaturaPlano.mensalista_id == mensalista_id,
            model.AssinaturaPlano.status == model.StatusAssinatura.ATIVA,
        )
        .first()
    )


def create_assinatura(
    db: Session, assinatura: schema.AssinaturaPlanoCreate
) -> model.AssinaturaPlano:
    db_assinatura = model.AssinaturaPlano(
        mensalista_id=assinatura.mensalista_id,
        plano_id=assinatura.plano_id,
        data_inicio=assinatura.data_inicio,
    )

    db.add(db_assinatura)
    db.commit()
    db.refresh(db_assinatura)
    return db_assinatura


def update_assinatura(
    db: Session,
    db_assinatura: model.AssinaturaPlano,
    assinatura_in: schema.AssinaturaPlanoUpdate,
) -> model.AssinaturaPlano:
    update_data = assinatura_in.model_dump(exclude_unset=True)

    if "status" in update_data and update_data["status"] in (
        model.StatusAssinatura.INATIVA,
        model.StatusAssinatura.CANCELADA,
    ):
        if "data_fim" not in update_data:
            update_data["data_fim"] = date.today()

    for key, value in update_data.items():
        setattr(db_assinatura, key, value)

    db.add(db_assinatura)
    db.commit()
    db.refresh(db_assinatura)
    return db_assinatura
