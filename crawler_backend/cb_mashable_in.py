import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    # find banner posts
    for a in soup.find_all('a', {'class':'box_title'}):
        obj.create_task(
            unique_key=a.attrs.get('href'),
            name=a.text.strip(),
            url=a.attrs.get('href')
        )

    # find remaining posts
    for li in soup.find_all('li', {'class': 'blogroll CATEGORY'}):
        a = li.find('a')
        if a:
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.text.strip(),
                url=a.attrs.get('href')
            )

