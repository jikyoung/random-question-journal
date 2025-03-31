from fastapi import APIRouter
from app.models import Answer
from app.database import get_db

router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/")
def save_answer(answer: Answer):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO answers (question_id, answer_text) VALUES (?, ?)",
        (answer.question_id, answer.answer_text)
    )
    conn.commit()
    return {"message": "Answer saved"}

@router.get("/")
def get_answers():
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM answers").fetchall()
    return [dict(row) for row in rows]