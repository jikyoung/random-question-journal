from fastapi import FastAPI
from app.routers import pages, questions, answers, auth, admin_questions  # ← ✅ 추가

app = FastAPI()

# 기존 라우터
app.include_router(pages.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(auth.router)

# ✅ 관리자 라우터 추가
app.include_router(admin_questions.router)