from sqlalchemy.orm import Session

from src.tipo_veiculo import model, schema

# READ


# get tipo_veiculo by id
def get_tipo_veiculo(db: Session, tipo_veiculo_id: int) -> model.TipoVeiculo | None:
    return (
        db.query(model.TipoVeiculo)
        .filter(model.TipoVeiculo.id == tipo_veiculo_id)
        .first()
    )


# skip e limit para paginacao
# get all tipo_veiculo
def get_tipos_veiculo(
    db: Session, skip: int = 0, limit: int = 100
) -> list[model.TipoVeiculo]:
    return db.query(model.TipoVeiculo).offset(skip).limit(limit).all()


# CREATE


def create_tipo_veiculo(
    db: Session, tipo_veiculo: schema.TipoVeiculoCreate
) -> model.TipoVeiculo:
    # cria um modelo sqlalchemy a partir dos dados recebidos no schema pydantic
    # **tipo_veiculo.model_dump() traduz o schema num formato que o SQLAlchemy entende
    db_tipo_veiculo = model.TipoVeiculo(**tipo_veiculo.model_dump())

    # adiciona novo objeto a session do db
    db.add(db_tipo_veiculo)

    # persiste o objeto
    db.commit()

    # atualiza o objeto com os dados que o db gerou
    db.refresh(db_tipo_veiculo)

    # retorna o objeto, agora com id
    return db_tipo_veiculo


def update_tipo_veiculo(
    db: Session,
    db_tipo_veiculo: model.TipoVeiculo,
    tipo_veiculo: schema.TipoVeiculoUpdate,
) -> model.TipoVeiculo:
    # pega dados do schema e converte em dicionario
    update_data = tipo_veiculo.model_dump(exclude_unset=True)

    # itera sobre os dados e atualiza os campos
    for key, value in update_data.items():
        setattr(db_tipo_veiculo, key, value)

    db.commit()
    db.refresh(db_tipo_veiculo)

    return db_tipo_veiculo


"""
padronizei que as funções de atualização e
deleção recebem um objeto e não um id. os endpoints
serão responsáveis por verificar se o objeto se
encontra na base antes de chamar a função
"""


def delete_tipo_veiculo(
    db: Session, db_tipo_veiculo: model.TipoVeiculo
) -> model.TipoVeiculo:
    db.delete(db_tipo_veiculo)
    db.commit()
    return db_tipo_veiculo
