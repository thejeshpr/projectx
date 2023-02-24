import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    arg = json.loads(obj.site_conf.extra_data_json)
    url = urllib.parse.urljoin(base_url, arg["tag"])

    res = WebClient.get(url)

    h2_list = res.html.find(".crayons-story__title")

    for h2 in h2_list[::-1]:
        a = h2.find('a', first=True)

        url = urllib.parse.urljoin(obj.site_conf.base_url, a.attrs.get('href'))

        obj.create_task(
            unique_key=a.attrs.get('id').strip(),
            name=a.text.strip(),
            url=url
        )
