from . import initDBQUERIES
import psycopg
import os
from dotenv import load_dotenv

def createNcaaBasketballDatabase():
    print(os.getenv("HOST_NAME"))
    default_conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DEFAULT_DB")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    default_conn = psycopg.connect(default_conn_string, autocommit=True)
    cur = default_conn.cursor()

    dbName = os.getenv("DB_NAME")
    cur.execute(initDBQUERIES.checkDatabaseExists.format(
        database=dbName
    ))
    dbExists = cur.fetchone()[0]
    if not dbExists:
        cur.execute(initDBQUERIES.createDatabase.format(
            database=dbName
            ))
        
    default_conn.commit()
    cur.close()
    default_conn.close()

def createSchemas(conn: psycopg.Connection):
    cur = conn.cursor()
    cur.execute(initDBQUERIES.createSchema.format(
        schema=("teamstat")
    ))
    cur.execute(initDBQUERIES.createSchema.format(
        schema=("stathead")
    ))
    conn.commit()

def initalizeDB():
    load_dotenv()

    createNcaaBasketballDatabase()
    
    conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DB_NAME")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    conn = psycopg.connect(conn_string)
    createSchemas(conn)
    conn.close()
