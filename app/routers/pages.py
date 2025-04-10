# 📁 app/routers/pages.py

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from app.utils.pdf import generate_pdf
from app.crud import get_question_for_today, save_answer, get_all_answers
import io
from app.auth_utils import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ✅ 질문 페이지: 로그인 여부와 관계없이 제공
@router.get("/", response_class=HTMLResponse)
def show_question(request: Request):
    user = get_current_user(request)
    user_id = user.get("user_id")
    nickname = user.get("nickname")

    print("🧪 user_id:", user_id)
    print("🧪 nickname:", nickname)

    try:
        user_id_int = int(user_id) if user_id else None
    except ValueError:
        user_id_int = None

    question = get_question_for_today()
    print("🧪 가져온 질문:", question)
    if question:
        print("🧪 질문 텍스트:", question.question_text)

    if not question:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "📌 오늘의 질문이 없습니다. 내일 다시 시도해보세요!",
            "nickname": nickname
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question,
        "nickname": nickname
    })


# ✅ 답변 저장: 로그인 여부와 관계없이 가능
@router.post("/submit")
def submit_answer(request: Request, question_id: int = Form(...), answer_text: str = Form(...)):
    user_id = request.cookies.get("user_id")
    try:
        user_id_int = int(user_id) if user_id else None
    except ValueError:
        user_id_int = None

    save_answer(question_id, user_id_int, answer_text)
    return RedirectResponse(url="/pages/answers", status_code=303)


# ✅ 사용자 답변 목록 조회: 로그인한 사용자만 해당 답변 조회
@router.get("/pages/answers", response_class=HTMLResponse)
def show_answers(request: Request):
    user = get_current_user(request)
    user_id = user.get("user_id")
    nickname = user.get("nickname")


    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        return RedirectResponse(url="/", status_code=303)

    answers = get_all_answers(user_id_int)

    return templates.TemplateResponse("answers.html", {
        "request": request,
        "answers": answers,
        "nickname": nickname
    })


# ✅ PDF 내보내기: 로그인한 사용자만 가능
@router.get("/export/pdf")
def export_pdf(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/", status_code=303)

    pdf = generate_pdf(int(user_id))
    return StreamingResponse(io.BytesIO(pdf), media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=answers.pdf"
    })
