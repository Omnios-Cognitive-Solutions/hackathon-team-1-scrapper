import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LinkedInScrapper():

    _url = "https://www.linkedin.com/"

    # Public:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._driver = webdriver.Firefox()

    def login(self, username: str, password: str) -> bool:
        try:
            self._driver.get("https://www.linkedin.com/")

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

    def close_driver(self) -> None:
        self._driver.close()

    def get_profile(self, username: str):
        basic_data = self.get_basic_info(username)
        return basic_data

    def __get_element_text(self, *args, **kwargs) -> str:
        try:
            return self._driver.find_element(args[0], args[1]).text
        except NoSuchElementException:
            self._logger.warning(f"Element {kwargs['target']} not found")
            return None

    def get_basic_info(self, username: str) -> list[str]:
        self._driver.get(f'https://www.linkedin.com/in/{username}/')

        name = self.__get_element_text(By.CSS_SELECTOR, ".text-heading-xlarge", **{"target": "name"})
        position = self.__get_element_text(By.CSS_SELECTOR, ".text-body-medium", **{"target": "position"})
        location =  self.__get_element_text(By.CSS_SELECTOR, "span.text-body-small:nth-child(1)", **{"target": "location"})
        # nbr_followers = self.__get_element_text(By.CSS_SELECTOR, "li.text-body-small:nth-child(1) > span:nth-child(1)", **{"target": "number of followers"})
        # nbr_connections = self.__get_element_text(By.CSS_SELECTOR, "li.text-body-small:nth-child(2) > span:nth-child(1) > span:nth-child(1)", **{"target": "number of connection"})

        return [
            name,
            position,
            location
            # nbr_followers,
            # nbr_connections
        ]

