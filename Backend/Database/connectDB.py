import pandas as pd
import psycopg2
from handleDB import connect, create_table
from cleanData import clean_df
from sqlalchemy import create_engine

cursor = None
connection = None
try:
    connection, cursor, url = connect()
    engine = create_engine(url)
    conn_engine = engine.connect()
    connection.autocommit = True

    table = create_table()
    cursor.execute(table)

    df = pd.read_csv('../data/100RowData.csv')

    gdf = clean_df(df)
    gdf.to_postgis("quake_text",conn_engine,if_exists="replace")

except(Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if cursor is not None:
        cursor.close()
        print('Cursor connection Terminated')
    if connection is not None:
        connection.close()
        print('Database connection Terminated')
