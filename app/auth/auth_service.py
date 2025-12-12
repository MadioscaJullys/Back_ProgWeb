# auth/auth_service.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import JWTError, jwt

from database import get_db
from ..users import user_repository
from security import verify_password, SECRET_KEY, ALGORITHM, TokenData
from ..users.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def authenticate_user(db: Session, email: str, password: str):
    user = user_repository.get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = user_repository.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role_name: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        # Be tolerant with role name variants (case-insensitive, abbreviations)
        role_obj = getattr(current_user, "role", None)
        role_name = getattr(role_obj, "name", None) if role_obj else None
        if not role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this user role"
            )

        r = role_name.lower()
        req = required_role_name.lower()

        # Accept exact match, contained/starts-with variants (e.g. 'adm' vs 'admin')
        if not (r == req or r.startswith(req) or req.startswith(r) or req in r or r in req):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this user role"
            )
        return current_user
    return role_checker