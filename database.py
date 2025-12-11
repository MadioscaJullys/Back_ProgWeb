
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 

APP_PROFILE = os.getenv("APP_PROFILE", "DEV")

# Prefer a DATABASE_URL from environment when present (useful in CI/Prod).
# For local development default to a lightweight SQLite DB so you don't need
# a running Postgres instance.
DATABASE_URL_ENV = os.getenv("DATABASE_URL")
# In development we force SQLite to avoid accidental use of a remote/local
# Postgres instance defined in the environment. This ensures a reproducible
# local dev database (`dev.db`). To use Postgres, set APP_PROFILE != "DEV"
# and provide a valid DATABASE_URL.
if APP_PROFILE == "DEV":
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234carlinhos!@5.161.88.20/jully_progwebIII"
else:
    SQLALCHEMY_DATABASE_URL = DATABASE_URL_ENV

# 1. Define a string de conexão com o banco PostgreSQL.
#    Formato: "postgresql://<user>:<password>@<host>/<dbname>"
#    Substitua com suas credenciais. É uma boa prática usar variáveis de ambiente aqui.


# 2. Cria a "engine" do SQLAlchemy, que é o ponto de entrada para o banco de dados.
#    Ela gerencia as conexões com o banco.
if SQLALCHEMY_DATABASE_URL is None:
    raise RuntimeError("No database URL configured. Set DATABASE_URL or APP_PROFILE accordingly.")

# When using SQLite we need connect_args to allow usage from multiple threads
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Cria uma fábrica de sessões (SessionLocal). Cada instância de SessionLocal
#    será uma sessão com o banco de dados. Pense nela como uma "conversa" temporária.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Cria uma classe Base. Nossos modelos de tabela do SQLAlchemy herdarão desta
#    classe para que o ORM possa gerenciá-los.
Base = declarative_base()

# 5. [NOVO] Função para obter a sessão do banco (Injeção de Dependência)
#    Esta função garante que a sessão com o banco seja sempre fechada após a requisição.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()