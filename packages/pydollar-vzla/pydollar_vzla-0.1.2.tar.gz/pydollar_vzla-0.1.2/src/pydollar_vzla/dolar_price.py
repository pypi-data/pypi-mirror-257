import inspect
from typing import List  # noqa

from pydollar_vzla.config.driver_config import SUPPORTED_DRIVER_TYPES
from pydollar_vzla.sources import bcv, dolartoday, monitordolar
from pydollar_vzla.sources.base import DolarSource


class DolarPrice:
    def __init__(self):
        self.extractors = self._get_all_extractors()

    def _get_all_extractors(self) -> list[DolarSource]:
        """
        Use reflection to get all classes that implement the DolarSource interface.
        """
        all_extractors = []
        for module in [bcv, dolartoday, monitordolar]:
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, DolarSource)
                    and obj != DolarSource
                ):
                    if "driver_type" in inspect.signature(obj.__init__).parameters:
                        extractor_instance = obj(SUPPORTED_DRIVER_TYPES["DriverChrome"])
                    else:
                        extractor_instance = obj()
                    all_extractors.append(extractor_instance)
        return all_extractors

    def add_extractor(self, extractor: DolarSource):
        """
        Add an extractor to the list of extractors.
        """
        self.extractors.append(extractor)

    def get_all_extractors(self) -> list[DolarSource]:
        """
        Gets all extractors that implement the DolarSource interface.
        """
        return self.extractors

    def get_all_dolar_prices(self):
        """
        Obtains prices from all data sources.
        """
        all_prices = {}
        for extractor in self.extractors:
            price = extractor.get_dolar_price()
            all_prices[extractor.get_name()] = price
        return all_prices
