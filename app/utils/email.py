from fastapi_mail import FastMail, MessageSchema
from app.config import mail_config

async def send_verification_email(to_email: str, token: str):
    link = f"http://localhost:8000/auth/verify-email?token={token}"
    message = MessageSchema(
        subject="이메일 인증 - 오늘의 질문",
        recipients=[to_email],
        body=f"""안녕하세요!\n\n이메일 인증을 위해 아래 링크를 클릭해주세요:\n{link}\n\n감사합니다!""",
        subtype="html",
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)