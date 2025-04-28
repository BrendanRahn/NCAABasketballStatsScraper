import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import dotenv
from .Service import Service
from .Parser import Parser
from . import CONSTS


def createUrlsTable(cursor):
    service = Service()
    parser = Parser()
    urls = service.getUrls()
    tableData = [(parser.getTableName(url), url) for url in urls] 
    cursor.execute(CONSTS.QUERIES["createUrlsTable"])
    cursor.executemany(CONSTS.QUERIES["loadUrlsTable"], tableData)

def createTables(cursor):
    service = Service()
    sortedUrlsByTable = service.getSortedUrlsByTable()
    for tableName in sortedUrlsByTable.keys():
        schema = "teamStat"
        table = service.getDataForTable(tableName, sortedUrlsByTable[tableName])
        query = f'CREATE TABLE {table.name} //columns'

def createNcaaBasketballDatabase():
    default_conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DEFAULT_DB")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    default_conn = psycopg2.connect(default_conn_string)
    default_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = default_conn.cursor()

    sanitizedDbName = (os.getenv("DB_NAME"),)
    cur.execute(CONSTS.QUERIES["checkDatabaseExists"], sanitizedDbName)
    dbExists = cur.fetchone()[0]
    if not dbExists:
        cur.execute(CONSTS.QUERIES["createDatabase"], sanitizedDbName)

    cur.close()
    default_conn.close()

def main():
    dotenv.load_dotenv()

    createNcaaBasketballDatabase()

    conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DB_NAME")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    conn = psycopg2.connect(conn_string)

    cur = conn.cursor()

    createUrlsTable(cur)
    conn.commit()

    cur.execute('SELECT * FROM urls;')
    records = cur.fetchall()

    print(records)

