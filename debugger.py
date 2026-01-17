from TeamStat import initDatabase
from tests import conftest
from StatHead import service
from StatHead import databaseHelper

service = service.Service()
dbHelper = databaseHelper.DatabaseHelper()
service.init_db()
service.startRun()
print('done')