import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for a in soup.find_all('a', {'class': 'post-block__title__link'}):
        url = a.attrs.get('href')
        obj.create_task(
            unique_key=url,
            name=a.text.strip(),
            url=url
        )

