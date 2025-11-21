from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.assinatura_plano import repository as assinatura_repo
from src.auth_deps import get_current_user
from src.db.dependencies import get_db
from src.pagamento_mensalidade.model import StatusPagamento

from . import repository, schema

router = APIRouter()


@router.post("/", response_model=schema.Mensalista, status_code=201)
def create_mensalista(
    mensalista: schema.MensalistaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_mensalista_by_email = repository.get_mensalista_by_email(
        db, email=mensalista.email
    )
    if db_mensalista_by_email:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    return repository.create_mensalista(db=db, mensalista=mensalista)


@router.get("/", response_model=List[schema.Mensalista])
def read_all_mensalistas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_all_mensalistas(db, skip=skip, limit=limit)


@router.get("/{mensalista_id}", response_model=schema.Mensalista)
def read_mensalista(
    mensalista_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_mensalista = repository.get_mensalista(db, mensalista_id=mensalista_id)
    if db_mensalista is None:
        raise HTTPException(status_code=404, detail="Mensalista não encontrado")
    return db_mensalista


@router.put("/{mensalista_id}", response_model=schema.Mensalista)
def update_mensalista(
    mensalista_id: int,
    mensalista_in: schema.MensalistaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_mensalista = repository.get_mensalista(db, mensalista_id=mensalista_id)
    if db_mensalista is None:
        raise HTTPException(status_code=404, detail="Mensalista não encontrado")

    return repository.update_mensalista(
        db=db, db_mensalista=db_mensalista, mensalista_in=mensalista_in
    )


@router.delete("/{mensalista_id}", response_model=schema.Mensalista)
def delete_mensalista(
    mensalista_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_mensalista = repository.get_mensalista(db, mensalista_id=mensalista_id)
    if db_mensalista is None:
        raise HTTPException(status_code=404, detail="Mensalista não encontrado")

    return repository.delete_mensalista(db=db, db_mensalista=db_mensalista)


@router.get("/publico/status/{placa}", response_model=schema.MensalistaStatusPublico)
def get_mensalista_status_publico(
    placa: str,
    db: Session = Depends(get_db),
):
    mensalista = repository.get_mensalista_by_placa(db, placa=placa)
    if not mensalista:
        raise HTTPException(
            status_code=404, detail="Mensalista não encontrado para esta placa."
        )

    assinatura_ativa = assinatura_repo.get_assinatura_ativa_por_mensalista(
        db, mensalista_id=mensalista.id
    )

    if not assinatura_ativa:
        return {
            "nome_completo": mensalista.nome_completo,
            "plano_nome": "Nenhum Plano Ativo",
            "status_assinatura": "INATIVA",
        }

    fatura_pendente = None
    for pag in assinatura_ativa.pagamentos:
        if pag.status == StatusPagamento.PENDENTE:
            fatura_pendente = pag
            break

    return {
        "nome_completo": mensalista.nome_completo,
        "plano_nome": assinatura_ativa.plano.nome,
        "status_assinatura": assinatura_ativa.status,
        "fatura_pendente_id": fatura_pendente.id if fatura_pendente else None,
        "valor_pendente": assinatura_ativa.plano.preco_mensal
        if fatura_pendente
        else None,
        "data_vencimento": fatura_pendente.data_vencimento if fatura_pendente else None,
    }
