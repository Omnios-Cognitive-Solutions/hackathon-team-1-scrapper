import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys

# from .utils.files_management_toolbox import get_extension
# from .utils.selenium_toolbox import BaseSeleniumCrawler
# from .utils.string_toolbox import convert_to_kebab_case
# from .utils.vartypes_toolbox import check_type


class LinkedInScrapper:

    _url = "https://www.linkedin.com/"

    # Public:
    def __init__(self, proxy=None):
        if proxy:
            raise NotImplementedError("Proxy is not implemented yet")
        self._logger = logging.getLogger(__name__)
        self._driver = webdriver.Firefox()

    def login(self, username: str, password: str) -> bool:
        try:
            self._driver.get("https://www.linkedin.com/")

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

    def get_profile(self, username):
        raise NotImplementedError
