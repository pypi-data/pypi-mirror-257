import re

import requests
from bs4 import BeautifulSoup

from .base import DolarSource
from .urls import URL_BCV


class BCVExtractor(DolarSource):
    def __init__(self):
        """
        Initializes the BCVExtractor instance with the specified driver type.

        """
        self._url = URL_BCV

    def get_dolar_data(self) -> str:
        """
        Retrieves the raw data of the parallel dollar from the BCV website.

        Returns:
            str: Raw data of the parallel dollar.
        """

        response = requests.get(self._url, verify=False)
        html_content = response.content

        soup = BeautifulSoup(html_content, "lxml")

        dolar_div = soup.find("div", id="dolar")

        dolar_price = "0.0"
        if dolar_div:
            dolar_price = dolar_div.find("strong").text
        return dolar_price

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
        return "BCV"
