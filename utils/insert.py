from sqlalchemy.orm import Session
from utils.models import InstagramPost, InstagramComment
from utils.schemas import ScraperRequest, PostData

def insert_instagram_data(data: ScraperRequest, posts: list[dict], session: Session) -> list[PostData]:
    response = []

    for post in posts:
        post_obj = InstagramPost(
            username=data.username,
            post_url=post["post_url"],
            likes=post["likes"],
            description=post["description"]
        )
        session.add(post_obj)
        session.flush()

        comments_list = []
        for comment in post["comments"]:
            if isinstance(comment, dict):
                text = comment.get("text", "")
            else:
                text = comment

            comment_obj = InstagramComment(
                text=text,
                post_id=post_obj.id
            )
            session.add(comment_obj)
            comments_list.append({"text": text})

        response.append(PostData(
            post_url=post["post_url"],
            likes=post["likes"],
            description=post["description"],
            comments=comments_list
        ))

    session.commit()
    return response
