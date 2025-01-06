import psycopg2
import os
import dotenv
from Service import Service
from Parser import Parser


def createUrlsTable(cursor):
    service = Service()
    parser = Parser()
    urls = service.getUrls()
    loadTableParams = [(parser.getTableName(url), url) for url in urls]
    createTableQuery = '''CREATE TABLE IF NOT EXISTS urls (
        statistic varchar PRIMARY KEY,
        url varchar
    )'''
    loadTableQuery = '''INSERT INTO urls (statistic, url) VALUES (%s, %s)'''
    cursor.execute(createTableQuery)
    cursor.executemany(loadTableQuery, loadTableParams)

def createTables(cursor, tables):
    service = Service()
    for table in tables:
        query = f'CREATE TABLE {table.name} //columns'


def main():
    dotenv.load_dotenv()
    conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DB_NAME")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # query = open("./init.sql").read()
    # cur.execute(query)

    # service = Service()
    # urls = service.getUrls()
    # sanatizedUrls = [(url,) for url in urls]
    # cur.executemany('CALL insert_urls_table(%s)', sanatizedUrls)
    createUrlsTable(cur)
    conn.commit()

    cur.execute('SELECT * FROM urls;')
    records = cur.fetchall()

    print(records)

main()