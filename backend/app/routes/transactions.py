from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..core import security
from ..db import database, models
from ..models import schemas

router = APIRouter()


@router.get("/transactions", response_model=List[schemas.Transaction])
def get_transactions(
    limit: Optional[int] = Query(None, description="Número de transações a retornar"),
    offset: Optional[int] = Query(None, description="Número de transações a pular"),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    """
    Busca as transações do usuário com paginação opcional.
    """
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)
    
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
        
    transactions = query.order_by(models.Transaction.date.desc()).all()
    return transactions


@router.post("/transactions", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    """
    Cria uma nova transação.
    """
    db_transaction = models.Transaction(**transaction.model_dump(), user_id=current_user.id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/transactions/date-range", response_model=List[schemas.Transaction])
def get_transactions_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    """
    Busca transações dentro de um período específico.
    """
    transactions = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.user_id == current_user.id,
            models.Transaction.date >= start_date,
            models.Transaction.date <= end_date,
        )
        .order_by(models.Transaction.date.desc())
        .all()
    )
    return transactions