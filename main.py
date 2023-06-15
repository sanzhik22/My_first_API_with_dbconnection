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


def search_airport(location):
    try:
        print('Connecting to the PostgreSQL database...')
        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        print('PostgreSQL database version:')
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)
        cursor.execute(select_airport, (location,))
        airports = cursor.fetchall()
        cursor.close()
        con.close()
        return airports
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return f'lost connection to database 500 {error}'

def add_airport(airport_name, city, coordinates):
    try:
        print('Connecting to the PostgreSQL database...')
        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        print('PostgreSQL database version:')
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)
        cursor.execute("INSERT INTO src_airports (airport_name, city, coordinates) VALUES (%s, %s, %s)", (airport_name, city, coordinates))
        print("Row succesfully added")
        con.commit()
        cursor.close()
        con.close()
        return 'Succes'
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error


def find_by_code(airport_code):
    try:
        print('Connecting to the PostgreSQL database...')
        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        print('PostgreSQL database version:')
        db_version = cursor.fetchone()
        print(db_version)
        cursor.execute(select_airport_by_code, (airport_code,))
        airport = cursor.fetchall()
        cursor.close()
        con.close()
        return airport
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error

app = Flask(__name__)

@app.route('/airport_data/<airport_code>')
def get_user(airport_code):
    try:
        air_data = find_by_code(airport_code)
        if air_data != []:
            return air_data, 200
        else:
            return "Sorry, but database doesen't contain that record", 404
    except (Exception, ConnectionError) as error:
        print(error)
        return error

@app.route('/loc/<my_location>')
def get_loc(my_location):
    try:
        answer = search_airport(location=my_location)
        if answer != []:
            return answer, 200
        else:
            return "Sorry, but database doesen't contain that record" ,404
    except (Exception, ConnectionError) as error:
        print(error)
        return error

@app.post('/add-airport')
def add_air():
    try:
        data = request.get_json()
        add_airport(airport_name=data['airport_name'],city=data['city'],coordinates=data['coordinates'])
        return f" asd {data['airport_name']}, {data['city']}, {data['coordinates']}", 201
    except (Exception, ConnectionError) as error:
        print(error)
        return error

if __name__ == '__main__':
    app.run(debug=True)