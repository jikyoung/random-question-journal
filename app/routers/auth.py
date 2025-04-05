from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
load_dotenv()  # .env 파일에서 환경변수 로드
from fastapi import Request

router = APIRouter()

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

@router.get("/login/kakao")
def login_kakao():
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?response_type=code"
        f"&client_id={KAKAO_CLIENT_ID}"
        f"&redirect_uri={KAKAO_REDIRECT_URI}"
    )
    return RedirectResponse(kakao_auth_url)


@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code found in callback URL"}

    # 액세스 토큰 요청
    import httpx

    token_url = "https://kauth.kakao.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)
        token_json = response.json()

    return token_json

@router.get("/login/kakao/callback")
async def kakao_callback(code: str):
    token_url = "https://kauth.kakao.com/oauth/token"
    user_info_url = "https://kapi.kakao.com/v2/user/me"

    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        # 액세스 토큰 요청
        token_res = await client.post(token_url, data=data)
        token_json = token_res.json()
        access_token = token_json.get("access_token")

        # 사용자 정보 요청
        headers = {"Authorization": f"Bearer {access_token}"}
        user_res = await client.get(user_info_url, headers=headers)
        user_json = user_res.json()

        # 사용자 정보 추출
        kakao_id = user_json.get("id")
        nickname = user_json.get("properties", {}).get("nickname")

        return {"kakao_id": kakao_id, "nickname": nickname}