from sqlalchemy.orm import Session

from . import model, schema


def get_solicitacao(
    db: Session, solicitacao_id: int
) -> model.SolicitacaoMensalista | None:
    return (
        db.query(model.SolicitacaoMensalista)
        .filter(model.SolicitacaoMensalista.id == solicitacao_id)
        .first()
    )


def get_all_solicitacoes(
    db: Session, skip: int = 0, limit: int = 100
) -> list[model.SolicitacaoMensalista]:
    return db.query(model.SolicitacaoMensalista).offset(skip).limit(limit).all()


def create_solicitacao(
    db: Session,
    solicitacao: schema.SolicitacaoMensalistaCreate,
    path_doc_pessoal: str,
    path_doc_comprovante: str,
) -> model.SolicitacaoMensalista:
    db_solicitacao = model.SolicitacaoMensalista(
        nome_completo=solicitacao.nome_completo,
        email=solicitacao.email,
        cpf=solicitacao.cpf,
        rg=solicitacao.rg,
        placa_veiculo=solicitacao.placa_veiculo,
        plano_id=solicitacao.plano_id,
        path_doc_pessoal=path_doc_pessoal,
        path_doc_comprovante=path_doc_comprovante,
    )
    db.add(db_solicitacao)
    db.commit()
    db.refresh(db_solicitacao)
    return db_solicitacao


def update_status_solicitacao(
    db: Session,
    db_solicitacao: model.SolicitacaoMensalista,
    solicitacao_mensalista: schema.SolicitacaoMensalistaUpdate,
) -> model.SolicitacaoMensalista:
    db_solicitacao.status = solicitacao_mensalista.status

    db.add(db_solicitacao)
    db.commit()
    db.refresh(db_solicitacao)
    return db_solicitacao


def delete_solicitacao(
    db: Session, db_solicitacao: model.SolicitacaoMensalista
) -> model.SolicitacaoMensalista:
    db.delete(db_solicitacao)
    db.commit()
    return db_solicitacao
