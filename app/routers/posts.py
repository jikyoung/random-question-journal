from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/posts")
def read_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})

@router.post("/posts")
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    nickname = request.session.get("nickname", "익명")
    print("🧪 현재 세션 nickname:", nickname)
    
    nickname = request.session.get("nickname", "익명")
    new_post = models.Post(title=title, content=content, nickname=nickname)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=302)