import requests
from packaging import version

current_version = "1.2.1"

response = requests.get('https://pypi.org/pypi/allproxy/json')
web_version = response.json()["info"]["version"]

if version.parse(web_version) > version.parse(current_version):
    print("Hey there! Please update to the new version of allproxy by using pip install --upgrade allproxy!")