import logging

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url.format(key=obj.get_config_val('mediastack')))
    for item in res.json()['data']:
        obj.create_task(
            unique_key=item.get('url'),
            name=item.get('title'),
            url=item.get('url'),
            data=f'{item.get("description")} - {item.get("published")}'
        )
