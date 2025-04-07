from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

@router.get("/login")
def login_kakao():
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?response_type=code"
        f"&client_id={KAKAO_CLIENT_ID}"
        f"&redirect_uri={KAKAO_REDIRECT_URI}"
    )
    return RedirectResponse(kakao_auth_url)


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
    nickname = user_json.get("properties", {}).get("nickname")

    response = RedirectResponse(url="/")
    response.set_cookie(key="user_id", value=str(kakao_id))
    response.set_cookie(key="nickname", value=nickname)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("user_id")
    response.delete_cookie("nickname")
    return response