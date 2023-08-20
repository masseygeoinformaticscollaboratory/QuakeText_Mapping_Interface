import psycopg2
from sqlalchemy import create_engine, URL
import pandas as pd
import time
from get_geonames_local import get_geonames_instance

from configDB import config

start = time.time()

cursor = None
connection = None


def connect():
    params = config()
    url = create_url(params)
    print('Connecting to PostgreSQL Database')
    conn = psycopg2.connect(**params)
    return conn, conn.cursor(), url


# Creates a url from the config file parameters
def create_url(params):
    url_object = URL.create(
        "postgresql+psycopg2",
        username=params['user'],
        password=params['password'],
        host=params['host'],
        database=params['database'],
    )
    return url_object


try:
    connection, cursor, url = connect()
    engine = create_engine(url)
    conn_engine = engine.connect()
    connection.autocommit = True

    # This can easily be used with a CSV file - just use the read_data() function from readCSVData.py
    # and use the handleDBForCSV in place of handleDBForJSON
    query = "SELECT * FROM geoname"
    geonames = pd.read_sql(query, conn_engine)
    geonames.to_csv("geonames.csv", index=False)



    '''
    gdf = read_data()
    if not gdf.empty:
        cursor.execute(create_table())
        for index, row in gdf.iterrows():
            query, data = insert_to_database(row)
            cursor.execute(query, data)

    # Only needed with insert_query1
    cursor.execute(remove_duplicates())
    '''

except(Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if cursor is not None:
        cursor.close()
        print('Cursor connection Terminated')
    if connection is not None:
        connection.close()
    print('Database connection Terminated')
    end = time.time()
    total = end - start
    print("Time taken: ")
    print(total)
