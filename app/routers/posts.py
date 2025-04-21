from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/posts")
def read_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    nickname = request.session.get("nickname", "익명")
    return templates.TemplateResponse("posts.html", {
        "request": request,
        "posts": posts,
        "session": {"nickname": nickname}  # ✨ 이걸 추가해야 템플릿에서 session.nickname 사용 가능
    })

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

@router.get("/posts/edit/{post_id}", response_class=HTMLResponse)
def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    nickname = request.session.get("nickname", "익명")
    if post.nickname != nickname:
        return RedirectResponse(url="/posts", status_code=302)

    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})

@router.post("/posts/edit/{post_id}")
def edit_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    nickname = request.session.get("nickname", "익명")
    if post.nickname != nickname:
        return RedirectResponse(url="/posts", status_code=302)

    post.title = title
    post.content = content
    db.commit()
    return RedirectResponse(url="/posts", status_code=302)