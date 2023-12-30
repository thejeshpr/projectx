import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    for item in res.json().get('items'):
        name = item.get('headline')
        url = item.get('url')

        data = f"Desc: {item.get('seo').get('meta-description')}\n" \
               f"Summary: {item.get('summary')}\n" \
               f"Created_at: {item.get('created-at')}\n" \
               f"Author: {item.get('author-name')}\n"

        obj.create_task(
            unique_key=item.get("id"),
            name=name,
            url=url,
            data=data
        )

