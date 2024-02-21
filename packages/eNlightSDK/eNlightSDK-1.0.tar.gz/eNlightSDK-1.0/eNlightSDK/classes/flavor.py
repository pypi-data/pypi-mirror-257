# flavor.py

from typing import Optional, List
from classes.api_caller import caller

class Flavor:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host

    def get_flavors(self, flavor_type: Optional[str] = None, status: Optional[str] = 'active') -> None:
        try:
            api_endpoint = "flavors"
            method = "POST"

            params = {
                'flavor_type': flavor_type,
                'status': status,
            }

            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
   
            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in Flavor.get_flavors: {e}")
