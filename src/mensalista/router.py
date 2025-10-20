from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auth_deps import get_current_user
from src.db.dependencies import get_db

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
