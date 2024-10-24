import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Base URLs and store names for multiple websites
websites = [
    {'base_url': 'https://sigma-computer.com/subcategory', 'store_name': 'Sigma Computer', 'categories': {
        'Desktop': ['Motherboard', 'Graphic Card', 'Ram', 'Processors', 'Desktop', 'Computer Case', 'Power Supply'],
        'Notebook': ['RAM', 'NOTEBOOK FANS', 'NOTEBOOK ( LAPTOPS )', 'NOTEBOOK CASE', 'NOTEBOOK STORAGE', 'NOTEBOOK MSI', 'GeForce RTX 30 Series', 'Laptop Chargers & Adapters'],
        'Storage': ['External Hard', 'Internal Hard', 'SSD', 'M.2', 'External SSD', 'Memory Card', 'Flash Disk', 'Storage Accessories'],
        'Monitors': ['Monitors'],
        'Network': ['Router', 'Switch', 'Wireless USB Adapter', 'Access Point'],
        'Accessories': ['PC Cooling', 'Keyboards', 'Headphones', 'Keyboard & Mouse COMBO', 'Mouse Pad', 'PC Game Controllers', 'Speaker', 'microphones', 'PRESENTER', 'Chair', 'Webcam', 'CABLE', 'Fans', 'Thermal Paste', 'HOLDER', 'PUNGEE', 'Gaming Desk', 'Mouse', 'Capture box', 'Scales', 'Battary', 'LED strips'],
        'Bundles': ['POWERED BY ASUS', 'HERO', 'BUNDLES', 'PANDA', 'FIGHTER', 'Dragon', 'NINJA', 'JINX'],
        'Other': ['Projector', 'Camera', 'Printer', 'Scanner', 'DVD'],
        'Tools': ['Tools'],
        'Printer Ink & Toner': ['Laser Cartridge'],
        'P.O.S System': ['Cashier Printer', 'Barcode Printer', 'Cashier & Barcode Roll', 'Barcode Scanner'],
        'GAMING CONSOLES': ['Sony PlayStation', 'PS5 Accessories', 'Xbox', 'Xbox Accessories'],
        'T.V': ['T.V'],
        'Tablet': ['Tablet'],
        'software': ['software'],
        'MOBILE ACCESSORIES': ['wrist watch', 'Power Bank', 'Adapter / Cable'],
        'MOUSE ACCESSORIES': ['FEET', 'GRIP'],
        'Media Equipment': ['Media Equipment'],
        'Powered by ASUS': ['Powered by ASUS']
    }},
    {'base_url': 'https://www.elnekhelytechnology.com', 'store_name': 'Elnekhely Technology', 'categories': {
        'Motherboard': 'motherboards',
        'Processor': 'processors',
        'RAM': 'ram',
        'SSD': 'ssd',
        'HDD': 'hdd',
        'Graphics Card': 'graphics-cards',
        'Cases': 'cases',
        'Power Supply': 'power-supply',
        'Fans & Coolers': 'fans-coolers',
        'Monitors': 'monitors',
        'Accessories': 'accessories',
        'Bundles': 'bundles'
    }}
]

# Function to scrape product details from a given subcategory URL
def scrape_products(subcategory_url, store_name, website):
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
        if website == 'Sigma Computer':
            product_items = soup.find_all('div', class_='product-layout')
        elif website == 'Elnekhely Technology':
            product_items = soup.find_all('div', class_='product-layout')

        if not product_items:
            print(f"No products found on {subcategory_url}?page={page}")
            break

        for item in product_items:
            try:
                if website == 'Sigma Computer':
                    name = item.find('a', title=True).get('title', '').strip() if item.find('a', title=True) else 'N/A'
                    product_url = item.find('a', title=True).get('href', '').strip() if item.find('a', title=True) else 'N/A'
                    price = item.find('span', class_='price-new').get_text(strip=True) if item.find('span', class_='price-new') else 'N/A'
                    image_url = item.find('img', class_='img-1').get('src', '').strip() if item.find('img', class_='img-1') else 'N/A'
                    add_to_cart_button = item.find('button', class_='addToCart')
                    stock_status = 'Out of Stock' if add_to_cart_button and 'out of stock' in add_to_cart_button.get_text(strip=True).lower() else 'In Stock'
                elif website == 'Elnekhely Technology':
                    name = item.find('a', class_='product-img').get('title', '').strip() if item.find('a', class_='product-img') else 'N/A'
                    product_url = item.find('a', class_='product-img').get('href', '').strip() if item.find('a', class_='product-img') else 'N/A'
                    price = item.find('span', class_='price-normal').get_text(strip=True) if item.find('span', class_='price-normal') else 'N/A'
                    image_url = item.find('img', class_='img-responsive').get('src', '').strip() if item.find('img', class_='img-responsive') else 'N/A'
                    stock_status = item.find('span', class_='stat-2').find('span').get_text(strip=True) if item.find('span', class_='stat-2') and item.find('span', class_='stat-2').find('span') else 'N/A'

                products.append({
                    'name': name,
                    'product_url': product_url,
                    'price': price,
                    'image_url': image_url,
                    'stock_status': stock_status,
                    'store_name': store_name
                })
            except AttributeError as e:
                print(f"Error processing item on {subcategory_url}?page={page}: {e}")
                continue

        page += 1

    return products

# Function to scrape all categories for a given website
def scrape_website(base_url, store_name, categories):
    all_products = []

    for category, subcategories in categories.items():
        if isinstance(subcategories, list):
            for subcategory in subcategories:
                subcategory_url = f'{base_url}?id=1&cname={category}&id2=1&scname={subcategory.replace(" ", "%20")}'
                print(f"Scraping {subcategory_url} for {store_name}")
                products = scrape_products(subcategory_url, store_name, store_name)

                # Append category and subcategory to each product data
                for product in products:
                    product['category'] = category
                    product['subcategory'] = subcategory

                all_products.extend(products)
        else:
            subcategory_url = f'{base_url}/{subcategories}'
            print(f"Scraping {subcategory_url} for {store_name}")
            products = scrape_products(subcategory_url, store_name, store_name)

            # Append category and subcategory to each product data
            for product in products:
                product['category'] = category
                product['subcategory'] = subcategories

            all_products.extend(products)

    return all_products

# Main function to scrape multiple websites concurrently
def scrape_all_websites():
    all_products = []

    with ThreadPoolExecutor(max_workers=len(websites)) as executor:
        future_to_website = {executor.submit(scrape_website, site['base_url'], site['store_name'], site['categories']): site for site in websites}

        for future in as_completed(future_to_website):
            site = future_to_website[future]
            try:
                products = future.result()
                all_products.extend(products)
            except Exception as exc:
                print(f"{site['store_name']} generated an exception: {exc}")

    return all_products

# Run the scraping process
scraped_data = scrape_all_websites()

# Convert the scraped data to a DataFrame
df = pd.DataFrame(scraped_data)

# Reorder the DataFrame columns
df = df[['category', 'subcategory', 'name', 'product_url', 'price', 'image_url', 'stock_status', 'store_name']]

# Save the DataFrame to an Excel file
df.to_excel('scraped_products.xlsx', index=False)

print("Data has been saved to scraped_products.xlsx")