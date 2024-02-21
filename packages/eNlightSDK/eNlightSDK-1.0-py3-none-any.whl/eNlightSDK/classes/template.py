# template.py

from typing import Optional
from classes.api_caller import caller

class Template:
    def __init__(self, token: str, host: str):
        self.token = token
        self.host = host

    def get_template_by_uuid(self, vhd_uuid: str) -> None:
        try:
            api_endpoint = f"templates/{vhd_uuid}"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
            method = "GET"

            response = caller(self.token, api_call_url, method)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in Template.get_template_by_uuid: {e}")

    def list_templates(self, vmm_id: Optional[str] = None, compute: Optional[str] = None,
                          template_category: Optional[str] = None, template_guestos_category: Optional[str] = None,
                          limit: Optional[int] = None, offset: Optional[int] = None,
                          filter_tags: Optional[str] = None, type: Optional[str] = None) -> None:
        try:
            api_endpoint = "templates"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
            method = "GET"

            params = {
                'vmm_id': vmm_id,
                'compute': compute,
                'template_category': template_category,
                'template_guestos_category': template_guestos_category,
                'limit': limit,
                'offset': offset,
                'filter_tags': filter_tags,
                'type': type
            }

            response = caller(self.token, api_call_url, method, params=params)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in Template.get_all_templates: {e}")




# template_category.py

    def get_template_category(self, category_id: Optional[str] = None) -> None:
        try:
            api_endpoint = f"template_categories/{category_id}" if category_id else "template_categories"
            api_call_url = f"http://{self.host}:30157/{api_endpoint}"
            method = "GET"

            response = caller(self.token, api_call_url, method)
            return response

        except Exception as e:
            raise RuntimeError(f"Error in TemplateCategory.get_template_category_by_id: {e}")
