import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper_factory import ScraperFactory

websites = [
    {'base_url': 'https://www.elnekhelytechnology.com', 'store_name': 'Elnekhely Technology', 'categories': {
        'Motherboard': 'motherboards',
        'Processor': 'processors',
        'RAM': 'ram',
        'SSD': 'ssd',
        'HDD': 'hdd',
        'Graphics Card': 'graphics-card',
        'Cases': 'cases',
        'Power Supply': 'power-supply',
        'Fans & Coolers': 'fans-coolers',
        'Monitors': 'monitors',
        'Accessories': 'accessories',
        'Bundles': 'bundeles'
    }},
    {'base_url': 'https://elbadrgroupeg.store', 'store_name': 'Elbadr Group', 'categories': {
        'Bundles': 'bundles',
        'CPU': 'cpu',
        'Motherboard': 'motherboard',
        'RAM': 'ram',
        'Cases': 'cases',
        'Hard': ['External', 'Internal'],
        'SSD': 'ssd',
        'Monitors': ['4K-2K-Monitors', 'Curved Monitors', 'Gaming Monitors'],
        'VGA': 'vga',
        'Cooling': 'cooling',
        'Power Supply': 'power-supply',
        'Accessories': ['Chairs', 'DVD', 'Flash Memory', 'Game PAD', 'Headphones'],
        'Laptop': 'Laptop',
    }},
    {'base_url': 'https://sigma-computer.com', 'store_name': 'Sigma Computer', 'categories': {
        'Desktop': {
            'Motherboard': {'id': 1, 'id2': 1},
            'Graphic Card': {'id': 1, 'id2': 2},
            'Ram': {'id': 1, 'id2': 3},
            'Processors': {'id': 1, 'id2': 4},
            'Desktop': {'id': 1, 'id2': 28},
            'Computer Case': {'id': 1, 'id2': 29},
            'Power Supply': {'id': 1, 'id2': 61},
        },
        'Notebook': {
            'RAM': {'id': 2, 'id2': 37},
            'NOTEBOOK FANS': {'id': 2, 'id2': 38},
            'NOTEBOOK ( LAPTOPS )': {'id': 2, 'id2': 40},
            'NOTEBOOK CASE': {'id': 2, 'id2': 41},
            'NOTEBOOK STORAGE': {'id': 2, 'id2': 46},
            'NOTEBOOK MSI': {'id': 2, 'id2': 68},
            'GeForce RTX 30 Series': {'id': 2, 'id2': 76},
            'Laptop Chargers & Adapters': {'id': 2, 'id2': 88},
        }
    }}
]

def scrape_website(base_url, store_name, categories):
    scraper = ScraperFactory.get_scraper(base_url, store_name, categories)
    all_products = []
    seen_urls = set()

    for category, subcategories in categories.items():
        if isinstance(subcategories, dict):
            for subcategory, ids in subcategories.items():
                subcategory_url = f'{base_url}/subcategory?id={ids["id"]}&id2={ids["id2"]}'
                print(f"Scraping {subcategory_url} for {store_name}")
                products = scraper.scrape_products(subcategory_url, store_name)

                for product in products:
                    product_url = product['product_url']
                    if product_url not in seen_urls:
                        product['category'] = category
                        product['subcategory'] = subcategory
                        all_products.append(product)
                        seen_urls.add(product_url)
        elif isinstance(subcategories, list):
            for subcategory in subcategories:
                subcategory_url = f'{base_url}/{category.lower().replace(" ", "-")}/{subcategory.lower().replace(" ", "-")}'
                print(f"Scraping {subcategory_url} for {store_name}")
                products = scraper.scrape_products(subcategory_url, store_name)

                for product in products:
                    product_url = product['product_url']
                    if product_url not in seen_urls:
                        product['category'] = category
                        product['subcategory'] = subcategory
                        all_products.append(product)
                        seen_urls.add(product_url)
        else:
            subcategory_url = f'{base_url}/{subcategories}'
            print(f"Scraping {subcategory_url} for {store_name}")
            products = scraper.scrape_products(subcategory_url, store_name)

            for product in products:
                product_url = product['product_url']
                if product_url not in seen_urls:
                    product['category'] = category
                    product['subcategory'] = subcategories
                    all_products.append(product)
                    seen_urls.add(product_url)

    return all_products

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