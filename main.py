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
        'Monitors': ['4K / 2K Monitors', 'Curved Monitors', 'Gaming Monitors'],
        'VGA': 'vga',
        'Cooling': 'cooling',
        'Power Supply': 'power-supply',
        'Accessories': ['Chairs', 'DVD', 'Flash Memory', 'Game PAD', 'Headphones', 'Laptop']
    }}
]

def scrape_website(base_url, store_name, categories):
    scraper = ScraperFactory.get_scraper(base_url, store_name, categories)
    all_products = []

    for category, subcategories in categories.items():
        if isinstance(subcategories, list):
            for subcategory in subcategories:
                subcategory_url = f'{base_url}?id=1&cname={category}&id2=1&scname={subcategory.replace(" ", "%20")}'
                print(f"Scraping {subcategory_url} for {store_name}")
                products = scraper.scrape_products(subcategory_url, store_name)

                for product in products:
                    product['category'] = category
                    product['subcategory'] = subcategory

                all_products.extend(products)
        else:
            subcategory_url = f'{base_url}/{subcategories}'
            print(f"Scraping {subcategory_url} for {store_name}")
            products = scraper.scrape_products(subcategory_url, store_name)

            for product in products:
                product['category'] = category
                product['subcategory'] = subcategories

            all_products.extend(products)

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