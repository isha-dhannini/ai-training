import schedule
import time
from tasks import backup_files, cleanup

def start_scheduler():

    schedule.every(10).seconds.do(backup_files)
    schedule.every(30).seconds.do(cleanup)

    start_time = time.time()

    print("Scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(1)

        if time.time() - start_time > 60:
            print("Stopping scheduler...")
            break