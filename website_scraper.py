import requests
from bs4 import BeautifulSoup
import time
import logging

# Configure logging
logging.basicConfig(filename='scraper_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class WebsiteScraper:
    def __init__(self, base_url, store_name, categories):
        self.base_url = base_url
        self.store_name = store_name
        self.categories = categories

    def scrape_products(self, subcategory_url, website):
        products = []
        seen_urls = set()
        page = 1
        max_retries = 3
        retry_delay = 5  # seconds
        last_product_count = 0
        consecutive_timeouts = 0
        max_consecutive_timeouts = 3  # Stop after 3 consecutive timeouts

        while True:
            for attempt in range(max_retries):
                try:
                    print(f"Requesting {subcategory_url}?page={page}")
                    response = requests.get(f"{subcategory_url}?page={page}", timeout=10)
                    if response.status_code == 200:
                        consecutive_timeouts = 0  # Reset timeout counter on success
                        break
                    elif response.status_code == 524:
                        print(f"Timeout error on {subcategory_url}?page={page}. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        consecutive_timeouts += 1
                        if consecutive_timeouts >= max_consecutive_timeouts:
                            print(f"Stopping due to {max_consecutive_timeouts} consecutive timeouts on {subcategory_url}?page={page}")
                            return products
                    else:
                        error_message = f"Failed to load {subcategory_url}?page={page} with status code {response.status_code}"
                        print(error_message)
                        logging.error(error_message)
                        return products
                except requests.exceptions.RequestException as e:
                    error_message = f"Request exception on {subcategory_url}?page={page}: {e}"
                    print(error_message)
                    logging.error(error_message)
                    time.sleep(retry_delay)
                    continue

            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            product_items = self.extract_product_items(soup, website)

            if not product_items:
                print(f"No products found on {subcategory_url}?page={page}. Exiting loop.")
                break

            for item in product_items:
                try:
                    product = self.extract_product_details(item, website)
                    product_url = product['product_url']
                    if product_url not in seen_urls:
                        products.append(product)
                        seen_urls.add(product_url)
                except AttributeError as e:
                    error_message = f"Error processing item on {subcategory_url}?page={page}: {e}"
                    print(error_message)
                    logging.error(error_message)
                    continue

            # Check if the number of products has increased
            if len(products) == last_product_count:
                print(f"No new products found on {subcategory_url}?page={page}. Exiting loop.")
                break

            last_product_count = len(products)
            page += 1
            print(f"Moving to next page: {page}")

        return products

    def extract_product_items(self, soup, website):
        raise NotImplementedError("This method should be implemented by subclasses")

    def extract_product_details(self, item, website):
        raise NotImplementedError("This method should be implemented by subclasses")