import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for a in soup.find_all('a', {'class': 'article-link'}):
        if a:
            data = ""
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.text.strip(),
                url=a.attrs.get('href'),
                data=data
            )
