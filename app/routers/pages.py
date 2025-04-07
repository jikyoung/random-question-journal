from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from app.utils.pdf import generate_pdf
from app.crud import get_random_question, save_answer, get_all_answers
import io

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ✅ 질문 페이지: 로그인한 사용자만 접근 가능
@router.get("/", response_class=HTMLResponse)
def show_question(request: Request):
    user_id = request.cookies.get("user_id")
    nickname = request.cookies.get("nickname")

    if not user_id:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "로그인이 필요합니다.",
            "nickname": nickname
        })

    question = get_random_question(int(user_id))  # 👈 문자열 → 정수형 변환 필수

    if not question:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "📌 모든 질문을 완료했어요!\n새로운 질문이 없어요. 내일 다시 확인해보세요 🙂",
            "nickname": nickname
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question,
        "nickname": nickname
    })


# ✅ 답변 제출 처리
@router.post("/submit")
def submit_answer(request: Request, question_id: int = Form(...), answer_text: str = Form(...)):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse(url="/", status_code=303)

    save_answer(question_id, int(user_id), answer_text)
    return RedirectResponse(url="/pages/answers", status_code=303)


# ✅ 사용자 답변 목록 조회
@router.get("/pages/answers", response_class=HTMLResponse)
def show_answers(request: Request):
    user_id = request.cookies.get("user_id")
    nickname = request.cookies.get("nickname")

    if not user_id:
        return RedirectResponse(url="/", status_code=303)

    answers = get_all_answers(int(user_id))

    return templates.TemplateResponse("answers.html", {
        "request": request,
        "answers": answers,
        "nickname": nickname
    })


# ✅ PDF 내보내기
@router.get("/export/pdf")
def export_pdf():
    pdf = generate_pdf()
    return StreamingResponse(io.BytesIO(pdf), media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=answers.pdf"
    })