import re

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

from pydollar_vzla.config.driver_config import DriverConfig

from .base import DolarSource
from .urls import URL_MONITORDOLAR


class MonitorDolarExtractor(DolarSource):
    def __init__(self, driver_type: str):
        """
        Initializes the MonitorDolarExtractor instance with the specified driver type.

        Args:
            driver_type (str): Type of driver to use for web scraping.
        """
        super().__init__(driver_type)
        self._url = URL_MONITORDOLAR
        self._driver = DriverConfig(driver_type)

    def get_dolar_data(self) -> str:
        """
        Retrieves the raw data of the parallel dollar from the MonitorDolar website.

        Returns:
            str: Raw data of the parallel dollar.
        """
        try:
            driver = self._driver.get_driver()
            driver.get(self._url)

            driver.implicitly_wait(10)

            html_content = driver.page_source

            driver.quit()

            soup = BeautifulSoup(html_content, "html.parser")

            result_div = soup.find("section", id="promedios")
            parallel_dollar_h3 = result_div.find("h3", text="@EnParaleloVzla3")
            parallal_dollar_data = parallel_dollar_h3.find_next_sibling("p")
            price = parallal_dollar_data.text.split("=")[1]

            return price

        except TimeoutException:
            print("Timeout when waiting for an element on the page.")
            return None

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
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
        price = self.get_dolar_data() if self.get_dolar_data() else "0:0"
        cleaned_price_str = re.sub(r"[^\d.,]", "", price)
        cleaned_price_str = cleaned_price_str.replace(",", ".")
        cleaned_price = float(cleaned_price_str)
        return cleaned_price

    def get_name(self):
        return "MonitorDolar"
