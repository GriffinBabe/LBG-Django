import json
import requests

request = {"request_type": "get_model", "auth_key": "77BSWLZRZ1"}
organisers_json = json.dumps(request)
url = "http://127.0.0.1:8000/api/"


r = requests.post(url, organisers_json, timeout=10)

print(r.text)
response_dictionnary = json.loads(r.text)
print(response_dictionnary)