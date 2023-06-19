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
For running test we use test pytest library
```python
pip install pytest
pythom -m test_example.py
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