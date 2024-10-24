import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper_factory import ScraperFactory

base_categories = {
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
}

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
    {'base_url': 'https://www.elnekhelytechnology.com', 'store_name': 'Elnekhely Technology', 'categories': base_categories},
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