import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    divs = soup.find_all("div", {"class": "styles_item__Dk_nz my-2 flex flex-1 flex-row gap-2 py-2 sm:gap-4"})
    for div in divs:
        a_list = div.find_all('a')
        if a_list:
            a = a_list[1]
            obj.create_task(
                unique_key=a.get('href'),
                name=a.text.strip(),
                url=urllib.parse.urljoin(base_url, a['href'])
                # data=data
            )
