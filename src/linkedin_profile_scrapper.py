import logging
from os.path import join as join_paths

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from src.exceptions import NotFoundProfileExperience, NotFoundProfileSections


class LinkedInProfileScrapper:

    _base_url = "https://www.linkedin.com/"

    # Public:
    @property
    def _sections(self) -> list:
        if not hasattr(self, "__sections") or self.__sections is None:
            self.__sections = self._get_profile_sections()
        return self.__sections

    @property
    def experience(self) -> list | None:
        if not hasattr(self, "__experience") or self.__experience is None:
            self.__experience = self.get_experience()
        return self.__experience

    @property
    def basic_info(self) -> list | None:
        if not hasattr(self, "__basic_info") or self.__basic_info is None:
            self.__basic_info = self.get_basic_info()
        return self.__basic_info

    def __init__(self, driver, username: str):
        self._driver = driver
        self.__username = username
        self.__url = join_paths(self._base_url, "in", username)
        self.__username = username
        self._logger = logging.getLogger(__name__)
        self._driver_get_user_profile()

    def get_data(self) -> dict:
        return {
            "username": self.__username,
            "basic_info": self.basic_info,
            "experience": self.experience,
        }

    def get_basic_info(self) -> list[str | None]:
        username = self.__username
        self._driver.get(f"https://www.linkedin.com/in/{username}/")

        name = self.__get_element_text(
            By.CSS_SELECTOR, ".text-heading-xlarge", **{"target": "name"}
        )
        position = self.__get_element_text(
            By.CSS_SELECTOR, ".text-body-medium", **{"target": "position"}
        )
        location = self.__get_element_text(
            By.CSS_SELECTOR,
            "span.text-body-small:nth-child(1)",
            **{"target": "location"},
        )
        # nbr_followers = self.__get_element_text(By.CSS_SELECTOR, "li.text-body-small:nth-child(1) > span:nth-child(1)", **{"target": "number of followers"})
        # nbr_connections = self.__get_element_text(By.CSS_SELECTOR, "li.text-body-small:nth-child(2) > span:nth-child(1) > span:nth-child(1)", **{"target": "number of connection"})

        return [
            name,
            position,
            location
            # nbr_followers,
            # nbr_connections
        ]

    def get_experience(self) -> dict:
        sections = self._sections
        experience_section_candidates = list(
            filter(lambda section: "Experience" in section.text, sections)
        )
        if not experience_section_candidates:
            raise NotFoundProfileExperience(
                f"Profile '{self.__username}' does not have any experience section"
            )
        elif len(experience_section_candidates) > 1:
            self._logger.warning(
                f"Profile '{self.__username}' has more than one experience section candidates, taking the first."
            )
        experience_section = experience_section_candidates[0]
        return experience_section

    # Private:
    def _driver_get_user_profile(self) -> None:
        url = self.__url
        self._driver.get(url)

    # Private:
    def _get_profile_sections(self) -> list:
        sections = self._driver.find_elements(By.TAG_NAME, "section")
        if not sections:
            raise NotFoundProfileSections(
                f"Profile '{self.__username}' does not have any experience section"
            )
        return sections

    def __get_element_text(self, *args, **kwargs) -> str | None:
        try:
            return self._driver.find_element(args[0], args[1]).text
        except NoSuchElementException:
            self._logger.warning(f"Element {kwargs['target']} not found")
            return None
