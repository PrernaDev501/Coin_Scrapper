import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

class CoinMarketCapScraper:
    def __init__(self):
        self.base_url = 'https://coinmarketcap.com/currencies/'

    def scrape_coin_data(self, coin):
        url = f"{self.base_url}{coin}/"
        driver = webdriver.Chrome()
        driver.get(url)

        try:
            data = {
                "price": self.get_element_text(driver, "price"),
                "price_change": self.get_element_text(driver, "price-change"),
                # Add other fields similarly
            }
        except Exception as e:
            print(f"Error scraping data for {coin}: {e}")
            data = None

        driver.quit()
        return data

    def get_element_text(self, driver, class_name):
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            return element.text
        except Exception as e:
            print(f"Error retrieving element text: {e}")
            return None

class CoinMarketCapAPI:
    def __init__(self):
        self.scraper = CoinMarketCapScraper()

    def get_coin_data(self, coin):
        data = self.scraper.scrape_coin_data(coin)
        if data:
            return {"coin": coin, "data": data}
        else:
            return {"error": f"Failed to retrieve data for {coin}"}
