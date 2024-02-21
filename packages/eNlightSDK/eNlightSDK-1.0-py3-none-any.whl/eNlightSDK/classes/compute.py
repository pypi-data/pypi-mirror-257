# compute.py

from typing import Optional
from classes.api_caller import caller

class ComputeData:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host

    def get_compute_details(self, vmm_id: Optional[str] = None, get_graph_data: Optional[bool] = None, get_cluster_sum: Optional[bool] = None, huuid: Optional[str] = None, compute: Optional[str] = None, hv: Optional[str] = None, policy: Optional[str] = None) -> None:
        try:
            api_endpoint = "compute"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
            method = "GET"
            params = {
                "vmm_id":vmm_id,
                "get_graph_data": get_graph_data,
                "get_cluster_sum": get_cluster_sum,
                "huuid": huuid,
                "compute": compute,
                "hv": hv,
                "policy": policy
            }

            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in Compute.get_compute_details: {e}")



# compute_data.py


    def get_compute_data(self, vmm_id: Optional[int] = None, region_id: Optional[str] = None, hypervisor: Optional[str] = None,
                         template_id: Optional[str] = None, vlan: Optional[str] = None, compute_url: Optional[str] = None,
                         is_add_vif: Optional[bool] = None, filter_tags: Optional[str] = None) -> None:

        try:
            api_endpoint = "compute_data"
            method = "GET"

            params = {
                'vmm_id': vmm_id,
                'region_id': region_id,
                'hypervisor': hypervisor,
                'template_id': template_id,
                'vlan': vlan,
                'compute_url': compute_url,
                'is_add_vif': is_add_vif,
                'filter_tags': filter_tags
            }

            api_call_url = f"http://{self.host}:30157/v2/{api_endpoint}"

            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in ComputeData.get_compute_data: {e}")

