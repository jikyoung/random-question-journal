from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnswerCreate(BaseModel):
    question_id: int
    user_id: int
    answer_text: str

class AnswerOut(BaseModel):
    id: int
    question_id: int
    user_id: int
    answer_text: str
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ Pydantic v2 대응 (기존 orm_mode 대체)