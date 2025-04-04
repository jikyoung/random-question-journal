from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.crud import get_random_question, save_answer, get_all_answers

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def show_question(request: Request):
    question = get_random_question()
    return templates.TemplateResponse("index.html", {"request": request, "question": question})

@router.post("/submit")
def submit_answer(question_id: int = Form(...), answer_text: str = Form(...)):
    save_answer(question_id, answer_text)
    return RedirectResponse(url="/pages/answers", status_code=303)  # ✅ 수정된 부분

@router.get("/pages/answers", response_class=HTMLResponse)  # ✅ 수정된 부분
def show_answers(request: Request):
    answers = get_all_answers()
    return templates.TemplateResponse("answers.html", {"request": request, "answers": answers})
