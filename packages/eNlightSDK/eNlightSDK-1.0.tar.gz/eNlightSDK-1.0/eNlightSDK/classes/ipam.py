# ippool.py

from typing import Optional, List
from classes.api_caller import caller

# network.py

class Network:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host


    def get_networks(self, project_id: Optional[str] = None, status: Optional[str] = None,
                     vlan: Optional[List[str]] = None, region_id: Optional[str] = None) -> None:
        try:
            api_endpoint = "networks"
            method = "GET"

            params = {
                'project_id': project_id,
                'status': status,
                'vlan': vlan,
                'region_id': region_id
            }

            api_call_url = f"http://{self.host}:30105/{api_endpoint}"

            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in Network.get_networks: {e}")




class Ippool:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host

    def get_ippool_details(self, network_id: str, id: Optional[str] = None,
                           is_public: Optional[str] = None, name: Optional[str] = None,
                           status: Optional[str] = None, ip_version: Optional[str] = 'IPv4') -> None:
        try:
            api_endpoint = "ippool"
            if id:
                api_endpoint += f"/{id}"

            params = {
                'network_id': network_id,
                'is_public': is_public,
                'name': name,
                'status': status,
                'ip_version': ip_version
            }

            api_call_url = f"http://{self.host}:30105/{api_endpoint}"
            method = "GET"


            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in Ippool.get_ippool_details: {e}")


# ip.py


class Ip:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host

    def get_ips(self, pool_id: str, id: Optional[str] = None, status: Optional[str] = None,
                is_public: Optional[str] = None, is_reserve: Optional[str] = None) -> None:
        try:
            api_endpoint = "ip"
            method = "GET"

            params = {
                'id': id,
                'pool_id': pool_id,
                'status': status,
                'is_public': is_public,
                'is_reserve': is_reserve
            }

            api_call_url = f"http://{self.host}:30105/{api_endpoint}"
            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in Ip.get_ips: {e}")
