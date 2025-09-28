from sqlalchemy.orm import Session
import bcrypt
from app.models import usuario as models
from app.schemas import usuario as schemas

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')

# READ

# get usuario by id
def get_usuario(db: Session, usuario_id: int) -> models.Usuario | None:
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

# get usuario by email
def get_usuario_by_email(db: Session, email: str) -> models.Usuario | None:
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

# get todos usuarios
def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[models.Usuario]:
    return db.query(models.Usuario).offset(skip).limit(limit).all()

# CREATE

def create_usuario(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    hashed_password = get_password_hash(usuario.senha)

    db_usuario = models.Usuario(
        **usuario.model_dump(exclude={"senha"}),
        senha_hash=hashed_password
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario

# UPDATE
def update_usuario(db: Session, db_usuario: models.Usuario, usuario: schemas.UsuarioUpdate) -> models.Usuario:
    update_data = usuario.model_dump(exclude_unset=True)

    if "senha" in update_data and update_data["senha"]:
        hashed_password = get_password_hash(update_data["senha"])
        db_usuario.senha_hash = hashed_password
        del update_data["senha"]

    for field, value in update_data.items():
        setattr(db_usuario, field, value)

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# DELETE
def delete_usuario(db: Session, db_usuario: models.Usuario) -> models.Usuario:
    db.delete(db_usuario)
    db.commit()
    return db_usuario