from pydantic import BaseModel
from typing import List, Literal, Optional

class CommentData(BaseModel):
    text: str

class PostData(BaseModel):
    post_url: str
    likes: Optional[int] = None
    description: Optional[str] = None
    comments: Optional[List[CommentData]] = None

class ScraperRequest(BaseModel):
    username: str
    scraper: Literal['instagram', 'twitter']
    no_of_posts: int
    db_name: str
