from src.linkedin_scrapper import LinkedInScrapper
from src.config import config

TEST_USERNAME = "NAREK"

scrapper = LinkedInScrapper()


def test_login():
    scrapper.login(
        config.get('LOGIN', 'username'),
        config.get('LOGIN', 'password')
    )


def test_get_profile_basic_data():
    data = scrapper.get_profile(TEST_USERNAME)
    assert data


def test_close():
    scrapper.close_driver()
