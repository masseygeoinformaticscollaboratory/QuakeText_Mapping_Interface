import psycopg2
from configDB import config
from sqlalchemy import create_engine


def connect():
    params = config()
    print('Connecting to PostgreSQL Database')
    conn = psycopg2.connect(**params)
    return conn, conn.cursor()


def create_table():
    create_script = ''' 
        CREATE TABLE IF NOT EXISTS data(
        id          int PRIMARY KEY,
        label       varchar(70),
        instance    varchar(100),
        tweetText   varchar(500),
        latitude    float,
        longitude   float
    
        )
        '''

    return create_script
