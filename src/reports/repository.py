from datetime import datetime, timedelta

from sqlalchemy import Date, cast, extract, func
from sqlalchemy.orm import Session, joinedload
from src.assinatura_plano.model import AssinaturaPlano
from src.pagamento_mensalidade.model import PagamentoMensalidade, StatusPagamento
from src.registro_estacionamento.model import RegistroEstacionamento

FUSO_HORARIO_LOCAL = "America/Sao_Paulo"
FUSO_HORARIO_DB = "UTC"


def _get_local_time(column):
    return (column.op("AT TIME ZONE")(FUSO_HORARIO_DB)).op("AT TIME ZONE")(
        FUSO_HORARIO_LOCAL
    )


def get_total_revenue_this_month(db: Session) -> float:
    hoje = datetime.now()
    inicio_do_mes = hoje.replace(day=1, hour=0, minute=0, second=0)

    total_avulso = (
        db.query(func.sum(RegistroEstacionamento.valor_pago))
        .filter(
            RegistroEstacionamento.hora_saida >= inicio_do_mes,
            RegistroEstacionamento.valor_pago > 0,
        )
        .scalar()
        or 0
    )

    total_mensalista = (
        db.query(func.sum(PagamentoMensalidade.valor_pago))
        .filter(
            PagamentoMensalidade.data_pagamento >= inicio_do_mes,
            PagamentoMensalidade.status == StatusPagamento.PAGO,
        )
        .scalar()
        or 0
    )

    return float(total_avulso) + float(total_mensalista)


def get_average_ticket_price_this_month(db: Session) -> float:
    hoje = datetime.now()
    inicio_do_mes = hoje.replace(day=1, hour=0, minute=0, second=0)

    query = db.query(func.avg(RegistroEstacionamento.valor_pago)).filter(
        RegistroEstacionamento.hora_saida >= inicio_do_mes,
        RegistroEstacionamento.valor_pago > 0,  # Apenas avulsos
    )

    media = query.scalar() or 0
    return float(media)


def get_recent_transactions(db: Session) -> list[RegistroEstacionamento]:
    return (
        db.query(RegistroEstacionamento)
        .options(joinedload(RegistroEstacionamento.veiculo))
        .order_by(RegistroEstacionamento.hora_entrada.desc())
        .limit(10)
    ).all()


def get_revenue_breakdown(db: Session):
    total_avulso = (
        db.query(func.sum(RegistroEstacionamento.valor_pago))
        .filter(RegistroEstacionamento.valor_pago > 0)
        .scalar()
        or 0
    )

    total_mensalista = (
        db.query(func.sum(PagamentoMensalidade.valor_pago))
        .filter(PagamentoMensalidade.status == StatusPagamento.PAGO)
        .scalar()
        or 0
    )

    return [
        {"name": "Casual Users", "value": float(total_avulso)},
        {"name": "Monthly Parkers", "value": float(total_mensalista)},
    ]


def get_avg_stay_time(db: Session) -> str:
    ontem = datetime.now() - timedelta(days=1)

    avg_seconds = (
        db.query(
            func.avg(
                extract(
                    "epoch",
                    RegistroEstacionamento.hora_saida
                    - RegistroEstacionamento.hora_entrada,
                )
            )
        ).filter(
            RegistroEstacionamento.hora_saida is not None,
            RegistroEstacionamento.valor_pago > 0,
            RegistroEstacionamento.hora_saida >= ontem,
        )
    ).scalar()

    if not avg_seconds or avg_seconds <= 0:
        return "--"

    total_minutos = int(avg_seconds / 60)
    horas = total_minutos // 60
    minutos = total_minutos % 60

    return f"{horas}h {minutos}m"


