from selenium import webdriver

SUPPORTED_DRIVER_TYPES = {"DriverChrome": "Chrome"}


class DriverConfig:
    """Manages WebDriver creation based on the specified driver type."""

    def __init__(self, driver_type: str):
        """
        Initializes the DriverConfig instance.

        Args:
            driver_type: The type of WebDriver to create (e.g., "Chrome").
                Supported types are listed in the SUPPORTED_DRIVER_TYPES constant.
        """
        self._driver_type = driver_type

    def get_driver(self) -> webdriver.Chrome:
        """
        Retrieves an instance of the specified web driver.

        Returns:
            selenium.webdriver: Instance of the web driver.

        Raises:
            ValueError: If the driver type is not supported.
        """

        driver_creators = {
            "Chrome": webdriver.Chrome,
        }

        if self._driver_type not in driver_creators:
            raise ValueError(
                f"Driver type '{self._driver_type}' not supported. Supported types are: {', '.join(driver_creators.keys())}"
            )

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        return driver_creators[self._driver_type](options=options)

    def set_driver(self, new_driver_type: str) -> None:
        """
        Sets a new driver type.

        Args:
            new_driver_type (str): New driver type to set.
        """
        self._driver_type = new_driver_type
