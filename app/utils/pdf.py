# app/utils/pdf.py

import weasyprint
from app.crud import get_all_answers

def generate_pdf():
    answers = get_all_answers()

    html = """
    <h1 style="font-family: sans-serif;">✨ 내 답변 모음</h1>
    <hr>
    """

    for a in answers:
        html += f"""
        <p><strong>{a['created_at'][:16]}</strong><br>
        {a['answer_text']}</p>
        <hr>
        """

    return weasyprint.HTML(string=html).write_pdf()