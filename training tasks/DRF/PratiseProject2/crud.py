import requests
import json

url = "http://localhost:8000/crud/"


def get_data(id=None):
    data = {}
    if id is not None:
        data['id'] = id

    json_data = json.dumps(data)
    response = requests.get(url=url, data=json_data)
    data = response.json()
    print(data)

def post_data():
    data = {
        'first_name': 'parth2 fake',
        'last_name': 'desai2 fake',
        'age': 31
    }
    json_data = json.dumps(data)
    response = requests.post(url=url, data=json_data)
    data = response.json()
    print(data)

def update_data():
    data = {
        'id': 12,
        'first_name': 'updated parth2 fake',
        'last_name': 'updated desai2 fake',
    }
    json_data = json.dumps(data)
    response = requests.put(url=url, data=json_data)
    data = response.json()
    print(data)


def delete_data():
    data = {
        'id': 12
    }
    json_data = json.dumps(data)
    response = requests.delete(url=url, data=json_data)
    data = response.json()
    print(data)



# get_data()
# post_data()
# update_data()
# delete_data()