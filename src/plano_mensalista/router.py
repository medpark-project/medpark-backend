from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auth_deps import get_current_user
from src.db.dependencies import get_db
from src.plano_mensalista import repository, schema

router = APIRouter()


@router.post("/", response_model=schema.PlanoMensalista, status_code=201)
def create_plano_mensalista(
    plano_mensalista: schema.PlanoMensalistaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.create_plano(db=db, plano_mensalista=plano_mensalista)


@router.get("/", response_model=List[schema.PlanoMensalista])
def read_all_planos_mensalista(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_all_planos(db, skip=skip, limit=limit)


@router.get("/{plano_mensalista_id}", response_model=schema.PlanoMensalista)
def read_plano_mensalista(
    plano_mensalista_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_plano_mensalista = repository.get_plano(
        db, plano_mensalista_id=plano_mensalista_id
    )
    if db_plano_mensalista is None:
        raise HTTPException(
            status_code=404, detail="Plano de Mensalista não encontrado"
        )
    return db_plano_mensalista


@router.put("/{plano_mensalista_id}", response_model=schema.PlanoMensalista)
def update_plano_mensalista(
    plano_mensalista_id: int,
    plano_mensalista: schema.PlanoMensalistaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_plano_mensalista = repository.get_plano(
        db, plano_mensalista_id=plano_mensalista_id
    )
    if db_plano_mensalista is None:
        raise HTTPException(
            status_code=404, detail="Plano de Mensalista não encontrado"
        )
    updated_plano = repository.update_plano(
        db=db,
        db_plano_mensalista=db_plano_mensalista,
        plano_mensalista=plano_mensalista,
    )
    return updated_plano


@router.delete("/{plano_mensalista_id}", response_model=schema.PlanoMensalista)
def delete_plano_mensalista(
    plano_mensalista_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_plano_mensalista = repository.get_plano(
        db, plano_mensalista_id=plano_mensalista_id
    )
    if db_plano_mensalista is None:
        raise HTTPException(
            status_code=404, detail="Plano de Mensalista não encontrado"
        )
    deleted_plano = repository.delete_plano(
        db=db, db_plano_mensalista=db_plano_mensalista
    )
    return deleted_plano
