import psycopg2
from sqlalchemy import create_engine
from handleDBForJSON import connect, create_table, insert_to_database, remove_duplicates
from readJSONData import read_data
import time

start = time.time()

cursor = None
connection = None

try:
    connection, cursor, url = connect()
    engine = create_engine(url)
    conn_engine = engine.connect()
    connection.autocommit = True

    # This can easily be used with a CSV file - just use the read_data() function from readCSVData.py
    # and use the handleDBForCSV in place of handleDBForJSON
    gdf = read_data()
    if not gdf.empty:
        cursor.execute(create_table())
        for index, row in gdf.iterrows():
            query, data = insert_to_database(row)
            cursor.execute(query, data)

    # Only needed with insert_query1
    cursor.execute(remove_duplicates())


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
