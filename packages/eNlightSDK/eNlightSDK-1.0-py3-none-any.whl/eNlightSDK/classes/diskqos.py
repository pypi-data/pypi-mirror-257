# diskqos.py

from typing import Optional
from classes.api_caller import caller

class DiskQOS:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host

    def get_diskqos(self, id: Optional[str] = None) -> None:
        try:
            api_endpoint = "diskqos"
            if id:
                api_endpoint += f"/{id}"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
            method = "GET"
            response = caller(self.token, api_call_url, method)
            return response

        except Exception as e:
            print(e)


