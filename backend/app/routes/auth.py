from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core import security
from ..db import database, models
from ..models import schemas

router = APIRouter()


@router.post("/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Registra um novo usuário no sistema.
    """
    db_user_by_username = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso.",
        )

    db_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso.",
        )

    hashed_password = security.get_password_hash(user.password)
    # Exclui o campo 'password' do dicionário antes de criar o modelo
    user_data = user.model_dump(exclude={"password"})
    db_user = models.User(**user_data, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Lógica para determinar o status do plano
    now = datetime.now(timezone.utc)
    trial_active = db_user.trial_ends_at and now <= db_user.trial_ends_at
    plan_status = "active" if db_user.is_paid or trial_active else "inactive"
    
    # Adiciona o campo computado ao objeto ORM ANTES da validação
    db_user.plan_status = plan_status
    response_user = schemas.User.model_validate(db_user)
    
    return response_user


@router.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """
    Autentica o usuário e retorna um token de acesso.
    """
    # A função authenticate_user não existe em security, vamos criá-la aqui.
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/user", response_model=schemas.User)
def read_current_user(
    current_user: models.User = Depends(security.get_current_active_user),
):
    """
    Retorna os dados do usuário autenticado.
    """
    now = datetime.now(timezone.utc)
    trial_active = current_user.trial_ends_at and now <= current_user.trial_ends_at
    plan_status = "active" if current_user.is_paid or trial_active else "inactive"

    # Adiciona o campo computado ao objeto ORM ANTES da validação
    current_user.plan_status = plan_status
    response_user = schemas.User.model_validate(current_user)

    return response_user