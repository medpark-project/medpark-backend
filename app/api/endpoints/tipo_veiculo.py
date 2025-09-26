from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import tipo_veiculo as schemas
from app.crud import tipo_veiculo as crud
from app.db.dependencies import get_db

router = APIRouter()

# endpoint CREATE novo tipo_veiculo
@router.post("/", response_model=schemas.TipoVeiculo)
def create_tipo_veiculo(tipo_veiculo: schemas.TipoVeiculoCreate, db: Session = Depends(get_db)):
    return crud.create_tipo_veiculo(db=db, tipo_veiculo=tipo_veiculo)

# endpoint READ lista de tipo_veiculo
@router.get("/", response_model=List[schemas.TipoVeiculo])
def read_tipos_veiculo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tipos_veiculo = crud.get_tipos_veiculo(db, skip=skip, limit=limit)
    return tipos_veiculo

# endpoint READ tipo_veiculo by id
@router.get("/{tipo_veiculo_id}", response_model=schemas.TipoVeiculo)
def read_tipo_veiculo(tipo_veiculo_id: int, db: Session = Depends(get_db)):
    db_tipo_veiculo = crud.get_tipo_veiculo(db, tipo_veiculo_id=tipo_veiculo_id)
    if db_tipo_veiculo is None:
        raise HTTPException(status_code=404, detail="Tipo de Veículo não encontrado.")
    return db_tipo_veiculo

# UPDATE
@router.put("/{tipo_veiculo_id}", response_model=schemas.TipoVeiculo)
def update_tipo_veiculo(tipo_veiculo_id: int, tipo_veiculo: schemas.TipoVeiculoUpdate, db: Session = Depends(get_db)):
    db_tipo_veiculo = crud.get_tipo_veiculo(db, tipo_veiculo_id=tipo_veiculo_id)
    if db_tipo_veiculo is None:
        raise HTTPException(status_code=404, detail="Tipo de Veiculo não encontrado.")
    
    return crud.update_tipo_veiculo(db=db, tipo_veiculo_id=tipo_veiculo_id, tipo_veiculo=tipo_veiculo)

# DELETE
@router.delete("/{tipo_veiculo_id}", response_model=schemas.TipoVeiculo)
def delete_tipo_veiculo(tipo_veiculo_id: int, db: Session = Depends(get_db)):
    db_tipo_veiculo = crud.get_tipo_veiculo(db, tipo_veiculo_id=tipo_veiculo_id)
    if db_tipo_veiculo is None:
        raise HTTPException(status_code=404, detail="Tipo de Veículo não encontrado.")
    
    return crud.delete_tipo_veiculo(db=db, tipo_veiculo_id=tipo_veiculo_id)
