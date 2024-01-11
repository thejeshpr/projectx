import json
import urllib.parse
from urllib.parse import urljoin
from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    for a in soup.find_all('a', {'class': 'af ag ah ai aj ak al am an ao ap aq ar as at'}):
        txt, link = a.text.strip(), a.get('href')
        if txt and link.startswith('/swlh/') and "min read" not in a.text:
            url = urllib.parse.urljoin(base_url, link)
            obj.create_task(
                unique_key=url,
                name=txt,
                url=url
            )

