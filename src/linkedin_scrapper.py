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

    def login(self, username, password):
        pass

    def get_profile(self, username):
        pass
