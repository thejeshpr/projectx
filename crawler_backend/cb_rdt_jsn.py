import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    for item in res.json().get('data').get('children'):
        data = item.get('data')
        name = data.get('title')
        url = urllib.parse.urljoin(extras.get("item_base_url"), data.get('permalink'))
        # url = item.get('url')

        additional_data = f"selfText: {data.get('selftext')}\n"

        obj.create_task(
            unique_key=data.get("id"),
            name=name,
            url=url,
            data=additional_data
        )

