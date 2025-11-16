from datetime import datetime, timedelta

from sqlalchemy import Date, cast, extract, func
from sqlalchemy.orm import Session
from src.pagamento_mensalidade.model import PagamentoMensalidade, StatusPagamento
from src.registro_estacionamento.model import RegistroEstacionamento

FUSO_HORARIO_LOCAL = "America/Sao_Paulo"
FUSO_HORARIO_DB = "UTC"  # Nosso banco de dados salva em UTC


def _get_local_time(column):
    return (column.op("AT TIME ZONE")(FUSO_HORARIO_DB)).op("AT TIME ZONE")(
        FUSO_HORARIO_LOCAL
    )


def get_total_revenue_this_month(db: Session) -> float:
    """Calcula a receita total (avulsos + mensalistas) deste mês."""
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
    """Calcula o ticket médio apenas de veículos avulsos deste mês."""
    hoje = datetime.now()
    inicio_do_mes = hoje.replace(day=1, hour=0, minute=0, second=0)

    query = db.query(func.avg(RegistroEstacionamento.valor_pago)).filter(
        RegistroEstacionamento.hora_saida >= inicio_do_mes,
        RegistroEstacionamento.valor_pago > 0,  # Apenas avulsos
    )

    media = query.scalar() or 0
    return float(media)


def get_transactions_today(db: Session) -> int:
    """Conta o total de transações de saída (avulsos) de hoje."""
    hoje_inicio = datetime.now().replace(hour=0, minute=0, second=0)

    # Converte a hora_saida (UTC) para o fuso local ANTES de filtrar
    local_hora_saida = _get_local_time(RegistroEstacionamento.hora_saida)

    count = (
        db.query(func.count(RegistroEstacionamento.id))
        .filter(
            cast(local_hora_saida, Date) == hoje_inicio.date(),
            RegistroEstacionamento.valor_pago > 0,
        )
        .scalar()
        or 0
    )

    return count


def get_recent_transactions(db: Session) -> list[RegistroEstacionamento]:
    """Busca as 5 transações de saída mais recentes."""
    return (
        db.query(RegistroEstacionamento)
        .filter(RegistroEstacionamento.hora_saida is not None)
        .order_by(RegistroEstacionamento.hora_saida.desc())
        .limit(5)
    ).all()


def get_revenue_breakdown(db: Session):
    """Retorna o faturamento total dividido entre Avulso e Mensalista."""

    # 1. Total Avulso (dos registros de estacionamento)
    total_avulso = (
        db.query(func.sum(RegistroEstacionamento.valor_pago))
        .filter(RegistroEstacionamento.valor_pago > 0)
        .scalar()
        or 0
    )

    # 2. Total Mensalista (dos pagamentos de mensalidade)
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
    """Calcula a receita total por dia dos últimos 7 dias, no fuso horário local."""
    sete_dias_atras = datetime.now() - timedelta(days=7)

    # --- CORREÇÃO AQUI ---
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

    # --- CORREÇÃO AQUI ---
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
    """Conta o total de entradas de veículos por hora DO DIA LOCAL (últimos 30 dias)."""
    um_mes_atras = datetime.now() - timedelta(days=30)

    # --- CORREÇÃO AQUI ---
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

    # Formata para o gráfico
    return [{"hour": f"{int(h):02d}:00", "vehicles": t} for h, t in registros]
