# app/routers/scrape.py

from fastapi import APIRouter, Depends
from app.dependencies import authenticate
from app.models import ScrapeRequest
from app.services.scraper import Scraper
from app.services.database import Database
from app.services.notifier import Notifier
from app.services.cache import Cache
from app.config import settings
import json

router = APIRouter(
    prefix="/scrape",
    tags=["scrape"],
    dependencies=[Depends(authenticate)],
)

@router.post("/")
def scrape_products(request: ScrapeRequest):
    scraper = Scraper(base_url=settings.SCRAPER_BASE_URL, max_pages=request.max_pages, proxy=request.proxy)
    database = Database(filepath=settings.JSON_FILE_PATH)
    notifier = Notifier()
    cache = Cache()

    # cache.client.flushall()

    scraped_data = scraper.scrape()
    if scraped_data:
        filtered_data = []
        for product in scraped_data:
            cache_key = f"{product['product_title']}_{product['path_to_image']}"
            if not cache.exists(cache_key):
                cache.set(cache_key, product)
                filtered_data.append(product)
            else:
                cache_data = cache.get(cache_key)
                if cache_data["product_price"] != product["product_price"]:
                    cache.update(cache_key, product)
                    filtered_data.append(cache_data)
                else:
                    filtered_data.append(cache_data)

            #Add else condition to pick and update value
        database.save_data(filtered_data)
        notifier.notify(f"Scraped {len(filtered_data)} products and updated the database.")
    return {"message": "Scraping completed."}
