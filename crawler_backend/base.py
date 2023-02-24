import argparse
import time
import os

import sys
import django
import uuid
import logging

logging.basicConfig(filename='scraper.log', format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

# parent_path = os.path.dirname(os.path.realpath(__file__))
#         base_path = os.path.dirname(parent_path)
#         script_path = os.path.join(base_path, 'crawler_backend', 'base.py')
#         cmd = f'python "{script_path}" {self.job.id}'
#         o = subprocess.Popen(cmd, shell=True)

parent_path = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.dirname(parent_path)

# print(parent_path, base_path)

sys.path.append(base_path)
# sys.path.append(r"./")
# print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectx_site.settings")

logging.debug("Setting up django")
django.setup()

from crawler.models import (
    SiteConf, Job, Task, ConfigValues
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("job_id", help="Job ID to Crawl")
    args = parser.parse_args()
    logging.info(f"Starts Scarping")
    logging.debug(f"JOB ID: {args.job_id}")

    logging.debug(f"Invoking Base Parser")
    _ = BaseParser(args.job_id)


class BaseParser():
    def __init__(self, job_id):
        self.job: Job = Job.objects.get(pk=job_id)
        self.job_start_time = time.time()
        self.site_conf: SiteConf = SiteConf.objects.get(pk=self.job.site_conf.pk)
        logging.debug(f"SiteConf: {self.site_conf.name}")

        logging.debug(f"starting execution")
        self.execute()

    def execute(self):
        self.scrape()

    def lock_site_conf(self):
        logging.debug(f"Locking SiteConf: {self.site_conf.name}")
        self.site_conf.is_locked = True
        self.site_conf.save()

    def unlock_site_conf(self):
        logging.debug(f"unlocking SiteConf: {self.site_conf.name}")
        self.site_conf.is_locked = False
        self.site_conf.save()

    def update_job_status(self, status):
        """"""
        logging.debug(f"Update Job {self.job.id} Status: {status}")
        if status == "SUCCESS":
            task_count = Task.objects.filter(job__pk=self.job.pk).count()
            status = "SUCCESS" if task_count > 0 else "NO-TASK"
        self.job.status = status
        self.job.save()

    def build_task_unique_key(self, unique_key):
        logging.debug(f"building unique_key: {unique_key}")
        return f"{self.site_conf.name}::{unique_key}"

    def update_elapsed_time(self):
        elapsed_time = time.time() - self.job_start_time
        logging.debug(f"updating elapsed time: {elapsed_time} for job: {self.job}")
        elapsed_time = elapsed_time if elapsed_time >= 1 else 1
        self.job.elapsed_time = elapsed_time
        self.job.save()

    @staticmethod
    def is_task_exist(unique_key):
        logging.debug(f"checking task existence: {unique_key}")
        count = Task.objects.filter(unique_key=unique_key).count()
        return True if count else False

    def create_task(self, unique_key, *args, **kwargs):
        """
        check and create the task if not exist
        """
        unique_key = self.build_task_unique_key(unique_key)
        if not BaseParser.is_task_exist(unique_key):
            logging.debug(f"creating unique_key : {unique_key}")
            _ = Task.objects.create(
                unique_key=unique_key,
                name=kwargs.get("name"),
                url=kwargs.get("url"),
                data=kwargs.get("data"),
                job=self.job,
                site_conf=self.site_conf
            )

    def create_tasks(self, tasks):
        tasks_to_create = []

        for task in tasks:
            logging.debug(f"Processing task : {task.get('name')}")
            unique_key = self.build_task_unique_key(task['unique_key'])
            logging.debug(f"unique key : {unique_key}")
            if not BaseParser.is_task_exist(unique_key):
                tasks_to_create.append(
                    Task(
                        unique_key=unique_key,
                        name=task.get("name"),
                        url=task.get("url"),
                        data=task.get("data"),
                        job=self.job,
                        site_conf=self.site_conf
                    )
                )
            else:
                logging.info(f"task already exist, name: {task['name']}, unique_key: {unique_key}")

        if tasks_to_create:
            logging.info(f"creating {len(tasks_to_create)} for {self.site_conf.name}, job: {self.job.id}")
            Task.objects.bulk_create(tasks_to_create)
        else:
            logging.info(
                f"data is up to date, no new tasks will be created for {self.site_conf.name}, job: {self.job.id}")

    def scrape(self):
        # from crawler_backend.scraper_config import get_scrapper
        from crawler_backend.scrapper_filder import get_scrapper
        scraper = get_scrapper(self.site_conf.scraper_name)
        self.lock_site_conf()
        self.update_job_status('RUNNING')
        try:
            scraper(self)
            # self.create_tasks(tasks)
            self.update_job_status('SUCCESS')
        except Exception as e:
            self.update_job_status('ERROR')
            self.job.error = str(e)
            self.job.save()
            logging.error(str(e))
        finally:
            self.update_elapsed_time()
            self.unlock_site_conf()

    @staticmethod
    def get_config_val(key):
        logging.debug(f'Fetching config values for key:{key}')
        conf: ConfigValues = ConfigValues.objects.filter(key=key).first()
        logging.debug(f"Conf: {conf}")
        if not conf:
            raise Exception("Invalid Configuration Key")
        logging.debug(f'config value for key is {conf.val}')
        return conf.val

    def create_test_tasks(self):
        self.site_conf.is_locked = True
        self.site_conf.save()
        self.job.status = "RUNNING"
        self.job.save()
        for i in range(10):
            time.sleep(1)
            uuid_ = uuid.uuid4()
            task = Task(name=f"Test: {uuid_}", site_conf=self.site_conf, job=self.job, data=uuid_,
                        unique_key=uuid_)
            task.save()

        self.site_conf.is_locked = False
        self.site_conf.save()


if __name__ == "__main__":
    main()
