
from fastapi import FastAPI
from .routes import (
    auth,
    categories,
    transactions,
    work_sessions,
    goals,
    profile,
)
from .db import models, database

app = FastAPI(
    title="Driver-App Backend",
    description="API para o aplicativo de gestão financeira para motoristas.",
    version="1.0.0",
)

# Adicionando os roteadores para cada módulo da API
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(categories.router, prefix="/api", tags=["Categories"])
app.include_router(transactions.router, prefix="/api", tags=["Transactions"])
app.include_router(work_sessions.router, prefix="/api", tags=["Work Sessions"])
app.include_router(goals.router, prefix="/api", tags=["Goals"])
app.include_router(profile.router, prefix="/api", tags=["Profile"])


@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz para verificar a saúde da API.
    """
    return {"status": "ok", "message": "Welcome to the Driver-App API!"}