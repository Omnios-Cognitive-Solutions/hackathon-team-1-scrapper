from src.config import config
from src.linkedin_scrapper import LinkedInScrapper

TEST_USERNAME = "dolores-fuertes-fernández-408743250"

scrapper = LinkedInScrapper(headless=True)


def test_login():
    scrapper.login(config.get("LOGIN", "username"), config.get("LOGIN", "password"))


def test_get_profile_basic_data():
    data = scrapper.get_profile(TEST_USERNAME)
    assert data


def test_close():
    scrapper.close_driver()
