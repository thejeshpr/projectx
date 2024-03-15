import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    for div in soup.find_all('div', {'class': 'col'}):
        a = div.find('a')
        heading = div.find('h4')
        body_div = div.find('div', {"class": "card__body"})
        data = ""
        if body_div:
            p = body_div.find('p')
            if p:
                data = p.text.strip() if p else ""

        obj.create_task(
            unique_key=a.get('href'),
            name=heading.text.strip(),
            url=a.get('href'),
            data=data
        )
