import re

from playwright._impl._errors import TimeoutError
from playwright.sync_api import sync_playwright

from .base import DolarSource
from .urls import URL_DOLARTODAY


class DolarTodayExtractor(DolarSource):
    """
    Class to extract parallel dollar data from the DolarToday website.
    """

    def __init__(self):
        """
        Initializes the DolarTodayExtractor instance with the specified driver type.

        Args:
            driver_type (str): Type of driver to use for web scraping.
        """
        self._url = URL_DOLARTODAY

    def get_dolar_data(self):
        """
        Retrieves the raw data of the parallel dollar from the DolarToday website.

        Returns:
            str: Raw data of the parallel dollar.
        """

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(self._url)

                page.wait_for_selector("#amount")
                amount_input = page.locator("#amount")
                amount_input.clear()
                amount_input.fill("1")

                page.wait_for_selector("#calculate-button")
                calculate_button = page.locator("#calculate-button")
                calculate_button.click()

                wait_function_script = """
                    function() {
                        const resultText = document.querySelector('#dt-currency-calculator-results p:nth-of-type(1)').textContent;
                        return resultText !== 'Dólar Paralelo: Bs. 0';
                    }
                """
                page.wait_for_function(wait_function_script)

                parallel_dollar_element = page.locator(
                    "#dt-currency-calculator-results p:nth-of-type(1)"
                )
                parallel_dollar_value = parallel_dollar_element.inner_text()

        except TimeoutError:
            print("Timeout when waiting for an element on the page - ", self.get_name())
            return None

        try:
            price = "0.0"
            if parallel_dollar_value:
                price = parallel_dollar_value.split(":")[1]
                price = price.split("Bs.")[1]
            return price

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None

    def clean_data(self) -> float:
        """
        Cleans the raw data of the parallel dollar and returns the cleaned price.

        Returns:
            float: Cleaned price of the parallel dollar.
        """
        price = self.get_dolar_data()
        if price is None:
            return 0
        cleaned_price_str = re.sub(r"[^\d.,]", "", price)
        cleaned_price_str = cleaned_price_str.replace(",", ".")
        cleaned_price = float(cleaned_price_str)
        cleaned_price = round(cleaned_price, 2)
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
