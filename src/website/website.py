import requests

from utils import utils


class Website:
    def __init__(self, url: str):
        self.url = url
        self.cookie = ""

    def login(self, credentials: str) -> bool:
        print("Login in corso...")
        try:
            response = requests.post(f"{self.url}/login", credentials)
            response.raise_for_status()
            session_id = response.json()["session_id"]
            token = response.cookies.get("TOKEN")
            self.cookie = f"TOKEN={token}; PHPSESSID={session_id}"
            return True
        except requests.exceptions.HTTPError as err:
            if response.status_code == 401:
                utils.clearscreen()
                print("Username o Password non validi")
            else:
                print("C'è stato un problema con il server, Riprovare più tardi")
                utils.die(err)

    def get(self, endpoint: str, params) -> list[dict]:
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(
                f"{self.url}/{endpoint}", headers=headers, params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print("C'è stato un problema con il server, Riprovare più tardi")
            utils.die(err)
