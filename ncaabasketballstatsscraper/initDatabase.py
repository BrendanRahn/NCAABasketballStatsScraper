import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import dotenv
from .Service import Service
from .Parser import Parser
from . import CONSTS
from . import QUERIES


def createUrlsTable(cursor):
    service = Service()
    parser = Parser()
    urls = service.getUrls()
    tableData = [(parser.getTableName(url), url) for url in urls] 
    cursor.execute(QUERIES.createUrlsTable)
    cursor.executemany(QUERIES.loadUrlsTable, tableData)

def createAndLoadTables(cursor):
    service = Service()
    tablesWithTheirUrls = service.getTablesAndTheirUrls()
    for tableName in tablesWithTheirUrls.keys():
        sanatizedSchema = ("teamStat",)
        table = service.getDataForTable(tableName, tablesWithTheirUrls[tableName])
        query = f'CREATE TABLE {table.name} //columns'
#temp
def testLoadOneTable(cursor):
    service = Service()
    tablesWithTheirUrls = service.getTablesAndTheirUrls()
    table = tablesWithTheirUrls.keys()[0]
    

def createNcaaBasketballDatabase():
    default_conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DEFAULT_DB")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    default_conn = psycopg2.connect(default_conn_string)
    default_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = default_conn.cursor()

    dbbName = os.getenv("DB_NAME")
    cur.execute(QUERIES.checkDatabaseExists.format(
        database=sql.Identifier(dbbName).string
    ))
    dbExists = cur.fetchone()[0]
    if not dbExists:
        cur.execute(QUERIES.createDatabase.format(
            database=sql.Identifier(dbbName).string
            ))

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

