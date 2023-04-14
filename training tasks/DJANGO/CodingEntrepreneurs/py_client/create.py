import requests

endpoint = "http://127.0.0.1:8000/api/products/"

data = {
    "title": "JSON is not good."
}
headers = {
    'Authorization': 'Bearer 3a8b4a3d3ae0d137083c96a564df09cded0c6ef3'
}

get_response = requests.post(endpoint, json=data, headers=headers)
print(get_response.json())