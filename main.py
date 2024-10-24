import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for categories
base_url = 'https://sigma-computer.com/subcategory'

# List of categories and subcategories
categories = {
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
}

# Function to scrape product details from a given subcategory URL
def scrape_products(subcategory_url):
    response = requests.get(subcategory_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []

        # Find product items based on the provided HTML structure
        product_items = soup.find_all('div', class_='product-layout')

        for item in product_items:
            name = item.find('a', title=True).get('title', '').strip()
            price = item.find('span', class_='price-new').get_text(strip=True)

            # Check stock status
            add_to_cart_button = item.find('button', class_='addToCart')
            if add_to_cart_button and 'out of stock' in add_to_cart_button.get_text(strip=True).lower():
                stock_status = 'Out of Stock'
            else:
                stock_status = 'In Stock'

            products.append({
                'name': name,
                'price': price,
                'stock_status': stock_status,
            })

        return products
    else:
        print(f"Failed to load {subcategory_url}")
        return []

# Main function to loop over all categories and subcategories
def scrape_all_categories():
    all_products = []

    for category, subcategories in categories.items():
        for subcategory in subcategories:
            subcategory_url = f'{base_url}?id=1&cname={category}&id2=1&scname={subcategory.replace(" ", "%20")}'
            print(f"Scraping {subcategory_url}")
            products = scrape_products(subcategory_url)

            # Append category and subcategory to each product data
            for product in products:
                product['category'] = category
                product['subcategory'] = subcategory

            all_products.extend(products)

    return all_products

# Run the scraping process
scraped_data = scrape_all_categories()

# Convert the scraped data to a DataFrame
df = pd.DataFrame(scraped_data)

# Save the DataFrame to an Excel file
df.to_excel('scraped_products.xlsx', index=False)

print("Data has been saved to scraped_products.xlsx")