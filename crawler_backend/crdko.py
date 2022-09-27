import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    logging.info("Establishing connection to url")
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)

    logging.debug(f"status code:{res.status_code}")
    logging.debug(f"response: {res.content}")

    links = res.html.xpath("/html/body/div[2]/div/div[1]/div/main/div[3]/div[1]/div[1]/div/div[*]/div[2]/h2/a")

    for link in links[::-1]:
        logging.debug(link)
        url_link = link.attrs.get('href')

        obj.create_task(
            unique_key=url_link,
            name=link.text.strip(),
            url=urllib.parse.urljoin(base_url, url_link)
        )

