from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth_deps import get_current_user
from src.db.dependencies import get_db
from src.mensalista import repository as mensalista_repo
from src.plano_mensalista import repository as plano_repo

from . import repository, schema

router = APIRouter()


@router.post(
    "/", response_model=schema.AssinaturaPlano, status_code=status.HTTP_201_CREATED
)
def create_assinatura(
    assinatura: schema.AssinaturaPlanoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not mensalista_repo.get_mensalista(db, mensalista_id=assinatura.mensalista_id):
        raise HTTPException(status_code=404, detail="Mensalista não encontrado.")
    if not plano_repo.get_plano(db, plano_mensalista_id=assinatura.plano_id):
        raise HTTPException(
            status_code=404, detail="Plano de Mensalista não encontrado."
        )

    assinatura_ativa = repository.get_assinatura_ativa_por_mensalista(
        db, mensalista_id=assinatura.mensalista_id
    )
    if assinatura_ativa:
        raise HTTPException(
            status_code=409, detail="Este mensalista já possui uma assinatura ativa."
        )

    return repository.create_assinatura(db=db, assinatura=assinatura)


@router.get("/mensalista/{mensalista_id}/ativa", response_model=schema.AssinaturaPlano)
def read_assinatura_ativa(
    mensalista_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_assinatura = repository.get_assinatura_ativa_por_mensalista(
        db, mensalista_id=mensalista_id
    )
    if db_assinatura is None:
        raise HTTPException(
            status_code=404, detail="Nenhuma assinatura ativa encontrada."
        )
    return db_assinatura


@router.get(
    "/mensalista/{mensalista_id}/historico", response_model=List[schema.AssinaturaPlano]
)
def read_historico_assinaturas(
    mensalista_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_all_assinaturas_by_mensalista(db, mensalista_id=mensalista_id)


@router.put("/{assinatura_id}", response_model=schema.AssinaturaPlano)
def update_assinatura(
    assinatura_id: int,
    assinatura_in: schema.AssinaturaPlanoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_assinatura = repository.get_assinatura(db, assinatura_id=assinatura_id)
    if db_assinatura is None:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada.")

    return repository.update_assinatura(
        db=db, db_assinatura=db_assinatura, assinatura_in=assinatura_in
    )
