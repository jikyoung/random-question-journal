from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/api/answers", tags=["answers"])

@router.post("/", response_model=schemas.AnswerOut)
def save_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    return crud.create_answer(db, answer)

@router.get("/", response_model=List[schemas.AnswerOut])
def get_answers(db: Session = Depends(get_db)):
    return crud.get_all_answers(db)