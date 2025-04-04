
import sqlite3

def get_db():
    conn = sqlite3.connect("questions.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # DROP & RE-CREATE for development reset (safe during early stage)
    cursor.execute("DROP TABLE IF EXISTS answers")

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
