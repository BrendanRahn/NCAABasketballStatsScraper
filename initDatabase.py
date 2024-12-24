import psycopg2
import os
import dotenv
from Service import Service


def createTables(cursor, tableNames):
    for name in tableNames:
        query = f'CREATE TABLE {name} //columns'


def main():
    dotenv.load_dotenv()
    conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DB_NAME")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    query = open("./init.sql").read()
    cur.execute(query)

    service = Service()
    urls = service.getUrls()
    sanatizedUrls = [(url,) for url in urls]
    cur.executemany('CALL insert_urls_table(%s)', sanatizedUrls)

    cur.execute('SELECT * FROM urls;')
    records = cur.fetchall()
    print(records)

main()