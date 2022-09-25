import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    logging.info("Establishing connection to url")
    base_url = obj.site_conf.base_url
    arg = json.loads(obj.site_conf.extra_data_json)
    url = urllib.parse.urljoin(base_url, arg["tag"])
    logging.debug(f"Connecting URL: {url}")
    res = WebClient.get(url)

    logging.debug(f"status code:{res.status_code}")
    logging.debug(f"response: {res.content}")

    tasks = []

    h2_list = res.html.find(".crayons-story__title")

    for h2 in h2_list[::-1]:
        a = h2.find('a', first=True)

        url = urllib.parse.urljoin(obj.site_conf.base_url, a.attrs.get('href'))

        tasks.append(
            dict(
                name=a.text.strip(),
                url=url,
                unique_key=a.attrs.get('id').strip()
            )
        )

    logging.debug(f"found {len(tasks)}")
    return tasks
