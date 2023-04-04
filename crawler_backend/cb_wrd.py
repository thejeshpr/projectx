import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)

    # json data retried and stored as part of response, so find and parse it
    start_index = res.html.text.find('{"@context')
    data = res.html.text[start_index:]
    end_index = data.find('\nwindow.Martech')
    data = data[:end_index]

    json_data = json.loads(data)

    for item in json_data.get('itemListElement'):
        obj.create_task(
            unique_key=item.get('url'),
            name=item.get('name'),
            url=item.get('url'),
        )


