from typing import Optional, List
from classes.api_caller import caller

class Queue:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host

    def get_queue(self, id: Optional[str] = None, project_id: Optional[str] = None, entity: Optional[str] = None,
                   vmm_id: Optional[str] = None, action: Optional[str] = None,
                   status_error: Optional[str] = None, from_date: Optional[str] = None,
                   to_date: Optional[str] = None, limit: Optional[int] = None,
                   offset: Optional[int] = None) -> None:
        try:
            api_endpoint = "queue"
            if id:
                api_endpoint += f"/{id}"
            method = "GET"

            params = {
                'project_id': project_id,
                'entity': entity,
                'vmm_id': vmm_id,
                'action': action,
                'status_error': status_error,
                'from_date': from_date,
                'to_date': to_date,
                'limit': limit,
                'offset': offset
            }

            api_call_url = f"http://{self.host}:30157/{api_endpoint}"

            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in QueueSDK.get_queues: {e}")
