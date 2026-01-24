import psycopg
from psycopg import sql
import os
import dotenv
from .teamstatService import Service
from . import CONSTS
from . import teamstatQUERIES

#necessary to create and load tables from here becaues table name isn't known until runtime
def createAndLoadTables(conn: psycopg.Connection):
    service = Service()
    tablesWithTheirUrls = service.getUrlsForTables()
    for tableName in tablesWithTheirUrls.keys():
        table = service.getDataForTable(tableName, tablesWithTheirUrls[tableName])

        statType = tableName.split("_")[0]
        if statType == "team":
            createAndLoadTeamTable(conn, table)
        elif statType == "player":
            createAndLoadPlayerTable(conn, table)

def createAndLoadTeamTable(conn, table):
    cursor = conn.cursor()
    cursor.execute(teamstatQUERIES.createTeamStatTeamTable.format(
        tableName=table.tableName,
        schema="teamstat"
    ))
    conn.commit()

    cursor.executemany(
        teamstatQUERIES.insertTeamStats.format(
            tableName=table.tableName,
            schema="teamstat"),
        table.data
    )
    conn.commit()

def createAndLoadPlayerTable(conn, table):
    cursor = conn.cursor()
    cursor.execute(teamstatQUERIES.createTeamStatPlayerTable.format(
        tableName=table.tableName,
        schema="teamstat"
    ))
    conn.commit()

    cursor.executemany(
        teamstatQUERIES.insertPlayerStats.format(
            tableName=table.tableName,
            schema="teamstat"),
        table.data
    )
    conn.commit()
  
#temp
def testLoadOneTable():
    dotenv.load_dotenv()
    conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DB_NAME")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    conn = psycopg.connect(conn_string)

    cur = conn.cursor()

    service = Service()
    tables = service.getUrlsForTables()
    tableName = "team_block_pct"
    tableUrls= tables[tableName]

    tableData = service.getOneUrlDataForTable(tableName, tableUrls)
    tableName = tableData.tableName

    cur.execute(teamstatQUERIES.createTeamStatTeamTable.format(
        tableName=tableName,
        schema="teamstat"
    ))
    

    cur.executemany(
        teamstatQUERIES.insertTeamStats.format(
            tableName=tableName,
            schema="teamstat"),
        tableData.data
    )

    # psycopg2.extras.execute_values(
    #     cur,
    #     QUERIES.insertPlayerStats.format(
    #         tableName=sql.Identifier(tableName).string),
    #     tableData.data,
    #     page_size=1000,

    # )
    conn.commit()
    cur.close()

#TODO: change structure of this, run should be started from the service
def main():
    dotenv.load_dotenv()

    conn_string = f'host={os.getenv("HOST_NAME")} dbname={os.getenv("DB_NAME")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    conn = psycopg.connect(conn_string)

    createAndLoadTables(conn)
    # testLoadOneTable()

    conn.commit()
    conn.close()


