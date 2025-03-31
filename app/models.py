from pydantic import BaseModel
from typing import Optional

class Question(BaseModel):
    id: int
    content: str

class Answer(BaseModel):
    id: Optional[int] = None
    question_id: int
    answer_text: str