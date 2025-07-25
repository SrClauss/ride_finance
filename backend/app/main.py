from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Importações necessárias para a criação do usuário admin
from .db.database import SessionLocal
from .db import models
from .core.security import get_password_hash

from .routes import auth, transactions, categories, goals, work_sessions, profile

app = FastAPI()

# --- INÍCIO DA CONFIGURAÇÃO DE CORS ---

# Lista de origens que têm permissão para fazer requisições à API.
origins = [
    "http://localhost",
    "http://localhost:3000", # Porta padrão do Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FIM DA CONFIGURAÇÃO DE CORS ---


@app.on_event("startup")
def on_startup():
    """
    Na inicialização, verifica e cria um usuário administrador padrão se não existir.
    Assume-se que as tabelas do banco de dados já foram criadas via Alembic.
    """
    db: Session = SessionLocal()
    try:
        # Procura pelo usuário admin no banco de dados
        admin_user = db.query(models.User).filter(models.User.email == "admin@admin.com").first()
        
        # Se o usuário não for encontrado, cria um novo
        if not admin_user:
            hashed_password = get_password_hash("admin")
            new_admin_user = models.User(
                username="admin",
                email="admin@admin.com",
                full_name="Admin User",
                password=hashed_password,
                is_paid=True  # Corrigido para usar 'is_paid' conforme o modelo User
            )
            db.add(new_admin_user)
            db.commit()
            print("Usuário administrador padrão ('admin@admin.com') foi criado.")
        else:
            print("Usuário administrador já existe. Nenhuma ação foi necessária.")
            
    finally:
        # Garante que a sessão com o banco de dados seja fechada
        db.close()


app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(transactions.router, prefix="/api", tags=["transactions"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(goals.router, prefix="/api", tags=["goals"])
app.include_router(work_sessions.router, prefix="/api", tags=["work_sessions"])
app.include_router(profile.router, prefix="/api", tags=["profile"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ride Finance API"}
