from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)

    city = Column(String(100), nullable=False)

    image_path = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
