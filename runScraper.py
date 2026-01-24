from InitDB import initDB
from TeamStat import teamstatDBHelper
from StatHead import service
from multiprocessing import Pool


def startRun():
    initDB.initalizeDB()
    statHeadService = service.Service()
    statHeadService.init_db()

    processes = 2  # Number of processes to run
    with Pool(processes=processes) as pool:
        pool.apply_async(teamstatDBHelper.main)
        pool.apply_async(service.run_stathead_service)
        pool.close()
        pool.join()

    print("Scraping completed :)")

