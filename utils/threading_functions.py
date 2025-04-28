from utils.schemas import ScraperRequest
from database.database_manager import DatabaseHandler
from utils.insert import insert_instagram_data
from apify.instagram_crawler import instagram_crawl
import asyncio


def process_instagram(data: ScraperRequest):
    db_handler = DatabaseHandler(db_name=data.db_name)
    try:
        print("Initializing database connection...")
        db_handler.create_db()
        db_handler.connect_db()
        db_handler.init_db()
    except Exception as db_err:
        print(f"Database connection error: {db_err}")
        return

    session = db_handler.session
    try:
        posts = asyncio.run(instagram_crawl(data.username, data.no_of_posts))
        print(f"Instagram crawl completed. Posts fetched: {len(posts)}.")

        if not posts:
            print("No posts returned from crawl.")

        print("Inserting Instagram data into the database...")
        insert_instagram_data(data, posts, session)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred during Instagram scrape: {type(e).__name__} - {e}")
    finally:
        print("Closing database session...")
        session.close()
