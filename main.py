import json

from flask import Flask, request
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
host = os.getenv('MY_HOST')
database = os.getenv('MY_DATABASE')
user = os.getenv('MY_USER')
password = os.getenv('MY_PASSWORD')
select_airport = "select * from src_airports where city = %s"

select_airport_by_code = "select * from src_airports where airport_code = %s"

con = psycopg2.connect(host=host, database=database, user=user, password=password)

def search_airport(location):
    cursor = con.cursor()
    cursor.execute(select_airport, (location,))
    airports = cursor.fetchall()
    cursor.close()
    con.close()
    return airports

def add_airport(airport_name, city, coordinates):
    cursor = con.cursor()
    cursor.execute("INSERT INTO src_airports (airport_name, city, coordinates) VALUES (%s, %s, %s)", (airport_name, city, coordinates))
    con.commit()
    cursor.close()
    con.close()

def find_by_code(airport_code):
    cursor = con.cursor()
    cursor.execute(select_airport_by_code, (airport_code,))
    airport = cursor.fetchall()
    return airport

app =Flask(__name__)

@app.route('/airport_data/<airport_code>')
def get_user(airport_code):
    air_data = find_by_code(airport_code)
    return air_data

@app.post('/my-location')
def send_post():
    data = request.get_json()
    location = data['city']
    answer = search_airport(location)
    json.dumps(answer,ensure_ascii=False)
    return answer
    # for row in answer:
    #     return f'В городе {location}, находится аэропорт {row[1]} котрый нахоитсься по координатам: {row[3]}', 200

@app.post('/add-airport')
def add_air():
    data = request.get_json()
    add_airport(airport_name=data['airport_name'],city=data['city'],coordinates=data['coordinates'])
    return f" asd {data['airport_name']}, {data['city']}, {data['coordinates']}", 201

if __name__ == '__main__':
    app.run(debug=True)