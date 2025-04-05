from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import get_db
import random
import sqlite3

router = APIRouter(prefix="/questions", tags=["questions"])

class QuestionCreate(BaseModel):
    question_text: str

# ✅ 무작위 질문 가져오기
@router.get("/random")
def get_random_question(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    questions = cursor.execute("SELECT * FROM questions").fetchall()

    if not questions:
        return {"message": "등록된 질문이 없습니다."}
    
    question = random.choice(questions)
    return {"id": question["id"], "question_text": question["question_text"]}

# ✅ 질문 추가
@router.post("/")
def create_question(question: QuestionCreate, db: sqlite3.Connection = Depends(get_db)):
    if not question.question_text.strip():
        raise HTTPException(status_code=400, detail="질문 내용은 비워둘 수 없습니다.")
    
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO questions (question_text) VALUES (?)",
        (question.question_text,)
    )
    db.commit()
    return {"message": "질문이 추가되었습니다!", "question": question.question_text}