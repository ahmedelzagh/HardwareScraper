# HardwareScraper

**HardwareScraper** is a specialized web scraping tool designed to extract product information from multiple hardware and computer e-commerce websites with varying HTML structures. The project is modularized to easily add new websites and handle different HTML layouts, making it a robust solution for aggregating hardware product data.

## Features

- Scrape product information from multiple hardware and computer e-commerce websites.
- Modular design to easily add new websites.
- Handles different HTML structures.
- Extracts product details such as name, URL, price, image URL, and stock status.
- Saves scraped data to an Excel file.

## Supported Websites

- Sigma Computer
- Elnekhely Technology
- Elbadr Group

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/ahmedelzagh/HardwareScraper.git
    cd HardwareScraper
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Update the `websites` list in `main.py` to include the websites you want to scrape.

2. Run the scraping process:

    ```sh
    python main.py
    ```

3. The scraped data will be saved to `scraped_products.xlsx`.

## Adding a New Website

1. Create a new scraper class for the website by extending `WebsiteScraper`.
2. Implement the `extract_product_items` and `extract_product_details` methods.
3. Update the `ScraperFactory` to include the new scraper.
4. Add the new website to the `websites` list in `main.py`.

## Example

```python
# Example of adding a new website to the websites list in main.py
websites = [
    {
        'base_url': 'https://example.com',
        'store_name': 'Example Store',
        'categories': {
            'Category1': 'category1',
            'Category2': 'category2'
        }
    }
]
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.
