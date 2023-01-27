import psycopg2
from configDB import config
from sqlalchemy.engine import URL

def connect():
    params = config()
    url = create_url(params)
    print('Connecting to PostgreSQL Database')
    conn = psycopg2.connect(**params)
    return conn, conn.cursor(), url


def create_table():
    create_script = ''' 
        CREATE TABLE IF NOT EXISTS quake_text(
        id          int PRIMARY KEY,
        label       varchar(70),
        instance    varchar(100),
        tweetText   varchar(500),
        geom        geometry(Point, 4326) 
        )
        '''
    return create_script

def create_url(params):

    url_object = URL.create(
        "postgresql+psycopg2",
        username=params['user'],
        password=params['password'],
        host=params['host'],
        database= params['database'],
    )
    return url_object