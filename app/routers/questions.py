from fastapi import APIRouter
import random
import json

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/random")
def get_random_question():
    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
    return random.choice(questions)

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import random
# import json
# import logging

# router = APIRouter(prefix="/questions", tags=["questions"])

# # ✅ 질문 스키마 정의
# class Question(BaseModel):
#     id: int
#     question: str

# # ✅ 앱 시작 시 질문 파일 읽기 (캐싱용)
# try:
#     with open("questions.json", "r", encoding="utf-8") as f:
#         questions_data = json.load(f)
#         if not isinstance(questions_data, list):
#             raise ValueError("questions.json must contain a list of questions")
# except Exception as e:
#     logging.error(f"Failed to load questions.json: {e}")
#     questions_data = []

# @router.get("/random", response_model=Question)
# def get_random_question():
#     if not questions_data:
#         raise HTTPException(status_code=500, detail="No questions available.")
#     return random.choice(questions_data)
