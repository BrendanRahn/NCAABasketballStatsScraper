import psycopg
from psycopg import sql
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

def createAndLoadTables(conn: psycopg.Connection):
    
    service = Service()
    tablesWithTheirUrls = service.getUrlsForTables()
    for tableName in tablesWithTheirUrls.keys():
        table = service.getDataForTable(tableName, tablesWithTheirUrls[tableName])

        statType = tableName.split("_")[0]
        if statType == "team":
            createTeamTable(conn, table)
        elif statType == "player":
            createPlayerTable(conn, table)

#rename, this creates table and inserts
def createTeamTable(conn, table):
    cursor = conn.cursor()
    cursor.execute(QUERIES.createTeamStatTeamTable.format(
        tableName=(table.tableName)
    ))
    conn.commit()

    cursor.executemany(
        QUERIES.insertTeamStats.format(
            tableName=(table.tableName)),
        table.data
    )
    conn.commit()

def createPlayerTable(conn, table):
    cursor = conn.cursor()
    cursor.execute(QUERIES.createTeamStatPlayerTable.format(
        tableName=(table.tableName)
    ))
    conn.commit()

    cursor.executemany(
        QUERIES.insertPlayerStats.format(
            tableName=(table.tableName)),
        table.data
    )
    conn.commit()
  

def createNcaaBasketballDatabase():
    default_conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("STATHEAD_TEST_DB")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    default_conn = psycopg.connect(default_conn_string)
    cur = default_conn.cursor()

    dbName = os.getenv("DB_NAME")
    cur.execute(QUERIES.checkDatabaseExists.format(
        database=dbName
    ))
    dbExists = cur.fetchone()[0]
    if not dbExists:
        cur.execute(QUERIES.createDatabase.format(
            database=dbName
            ))
        
    default_conn.commit()
    cur.close()
    default_conn.close()

def createSchemas(conn):
    cur = conn.cursor()
    cur.execute(QUERIES.createSchema.format(
        schema=("team")
    ))
    cur.execute(QUERIES.createSchema.format(
        schema=("player")
    ))
    conn.commit()

def main():
    dotenv.load_dotenv()

    createNcaaBasketballDatabase()

    conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("STATHEAD_TEST_DB")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    conn = psycopg.connect(conn_string)

    createSchemas(conn)
    createAndLoadTables(conn)

    conn.commit()
    conn.close()


