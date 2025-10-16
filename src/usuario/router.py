from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.dependencies import get_db
from src.usuario import repository, schema

router = APIRouter()


# CREATE
@router.post("/", response_model=schema.Usuario, status_code=201)
def create_usuario(usuario: schema.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = repository.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado no sistema.")
    return repository.create_usuario(db=db, usuario=usuario)


# READ
@router.get("/", response_model=List[schema.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_usuarios = repository.get_usuarios(db, skip=skip, limit=limit)
    return db_usuarios


@router.get("/{usuario_id}", response_model=schema.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = repository.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_usuario


# UPDATE
@router.put("/{usuario_id}", response_model=schema.Usuario)
def update_usuario(
    usuario_id: int, usuario: schema.UsuarioUpdate, db: Session = Depends(get_db)
):
    db_usuario = repository.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return repository.update_usuario(db=db, db_usuario=db_usuario, usuario=usuario)


# DELETE
@router.delete("/{usuario_id}", response_model=schema.Usuario)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = repository.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return repository.delete_usuario(db=db, db_usuario=db_usuario)
