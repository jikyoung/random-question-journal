# app/routers/admin_questions.py

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.models import Question

router = APIRouter(prefix="/admin/questions", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")

# ✅ 질문 목록 보기
@router.get("/", response_class=HTMLResponse)
def list_questions(request: Request):
    db = SessionLocal()
    questions = db.query(Question).all()
    db.close()
    return templates.TemplateResponse("admin_questions.html", {
        "request": request,
        "questions": questions
    })

# ✅ 새 질문 폼 페이지
@router.get("/new", response_class=HTMLResponse)
def new_question_form(request: Request):
    return templates.TemplateResponse("new_question.html", {
        "request": request
    })

# ✅ 질문 저장 처리
@router.post("/")
def create_question(question_text: str = Form(...)):
    db = SessionLocal()
    q = Question(question_text=question_text)
    db.add(q)
    db.commit()
    db.close()
    return RedirectResponse(url="/admin/questions", status_code=303)

# ✅ 질문 삭제 처리
@router.post("/delete")
def delete_question(question_id: int = Form(...)):
    db = SessionLocal()
    q = db.query(Question).filter(Question.id == question_id).first()
    if q:
        db.delete(q)
        db.commit()
    db.close()
    return RedirectResponse(url="/admin/questions", status_code=303)

# ✅ 줄바꿈 기반 다중 질문 추가
@router.post("/add")
def add_questions(request: Request, question_text: str = Form(...)):
    db = SessionLocal()
    lines = question_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line:
            db.add(Question(question_text=line))  # ← 수정 완료
    db.commit()
    db.close()
    return RedirectResponse(url="/admin/questions/", status_code=303)


@router.get("/more", response_class=HTMLResponse)
def show_additional_question(request: Request):
    question = get_random_question()

    if not question:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "📌 더 이상 제공할 질문이 없습니다."
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question
    })