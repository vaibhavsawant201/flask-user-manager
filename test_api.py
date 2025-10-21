import requests

url = "http://localhost:5000/users"  # replace with your endpoint

data = {
    "name": "Vaibhav",
    "email": "vaibhav@example.com"
}

response = requests.post(url, json=data)
print(response.json())
