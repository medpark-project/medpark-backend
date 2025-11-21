from datetime import date

from sqlalchemy.orm import Session, joinedload

from src.assinatura_plano.model import AssinaturaPlano, StatusAssinatura

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
        .options(
            joinedload(model.PagamentoMensalidade.assinatura).joinedload(
                AssinaturaPlano.plano
            )
        )
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


def gerar_faturas_mensais(db: Session):
    hoje = date.today()
    mes_atual_int = int(hoje.strftime("%Y%m"))  # Ex: 202511

    assinaturas_ativas = (
        db.query(AssinaturaPlano)
        .filter(AssinaturaPlano.status == StatusAssinatura.ATIVA)
        .all()
    )

    faturas_criadas = 0

    for assinatura in assinaturas_ativas:
        fatura_existente = (
            db.query(model.PagamentoMensalidade)
            .filter(
                model.PagamentoMensalidade.assinatura_id == assinatura.id,
                model.PagamentoMensalidade.mes_referencia == mes_atual_int,
            )
            .first()
        )

        if not fatura_existente:
            try:
                vencimento = date(hoje.year, hoje.month, 10)
                if vencimento < hoje:
                    vencimento = hoje
            except ValueError:
                vencimento = hoje

            nova_fatura = model.PagamentoMensalidade(
                assinatura_id=assinatura.id,
                data_vencimento=vencimento,
                mes_referencia=mes_atual_int,
                status=model.StatusPagamento.PENDENTE,
                valor_pago=None,
            )
            db.add(nova_fatura)
            faturas_criadas += 1

    db.commit()
    return faturas_criadas
