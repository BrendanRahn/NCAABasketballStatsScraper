import psycopg2
import psycopg2.extras
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

def createAndLoadTables(conn: psycopg2.extensions.connection):
    
    service = Service()
    tablesWithTheirUrls = service.getTablesAndTheirUrls()
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
        tableName=sql.Identifier(table.tableName).string
    ))
    conn.commit()

    psycopg2.extras.execute_values(
        cursor,
        QUERIES.insertTeamStats.format(
            tableName=sql.Identifier(table.tableName).string),
        table.data,
        page_size=1000,
    )
    conn.commit()

def createPlayerTable(conn, table):
    cursor = conn.cursor()
    cursor.execute(QUERIES.createTeamStatPlayerTable.format(
        tableName=sql.Identifier(table.tableName).string
    ))
    conn.commit()

    psycopg2.extras.execute_values(
        cursor,
        QUERIES.insertPlayerStats.format(
            tableName=sql.Identifier(table.tableName).string),
        table.data,
        page_size=1000,
    )
    conn.commit()
#temp
def testLoadOneTable(conn: psycopg2.extensions.connection):
    cur = conn.cursor()

    service = Service()
    tablesWithTheirUrls = service.getTablesAndTheirUrls()
    testTable = next(iter(tablesWithTheirUrls))

    tableData = service.getOneUrlDataForTable(testTable, tablesWithTheirUrls[testTable])
    tableName = tableData.tableName

    cur.execute(QUERIES.createTeamStatPlayerTable.format(
        tableName=sql.Identifier(tableName).string
    ))

    psycopg2.extras.execute_values(
        cur,
        QUERIES.insertPlayerStats.format(
            tableName=sql.Identifier(tableName).string),
        tableData.data,
        page_size=1000,

    )


    

def createNcaaBasketballDatabase():
    default_conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DEFAULT_DB")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    default_conn = psycopg2.connect(default_conn_string)
    default_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = default_conn.cursor()

    dbName = os.getenv("DB_NAME")
    cur.execute(QUERIES.checkDatabaseExists.format(
        database=sql.Identifier(dbName).string
    ))
    dbExists = cur.fetchone()[0]
    if not dbExists:
        cur.execute(QUERIES.createDatabase.format(
            database=sql.Identifier(dbName).string
            ))
        
    default_conn.commit()
    cur.close()
    default_conn.close()

def createSchemas(conn):
    cur = conn.cursor()
    cur.execute(QUERIES.createSchema.format(
        schema=sql.Identifier("team").string
    ))
    cur.execute(QUERIES.createSchema.format(
        schema=sql.Identifier("player").string
    ))
    conn.commit()

def main():
    dotenv.load_dotenv()

    createNcaaBasketballDatabase()

    conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DB_NAME")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    conn = psycopg2.connect(conn_string)


    createSchemas(conn)
    createAndLoadTables(conn)
    # testLoadOneTable(conn)

    conn.commit()
    conn.close()



    # cur.execute('SELECT * FROM urls;')
    # records = cur.fetchall()

