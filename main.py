from flask import Flask, request
import os
import psycopg2
from dotenv import load_dotenv
import requests


# CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL,
#                         date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""
#
# INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
insert_airport = (
    "INSERT INTO src_airports (airport_name, city, coordinates) VALUES (%s, %s, %s);"
)




con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='postgres')

def search_airport(location):
    cursor = con.cursor()
    cursor.execute(select_airport, (location,))
    airports = cursor.fetchall()
    return airports

def add_airport(airport_name, city, coordinates):
    cursor = con.cursor()
    cursor.execute("INSERT INTO src_airports (airport_name, city, coordinates) VALUES (%s, %s, %s)", (airport_name, city, coordinates))
    con.commit()
    cursor.close()
    con.close()

app =Flask(__name__)

@app.post('/my-location')
def send_post():
    data = request.get_json()
    location = data['city']
    answer = search_airport(location)
    for row in answer:
        return f'В городе {location}, находится аэропорт {row[1]} котрый нахоитсься по координатам: {row[3]}', 200

@app.post('/add-airport')
def add_air():
    data = request.get_json()
    add_airport(airport_name=data['airport_name'],city=data['city'],coordinates=data['coordinates'])
    return f" asd {data['airport_name']}, {data['city']}, {data['coordinates']}", 201

if __name__ == '__main__':
    app.run(debug=True)