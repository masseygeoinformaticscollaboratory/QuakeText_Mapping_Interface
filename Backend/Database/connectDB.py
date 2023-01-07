import pandas as pd
import psycopg2
from handleDB import connect
from cleanData import clean_df

cursor = None
connection = None
try:
    connection, cursor = connect()
    connection.autocommit = True

    data = pd.read_csv('../data/10RowData.csv')

    cleaned_data = clean_df(data)


except(Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if cursor is not None:
        cursor.close()
        print('Cursor connection Terminated')

    if connection is not None:
        connection.close()
        print('Database connection Terminated')
