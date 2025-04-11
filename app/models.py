from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)  # ✅ 템플릿에서는 이 필드를 사용

    # 관계 설정 (답변들)
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, nullable=True)
    answer_text = Column(String)
    created_at = Column(String)

    # 관계 역방향 설정
    question = relationship("Question", back_populates="answers")