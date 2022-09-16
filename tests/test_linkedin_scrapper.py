from src.linkedin_scrapper import LinkedInScrapper

TEST_USERNAME = "NAREK"

scrapper = LinkedInScrapper()


def test_login():
    scrapper.login()


def test_get_profile_basic_data():
    data = scrapper.get_profile(TEST_USERNAME)
    assert data
