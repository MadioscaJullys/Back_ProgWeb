#!/usr/bin/env python3
"""Create a test user directly in the database.

Usage:
  python scripts/create_test_user.py [email] [password]

If run from the `scripts/` folder, the script will add the project root
to `sys.path` so imports work regardless of how it's executed.
"""
import os
import sys
from typing import Optional

# Ensure project root is on sys.path when script is executed from /scripts
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import SessionLocal, engine
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from app.roles.role_model import Role
from app.users.user_model import User
from security import get_password_hash

def ensure_roles(db):
    names = ["adm", "admin", "user"]
    created = []
    for name in names:
        exists = db.query(Role).filter(Role.name == name).first()
        if not exists:
            r = Role(name=name)
            db.add(r)
            created.append(name)
    if created:
        try:
            db.commit()
        except IntegrityError:
            # Concurrent insertion or sequence issues may raise unique/PK errors.
            db.rollback()
            # Try to insert one-by-one ignoring conflicts
            for name in created:
                try:
                    exists = db.query(Role).filter(Role.name == name).first()
                    if not exists:
                        r = Role(name=name)
                        db.add(r)
                        db.commit()
                except IntegrityError:
                    db.rollback()
    return created

def create_user(db, email: str, password: str, full_name: Optional[str] = "Test User", role_name: str = "adm"):
    # find role
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise RuntimeError(f"Role '{role_name}' not found; run ensure_roles first")

    hashed = get_password_hash(password)
    user = User(
        email=email,
        hashed_password=hashed,
        full_name=full_name,
        profile_image_url=None,
        profile_image_base64=None,
        role_id=role.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def main():
    email = sys.argv[1] if len(sys.argv) > 1 else "test_db_user@example.com"
    password = sys.argv[2] if len(sys.argv) > 2 else "Password123!"

    db = SessionLocal()
    try:
        created = ensure_roles(db)
        if created:
            print("Created roles:", created)

        # If using Postgres, ensure the sequence for roles.id is set to max(id)
        try:
            if engine.dialect.name == 'postgresql':
                print('Postgres detected: synchronizing roles sequence...')
                db.execute(text(
                    "SELECT setval(pg_get_serial_sequence('roles','id'), COALESCE((SELECT MAX(id) FROM roles), 1), true)"
                ))
                db.commit()
                print('Sequence synchronized')
        except Exception as e:
            print('Could not synchronize sequence:', e)

        user = create_user(db, email=email, password=password)
        print("Created user:", {"id": user.id, "email": user.email, "role_id": user.role_id})
    except Exception as e:
        print("Error creating user:", e)
    finally:
        db.close()

if __name__ == '__main__':
    main()
