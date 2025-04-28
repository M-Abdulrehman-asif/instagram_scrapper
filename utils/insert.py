import json
from sqlalchemy.orm import Session
from utils.models import InstagramPost
from utils.schemas import ScraperRequest, PostData, CommentData

def insert_instagram_data(data: ScraperRequest, posts: list[dict], session: Session) -> list[PostData]:
    response = []

    for post in posts:
        comments = post.get("comments", [])
        comments_json = json.dumps(post.get("comments", []), ensure_ascii=False)
        print(comments_json)
        post_obj = InstagramPost(
            username=data.username,
            post_url=post["post_url"],
            likes=post["likes"],
            description=post["description"],
            comments=comments_json
        )
        session.add(post_obj)

        response.append(PostData(
            post_url=post["post_url"],
            likes=post["likes"],
            description=post["description"],
            comments=[CommentData(text=comment) for comment in comments]
        ))

    session.commit()
    return response
