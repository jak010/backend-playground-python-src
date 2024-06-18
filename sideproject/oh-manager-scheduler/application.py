import datetime
import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler

from src.app.otr.runner import OTRRunner
from src.app.remaker.runner import RemakeRunner
from src.config.base import patch_dependency


class SchedulerApplication:
    otr_runner = OTRRunner()
    remake_runner = RemakeRunner()

    def scheduler(self):
        background_scheduler = BackgroundScheduler(timezone='Asia/Seoul', daemon=True)
        background_scheduler.add_job(self.otr_runner.transport, "interval", seconds=1800, id='OTR')
        background_scheduler.add_job(self.remake_runner.execute, "interval", seconds=1800, id='REMAKER')

        return background_scheduler

    def run(self):
        patch_dependency()

        daemon_thread = threading.Thread(target=self.scheduler().start)
        daemon_thread.daemon = True
        daemon_thread.start()

        while True:
            print(f"[{datetime.datetime.now()}] RUNNING SCHEDULING...")
            time.sleep(1)


if __name__ == '__main__':
    application = SchedulerApplication()
    application.run()
