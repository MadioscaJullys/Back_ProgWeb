import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Ensure project root is on sys.path so 'app' package can be imported
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.roles.role_model import Role
from database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
with Session(engine) as session:
    for name in ("user", "admin"):
        exists = session.query(Role).filter(Role.name == name).first()
        if not exists:
            r = Role(name=name)
            session.add(r)
    session.commit()
    print("Seeded roles: user, admin")
