import json
import logging
import urllib.parse
from pprint import pprint

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    # pprint(res.json())
    # extras = json.loads(obj.site_conf.extra_data_json)

    for post in res.json().get('posts'):
        name = post.get('title')
        if post['publication'].get('domainStatus'):
            if post['publication']['domainStatus'].get('ready'):
                url = f"https://{post['publication']['domain']}/{post['slug']}"
            else:
                url = f"https://{post['publication']['username']}.hashnode.dev/{post['slug']}"
        else:
            url = f"https://{post['author']['username']}.hashnode.dev/{post['slug']}"

        obj.create_task(
            unique_key=post["_id"],
            name=name,
            url=url,
        )

