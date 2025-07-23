import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Carrega as variáveis de ambiente (ex: DATABASE_URL) do arquivo .env
load_dotenv()

# URL de conexão com o banco de dados
# Exemplo para PostgreSQL: "postgresql://user:password@host:port/database"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Cria o motor de conexão do SQLAlchemy
# O argumento connect_args é necessário apenas para o SQLite.
engine_args = {}
if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_args)

# Cria uma fábrica de sessões (SessionLocal) que será usada para criar sessões individuais
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base para os modelos declarativos do ORM
Base = declarative_base()


# --- Dependência para obter a sessão do DB ---
def get_db():
    """
    Função geradora que cria e fornece uma sessão de banco de dados por requisição.
    Garante que a sessão seja sempre fechada após a requisição, mesmo em caso de erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()