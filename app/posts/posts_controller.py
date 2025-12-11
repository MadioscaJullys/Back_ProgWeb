# app/posts/post_controller.py
from fastapi import APIRouter, Depends, UploadFile, Form
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user
from posts_service import create_new_post, get_feed

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/")
def create_post(
    title: str = Form(...),
    description: str = Form(...),
    city: str = Form(...),
    image: UploadFile = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return create_new_post(db, user.id, title, description, city, image)


@router.get("/")
def list_posts(
    city: str | None = None,
    db: Session = Depends(get_db)
):
    return get_feed(db, city)
