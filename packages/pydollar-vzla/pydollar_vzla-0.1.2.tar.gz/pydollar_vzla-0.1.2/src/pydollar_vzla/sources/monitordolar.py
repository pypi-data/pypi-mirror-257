import re

from bs4 import BeautifulSoup
from playwright._impl._errors import TimeoutError
from playwright.sync_api import sync_playwright

from .base import DolarSource
from .urls import URL_MONITORDOLAR


class MonitorDolarExtractor(DolarSource):
    def __init__(self):
        """
        Initializes the MonitorDolarExtractor instance with the specified driver type.

        Args:
            driver_type (str): Type of driver to use for web scraping.
        """
        self._url = URL_MONITORDOLAR

    def get_dolar_data(self) -> str:
        """
        Retrieves the raw data of the parallel dollar from the MonitorDolar website.

        Returns:
            str: Raw data of the parallel dollar.
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(self._url)

                html_content = page.content()

        except TimeoutError:
            print("Timeout when waiting for an element on the page - ", self.get_name())
            return None

        except Exception as e:
            print(f"Error downloading html content: {str(e)}")
            return None

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            result_div = soup.find("section", id="promedios")
            parallel_dollar_h3 = result_div.find("h3", text="@EnParaleloVzla3")
            parallal_dollar_data = parallel_dollar_h3.find_next_sibling("p")
            price = parallal_dollar_data.text.split("=")[1]

            return price

        except Exception as e:
            print(f"Error parsing html: {str(e)}")
            return None

    def get_dolar_price(self) -> float:
        """
        Retrieves the price of the parallel dollar.

        Returns:
            float: Price of the parallel dollar.
        """
        price = self.clean_data()
        return price if price > 0 else None

    def clean_data(self) -> float:
        """
        Cleans the raw data of the parallel dollar and returns the cleaned price.

        Returns:
            float: Cleaned price of the parallel dollar.
        """
        price = self.get_dolar_data()
        if price is None:
            return None
        cleaned_price_str = re.sub(r"[^\d.,]", "", price)
        cleaned_price_str = cleaned_price_str.replace(",", ".")
        cleaned_price = float(cleaned_price_str)
        return cleaned_price

    def get_name(self):
        return "MonitorDolar"
