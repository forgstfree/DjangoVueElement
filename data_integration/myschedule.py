import json
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import pydbclib

class MySchedule():
    def __init__(self) -> None:
        super().__init__()
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_jobstore(DjangoJobStore(), 'default')
    
    """
    fun:定时执行的主体函数
    params:定时所需的具体参数，类型为字典
    arge:主体函数的参数
    """
    def add_job(self, fun, params, arge):
        pass

    def pause_job(self, id):
        pass

    def start_job(self, id):
        pass

    def delete_job(self, id):
        pass

    def update_job(self, id, params):
        self.delete_job(id)
        self.add_job(id, params)

