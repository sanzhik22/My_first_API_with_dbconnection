from flask import Flask, request
import os
import psycopg2
from dotenv import load_dotenv
import requests

select_airport = (
    "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
)
CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL, 
                        date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
)

con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='postgres')

app =Flask(__name__)

@app.post('/api/room')
def create_room():
    data = request.get_json()
    name = data['name']
    with con:
        with  con.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID, (name,))
            room_id = cursor.fetchone()[0]
    return {'id': room_id, 'message': f'Room {name} created'}, 201



if __name__ == '__main__':
    app.run(debug=True)