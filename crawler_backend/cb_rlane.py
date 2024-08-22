import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    for div in soup.find_all('div', {'class': 'td-module-meta-info'}):
        a = div.find('a')
        if a:
            desc_div = div.find('div', {"class": "td-excerpt"})
            desc = desc_div.text.strip() if desc_div else ""
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.text.strip(),
                url=a.attrs.get('href'),
                data=desc
            )




