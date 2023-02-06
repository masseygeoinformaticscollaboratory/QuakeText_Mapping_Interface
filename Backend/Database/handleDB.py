import psycopg2
from configDB import config
from sqlalchemy.engine import URL


def connect():
    params = config()
    url = create_url(params)
    print('Connecting to PostgreSQL Database')
    conn = psycopg2.connect(**params)
    return conn, conn.cursor(), url


def create_url(params):
    url_object = URL.create(
        "postgresql+psycopg2",
        username=params['user'],
        password=params['password'],
        host=params['host'],
        database=params['database'],
    )
    return url_object


def create_table():
    return """
      CREATE TABLE IF NOT EXISTS quake_text(
          label       varchar(70),
          instance    varchar(100),
          tweet_text   varchar(500),
          tweet_id     varchar(500),
          geometry    geometry(Point, 4326)
          );
      """


def insert_to_database(row):
    insert_query = """ 
         INSERT INTO quake_text (label, instance, tweet_text, tweet_id,geometry) 
         VALUES (%s,%s,%s,%s,%s);
         """
    record_to_insert = (row["label"], row["instance"], row["tweetText"], row["tweetId"], row["geometry"].wkt)
    return insert_query, record_to_insert


def remove_duplicates():
    return """
    DELETE FROM quake_text T1
	    USING   quake_text T2
	WHERE  T1.ctid    < T2.ctid       
    AND  T1.instance    = T2.instance      
    AND  T1.tweet_id = T2.tweet_id
    AND  T1.tweet_text = T2.tweet_text;
    """
