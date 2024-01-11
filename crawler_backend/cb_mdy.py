import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    items = res.json()['items'][0]['products']['position1']
    items.extend(res.json()['items'][0]['products']['position2'])

    for item in items:
        name = item.get('title')
        url = item.get('URL') or item.get('url')
        data = f"desc: {item.get('short_description')}\n" \
               f"location: {item.get('location')}\n" \
               f"DateTime: {item.get('DateTime')}\n"

        obj.create_task(
            unique_key=url,
            name=name,
            url=url,
            data=data
        )

