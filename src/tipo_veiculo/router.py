from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.tipo_veiculo import schema, repository
from src.db.dependencies import get_db

router = APIRouter()

# endpoint CREATE novo tipo_veiculo
@router.post("/", response_model=schema.TipoVeiculo)
def create_tipo_veiculo(tipo_veiculo: schema.TipoVeiculoCreate, db: Session = Depends(get_db)):
    return repository.create_tipo_veiculo(db=db, tipo_veiculo=tipo_veiculo)

# endpoint READ lista de tipo_veiculo
@router.get("/", response_model=List[schema.TipoVeiculo])
def read_tipos_veiculo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tipos_veiculo = repository.get_tipos_veiculo(db, skip=skip, limit=limit)
    return tipos_veiculo

# endpoint READ tipo_veiculo by id
@router.get("/{tipo_veiculo_id}", response_model=schema.TipoVeiculo)
def read_tipo_veiculo(tipo_veiculo_id: int, db: Session = Depends(get_db)):
    db_tipo_veiculo = repository.get_tipo_veiculo(db, tipo_veiculo_id=tipo_veiculo_id)
    if db_tipo_veiculo is None:
        raise HTTPException(status_code=404, detail="Tipo de Veículo não encontrado.")
    return db_tipo_veiculo

# UPDATE
@router.put("/{tipo_veiculo_id}", response_model=schema.TipoVeiculo)
def update_tipo_veiculo(tipo_veiculo_id: int, tipo_veiculo: schema.TipoVeiculoUpdate, db: Session = Depends(get_db)):
    db_tipo_veiculo = repository.get_tipo_veiculo(db, tipo_veiculo_id=tipo_veiculo_id)
    if db_tipo_veiculo is None:
        raise HTTPException(status_code=404, detail="Tipo de Veiculo não encontrado.")
    
    return repository.update_tipo_veiculo(db=db, db_tipo_veiculo=db_tipo_veiculo, tipo_veiculo=tipo_veiculo)

"""
padronizei que as funções de atualização e deleção recebem um objeto e não um id. os endpoints
serão responsáveis por verificar se o objeto se encontra na base antes de chamar a função
"""
# DELETE
@router.delete("/{tipo_veiculo_id}", response_model=schema.TipoVeiculo)
def delete_tipo_veiculo(tipo_veiculo_id: int, db: Session = Depends(get_db)):
    db_tipo_veiculo = repository.get_tipo_veiculo(db, tipo_veiculo_id=tipo_veiculo_id)
    if db_tipo_veiculo is None:
        raise HTTPException(status_code=404, detail="Tipo de Veículo não encontrado.")
    
    return repository.delete_tipo_veiculo(db=db, db_tipo_veiculo=db_tipo_veiculo)
