import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    a_list = soup.find_all('a', {'class': '_1lkmsmo1'})
    a_list.extend(soup.find_all('a', {'class': 'yy0d3l8'}))

    for a in a_list:
        if a and a.attrs.get('href') and a.text.strip():
            url = urllib.parse.urljoin(base_url, a.get('href'))
            obj.create_task(
                unique_key=a.get('href'),
                name=a.text.strip(),
                url=url,
            )

