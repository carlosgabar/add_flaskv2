import psycopg
from psycopg import DatabaseError

def get_connection():

    try:

        return psycopg.connect(
            
            host="localhost",
            user="postgres",
            password="Yayel.2027",
            dbname="app_flask"

        )

    except DatabaseError as ex:
        raise ex

    