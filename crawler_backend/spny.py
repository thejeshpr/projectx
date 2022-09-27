import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    for item in res.json().get('results'):
        name = f"{item.get('fuel_type')}:{item.get('model')}:{item.get('make_year')}:{item.get('price')}"
        url = urllib.parse.urljoin(extras.get("item_base_url"), item.get('permanent_url'))
        obj.create_task(
            unique_key=item.get("id"),
            name=name,
            url=url,
        )

