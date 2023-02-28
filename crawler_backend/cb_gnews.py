import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    key = obj.get_config_val('gnews_key')
    base_url = base_url.format(api_key=key)
    res = WebClient.get(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    if res.status_code == 200:
        json_data = res.json()

        for article in json_data.get('articles'):

            obj.create_task(
                unique_key=article["url"],
                name=article.get('title'),
                url=article["url"],
                data=article["content"] if article.get('content') else None
            )
