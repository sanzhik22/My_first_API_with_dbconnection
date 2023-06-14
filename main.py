from flask import Flask, request
import os
import psycopg2
from dotenv import load_dotenv
import requests

select_airport = (
    "select * from src_airports where city = %s"
)
# CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL,
#                         date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""
#
# INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
insert_airport = (
    "INSERT INTO src_airport (airport_code, airport_name, city, coordinates, timezone) VALUES (%s, %s, %s, %s, %s);")




con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='postgres')

def search_airport(location):
    cursor = con.cursor()
    cursor.execute(select_airport, (location,))
    airports = cursor.fetchall()
    return airports

def add_airport(airport_code, airport_name, city, coordinates, timezone):
    cursor = con.cursor()
    cursor.execute(insert_airport, (airport_code,),(airport_name,), (city,), (coordinates,), (timezone,))

app =Flask(__name__)

@app.post('/my_loction')
def send_post():
    data = request.get_json()
    location = data['city']
    answer = search_airport(location)
    for row in answer:
        return f'В городе {location}, находится аэропорт {row[1]} котрый нахоитсься по координатам: {row[3]}', 201

@app.post('/add_airport')
def add_air():
    data = request.get_json()
    add_airport(data['airport_code'], data['airport_name'], data['city'], data['coordinates'], data['timezone'])
    return 201

if __name__ == '__main__':
    app.run(debug=True)