import os
import subprocess

from .models import SiteConf, Job


class InvokeBackend():
    """"""
    def __init__(self, site_conf, auto_start=True):
        self.site_conf = site_conf
        self.job = None
        if auto_start:
            self.execute()

    def execute(self):
        self.create_job()
        self.invoke_backend_crawler()

    def create_job(self):
        self.job = Job(site_conf=self.site_conf)
        self.job.save()


    def invoke_backend_crawler(self):
        # print(f"Path:------------> { os.path.dirname(os.path.realpath(__file__)) }")

        parent_path = os.path.dirname(os.path.realpath(__file__))
        base_path = os.path.dirname(parent_path)
        print(f'ParentPath: {parent_path}')
        print(f'BasePath: {base_path}')
        script_path = os.path.join(base_path, 'crawler_backend', 'base.py')
        print(script_path)
        cmd = f'python "{script_path}" {self.job.id}'
        print(f'cmd: {cmd}')
        o = subprocess.Popen(cmd, shell=True)
        print('res', o)



