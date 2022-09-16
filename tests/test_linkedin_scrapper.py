from src.linkedin_scrapper import LinkedInScrapper

# USERNAME = "hack2@omnios.ai"
# PASSWORD = "


def test_login():
    LinkedInScrapper().login()


def test_get_profile():
    LinkedInScrapper().get_profile()
