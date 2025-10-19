import shutil
import uuid
from pathlib import Path
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.auth_deps import get_current_user
from src.db.dependencies import get_db
from src.plano_mensalista import repository as plano_repo

from . import repository, schema

router = APIRouter()


def solicitacao_form(
    nome_completo: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    rg: str = Form(...),
    placa_veiculo: str = Form(...),
    plano_id: int = Form(...),
) -> schema.SolicitacaoMensalistaCreate:
    try:
        return schema.SolicitacaoMensalistaCreate(
            nome_completo=nome_completo,
            email=email,
            cpf=cpf,
            rg=rg,
            placa_veiculo=placa_veiculo,
            plano_id=plano_id,
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())


@router.post("/", response_model=schema.SolicitacaoMensalista, status_code=201)
def create_solicitacao(
    db: Session = Depends(get_db),
    solicitacao_mensalista: schema.SolicitacaoMensalistaCreate = Depends(
        solicitacao_form
    ),
    doc_pessoal: UploadFile = File(...),
    doc_comprovante: UploadFile = File(...),
):
    plano_existente = plano_repo.get_plano(
        db, plano_mensalista_id=solicitacao_mensalista.plano_id
    )
    if not plano_existente:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Plano de ID {solicitacao_mensalista.plano_id} não foi encontrado."
            ),
        )

    upload_dir = Path("uploads/solicitacoes")
    upload_dir.mkdir(parents=True, exist_ok=True)

    path_doc_pessoal = upload_dir / f"{uuid.uuid4()}-{doc_pessoal.filename}"
    path_doc_comprovante = upload_dir / f"{uuid.uuid4()}-{doc_comprovante.filename}"

    with open(path_doc_pessoal, "wb") as buffer:
        shutil.copyfileobj(doc_pessoal.file, buffer)
    with open(path_doc_comprovante, "wb") as buffer:
        shutil.copyfileobj(doc_comprovante.file, buffer)

    return repository.create_solicitacao(
        db=db,
        solicitacao=solicitacao_mensalista,
        path_doc_pessoal=str(path_doc_pessoal),
        path_doc_comprovante=str(path_doc_comprovante),
    )


@router.get("/", response_model=List[schema.SolicitacaoMensalista])
def read_all_solicitacoes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_all_solicitacoes(db, skip=skip, limit=limit)


@router.get("/{solicitacao_id}", response_model=schema.SolicitacaoMensalista)
def read_solicitacao(
    solicitacao_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),  # Rota protegida
):
    db_solicitacao = repository.get_solicitacao(db, solicitacao_id=solicitacao_id)
    if db_solicitacao is None:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    return db_solicitacao


@router.put("/{solicitacao_id}", response_model=schema.SolicitacaoMensalista)
def update_solicitacao_status(
    solicitacao_id: int,
    solicitacao_mensalista: schema.SolicitacaoMensalistaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_solicitacao = repository.get_solicitacao(db, solicitacao_id=solicitacao_id)
    if db_solicitacao is None:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    return repository.update_status_solicitacao(
        db=db,
        db_solicitacao=db_solicitacao,
        solicitacao_mensalista=solicitacao_mensalista,
    )
