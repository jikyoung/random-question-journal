import sqlite3

def get_db():
    conn = sqlite3.connect("questions.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 개발 단계에서는 테이블 초기화(DROP 후 CREATE)
    cursor.execute("DROP TABLE IF EXISTS answers")
    cursor.execute("DROP TABLE IF EXISTS questions")  # ✅ 추가

    # ✅ questions 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL
        )
    ''')

    # ✅ answers 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            answer_text TEXT,
            created_at TEXT,
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
    ''')

    conn.commit()
    conn.close()

# 실행용
if __name__ == "__main__":
    init_db()