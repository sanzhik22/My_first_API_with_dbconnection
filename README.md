# My_first_API_with_dbconnection

I've created my first api service with GET and POST methods and connection to my local PostgreSQL 

## Installation
Clone the repo
```
$ git clone https://github.com/sanzhik22/My_first_API_with_dbconnection/blob/main/README.md
```
Requires Python 3.11.3 # adjust it

Install dependencies using pip


```
pip install -r requirements.txt
```
python main.py
### Environment configuration
Rename *env.template* file to *.env* file and edit it 
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

## API 
`/airport_data/<airport_code>`

*Method:* `GET`

*Querry Parammeters:*

 - `<airport_code>` - write airport code by which it will be selected

 *Returns*

JSON:

```
{
    
    "LED",
    "Пулково",
    "Санкт-Петербург",
    "(30.262500762939453,59.80030059814453)",
}
```
if no such rows

```
{
    'status': 'Couldnt find that location in datatbase'
}
```

if error 
```
{
    'status': type of error
}
```
## Add row to database

`/add-airport`

*Method:* `POST`

*Query Parameters:*

*Body:*

JSON content with the following structure:

```
{
    "city": "Кызылорда",
    "airport_name": "Кызылординский государственный",
    "coordinates": "(561,66557)"
}
```
Returns

json
```
{
  'status': 'Row added to database'
}
```
if error
```
{
    'status': type of error
}
```

## Logging 
All output logs saved in log.txt