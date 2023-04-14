import requests

# endpoint = "https://httpbin.org/status/200/"
# endpoint = "https://httpbin.org/anything"
endpoint = "http://127.0.0.1:8000/api/"

data ={
    "title": "Python Django",
    # "content": "Django is webframework of Python language",
    # "price": 123.45
}
get_response = requests.post(endpoint, json=data)
print(get_response.text)
print(get_response.status_code)