from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core import security
from ..db import database, models
from ..models import schemas

router = APIRouter()

@router.post("/goals", response_model=schemas.Goal, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal: schemas.GoalCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    db_goal = models.Goal(**goal.model_dump(), user_id=current_user.id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/goals", response_model=List[schemas.Goal])
def get_goals(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    # A lógica de cálculo de progresso em tempo real pode ser adicionada aqui
    goals = db.query(models.Goal).filter(models.Goal.user_id == current_user.id).all()
    return goals