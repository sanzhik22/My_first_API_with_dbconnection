import requests
import json
import pytest
import random
from main import app

list_of_test_1 = ['Москва', 'Астрахань', 'Якутск', 'Мирный', 'Пулково', 'Кемерово']

data_to_post ={
    'airport_name': 'Warsaw airport',
    "city": "Warsaw",
    'coordinates': '(52,123123, 67,1231245)'
}
data_to_fail_post = {}

def test_endpoint():
    # Testing is connection successful
    responce = app.test_client().get('/')

    assert responce.status_code == 200

@pytest.mark.get_requests
def test_get_cli_by_loc():
    response = app.test_client().get(f'/loc/{random.choice(list_of_test_1)}')
    res = json.loads(response.data.decode('utf-8'))
    assert  response.status_code == 200

@pytest.mark.post_request
def test_post_db_insert():
    response = app.test_client().post('/add-airport', json = data_to_post)
    res = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200

@pytest.mark.post_requests
def test_post_fail():
    responce = app.test_client().post('/add-airport', json = data_to_fail_post)
    res = json.loads(responce.data.decode('utf-8'))
    assert responce.status_code == 400