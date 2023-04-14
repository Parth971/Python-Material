import requests
import json

url = "http://localhost:8000/serializer-app/create-student/"

data = {
    'first_name': 'Parth1',
    'last_name': 'Desai2',
    'age': 9
}

json_data = json.dumps(data)
response = requests.post(url=url, data=json_data)
data = response.json()
print(data)