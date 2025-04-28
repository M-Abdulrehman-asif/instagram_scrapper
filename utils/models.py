from sqlalchemy import Column, Integer, String, Text, UnicodeText
from database.database_manager import Base

class InstagramPost(Base):
    __tablename__ = 'instagram'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    post_url = Column(String)
    likes = Column(Integer)
    description = Column(String)
    comments = Column(UnicodeText)
