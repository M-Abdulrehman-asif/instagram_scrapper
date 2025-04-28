import os
import threading
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from utils.schemas import ScraperRequest
from utils.threading_functions import process_instagram

router = APIRouter()

load_dotenv()

APIFY_TOKEN = os.getenv('APIFY_TOKEN')

if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN environment variable not set.")


@router.post("/scrape_instagram", response_model=dict)
async def scrape_instagram(scraper_request: ScraperRequest):
    missing_fields = [field for field, value in scraper_request.model_dump().items() if not value]
    if missing_fields:
        print(f"Missing fields: {', '.join(missing_fields)}")
        raise HTTPException(status_code=400, detail=f"Please provide the {', '.join(missing_fields)} field(s).")

    if scraper_request.scraper != "instagram":
        raise HTTPException(status_code=400, detail="Only Instagram scraper is supported currently.")

    print(f"All fields are provided, proceeding with scraping for Instagram user: {scraper_request.username}.")

    thread = threading.Thread(
        target=process_instagram,
        args=(scraper_request,)
    )
    thread.start()

    return {
        "message": "Instagram scraping started in background."
    }
