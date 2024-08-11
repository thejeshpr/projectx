import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for div in soup.find_all('div', {'class': 'wp-block-tc23-post-picker'}):
        h2 = div.find("h2")
        if h2:
            a = h2.find("a")
            if a:
                url = a.attrs.get('href')
                obj.create_task(
                    unique_key=url,
                    name=a.text.strip(),
                    url=url
                )

