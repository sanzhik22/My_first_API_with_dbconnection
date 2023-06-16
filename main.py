import logging
from datetime import datetime

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

logging.basicConfig(filename='app.log',level=logging.INFO)

def search_airport(location):
    try:
        logging.info('Connecting to the PostgreSQL database... ' + str(datetime.now()))
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
        logging.error('Error occured ' + str(error) + " " + str(datetime.now()))
        return f'lost connection to database 500 {error}'

def add_airport(airport_name, city, coordinates):
    try:
        logging.info('Connecting to the PostgreSQL database... ' + str(datetime.now()))
        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        logging.info('PostgreSQL database version: ' + str(datetime.now()))
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)
        cursor.execute("INSERT INTO src_airports (airport_name, city, coordinates) VALUES (%s, %s, %s)", (airport_name, city, coordinates))
        logging.info("Row succesfully added " + str(datetime.now()))
        con.commit()
        cursor.close()
        con.close()
        return 'Succes'
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Error occured' + str(error) + " " + str(datetime.now()))
        return str(error)


def find_by_code(airport_code):
    try:
        logging.info('Connecting to the PostgreSQL database... /' + str(datetime.now()))
        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        logging.info('PostgreSQL database version: /' + str(datetime.now()))
        db_version = cursor.fetchone()
        logging.info(db_version + " /" + str(datetime.now()))
        cursor.execute(select_airport_by_code, (airport_code,))
        airport = cursor.fetchall()
        cursor.close()
        con.close()
        return airport
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Error occured' + str(error) + " /" + str(datetime.now()))
        return str(error)

app = Flask(__name__)

@app.route('/airport_data/<airport_code>')
def get_user(airport_code):
    try:
        logging.info('Trying to connect to server /' + str(datetime.now()))
        air_data = find_by_code(airport_code)
        if air_data != [] and type(air_data) != str:
            logging.info('Succesfully found airport on ' +  airport_code + " /" + str(datetime.now()))
            return air_data, 200
        elif air_data == []:
            logging.warning("Couldn't find data related to: " + str(airport_code) + " /" + str(datetime.now()))
            return "Sorry, but database doesen't contain that record", 404
        else:
            return air_data
    except (Exception, ConnectionError) as error:
        logging.error('Error ocured:' + str(error) + " /" + str(datetime.now()))
        return error

@app.route('/loc/<my_location>')
def get_loc(my_location):
    try:
        logging.info('Trying to connect to server /' + str(datetime.now()))
        answer = search_airport(location=my_location)
        if answer != [] and type(answer) != str:
            logging.info('Succersfully find location info on ' + my_location + " /" + str(datetime.now()))
            return answer, 200
        elif answer == []:
            logging.warning("Couldn't find that record in database " + my_location + " /" + str(datetime.now()))
            return "Sorry, but database doesen't contain that record" ,404
        else:
            return answer
    except (Exception, ConnectionError) as error:
        logging.error('Error occured' + str(error) + ' /' + str(datetime.now()))
        return error

@app.post('/add-airport')
def add_air():
    try:
        logging.info('trying to connect to server /' + str(datetime.now()))
        data = request.get_json()
        try:
            add_airport(airport_name=data['airport_name'],city=data['city'],coordinates=data['coordinates'])
        except (Exception, KeyError) as error:
            logging.error('Error occured ' + str(error) + " /" + str(datetime.now()))
        return f" asd {data['airport_name']}, {data['city']}, {data['coordinates']}", 201
    except (Exception, ConnectionError) as error:
        logging.error('Error ocured' + str(error) + " /" + str(datetime.now()))
        return error

if __name__ == '__main__':
    app.run(debug=True)