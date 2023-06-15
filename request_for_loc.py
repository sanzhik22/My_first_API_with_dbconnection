import requests
url = 'http://127.0.0.1:5000/add-airport'
data = {
    'airport_name': 'Jogn Kennedy',
    "city": "New York",
    'coordinates': '(3432, 3214)'
}
x = requests.post(url, json = data)

print(x.text)