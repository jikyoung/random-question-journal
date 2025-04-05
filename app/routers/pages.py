from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from app.utils.pdf import generate_pdf
import io

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


@router.get("/export/pdf")
def export_pdf():
    pdf = generate_pdf()
    return StreamingResponse(io.BytesIO(pdf), media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=answers.pdf"
    })

@router.get("/", response_class=HTMLResponse)
def show_question(request: Request):
    question = get_random_question()
    if not question:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "📌 모든 질문을 완료했어요!\n새로운 질문이 없어요. 내일 다시 확인해보세요 🙂"
        })
    return templates.TemplateResponse("index.html", {"request": request, "question": question})