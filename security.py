from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pydantic import BaseModel
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)

SECRET_KEY = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto",
    bcrypt_sha256__rounds=12  # faster but still secure
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    # bcrypt_sha256 avoids the 72-byte limitation by hashing with SHA-256 first
    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise ValueError(f"Erro ao criar hash da senha: {str(e)}")

def create_access_token(data: dict):
    to_encode = data.copy()
    # Utiliza o método timezone-aware recomendado
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None