import math
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth_deps import get_current_user
from src.db.dependencies import get_db
from src.tipo_veiculo import repository as tipo_veiculo_repo
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
        if registro.tipo_veiculo_id is None:
            raise HTTPException(
                status_code=422,
                detail="tipo_veiculo_id é obrigatório para veículos novos.",
            )

        db_tipo_veiculo = tipo_veiculo_repo.get_tipo_veiculo(
            db, tipo_veiculo_id=registro.tipo_veiculo_id
        )
        if not db_tipo_veiculo:
            raise HTTPException(
                status_code=404, detail="Tipo de Veículo não encontrado."
            )

        veiculo_novo = veiculo_schema.VeiculoCreate(
            placa=registro.veiculo_placa,
            tipo_veiculo_id=registro.tipo_veiculo_id,
            mensalista_id=None,
        )
        veiculo_repo.create_veiculo(db, veiculo=veiculo_novo)

    return repository.create_registro_entrada(db=db, registro=registro)


@router.put("/saida/{placa}", response_model=schema.RegistroEstacionamento)
def registrar_saida(
    placa: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_registro = repository.get_registro_aberto_por_placa(db, veiculo_placa=placa)
    if db_registro is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhum registro de entrada ativo encontrado para esta placa.",
        )

    db_veiculo = veiculo_repo.get_veiculo_by_placa(db, placa=placa)
    if not db_veiculo:
        raise HTTPException(
            status_code=500,
            detail="Inconsistência de dados: Registro encontrado, mas veículo não.",
        )

    if db_veiculo.mensalista_id is not None:
        valor_a_pagar = 0.0
    else:
        db_tipo_veiculo = tipo_veiculo_repo.get_tipo_veiculo(
            db, tipo_veiculo_id=db_veiculo.tipo_veiculo_id
        )
        if not db_tipo_veiculo:
            raise HTTPException(
                status_code=500,
                detail=f"Inconsistência de dados: Tipo de veículo ID "
                f"{db_veiculo.tipo_veiculo_id} não encontrado.",
            )

        hora_saida = datetime.now()
        duracao_total = hora_saida - db_registro.hora_entrada
        duracao_em_horas = math.ceil(duracao_total.total_seconds() / 3600)

        if duracao_em_horas <= 0:
            duracao_em_horas = 1

        valor_a_pagar = round(duracao_em_horas * db_tipo_veiculo.tarifa_hora, 2)

    return repository.update_registro_saida(
        db=db, db_registro=db_registro, valor_pago=valor_a_pagar
    )


@router.get("/ativos", response_model=List[schema.RegistroEstacionamento])
def get_veiculos_no_patio(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_all_registros_ativos(db)
