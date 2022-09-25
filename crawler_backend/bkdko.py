import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    logging.info("Establishing connection to url")
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)

    logging.debug(f"status code:{res.status_code}")
    logging.debug(f"response: {res.content}")

    tasks = []

    links = res.html.xpath("/html/body/div[2]/div/div[1]/div/main/div[3]/div[1]/div[1]/div/div[*]/div[2]/h2/a")

    for link in links[::-1]:
        logging.debug(link)
        url_link = link.attrs.get('href')
        tasks.append(
            dict(
                name=link.text.strip(),
                url=urllib.parse.urljoin(base_url, url_link),
                unique_key=url_link
            )
        )

    logging.debug(f"found {len(tasks)}")
    return tasks
