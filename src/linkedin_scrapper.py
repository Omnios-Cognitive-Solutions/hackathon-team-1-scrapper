import logging

from selenium import webdriver
from selenium.webdriver.common.by import By


class LinkedInScrapper:

    _base_url = "https://www.linkedin.com/"

    # Public:
    def __init__(self, headless: bool = True, proxy=None):
        if proxy:
            raise NotImplementedError("Proxy is not implemented yet")
        self._logger = logging.getLogger(__name__)
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        self._driver = webdriver.Firefox(options=options)

    def login(self, username: str, password: str) -> bool:
        try:
            self._driver.get(self._base_url)
            elem = self._driver.find_element(By.XPATH, "/html/body/nav/div/a[2]")
            elem.click()
            elem = self._driver.find_element(By.ID, "username")
            elem.send_keys(username)
            elem = self._driver.find_element(By.ID, "password")
            elem.send_keys(password)
            elem = self._driver.find_element(
                By.XPATH, "/html/body/div/main/div[3]/div[1]/form/div[3]/button"
            )
            elem.click()
        except Exception as e:
            self._logger.error(e, exc_info=True)
            return False

        return True

    def close_driver(self) -> None:
        self._driver.close()

    def get_profile(self, username: str):
        basic_data = self.get_basic_info(username)
        return basic_data
