from fastapi import Request
from urllib.parse import unquote

def get_current_user(request: Request):
    user_id = request.cookies.get("user_id")
    nickname = request.cookies.get("nickname")
    if nickname:
        nickname = unquote(nickname)
    return {
        "user_id": user_id,
        "nickname": nickname
    }