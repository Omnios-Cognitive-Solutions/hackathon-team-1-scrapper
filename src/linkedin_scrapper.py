import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .utils.files_management_toolbox import get_extension
from .utils.selenium_toolbox import BaseSeleniumCrawler
from .utils.string_toolbox import convert_to_kebab_case
from .utils.vartypes_toolbox import check_type


class LinkedInScrapper(BaseSeleniumCrawler):

    _url = "https://www.linkedin.com/"

    # Public:
    def __init__(self, *args, **kwargs):
        url = self._url
        super().__init__(url, *args, **kwargs)
        self._logger = logging.getLogger(__name__)

    def login(self, username: str, password: str) -> bool:
        try:
            elem = self._driver.find_element(By.XPATH, "/html/body/nav/div/a[2]")  # nopep8
            elem.click()

            elem = self._driver.find_element(By.ID, "username")
            elem.send_keys(username)
            elem = self._driver.find_element(By.ID, "password")
            elem.send_keys(password)
            elem = self._driver.find_element(By.XPATH, "/html/body/div/main/div[3]/div[1]/form/div[3]/button")  # nopep8
            elem.click()

        except Exception as e:
            self._logger.error(e, exc_info=True)
            return False

        return True

    def get_profile(self, username):
        pass
