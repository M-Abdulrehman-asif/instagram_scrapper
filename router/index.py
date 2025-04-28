import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from utils.schemas import ScraperRequest, PostData
from database.database_manager import DatabaseHandler
from utils.insert import insert_instagram_data
from apify.instagram_crawler import instagram_crawl
from typing import List

router = APIRouter()

load_dotenv()

APIFY_TOKEN = os.getenv('APIFY_TOKEN')

if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN environment variable not set.")

@router.post("/scrape_instagram", response_model=List[PostData])
async def scrape_instagram(scraper_request: ScraperRequest):

    missing_fields = [field for field, value in scraper_request.model_dump().items() if not value]
    if missing_fields:
        print(f"Missing fields: {', '.join(missing_fields)}")
        raise HTTPException(status_code=400, detail=f"Please provide the {', '.join(missing_fields)} field(s).")

    if scraper_request.scraper != "instagram":
        raise HTTPException(status_code=400, detail="Only Instagram scraper is supported currently.")
    print(f"All fields are provided, proceeding with scraping for Instagram user: {scraper_request.username}.")

    data = scraper_request

    db_handler = DatabaseHandler(db_name=data.db_name)
    try:
        print("Initializing database connection...")
        db_handler.create_db()
        db_handler.connect_db()
        db_handler.init_db()
    except Exception as db_err:
        raise HTTPException(status_code=500, detail=f"Database connection error: {db_err}")
    session = db_handler.session
    try:
        posts = await instagram_crawl(data.username, data.no_of_posts)
        print(f"Instagram crawl completed. Posts fetched: {len(posts)}.")

        if not posts:
            print("No posts returned from crawl.")

        print("Inserting Instagram data into the database...")
        result = insert_instagram_data(data, posts, session)
        print(f"Data inserted successfully, returning response.")
        return result
    except Exception as e:
        print(f"An error occurred during Instagram scrape: {type(e).__name__} - {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        print("Closing database session...")
        session.close()
