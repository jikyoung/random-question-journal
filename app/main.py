from fastapi import FastAPI
from app.routers import pages, answers, questions, auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 라우터 등록
app.include_router(pages.router)
app.include_router(answers.router)
app.include_router(questions.router)
app.include_router(auth.router)
