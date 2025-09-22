from app.models import tipo_veiculo as models
from app.schemas import tipo_veiculo as schemas

# READ

# get tipo_veiculo by id
def get_tipo_veiculo(db: Session, tipo_veiculo_id: int):
    return db.query(models.TipoVeiculo).filter(models.TipoVeiculo.id == tipo_veiculo_id).first()

# skip e limit para paginacao
# get all tipo_veiculo
def get_tipos_veiculo(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TipoVeiculo).offset(skip).limit(limit).all()

# CREATE

def create_tipo_veiculo(db: Session, tipo_veiculo: schemas.TipoVeiculoCreate):
    # cria um modelo sqlalchemy a partir dos dados recebidos no schema pydantic
    # **tipo_veiculo.model_dump() traduz o schema num formato que o SQLAlchemy entende
    db_tipo_veiculo = models.TipoVeiculo(**tipo_veiculo.model_dump())

    # adiciona novo objeto a session do db
    db.add(db_tipo_veiculo)

    # persiste o objeto
    db.commit()

    # atualiza o objeto com os dados que o db gerou
    db.refresh(db_tipo_veiculo)

    # retorna o objeto, agora com id
    return db_tipo_veiculo