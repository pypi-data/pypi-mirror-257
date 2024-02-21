from setuptools import setup, find_packages

setup(
    name='eNlightSDK',
    version='1.0',
    description='eNlight Cloud VM create, update, retrive, delete and VM actions',
    author='Akshay Ghatol',
    author_email='akshay.ghatol@esds.co.in',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)








# 125
# {"entity": "vm", "method": "vm_create", "call_from": null, "params": "{\"vmm_id\": \"1\", \"host_uuid\": \"e725a09d-23d9-422f-a597-edc7d9678830\", \"vm_name\": \"akshy123\", \"additional_vm_name\": \"\", \"uid\": [\"7117a498-41c3-11ea-9e9a-0242ac110003\"], \"gid\": [\"1a7b80c7-a95b-11ee-a5ae-9ae834df5515\"], \"uid_str\": \"7117a498-41c3-11ea-9e9a-0242ac110003\", \"gid_str\": \"1a7b80c7-a95b-11ee-a5ae-9ae834df5515\", \"user\": \"7117a498-41c3-11ea-9e9a-0242ac110003:Master Admin\", \"url\": \"http://10.14.21.32\", \"download_url\": \"http://10.14.21.103/templates/xen/centos7_cloud-init_template.vhd\", \"sr_uuid\": \"481def2d-a4e4-0c6c-9a4d-0e37cc2c3c64\", \"min_cpu\": 2, \"max_cpu\": 2, \"min_ram\": 2048, \"max_ram\": 2048, \"password\": \"$Fqm@8Vk9WdDRk\", \"ssh_key\": \"\", \"vlan_id\": \"420\", \"network\": \"VLAN-420\", \"ip\": \"10.10.10.5\", \"gateway\": \"10.10.10.1\", \"subnet\": \"255.255.254.0\", \"mac_addr\": \"00:03:60:1b:c1:55\", \"schedule\": 1707731580.0, \"vm_tag\": \"\", \"REQUESTID\": \"65c9eac3e1480\", \"recipe_name\": \"\", \"recipe_data\": \"\", \"login_id\": \"7117a498-41c3-11ea-9e9a-0242ac110003\", \"login_fullname\": \"Master Admin\", \"pv\": \"True\", \"is_sdn_vm\": \"no\", \"quota_reservation_id\": \"2cf5cd64-669d-4b24-9dd6-82ca2edd47ce\", \"ip_reservation_id\": \"0a4a3ef6-9e22-4ccd-a986-13094c07053a\", \"template_name\": \"XENtemplate\", \"template\": \"XENtemplate\", \"template_uuid\": \"7438683f-95c1-4411-be62-3081408bf8af\", \"command\": \"None\", \"metadata\": \"centos7_64Guest\", \"guest_os_desc\": \"CentOS 7 (64-bit)\", \"os_name\": \"CentOS 7 (64-bit)\", \"template_size\": 10240, \"network_id\": \"19c94c9c-a3ef-4651-a6b8-5199f9727ff2\", \"ippool_id\": \"567391e6-f764-4d29-afe3-79fc2565d234\", \"request_ip\": \"10.212.133.164\", \"service_type\": null, \"user_email\": \"admin@enlightcloud.com\", \"project_id\": \"1a7b80c7-a95b-11ee-a5ae-9ae834df5515\"}", "host_uuid": "e725a09d-23d9-422f-a597-edc7d9678830", "vmm_id": "1", "action": "queue_update", "status": "Initiated"}

# 126
# {"entity": "vm", "method": "vm_create", "call_from": null, "params": "{\"vmm_id\": 1, \"host_uuid\": \"e725a09d-23d9-422f-a597-edc7d9678830\", \"vm_name\": \"rewtadve\", \"additional_vm_name\": \"testVM\", \"uid\": [\"7117a498-41c3-11ea-9e9a-0242ac110003\"], \"gid\": [\"1a7b80c7-a95b-11ee-a5ae-9ae834df5515\"], \"uid_str\": \"7117a498-41c3-11ea-9e9a-0242ac110003\", \"gid_str\": \"1a7b80c7-a95b-11ee-a5ae-9ae834df5515\", \"user\": \"7117a498-41c3-11ea-9e9a-0242ac110003:Master Admin\", \"url\": \"http://10.14.21.32\", \"download_url\": \"http://10.14.21.103/templates/xen/centos7_cloud-init_template.vhd\", \"sr_uuid\": \"481def2d-a4e4-0c6c-9a4d-0e37cc2c3c64\", \"min_cpu\": 2, \"max_cpu\": 2, \"min_ram\": 2048, \"max_ram\": 2048, \"password\": \"!aVl.8r{-Sg)\", \"ssh_key\": \"\", \"vlan_id\": 420, \"network\": \"VLAN-420\", \"ip\": \"10.10.10.23\", \"gateway\": \"10.10.10.1\", \"subnet\": \"255.255.254.0\", \"mac_addr\": \"00:03:60:81:76:c9\", \"schedule\": 1733133540.0, \"vm_tag\": \"\", \"REQUESTID\": \"\", \"recipe_name\": \"\", \"recipe_data\": \"\", \"login_id\": \"7117a498-41c3-11ea-9e9a-0242ac110003\", \"login_fullname\": \"Master Admin\", \"pv\": \"True\", \"is_sdn_vm\": \"no\", \"quota_reservation_id\": \"e3d7b62a-73ad-456d-bf57-0862ac7d6819\", \"ip_reservation_id\": \"9b8bba8b-0470-4bd0-a2d0-62f8e0620054\", \"template_name\": \"XENtemplate\", \"template\": \"XENtemplate\", \"template_uuid\": \"7438683f-95c1-4411-be62-3081408bf8af\", \"command\": \"None\", \"metadata\": \"centos7_64Guest\", \"guest_os_desc\": \"CentOS 7 (64-bit)\", \"os_name\": \"CentOS 7 (64-bit)\", \"template_size\": 10240, \"network_id\": \"19c94c9c-a3ef-4651-a6b8-5199f9727ff2\", \"ippool_id\": \"567391e6-f764-4d29-afe3-79fc2565d234\", \"request_ip\": \"UNKNOWN\", \"service_type\": null, \"user_email\": \"admin@enlightcloud.com\", \"project_id\": \"1a7b80c7-a95b-11ee-a5ae-9ae834df5515\"}", "host_uuid": "e725a09d-23d9-422f-a597-edc7d9678830", "vmm_id": 1, "action": "queue_update", "status": "Initiated"}