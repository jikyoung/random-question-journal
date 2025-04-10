from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal
import random
from datetime import datetime

# ✅ DB 세션 가져오기 (FastAPI Depends용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 1. 사용자별로 아직 답변하지 않은 질문 중 랜덤 1개 가져오기
def get_random_question(user_id: int = None):
    db = SessionLocal()

    if user_id:
        # 사용자별로 이미 답한 질문 제외
        answered_ids = db.query(models.Answer.question_id).filter(
            models.Answer.user_id == user_id
        ).all()
        answered_ids = [row[0] for row in answered_ids]

        questions = db.query(models.Question).filter(
            ~models.Question.id.in_(answered_ids)
        ).all()
    else:
        # 비로그인 사용자는 전체 질문 중 랜덤
        questions = db.query(models.Question).all()

    db.close()

    if not questions:
        return None

    return random.choice(questions)

    if not questions:
        return None

    return random.choice(questions)

# ✅ 2. 답변 저장 (question_id, user_id, answer_text)
def save_answer(question_id: int, user_id: int, answer_text: str):
    db = SessionLocal()
    answer = models.Answer(
        question_id=question_id,
        user_id=user_id,
        answer_text=answer_text,
        created_at=datetime.utcnow().isoformat()
    )
    db.add(answer)
    db.commit()
    db.close()

# ✅ 3. 사용자 답변 전체 가져오기
def get_all_answers(user_id: int):
    db = SessionLocal()
    answers = db.query(models.Answer).filter(
        models.Answer.user_id == user_id
    ).order_by(models.Answer.created_at.desc()).all()
    db.close()
    return answers