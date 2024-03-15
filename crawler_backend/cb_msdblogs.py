import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    for div in soup.find_all('div', {'class': 'col-lg-8 col-md-12 post-card-header'}):
        a = div.find('a')
        p = div.find('p')
        data = p.text.strip() if p else ""

        obj.create_task(
            unique_key=a.get('href'),
            name=a.text.strip(),
            url=a.get('href'),
            data=data
        )
