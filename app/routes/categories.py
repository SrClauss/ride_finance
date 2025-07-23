from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..core import security
from ..db import database, models
from ..models import schemas

router = APIRouter()


@router.get("/categories", response_model=List[schemas.Category])
def get_categories(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    """
    Busca todas as categorias do usuário mais as categorias padrão.
    """
    categories = db.query(models.Category).filter(
        or_(models.Category.user_id == current_user.id, models.Category.is_default == True)
    ).all()
    return categories


@router.post("/categories", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    """
    Cria uma nova categoria para o usuário.
    """
    db_category = models.Category(**category.dict(), user_id=current_user.id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category