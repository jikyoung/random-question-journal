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
