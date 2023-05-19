import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    # find h2
    for h2 in soup.find_all('h2', {'class': "portfolio-title"}):
        # find links
        a = h2.find('a')
        if a:
            url = urllib.parse.urljoin(base_url, a.attrs.get('href'))
            obj.create_task(
                unique_key=url,
                name=a.text.strip(),
                url=url
            )

