from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auth_deps import get_current_user
from src.db.dependencies import get_db

# Importa os repositórios das entidades relacionadas para validação
from src.mensalista import repository as mensalista_repo
from src.tipo_veiculo import repository as tipo_veiculo_repo

from . import repository, schema

router = APIRouter()


@router.post("/", response_model=schema.Veiculo, status_code=201)
def create_veiculo(
    veiculo: schema.VeiculoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_mensalista = mensalista_repo.get_mensalista(
        db, mensalista_id=veiculo.mensalista_id
    )
    if not db_mensalista:
        raise HTTPException(status_code=404, detail="Mensalista não encontrado.")

    db_tipo_veiculo = tipo_veiculo_repo.get_tipo_veiculo(
        db, tipo_veiculo_id=veiculo.tipo_veiculo_id
    )
    if not db_tipo_veiculo:
        raise HTTPException(status_code=404, detail="Tipo de Veículo não encontrado.")

    db_veiculo = repository.get_veiculo_by_placa(db, placa=veiculo.placa)
    if db_veiculo:
        raise HTTPException(status_code=400, detail="Placa de veículo já cadastrada.")

    return repository.create_veiculo(db=db, veiculo=veiculo)


@router.get("/por-mensalista/{mensalista_id}", response_model=List[schema.Veiculo])
def read_veiculos_por_mensalista(
    mensalista_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    veiculos = repository.get_all_veiculos_by_mensalista(
        db, mensalista_id=mensalista_id
    )
    return veiculos


@router.get("/{placa}", response_model=schema.Veiculo)
def read_veiculo(
    placa: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_veiculo = repository.get_veiculo_by_placa(db, placa=placa)
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    return db_veiculo


@router.put("/{placa}", response_model=schema.Veiculo)
def update_veiculo(
    placa: str,
    veiculo: schema.VeiculoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_veiculo = repository.get_veiculo_by_placa(db, placa=placa)
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    return repository.update_veiculo(db=db, db_veiculo=db_veiculo, veiculo=veiculo)


@router.delete("/{placa}", response_model=schema.Veiculo)
def delete_veiculo(
    placa: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_veiculo = repository.get_veiculo_by_placa(db, placa=placa)
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    return repository.delete_veiculo(db=db, db_veiculo=db_veiculo)


@router.patch("/{placa}/assign-owner", response_model=schema.Veiculo)
def assign_owner_to_veiculo(
    placa: str,
    owner_data: schema.VeiculoAssignOwner,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_veiculo = repository.get_veiculo_by_placa(db, placa=placa)
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    db_mensalista = mensalista_repo.get_mensalista(
        db, mensalista_id=owner_data.mensalista_id
    )
    if not db_mensalista:
        raise HTTPException(status_code=404, detail="Mensalista não encontrado.")

    return repository.assign_mensalista_to_veiculo(
        db=db, db_veiculo=db_veiculo, mensalista_id=owner_data.mensalista_id
    )