def get_revenue_last_7_days(db: Session):
    sete_dias_atras = datetime.now() - timedelta(days=7)

    local_hora_saida = _get_local_time(RegistroEstacionamento.hora_saida)
    registros = (
        db.query(
            cast(local_hora_saida, Date).label("dia"),
            func.sum(RegistroEstacionamento.valor_pago).label("total"),
        )
        .filter(
            RegistroEstacionamento.hora_saida >= sete_dias_atras,
            RegistroEstacionamento.valor_pago > 0,
        )
        .group_by(cast(local_hora_saida, Date))
    ).all()

    local_data_pagamento = _get_local_time(PagamentoMensalidade.data_pagamento)
    mensalidades = (
        db.query(
            cast(local_data_pagamento, Date).label("dia"),
            func.sum(PagamentoMensalidade.valor_pago).label("total"),
        )
        .filter(
            PagamentoMensalidade.data_pagamento >= sete_dias_atras,
            PagamentoMensalidade.status == StatusPagamento.PAGO,
        )
        .group_by(cast(local_data_pagamento, Date))
    ).all()

    receita = {}
    for dia, total in registros + mensalidades:
        if dia:
            receita[dia] = receita.get(dia, 0) + float(total)

    dados_formatados = []
    for i in range(7):
        dia = (datetime.now() - timedelta(days=i)).date()
        dados_formatados.append(
            {"name": dia.strftime("%a"), "revenue": receita.get(dia, 0)}
        )

    return dados_formatados[::-1]


def get_entries_by_hour(db: Session):
    um_mes_atras = datetime.now() - timedelta(days=30)

    local_hora_entrada = _get_local_time(RegistroEstacionamento.hora_entrada)

    registros = (
        db.query(
            extract("hour", local_hora_entrada).label("hora"),  # Extrai a hora local
            func.count(RegistroEstacionamento.id).label("total"),
        )
        .filter(RegistroEstacionamento.hora_entrada >= um_mes_atras)
        .group_by(extract("hour", local_hora_entrada))  # Agrupa pela hora local
        .order_by(extract("hour", local_hora_entrada))  # Ordena pela hora local
    ).all()

    return [{"hour": f"{int(h):02d}:00", "vehicles": t} for h, t in registros]


def get_financial_transactions(db: Session, limit: int = 20):
    avulsos = (
        db.query(RegistroEstacionamento)
        .options(joinedload(RegistroEstacionamento.veiculo))
        .filter(RegistroEstacionamento.valor_pago > 0)
        .filter(RegistroEstacionamento.hora_saida is not None)
        .order_by(RegistroEstacionamento.hora_saida.desc())
        .limit(limit)
    ).all()

    mensalidades = (
        db.query(PagamentoMensalidade)
        .options(
            joinedload(PagamentoMensalidade.assinatura).joinedload(
                AssinaturaPlano.mensalista
            )
        )
        .filter(PagamentoMensalidade.status == StatusPagamento.PAGO)
        .order_by(PagamentoMensalidade.data_pagamento.desc())
        .limit(limit)
    ).all()

    lista_unificada = []

    for a in avulsos:
        lista_unificada.append(
            {
                "id": f"avulso-{a.id}",
                "data": a.hora_saida,  # DateTime
                "descricao": f"Ticket Avulso - {a.veiculo_placa}",
                "tipo": "Casual",
                "valor": float(a.valor_pago),
                "placa": a.veiculo_placa,
            }
        )

    for m in mensalidades:
        data_formatada = datetime.combine(
            m.data_pagamento, datetime.min.time().replace(hour=12)
        )
        nome_mensalista = (
            m.assinatura.mensalista.nome_completo
            if m.assinatura and m.assinatura.mensalista
            else "Desconhecido"
        )

        lista_unificada.append(
            {
                "id": f"mensal-{m.id}",
                "data": data_formatada,
                "descricao": f"Mensalidade - {nome_mensalista}",
                "tipo": "Monthly",
                "valor": float(m.valor_pago or 0),
            }
        )

    lista_unificada.sort(key=lambda x: x["data"], reverse=True)

    return lista_unificada[:limit]


def get_transactions_today(db: Session) -> int:
    hoje_local = (datetime.now() - timedelta(hours=3)).date()

    local_hora_saida = _get_local_time(RegistroEstacionamento.hora_saida)

    total_avulsos = (
        db.query(func.count(RegistroEstacionamento.id))
        .filter(
            cast(local_hora_saida, Date) == hoje_local,
            RegistroEstacionamento.valor_pago > 0,
        )
        .scalar()
        or 0
    )

    total_mensalistas = (
        db.query(func.count(PagamentoMensalidade.id))
        .filter(
            PagamentoMensalidade.data_pagamento == hoje_local,
            PagamentoMensalidade.status == StatusPagamento.PAGO,
        )
        .scalar()
        or 0
    )

    return total_avulsos + total_mensalistas
