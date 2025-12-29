from TeamStat import initDatabase
from tests import conftest
from StatHead import service
from StatHead import databaseHelper

# initDatabase.main()
service = service.Service()
service.init_db()
print('done')