import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    divs = soup.find_all("div", {"class": "flex flex-1 flex-col"})

    for div in divs:
        a_list = div.find_all('a')

        if a_list:
            a = a_list[0]
            url = a.get('href')
            if url.startswith("/product"):
                continue

            if len(a_list) > 1:
                data = a_list[1].text.strip()
            else:
                data = ""

            obj.create_task(
                unique_key=url,
                name=a.text.strip(),
                url=urllib.parse.urljoin(base_url, url),
                data=data
            )
