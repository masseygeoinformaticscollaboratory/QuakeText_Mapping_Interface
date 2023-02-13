import psycopg2
#from handleDBForCSV import connect, create_table, insert_to_database, remove_duplicates
from sqlalchemy import create_engine
#from readData import read_data
from handleDBForJSON import connect, create_table, insert_to_database, remove_duplicates

from readJSONData import get_json_data

cursor = None
connection = None

try:
    connection, cursor, url = connect()
    engine = create_engine(url)
    conn_engine = engine.connect()
    connection.autocommit = True

    gdf = get_json_data()
    if not gdf.empty:
        cursor.execute(create_table())
        for index, row in gdf.iterrows():
            query, data = insert_to_database(row)
            cursor.execute(query, data)

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
