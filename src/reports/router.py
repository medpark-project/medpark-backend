# src/reports/router.py

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth_deps import get_current_user
from src.db.dependencies import get_db
from src.registro_estacionamento import schema as registro_schema

from . import repository

router = APIRouter()


@router.get("/daily-revenue")
def get_daily_revenue_report(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Retorna a receita agregada por dia dos últimos 7 dias."""
    return repository.get_revenue_last_7_days(db)


@router.get("/hourly-entries")
def get_hourly_entries_report(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Retorna o total de entradas de veículos por hora."""
    return repository.get_entries_by_hour(db)


@router.get("/revenue-breakdown")
def get_revenue_breakdown_report(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Retorna o faturamento total dividido entre Avulso e Mensalista."""
    return repository.get_revenue_breakdown(db)


@router.get("/avg-stay-time")
def get_avg_stay_time_report(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Retorna o tempo médio de permanência formatado (ex: '2h 30m')."""
    return {"average_stay_time": repository.get_avg_stay_time(db)}


@router.get("/metrics/total-revenue-month")
def get_total_revenue_month_report(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    return {"total_revenue": repository.get_total_revenue_this_month(db)}


@router.get("/metrics/avg-ticket-month")
def get_avg_ticket_month_report(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    return {"average_ticket": repository.get_average_ticket_price_this_month(db)}


@router.get("/metrics/transactions-today")
def get_transactions_today_report(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    return {"transactions_today": repository.get_transactions_today(db)}


@router.get(
    "/recent-transactions", response_model=List[registro_schema.RegistroEstacionamento]
)
def get_recent_transactions_report(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_recent_transactions(db)
