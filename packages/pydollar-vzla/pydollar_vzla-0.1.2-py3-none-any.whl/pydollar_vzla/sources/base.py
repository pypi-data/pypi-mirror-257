from abc import ABC, abstractmethod


class DolarSource(ABC):
    def __init__(self, driver_type=None):
        self._driver_type = driver_type

    @abstractmethod
    def get_dolar_data(self):
        pass

    @abstractmethod
    def clean_data(self):
        pass

    @abstractmethod
    def get_dolar_price(self):
        pass

    @abstractmethod
    def get_name(self):
        pass
