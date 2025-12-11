from sqlalchemy.orm import Session
from posts_model import Post

def create_post(db: Session, post: Post):
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def list_posts_by_city(db: Session, city: str):
    return db.query(Post).filter(Post.city == city).order_by(Post.created_at.desc()).all()

def list_all_posts(db: Session):
    return db.query(Post).order_by(Post.created_at.desc()).all()
