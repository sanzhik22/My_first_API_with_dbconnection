import logging
from datetime import datetime
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

logging.basicConfig(filename='log.txt',level=logging.INFO)

status_fail = {'status': 'Couldnt find that location in datatbase'}
status_added = {'status': 'Row added to database'}
error_ocured = {'status': ''}

def json_conv(data):
    result = json.dumps(data, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))
    return result


def search_airport(location):
    try:
        logging.info('Connecting to the PostgreSQL database... ' + str(datetime.now()))
        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        logging.info('Succesfully connected to database /' + str(datetime.now()))
        logging.info('PostgreSQL database version: / ' + str(datetime.now()))
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        logging.info(str(db_version) + " /" + str(datetime.now()))
        cursor.execute(select_airport, (location,))
        airports = cursor.fetchall()
        airports = json_conv(airports)
        logging.info(f'Success Row {airports} fetched')
        cursor.close()
        con.close()
        logging.info('Closed connection to database /' + str(datetime.now()))
        if airports != []:
            return airports
        else:
            return status_fail
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Error occured ' + str(error) + " " + str(datetime.now()))
        error_ocured['status'] = str(error)
        return error_ocured


def add_airport(airport_name, city, coordinates):
    try:
        logging.info('Connecting to the PostgreSQL database... ' + str(datetime.now()))
        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        logging.info('Succesfully connected to database /' + str(datetime.now()))
        logging.info('PostgreSQL database version: ' + str(datetime.now()))
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)
        cursor.execute("INSERT INTO src_airports (airport_name, city, coordinates) VALUES (%s, %s, %s)", (airport_name, city, coordinates))
        logging.info(f"Row succesfully added {str(datetime.now())}")
        con.commit()
        cursor.close()
        con.close()
        logging.info('Closed connection to database /' + str(datetime.now()))
        return status_added
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Error occured' + str(error) + " " + str(datetime.now()))
        error_ocured['status'] = str(error)
        return error_ocured


def find_by_code(airport_code):
    try:
        logging.info('Connecting to the PostgreSQL database... /' + str(datetime.now()))
        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = con.cursor()
        logging.info('Succesfully connected to database /' + str(datetime.now()))
        logging.info('PostgreSQL database version: /' + str(datetime.now()))
        db_version = cursor.fetchone()
        logging.info(db_version + " /" + str(datetime.now()))
        cursor.execute(select_airport_by_code, (airport_code,))
        airport = cursor.fetchall()
        airport = json_conv(airport)
        logging.info(f'Success row added {airport}')
        cursor.close()
        con.close()
        logging.info('Closed connection to database /' + str(datetime.now()))
        if airport != []:
            return airport
        else:
            return status_fail
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Error occured' + str(error) + " /" + str(datetime.now()))
        error_ocured['status'] = str(error)
        return error_ocured

app = Flask(__name__)

@app.route('/airport_data/<airport_code>')
def get_user(airport_code):
    try:
        logging.info('Opened connection to server /' + str(datetime.now()))
        air_data = find_by_code(airport_code)
        logging.info('Succesfully send data')
        logging.info('Connection closed')
        return air_data, 200
    except (Exception, ConnectionError) as error:
        logging.error('Error ocured:' + str(error) + " /" + str(datetime.now()))
        error_ocured['status'] = str(error)
        return error_ocured

@app.route('/loc/<my_location>')
def get_loc(my_location):
    try:
        logging.info('Opened connection to server /' + str(datetime.now()))
        answer = search_airport(location=my_location)
        logging.info('Succesfully send data')
        logging.info('Connection closed')
        return answer, 200
    except (Exception, ConnectionError) as error:
        logging.error('Error occured' + str(error) + ' /' + str(datetime.now()))
        error_ocured['status'] = str(error)
        return error_ocured

@app.post('/add-airport')
def add_air():
    try:
        logging.info('Opened connection to server /' + str(datetime.now()))
        data = request.get_json()
        try:
            answer = add_airport(airport_name=data['airport_name'],city=data['city'],coordinates=data['coordinates'])
            return answer
        except (Exception, KeyError) as error:
            logging.error('Error occured ' + str(error) + " /" + str(datetime.now()))
            error_ocured['status'] = str(error)
            return error_ocured
    except (Exception, ConnectionError) as error:
        logging.error('Error ocured' + str(error) + " /" + str(datetime.now()))
        error_ocured['status'] = str(error)
        return error_ocured

if __name__ == '__main__':
    app.run(debug=True)