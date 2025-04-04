from fastapi import FastAPI
from app.routers import pages, answers, questions  #
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 🔽 여기에 각 라우터를 연결해야 함
app.include_router(pages.router)
app.include_router(answers.router)
app.include_router(questions.router)

@app.get("/")
def root():
    return {"message": "Hello, Random Question Journal!"}