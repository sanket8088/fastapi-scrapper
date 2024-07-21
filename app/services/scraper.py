import requests
from bs4 import BeautifulSoup
import time
from typing import Optional

class Scraper:
    def __init__(self, base_url: str, max_pages: Optional[int] = None, proxy: Optional[str] = None):
        self.base_url = base_url
        self.max_pages = max_pages
        self.proxy = proxy
        self.proxies = {"http": proxy, "https": proxy} if proxy else None

    def scrape_page(self, page_number: int, retries: int = 3, delay: int = 2):
        url = f"{self.base_url}/page/{page_number}/"
        attempt = 0

        while attempt < retries:
            try:
                response = requests.get(url, proxies=self.proxies)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    products = soup.select('.type-product')
                    result = []
                    for product in products:
                        title = product.select_one('.woo-loop-product__title a').get_text(strip=True)
                        price_element = product.select_one('.price')
                        if price_element:
                            sale_price = price_element.select_one('ins .woocommerce-Price-amount')
                            if sale_price:
                                price = sale_price.get_text(strip=True)
                            else:
                                price = price_element.get_text(strip=True)
                        else:
                            price = 'Price not found'

                        image_url_element = product.select_one('.mf-product-thumbnail img')
                        if image_url_element:
                            image_url = image_url_element.get('data-lazy-src') or image_url_element.get('src')
                        else:
                            image_url = "Image not available"

                        result.append({
                            "product_title": title,
                            "product_price": price,
                            "path_to_image": image_url,
                        })

                    return result
                else:
                    print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Request failed with error: {e}")
                time.sleep(delay)
                attempt += 1
                delay *= 2  # Exponential backoff

        return None

    def scrape(self):
        all_products = []
        page_number = 1
        while self.max_pages is None or page_number <= self.max_pages:
            print(f"Scraping page {page_number}")
            page_data = self.scrape_page(page_number)
            if not page_data:
                print(f"No data found on page {page_number}. Stopping.")
                break
            all_products.extend(page_data)
            page_number += 1
        return all_products
