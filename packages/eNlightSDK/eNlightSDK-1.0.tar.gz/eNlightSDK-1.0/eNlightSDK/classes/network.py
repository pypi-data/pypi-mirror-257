# # network.py

from typing import Optional, List
from classes.api_caller import caller

# class Network:
#     def __init__(self, token: str, host: str):
#         self.token = token
#         self.host = host

#     def get_network_details(self, vmm_id: Optional[str] = None, url: Optional[str] = None) -> None:
#         try:
#             api_endpoint = f"networks"
#             api_call_url = f"http://{self.host}:30157/{api_endpoint}"
#             method = "GET"

#             params = {
#                 "vmm_id" : vmm_id,
#                 "url": url
#             }

#             response = caller(self.token, api_call_url, method, params=params)
#             return response

#         except Exception as e:
#             raise RuntimeError(f"Error in Network.get_network_details: {e}")




# sdn_network.py


class SDNNetwork:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host

    def get_sdn_network_details(self, id: Optional[str] = None, status: Optional[str] = None,
                                external: Optional[str] = None, vlan: Optional[List[str]] = None,
                                project_id: Optional[str] = None) -> None:
        try:
            api_endpoint = "sdn/network"
            if id:
                api_endpoint += f"/{id}"

            params = {
                'status': status,
                'external': external,
                'vlan': vlan,
                'project_id': project_id,
            }

            api_call_url = f"http://{self.host}:30105/{api_endpoint}"
            method = "GET"

            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in SDNNetwork.get_sdn_network_details: {e}")
