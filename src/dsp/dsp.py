from InquirerPy import prompt

from website.website import Website
from utils import utils

API_URL = "https://www.carloeusebiwebdeveloper.it/api"


def get_credentials():
    return prompt(
        [
            {"type": "input", "message": "Username:", "name": "username"},
            {"type": "password", "message": "Password", "name": "password"},
        ]
    )


def main():
    utils.clearscreen()
    website = Website(API_URL)
    while not website.login(get_credentials()):
        pass
    print("Accesso riuscito")


if __name__ == "__main__":
    main()
