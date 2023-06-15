# My_first_API_with_dbconnection

I've created my first api service with GET and POST methods and connection to my local PostgreSQL 

## Installation
Requires Python 3.11.3
```
pip install -r requirements.txt
```
### Environment configuration
Rename env.template file to .env file and edit it 
```
MY_HOST = <<Host name>>
MY_DATABASE = <<Database name>>
MY_USER = <<Your user name to your postgres database>>
MY_PASSWORD = <<Your database user password>>
```

## Testing
After running, you can test server by sending POST methods you can do it by [Postman application](https://web.postman.co/workspace/test_workspace~9296645f-ffb9-4f4f-885c-f3b0b6f2e94f/overview) 
or by running following scripts:
```python
import requests
url = 'http://<YOUR_API>/add-airport' # server api
data = {
    'airport_name': 'Jogn Kennedy',
    "city": "New York",
    'coordinates': '(3432, 3214)'
} # data to send
x = requests.post(url, json = data) # sending data to server

print(x.text)
```

To check GET method you also can use [Postman application](https://web.postman.co/workspace/test_workspace~9296645f-ffb9-4f4f-885c-f3b0b6f2e94f/overview)
Another way just browse it by link
```
http://<YOUR_API>/loc/<my_location> 
http://<YOUR_API>/airport_data/<airport_code>
<YOUR_API> - ваша сгенерированная ссылка
<my_location> - city which fetches by db
<airport_code> - code of airport 
```