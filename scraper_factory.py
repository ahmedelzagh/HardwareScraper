from sigma_computer_scraper import SigmaComputerScraper
from elnekhely_technology_scraper import ElnekhelyTechnologyScraper
from elbadr_group_scraper import ElbadrGroupScraper

class ScraperFactory:
    @staticmethod
    def get_scraper(base_url, store_name, categories):
        if store_name == 'Sigma Computer':
            return SigmaComputerScraper(base_url, store_name, categories)
        elif store_name == 'Elnekhely Technology':
            return ElnekhelyTechnologyScraper(base_url, store_name, categories)
        elif store_name == 'Elbadr Group':
            return ElbadrGroupScraper(base_url, store_name, categories)
        else:
            raise ValueError(f"No scraper available for store: {store_name}")