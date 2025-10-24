from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth_deps import get_current_user
from src.db.dependencies import get_db
from src.veiculo import repository as veiculo_repo
from src.veiculo import schema as veiculo_schema

from . import repository, schema

router = APIRouter()


@router.post(
    "/entrada",
    response_model=schema.RegistroEstacionamento,
    status_code=status.HTTP_201_CREATED,
)
def registrar_entrada(
    registro: schema.RegistroEstacionamentoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    registro_aberto = repository.get_registro_aberto_por_placa(
        db, veiculo_placa=registro.veiculo_placa
    )
    if registro_aberto:
        raise HTTPException(
            status_code=409,
            detail="Este veículo já possui um registro de entrada ativo.",
        )

    db_veiculo = veiculo_repo.get_veiculo_by_placa(db, placa=registro.veiculo_placa)
    if not db_veiculo:
        veiculo_novo = veiculo_schema.VeiculoCreate(
            placa=registro.veiculo_placa, tipo_veiculo_id=1, mensalista_id=None
        )
        veiculo_repo.create_veiculo(db, veiculo=veiculo_novo)

    return repository.create_registro_entrada(db=db, registro=registro)


@router.put("/saida/{placa}", response_model=schema.RegistroEstacionamento)
def registrar_saida(
    placa: str,
    registro_in: schema.RegistroEstacionamentoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_registro = repository.get_registro_aberto_por_placa(db, veiculo_placa=placa)
    if db_registro is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhum registro de entrada ativo encontrado para esta placa.",
        )

    return repository.update_registro_saida(
        db=db, db_registro=db_registro, registro_in=registro_in
    )


@router.get("/ativos", response_model=List[schema.RegistroEstacionamento])
def get_veiculos_no_patio(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_all_registros_ativos(db)
