import os
# django project name is adleads, replace adleads with your project name
import sys
import django

sys.path.append(r"C:\Users\tpr\PycharmProjects\projectx") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectx_site.settings")
django.setup()


from crawler.models import (
    SiteConf
)

def test():
    print("TEST--------------------->")