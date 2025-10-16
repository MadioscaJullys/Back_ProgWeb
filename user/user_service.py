from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import user_repository, user_model

def create_new_user(db: Session, user: user_model.UserCreate):
    """Serviço para criar um novo usuário com regras de negócio."""
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    return user_repository.create_user(db=db, user=user, role_id=user_role.id)

def get_all_users(db: Session):
    """Serviço para listar todos os usuários. Neste caso, apenas repassa a chamada."""
    return user_repository.get_users(db)

def get_user_by_id(db: Session, user_id: int):
    """Serviço para buscar um usuário pelo ID, com tratamento de erro."""
    db_user = user_repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

def update_existing_user(db: Session, user_id: int, user_in: user_model.UserUpdate):
    """Serviço para atualizar um usuário, com tratamento de erro."""
    db_user = get_user_by_id(db, user_id)
    return user_repository.update_user(db=db, db_user=db_user, user_in=user_in)

def delete_user_by_id(db: Session, user_id: int):
    """Serviço para deletar um usuário, com tratamento de erro."""
    db_user = get_user_by_id(db, user_id)
    return user_repository.delete_user(db=db, db_user=db_user)