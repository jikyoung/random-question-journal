from fastapi import APIRouter, Depends
from app.models import Answer
from app.database import get_db
from datetime import datetime
from sqlite3 import Connection

router = APIRouter(prefix="/api/answers", tags=["answers"])

@router.post("/")
def save_answer(answer: Answer, db: Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO answers (question_id, answer_text, created_at) VALUES (?, ?, ?)",
        (answer.question_id, answer.answer_text, datetime.now().isoformat())
    )
    db.commit()
    return {"message": "Answer saved"}

@router.get("/")
def get_answers(db: Connection = Depends(get_db)):
    cursor = db.cursor()
    rows = cursor.execute("SELECT * FROM answers ORDER BY created_at DESC").fetchall()
    return [dict(row) for row in rows]