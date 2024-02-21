# Defaultvmm.py

from typing import Optional
from classes.api_caller import caller

class DefaultVmm:

    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host



    def get_regions(self):
        try:
            api_endpoint = "regions"
            api_call_url = f"http://{self.host}:30142/{api_endpoint}"
            method = "POST"
   
            response = caller(self.token, api_call_url, method)
            return response

        except Exception as e:
            print(e)



    def get_default_pod(self, region_id: Optional[str] = None):
        try:
            api_endpoint = "default_vmm"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
            method = "GET"
            params = {
                "region_id": region_id
            }
            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            print(e)