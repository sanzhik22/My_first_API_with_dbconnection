import requests
url = 'http://127.0.0.1:5000/my-location'
data = {
    "city": "Новосибирск"
}
x = requests.post(url, json = data)

print(x.text)