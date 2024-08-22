import os
import subprocess
import time

from .models import SiteConf, Job


class InvokeBackend:
    """"""
    def __init__(self, site_conf, auto_start=True, wait_time=0):
        self.site_conf = site_conf
        self.job = None
        self.wait_time = wait_time
        if auto_start:
            self.execute()

    def execute(self):
        self.create_job()
        self.invoke_backend_crawler()

    def create_job(self):
        self.job = Job(site_conf=self.site_conf)
        self.job.save()

    def invoke_backend_crawler(self):
        parent_path = os.path.dirname(os.path.realpath(__file__))
        base_path = os.path.dirname(parent_path)
        #base_path = "/home/ubuntu/pyenvs/projectx_dev/src/projectx"
        script_path = os.path.join(base_path, 'crawler_backend', 'base.py')

        # create config object to place python interpreter
        cmd = f'/home/ubuntu/pyenvs/projectx_dev/bin/python "{script_path}" {self.job.id} --wait-time {self.wait_time}'
        o = subprocess.Popen(cmd, shell=True)

    # def invoke_backend_crawler(self):
    #     # if self.validate_num_of_running_job():
    #     parent_path = os.path.dirname(os.path.realpath(__file__))
    #     base_path = os.path.dirname(parent_path)
    #     #base_path = "/home/ubuntu/pyenvs/projectx_dev/src/projectx"
    #     script_path = os.path.join(base_path, 'crawler_backend', 'base.py')
    #
    #     # create config object to place python interpreter
    #     # cmd = f'/home/ubuntu/pyenvs/projectx_dev/bin/python "{script_path}" {self.job.id}'
    #     cmd = f'python "{script_path}" {self.job.id} --wait-time {self.wait_time}'
    #     o = subprocess.Popen(cmd, shell=True)
    #     print("starting process")
    #     print(o)




