from water_controller import Scheduler_Plugin, log
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler

import logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.ERROR)

class Interval(Scheduler_Plugin):
    def __init__(self,zone,opts):
        super().__init__()
        self.zone = zone
        self.job = self.zone.water_on
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.job, 'interval', **opts)
        self.scheduler.start()

class Cron(Scheduler_Plugin):
    def __init__(self,zone,opts):
        super().__init__()
        self.zone = zone
        self.job = self.zone.water_on
        self.scheduler = BackgroundScheduler()
        if type(opts) is list:
            for x in opts:
                self.scheduler.add_job(self.job, 'cron', **x)
        else:
            self.scheduler.add_job(self.job, 'cron', **opts)
        self.scheduler.start()
