import psycopg2
from configDB import config
from sqlalchemy.engine import URL


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


# Creates a postGIS table in the PostGreSQL database if one has not yet been created
def create_table():
    return """
      CREATE TABLE IF NOT EXISTS quake_text(

          place_name                varchar(70),
          impact_type              varchar(500),
          impact_place_rel         varchar(500),
          modifier_place_rel       varchar(500),
          severity_impact_rel      varchar(500),
          item_impact_rel          varchar(500),
          impact_category          varchar(500),
          tweet_text               varchar(500),
          geometry                 geometry(Point, 4326)
          );
      """


columns = ['place name', 'type of impact', 'impact place relation', 'modifier place relation',
           'severity impact_relation', 'item impact relation', 'tweet text', 'impact category']


# Done insert per row as the to_postGIS function overrides the whole database, and I was short on time to find a more efficient method
def insert_to_database(row):
    # The below query simply inserts the data into the database without checking for duplicates. Using this query, a second
    # query is called to remove any duplicates
    insert_query1 = """ 
         INSERT INTO quake_text (place_name, impact_type, impact_place_rel, modifier_place_rel, severity_impact_rel, item_impact_rel, impact_category, tweet_text, geometry) 
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s,4326)); 
         """

    # The below Query checks if the row already exists before it inserts the data - however this may not be very efficient with
    # a large amount of data - we didn't have enough data ready at the time to test this.
    insert_query2 = """
        INSERT INTO quake_text (place_name, impact_type, impact_place_rel, modifier_place_rel, severity_impact_rel, item_impact_rel, impact_category, tweet_text, geometry) 
        SELECT *
        FROM  (
            VALUES 
          (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s,4326))
        ) AS i(place_name, impact_type, impact_place_rel, modifier_place_rel, severity_impact_rel, item_impact_rel, impact_category, tweet_text, geometry)
        WHERE  NOT EXISTS (
        SELECT FROM quake_text m
        WHERE  m.place_name = i.place_name
        AND    m.impact_type = i.impact_type
        AND    m.tweetText = i.tweetText
          );
    
    """
    record_to_insert = (
        row["place name"], row["type of impact"], row["impact place relation"], row["modifier place relation"],
        row["severity impact relation"], row["item impact relation"], row["impact category"], row["tweet text"],
        row["geometry"].wkt)
    return insert_query1, record_to_insert


# Only needed with insert_query1
def remove_duplicates():
    return """
    DELETE FROM quake_text T1
	    USING   quake_text T2
	WHERE  T1.ctid    < T2.ctid       
    AND  T1.tweet_text = T2.tweet_text
    AND  T1.place_name = T2.place_name
    AND  T1.impact_type = T2.impact_type

    """
