from app.database import get_db
from datetime import datetime


def get_random_question():
    conn = get_db()
    row = conn.execute("SELECT * FROM questions WHERE used = 0 ORDER BY RANDOM() LIMIT 1").fetchone()
    if row:
        # print("질문 ID:", row["id"], " → used = 1 업데이트 실행")  # ✅ 요기!
        conn.execute("UPDATE questions SET used = 1 WHERE id = ?", (row["id"],))
        conn.commit()
    conn.close()
    return row

def save_answer(question_id, answer_text):
    conn = get_db()
    conn.execute(
        "INSERT INTO answers (question_id, answer_text, created_at) VALUES (?, ?, ?)",
        (question_id, answer_text, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_all_answers():
    conn = get_db()
    rows = conn.execute("SELECT * FROM answers ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows