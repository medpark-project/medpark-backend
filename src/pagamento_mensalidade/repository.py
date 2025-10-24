from sqlalchemy.orm import Session

from . import model, schema


def create_pagamento(
    db: Session, pagamento: schema.PagamentoMensalidadeCreate
) -> model.PagamentoMensalidade:
    db_pagamento = model.PagamentoMensalidade(**pagamento.model_dump())
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


def get_pagamento(db: Session, pagamento_id: int) -> model.PagamentoMensalidade | None:
    return (
        db.query(model.PagamentoMensalidade)
        .filter(model.PagamentoMensalidade.id == pagamento_id)
        .first()
    )


def get_pagamentos_por_assinatura(
    db: Session, assinatura_id: int
) -> list[model.PagamentoMensalidade]:
    return (
        db.query(model.PagamentoMensalidade)
        .filter(model.PagamentoMensalidade.assinatura_id == assinatura_id)
        .order_by(model.PagamentoMensalidade.data_vencimento.desc())
        .all()
    )


def update_pagamento(
    db: Session,
    db_pagamento: model.PagamentoMensalidade,
    pagamento_in: schema.PagamentoMensalidadeUpdate,
) -> model.PagamentoMensalidade:
    update_data = pagamento_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_pagamento, key, value)

    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento
