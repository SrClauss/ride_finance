from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core import security
from ..db import database, models
from ..models import schemas

router = APIRouter()

@router.post("/work-sessions", response_model=schemas.WorkSession, status_code=status.HTTP_201_CREATED)
def create_work_session(
    session: schemas.WorkSessionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    db_session = models.WorkSession(**session.model_dump(), user_id=current_user.id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/work-sessions", response_model=List[schemas.WorkSession])
def get_work_sessions(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    sessions = db.query(models.WorkSession).filter(models.WorkSession.user_id == current_user.id).all()
    return sessions