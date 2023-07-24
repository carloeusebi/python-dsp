import os
import requests


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
            if err.response.status_code == 401:
                os.system("cls" if os.name in ("nt", "dos") else "clear")
                print("Username o Password non validi")
            else:
                print("C'è stato un problema con il server, Riprovare più tardi")
                input("Premi un tasto per uscire")
                exit()
