import psycopg2
from configDB import config

def connect():
    connection = None
    try:
        params = config()
        print('Connecting to PostgreSQL Database')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        print('PostgreSQL data vase version: ')
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)
        cursor.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()
            print('Database connection Terminated')

connect()