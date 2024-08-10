import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    json_data = res.json()

    for item in json_data["data"]:
        obj.create_task(
            unique_key=item["id"],
            name=f"[{item['type']}] - {item['attributes']['title']}",
            url=item['attributes']['shareUrl'],
            data=f"createdAt - {item['attributes']['createdAt']}"
        )
