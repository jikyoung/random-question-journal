import json
from app.database import SessionLocal
from app.models import Question

def seed_questions_from_json(filepath="questions.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        questions = json.load(f)

    db = SessionLocal()
    existing_texts = set(q.question_text for q in db.query(Question).all())

    added_count = 0
    for text in questions:
        if text not in existing_texts:
            db.add(Question(question_text=text))
            added_count += 1

    db.commit()
    db.close()
    print(f"✅ 질문 {added_count}개 삽입 완료!")

if __name__ == "__main__":
    seed_questions_from_json()