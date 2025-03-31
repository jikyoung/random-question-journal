from fastapi import FastAPI
from app.routers import questions, answers

app = FastAPI()

app.include_router(questions.router)
app.include_router(answers.router)

@app.get("/")
def root():
    return {"message": "Hello, Random Question Journal!"}