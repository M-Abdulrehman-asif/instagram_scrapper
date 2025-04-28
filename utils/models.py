from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database_manager import Base


class InstagramPost(Base):
    __tablename__ = 'instagram_posts'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    post_url = Column(String)
    likes = Column(Integer)
    description = Column(String)
    comments = relationship("InstagramComment", back_populates="post", cascade="all, delete-orphan")


class InstagramComment(Base):
    __tablename__ = 'instagram_comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    post_id = Column(Integer, ForeignKey("instagram_posts.id"))
    post = relationship("InstagramPost", back_populates="comments")
