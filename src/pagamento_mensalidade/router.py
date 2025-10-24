from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.assinatura_plano import repository as assinatura_repo
from src.auth_deps import get_current_user
from src.db.dependencies import get_db

from . import repository, schema

router = APIRouter()


@router.post(
    "/", response_model=schema.PagamentoMensalidade, status_code=status.HTTP_201_CREATED
)
def create_pagamento(
    pagamento: schema.PagamentoMensalidadeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_assinatura = assinatura_repo.get_assinatura(
        db, assinatura_id=pagamento.assinatura_id
    )
    if not db_assinatura:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada.")

    return repository.create_pagamento(db=db, pagamento=pagamento)


@router.get(
    "/assinatura/{assinatura_id}", response_model=List[schema.PagamentoMensalidade]
)
def read_pagamentos_por_assinatura(
    assinatura_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_pagamentos_por_assinatura(db, assinatura_id=assinatura_id)


@router.put("/{pagamento_id}", response_model=schema.PagamentoMensalidade)
def update_pagamento(
    pagamento_id: int,
    pagamento_in: schema.PagamentoMensalidadeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_pagamento = repository.get_pagamento(db, pagamento_id=pagamento_id)
    if db_pagamento is None:
        raise HTTPException(
            status_code=404, detail="Registro de pagamento não encontrado."
        )

    return repository.update_pagamento(
        db=db, db_pagamento=db_pagamento, pagamento_in=pagamento_in
    )
