from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from database import Base
from role.role_model import RolePublic

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
# Esta classe define a estrutura da tabela 'users' no banco de dados.
class User(Base):
    __tablename__ = "user"  # Nome da tabela no banco

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) # E-mail deve ser único
    hashed_password = Column(String) # Armazenaremos a senha "hasheada"
    full_name = Column(String, index=True, nullable=True) # Nome pode ser nulo
    profile_image_url = Column(String, nullable=True)
    # Chave estrangeira que aponta para a tabela 'role'
    role_id = Column(Integer, ForeignKey("role.id"))
    # Cria a relação para que possamos acessar o objeto Role a partir de um User
    role = relationship("Role")

# ==================================
# SCHEMAS (Pydantic) - O CONTRATO DA API
# ==================================
# Estes schemas definem como os dados são recebidos e enviados pela API.

# Schema para os dados que o cliente envia ao CRIAR um usuário
class UserCreate(BaseModel):
    email: EmailStr  # Valida o formato do e-mail
    password: str = Field(min_length=8)
    full_name: str | None = Field(default=None, min_length=3)
    profile_image_url: str | None = None
    role_id: int = Field(description="ID do role a ser associado ao usuário")

# Schema para os dados que o cliente envia ao ATUALIZAR um usuário
class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=3)
    profile_image_url: str | None = None

# Schema para os dados que a API RETORNA ao cliente (público)
# NUNCA inclua a senha ou outros dados sensíveis aqui!
class UserPublic(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None