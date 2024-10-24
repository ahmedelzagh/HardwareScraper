import requests
from bs4 import BeautifulSoup
import time

class WebsiteScraper:
    def __init__(self, base_url, store_name, categories):
        self.base_url = base_url
        self.store_name = store_name
        self.categories = categories

    def scrape_products(self, subcategory_url, website):
        products = []
        page = 1
        max_retries = 3
        retry_delay = 5  # seconds

        while True:
            for attempt in range(max_retries):
                response = requests.get(f"{subcategory_url}?page={page}")
                if response.status_code == 200:
                    break
                elif response.status_code == 524:
                    print(f"Timeout error on {subcategory_url}?page={page}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Failed to load {subcategory_url}?page={page} with status code {response.status_code}")
                    return products

            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            product_items = self.extract_product_items(soup, website)

            if not product_items:
                print(f"No products found on {subcategory_url}?page={page}")
                break

            for item in product_items:
                try:
                    product = self.extract_product_details(item, website)
                    products.append(product)
                except AttributeError as e:
                    print(f"Error processing item on {subcategory_url}?page={page}: {e}")
                    continue

            page += 1

        return products

    def extract_product_items(self, soup, website):
        raise NotImplementedError("This method should be implemented by subclasses")

    def extract_product_details(self, item, website):
        raise NotImplementedError("This method should be implemented by subclasses")