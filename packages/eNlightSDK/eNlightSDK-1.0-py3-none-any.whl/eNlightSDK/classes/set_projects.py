import json
from .caller import caller


def get_and_set_active_project(host, token, project_name):
	try:
		port = 30142
		api_endpoint = "get_user_projects"
		project_url = f"http://{host}:{port}/{api_endpoint}"
		parameters = {"module_key": "ENLIGHT360"}
		method="POST"
		get_projects = caller(token,project_url,method,parameters)
		get_projects = json.loads(get_projects)

		if "status" in get_projects and get_projects['status'] == 'success' and 'records' in get_projects['data']:
			for item in  get_projects["data"]['records']:
				if item['name'].lower() == project_name.lower():
					project_id =  item['project_id']
					# print(project_id)
		else:
			raise Exception(f"No Project Found with name {project_name}")
		
# To Set actrive project  use this function and provide the project id which you got from above function

		if project_id and project_id != "" and project_id != None:
			api_endpoint = "set_active_project"
			project_url = f"http://{host}:{port}/{api_endpoint}"
			parameters = {"project_id": project_id, "module_key": "ENLIGHT360"}
			method="POST"
			set_active_project = caller(token,project_url,method,parameters)
			# print(set_active_project)
		else:
			raise ValueError("Invalid project ID")

	except Exception as e:
		print(e)



# def set_active_project(host, token, project_id):
# 	try:
# 		port = 30142
# 		api_endpoint = "set_active_project"
# 		project_url = f"http://{host}:{port}/{api_endpoint}"
# 		parameters = {"project_id": project_id, "module_key": "ENLIGHT360"}
# 		method="POST"
# 		response_data = caller(token,project_url,method,parameters)
# 		# print(response_data)


# 	except Exception as e:
# 		print("get project id",e)

