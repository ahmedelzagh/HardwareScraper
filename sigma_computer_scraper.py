from website_scraper import WebsiteScraper

class SigmaComputerScraper(WebsiteScraper):
    def extract_product_items(self, soup, website):
        return soup.find_all('div', class_='product-layout')

    def extract_product_details(self, item, website):
        name = item.find('a', title=True).get('title', '').strip() if item.find('a', title=True) else 'N/A'
        product_url = item.find('a', title=True).get('href', '').strip() if item.find('a', title=True) else 'N/A'
        price = item.find('span', class_='price-new').get_text(strip=True) if item.find('span', class_='price-new') else 'N/A'
        image_url = item.find('img', class_='img-1').get('src', '').strip() if item.find('img', class_='img-1') else 'N/A'
        add_to_cart_button = item.find('button', class_='addToCart')
        stock_status = 'Out of Stock' if add_to_cart_button and 'out of stock' in add_to_cart_button.get_text(strip=True).lower() else 'In Stock'

        return {
            'name': name,
            'product_url': product_url,
            'price': price,
            'image_url': image_url,
            'stock_status': stock_status,
            'store_name': self.store_name
        }