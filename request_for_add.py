import requests
url = 'http://127.0.0.1:5000/add-airport'
data = {
    "city": "Семей",
    "airport_name": "Семей аэропорт прикинь",
    "coordinates": "(67,667)"
}
x = requests.post(url, json = data)

print(x.text)