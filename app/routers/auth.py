from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import httpx
from dotenv import load_dotenv
from urllib.parse import quote
from app.database import SessionLocal
from passlib.hash import bcrypt
from app import models

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

# ✅ 로그인 선택 화면 (카카오 + 이메일)
@router.get("/login", response_class=HTMLResponse)
def login_options(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# ✅ 카카오 로그인 시작
@router.get("/login/kakao")
def login_kakao():
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?response_type=code"
        f"&client_id={KAKAO_CLIENT_ID}"
        f"&redirect_uri={KAKAO_REDIRECT_URI}"
        f"&scope=profile_nickname"
    )
    return RedirectResponse(kakao_auth_url)

# ✅ 카카오 로그인 콜백 처리
@router.get("/callback")
async def kakao_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code found in callback URL"}

    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=token_data, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })
        token_json = token_response.json()
        access_token = token_json.get("access_token")

        if not access_token:
            return {"error": "Failed to get access token", "details": token_json}

        user_info_url = "https://kapi.kakao.com/v2/user/me"
        user_response = await client.get(user_info_url, headers={
            "Authorization": f"Bearer {access_token}"
        })
        user_json = user_response.json()

    kakao_id = user_json.get("id")
    nickname = user_json.get("properties", {}).get("nickname") or f"사용자{str(kakao_id)[-4:]}"
    encoded_nickname = quote(nickname)

    request.session["nickname"] = nickname

    response = RedirectResponse(url="/")
    response.set_cookie(key="user_id", value=str(kakao_id))
    response.set_cookie(key="nickname", value=encoded_nickname)
    return response

# ✅ 이메일 회원가입 폼
@router.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# ✅ 이메일 회원가입 처리
@router.post("/signup")
def handle_signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    nickname: str = Form(...)
):
    db = SessionLocal()
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        db.close()
        return HTMLResponse("이미 존재하는 이메일입니다.", status_code=400)

    hashed_pw = bcrypt.hash(password)
    new_user = models.User(email=email, hashed_password=hashed_pw, nickname=nickname)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    request.session["nickname"] = nickname

    encoded_nickname = quote(nickname)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_id", value=str(new_user.id))
    response.set_cookie(key="nickname", value=encoded_nickname)
    return response

# ✅ 이메일 로그인 폼
@router.get("/login/email", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# ✅ 이메일 로그인 처리
@router.post("/login/email")
def handle_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == email).first()
    db.close()

    if not user or not bcrypt.verify(password, user.hashed_password):
        return HTMLResponse("이메일 또는 비밀번호가 올바르지 않습니다.", status_code=400)

    request.session["nickname"] = user.nickname

    encoded_nickname = quote(user.nickname)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_id", value=str(user.id))
    response.set_cookie(key="nickname", value=encoded_nickname)
    return response

# ✅ 로그아웃 처리
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("user_id")
    response.delete_cookie("nickname")
    return response