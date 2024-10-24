from website_scraper import WebsiteScraper

class ElbadrGroupScraper(WebsiteScraper):
    def extract_product_items(self, soup, website):
        return soup.find_all('div', class_='product-layout')

    def extract_product_details(self, item, website):
        name = item.find('a', class_='product-img').get('title', '').strip() if item.find('a', class_='product-img') else 'N/A'
        product_url = item.find('a', class_='product-img').get('href', '').strip() if item.find('a', class_='product-img') else 'N/A'
        price = item.find('span', class_='price-normal').get_text(strip=True) if item.find('span', class_='price-normal') else 'N/A'
        image_url = item.find('img', class_='img-responsive').get('src', '').strip() if item.find('img', class_='img-responsive') else 'N/A'
        stock_status = 'Out of Stock' if 'out-of-stock' in item.get('class', []) else 'In Stock'

        return {
            'name': name,
            'product_url': product_url,
            'price': price,
            'image_url': image_url,
            'stock_status': stock_status,
            'store_name': self.store_name
        }