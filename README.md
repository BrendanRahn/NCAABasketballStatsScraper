Uses Python 3.10.2

TODO:
- Containerize repo with Docker, use Poetry to manage python packages
- Set up scraper for Stathead webpages


# Requirements
- Poetry
    - Download: https://python-poetry.org/docs/#installation
- PostgresSQL
    - Download: https://www.postgresql.org/download/

# .env
A .env file with the following variables is required to initalize and connect to your postgreSQL database:
- HOST_NAME = server name 
- DB_NAME = "ncaabasketball"
- DEFAULT_DB = "postgres"
- USER = "postgres"
- PASSWORD = your postgres password

# Execution
- First run 'poetry install'
- Then run 'poetry init_db'


TODO: 
- add test case for null/"--" values
- Fix casing across the project(lower snake case)
- CurrentSeason values are getting trimmed for team tabels (no decimal places)
- Move tests in root folder to TeamStat folder
-Change structure of classes to allow for top-level functions for multiprocessing
