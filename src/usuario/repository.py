import bcrypt
from sqlalchemy.orm import Session

from src.usuario import model, schema


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


# READ


# get usuario by id
def get_usuario(db: Session, usuario_id: int) -> model.Usuario | None:
    return db.query(model.Usuario).filter(model.Usuario.id == usuario_id).first()


# get usuario by email
def get_usuario_by_email(db: Session, email: str) -> model.Usuario | None:
    return db.query(model.Usuario).filter(model.Usuario.email == email).first()


# get todos usuarios
def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[model.Usuario]:
    return db.query(model.Usuario).offset(skip).limit(limit).all()


# CREATE


def create_usuario(db: Session, usuario: schema.UsuarioCreate) -> model.Usuario:
    if len(usuario.senha) < 8:
        raise ValueError("A senha deve ter no mínimo 8 caracteres.")

    hashed_password = get_password_hash(usuario.senha)

    db_usuario = model.Usuario(
        **usuario.model_dump(exclude={"senha"}), senha_hash=hashed_password
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario


# UPDATE
def update_usuario(
    db: Session, db_usuario: model.Usuario, usuario: schema.UsuarioUpdate
) -> model.Usuario:
    update_data = usuario.model_dump(exclude_unset=True)

    if "senha" in update_data and update_data["senha"]:
        if len(update_data["senha"]) < 8:
            raise ValueError("A senha deve ter no mínimo 8 caracteres.")

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
def delete_usuario(db: Session, db_usuario: model.Usuario) -> model.Usuario:
    db.delete(db_usuario)
    db.commit()
    return db_usuario
