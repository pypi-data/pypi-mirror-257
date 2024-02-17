import re

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pydollar_vzla.config.driver_config import DriverConfig

from .base import DolarSource
from .urls import URL_DOLARTODAY


class DolarTodayExtractor(DolarSource):
    """
    Class to extract parallel dollar data from the DolarToday website.
    """

    def __init__(self, driver_type: str):
        """
        Initializes the DolarTodayExtractor instance with the specified driver type.

        Args:
            driver_type (str): Type of driver to use for web scraping.
        """
        super().__init__(driver_type)
        self._url = URL_DOLARTODAY
        self._driver = DriverConfig(driver_type)

    def get_dolar_data(self):
        """
        Retrieves the raw data of the parallel dollar from the DolarToday website.

        Returns:
            str: Raw data of the parallel dollar.
        """
        try:
            driver = self._driver.get_driver()
            driver.get(self._url)

            amount_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "amount"))
            )

            amount_input.clear()
            amount_input.send_keys("1")

            calculate_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "calculate-button"))
            )

            calculate_button.click()

            WebDriverWait(driver, 10).until(
                lambda driver: not EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "#dt-currency-calculator-results p"), "Bs. 0"
                )(driver)
            )

            html_content = driver.page_source

            driver.quit()
            soup = BeautifulSoup(html_content, "html.parser")
            results_div = soup.find("div", id="dt-currency-calculator-results")

            parallel_dollar_span = results_div.find("span", text="Dólar Paralelo")

            price = "0:0"
            if parallel_dollar_span:
                parent_element = parallel_dollar_span.parent
                parallel_dollar_text = parent_element.get_text(strip=True)
                price = parallel_dollar_text.split(":")[1]
                price = price.split("Bs.")[1]
            return price

        except TimeoutException:
            print("Timeout when waiting for an element on the page.")
            return None

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None

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

    def get_dolar_price(self) -> float:
        """
        Retrieves the price of the parallel dollar.

        Returns:
            float: Price of the parallel dollar.
        """
        price = self.clean_data()
        return price if price > 0 else None

    def get_name(self):
        return "DolarToday"
