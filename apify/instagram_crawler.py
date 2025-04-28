import os
from apify_client import ApifyClientAsync
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv('APIFY_TOKEN')

if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN environment variable not set.")

async def instagram_crawl(username: str, limit: int):
    print(f"Scraping Instagram posts for {username}...")

    apify_client = ApifyClientAsync(APIFY_TOKEN)
    print(f"Apify client initialized with token: {APIFY_TOKEN[:5]}...")

    actor_client = apify_client.actor('apify/instagram-post-scraper')
    print(f"Starting the actor for username: {username}...")

    try:
        call_result = await actor_client.call(run_input={"username": [username], "resultsLimit": limit})
        print("Actor call result received.")

        if call_result is None:
            print('Actor run failed, no result returned.')
            return []

        print(f"Actor run successful. Dataset ID: {call_result['defaultDatasetId']}")

        dataset_client = apify_client.dataset(call_result['defaultDatasetId'])
        print(f"Fetching dataset with ID: {call_result['defaultDatasetId']}...")

        list_page = await dataset_client.list_items()
        print(f"Dataset fetched. Total items: {len(list_page.items)}")

        list_items_result = list_page.items

        if not list_items_result:
            print("No posts found for the given username.")
            return []

        limited_items = list_items_result[:limit] if len(list_items_result) > limit else list_items_result
        print(f"Limiting to {limit} posts.")

        post_data = []

        for item in limited_items:
            print(f"Processing post with URL: {item.get('url', 'Unknown URL')}")

            post_details = {
                "post_url": item.get('url', None),
                "description": item.get('caption', None),
                "comments": [comment['text'] for comment in item.get('latestComments', [])],
                "likes": item.get('likesCount', None),
            }

            print(f"Post details: {post_details}")
            post_data.append(post_details)

        print(f"Extracted post data: {post_data}")
        return post_data

    except Exception as e:
        print(f"An error occurred during the actor call: {type(e).__name__}: {e}")
        return []
