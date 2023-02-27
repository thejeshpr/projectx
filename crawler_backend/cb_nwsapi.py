import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    key = obj.get_config_val('nwsapi_key')
    base_url = base_url.format(key=key)
    res = WebClient.get(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    if res.status_code == 200:
        json_data = res.json()

        if json_data['status'] == 'ok':
            for article in json_data.get('articles'):
                name = f"{article.get('author')} - {article.get('title')}"
                url = article["url"]
                obj.create_task(
                    unique_key=article["url"],
                    name=name,
                    url=url,
                )

