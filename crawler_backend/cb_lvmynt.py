import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    for h2 in soup.find_all('h2', {'class': 'headline'}):
        a = h2.find('a')
        url = urllib.parse.urljoin(extras.get("article_base_url"), a.get('href'))
        obj.create_task(
            unique_key=url,
            name=a.text.strip(),
            url=url
        )
