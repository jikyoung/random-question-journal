from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routers import pages, questions, answers, auth, admin_questions, posts

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="dev-secret-key")

# 기존 라우터
app.include_router(pages.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(auth.router)
app.include_router(posts.router)

# ✅ 관리자 라우터 추가
app.include_router(admin_questions.router)