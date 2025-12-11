from fastapi import UploadFile
from sqlalchemy.orm import Session
from .posts_model import Post
from .posts_repository import create_post, list_posts_by_city, list_all_posts
from ..utils.image_processor import save_image

def create_new_post(db: Session, user_id: int, title: str, description: str, city: str, image: UploadFile):
    
    image_path = None
    if image:
        image_path = save_image(image)

    post = Post(
        user_id=user_id,
        title=title,
        description=description,
        city=city,
        image_path=image_path
    )

    return create_post(db, post)

def get_feed(db: Session, city: str | None):
    if city:
        return list_posts_by_city(db, city)
    return list_all_posts(db)
