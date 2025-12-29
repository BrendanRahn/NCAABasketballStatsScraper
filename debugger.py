from team_stat import initDatabase
from tests import conftest
from stat_head import service
from stat_head import databaseHelper

# initDatabase.main()
service = service.Service()
service.init_db()
print('done')