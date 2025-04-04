from fastapi import APIRouter
from app.models import Answer
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/api/answers", tags=["answers"])

@router.post("/")
def save_answer(answer: Answer):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO answers (question_id, answer_text, created_at) VALUES (?, ?, ?)",
        (answer.question_id, answer.answer_text, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return {"message": "Answer saved"}

@router.get("/")
def get_answers():
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM answers ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]
