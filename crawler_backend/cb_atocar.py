import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    for div in soup.find_all('div', {'class': 'ns-con-height'}):
        a = div.find('a')
        a.get('href')
        p = div.find('p', {"class": "new-pare-p"})
        data = p.text.strip() if p else ""

        obj.create_task(
            unique_key=a.get('href'),
            name=div.find('h2').text.strip(),
            url=urllib.parse.urljoin(extras.get("item_base_url"), a.get('href')),
            data=data
        )
